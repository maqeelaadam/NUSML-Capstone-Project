"""FastAPI prediction mock-up; launch using python -m ...deployment.api."""
import logging
from datetime import datetime
from functools import lru_cache
from pathlib import Path
import joblib
import pandas as pd
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field,field_validator
from capstone_part3.supervised.common import features
from capstone_part2.cleaning import WEATHER_SEVERITY

logger=logging.getLogger(__name__)
ROOT=Path(__file__).resolve().parents[2]
app=FastAPI(title="I-94 Traffic Prediction Simulation")


class TrafficInput(BaseModel):
    date_time: datetime
    temp: float=Field(gt=0,le=350,allow_inf_nan=False)
    rain_1h: float=Field(ge=0,le=9000,allow_inf_nan=False)
    snow_1h: float=Field(ge=0,allow_inf_nan=False)
    clouds_all: float=Field(ge=0,le=100,allow_inf_nan=False)
    weather_main: str
    holiday: str="None"

    @field_validator("date_time")
    @classmethod
    def local_time(cls,value):
        if value.tzinfo is not None or value.minute or value.second or value.microsecond:
            raise ValueError("Use a naive supplied-local timestamp at an exact hour")
        return value

    @field_validator("weather_main")
    @classmethod
    def known_weather(cls,value):
        if value not in WEATHER_SEVERITY:raise ValueError("Unknown weather category")
        return value


@lru_cache(maxsize=1)
def load_model():
    return joblib.load(ROOT/"capstone_part3/models/traffic_model.joblib")


@app.get("/health")
def health():
    return {"status":"ready" if (ROOT/"capstone_part3/models/traffic_model.joblib").exists() else "model_missing","simulation":True}


@app.post("/predict")
def predict(request:TrafficInput):
    try:
        data=pd.DataFrame([request.model_dump()])
        value=float(load_model().predict(features(data))[0])
        logger.info("Served simulated traffic prediction for %s",request.date_time)
        return {"predicted_vehicles_per_hour":value,"model_version":"v1","simulation":True,"scope":"Retrospective traffic estimate given supplied weather; single corridor."}
    except (OSError,ValueError,RuntimeError) as exc:
        logger.error("Prediction unavailable: %s",exc)
        raise HTTPException(status_code=503,detail="Prediction model unavailable; run the training workflow") from exc


if __name__=="__main__":
    import uvicorn
    logging.basicConfig(level=logging.INFO,format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",handlers=[logging.StreamHandler(),logging.FileHandler(ROOT/"capstone_part3/deployment.log",encoding="utf-8")],force=True)
    uvicorn.run(app,host="127.0.0.1",port=8000)
