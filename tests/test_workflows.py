"""Acceptance checks for schema, leakage boundaries and deployed query behavior."""
import json
import logging
import tempfile
import unittest
from pathlib import Path
import numpy as np
import pandas as pd
from fastapi.testclient import TestClient
from capstone_part2.data_io import load_records
from capstone_part2.cleaning import clean_data,hourly_view
from capstone_part2.feature_engineering import quartile_categories
from capstone_part2.mini_app.__main__ import main as cli_main
from capstone_part3.supervised.common import chronological_split,FEATURES
from capstone_part3.deployment.api import app
from capstone_part3.monitoring.check import check_drift

logger=logging.getLogger(__name__)
ROOT=Path(__file__).resolve().parents[1]


def record(timestamp,temp=280):
    return {'holiday':'None','temp':temp,'rain_1h':0,'snow_1h':0,'clouds_all':20,'weather_main':'Clear','weather_description':'sky is clear','date_time':timestamp,'traffic_volume':1000}


class AcceptanceChecks(unittest.TestCase):
    def test_schema_rejected_before_processing(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'wrong.csv';path.write_text('temp\n280\n')
            with self.assertRaisesRegex(ValueError,'Missing required columns'):load_records(path)

    def test_no_holiday_text_preserved(self):
        df=clean_data(pd.DataFrame([record('2017-01-01 00:00:00')]))
        self.assertEqual(df.holiday.iloc[0],'None')

    def test_reference_imputation_does_not_fit_on_holdout(self):
        train=pd.DataFrame([record('2017-01-01 00:00:00',270),record('2017-01-01 01:00:00',280)])
        holdout=pd.DataFrame([record('2018-01-01 00:00:00',0),record('2018-01-01 01:00:00',340)])
        result=clean_data(holdout,reference=train)
        self.assertEqual(result.temp.iloc[0],275)

    def test_conflicting_hourly_targets_rejected(self):
        row=record('2017-01-01 00:00:00');other=dict(row,traffic_volume=2000)
        with self.assertRaisesRegex(ValueError,'Conflicting'):hourly_view(clean_data(pd.DataFrame([row,other])))

    def test_timestamp_splits_are_disjoint_and_chronological(self):
        df=pd.DataFrame([record(str(t)) for t in pd.date_range('2017-01-01',periods=100,freq='h')])
        df=pd.concat([df,df.iloc[[69,84]]],ignore_index=True)
        train,val,test=chronological_split(df)
        self.assertLess(train.date_time.max(),val.date_time.min())
        self.assertLess(val.date_time.max(),test.date_time.min())
        self.assertFalse(set(train.date_time)&set(val.date_time))
        self.assertFalse(set(val.date_time)&set(test.date_time))
        self.assertNotIn('traffic_volume',FEATURES)
        self.assertFalse(any('congestion' in f or 'high_risk' in f for f in FEATURES))

    def test_quartile_boundaries(self):
        labels=quartile_categories(pd.Series([10,20,30,31]),[10,20,30])
        self.assertEqual(list(labels),['Low','Medium','High','Severe'])

    def test_cli_invalid_date_returns_failure(self):
        self.assertEqual(cli_main(['at','--datetime','malformed']),1)

    def test_api_valid_and_invalid_requests(self):
        client=TestClient(app)
        request=json.loads((ROOT/'capstone_part3/deployment/example_request.json').read_text())
        response=client.post('/predict',json=request)
        self.assertEqual(response.status_code,200)
        self.assertTrue(np.isfinite(response.json()['predicted_vehicles_per_hour']))
        (ROOT/'capstone_part3/deployment/example_response.json').write_text(json.dumps(response.json(),indent=2)+'\n')
        self.assertEqual(client.post('/predict',json={**request,'temp':0}).status_code,422)
        self.assertEqual(client.post('/predict',json={**request,'date_time':'2018-01-01T12:30:00'}).status_code,422)
        self.assertEqual(client.post('/predict',json={**request,'weather_main':'invalid'}).status_code,422)

    def test_monitoring_controls(self):
        reference=pd.DataFrame({'temp':np.arange(100)+250,'rain_1h':np.zeros(100),'clouds_all':np.arange(100)})
        self.assertEqual(check_drift(reference,reference)['status'],'PASS')
        shifted=reference.copy();shifted.temp+=100
        self.assertEqual(check_drift(reference,shifted)['status'],'ALERT')


if __name__=='__main__':unittest.main()
