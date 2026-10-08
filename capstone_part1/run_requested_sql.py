"""Import the unchanged CSV and execute each requested calculation in SQLite."""
import argparse
import csv
import hashlib
import json
import logging
import math
from pathlib import Path
import re
import sqlite3

logger = logging.getLogger(__name__)
ROOT = Path(__file__).resolve().parents[1]
COLUMNS = ['holiday','temp','rain_1h','snow_1h','clouds_all','weather_main',
           'weather_description','date_time','traffic_volume']


def run(source, output):
    output.mkdir(parents=True,exist_ok=True)
    database = ROOT / 'capstone_part2/data/processed/requested_raw_analysis.sqlite'
    database.parent.mkdir(parents=True,exist_ok=True)
    with source.open(encoding='utf-8-sig',newline='') as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != COLUMNS:
            raise ValueError('Unexpected CSV schema or column order')
        rows = []
        for line,row in enumerate(reader,start=2):
            if None in row or any(value is None for value in row.values()):
                raise ValueError(f'Malformed CSV row {line}')
            rows.append(tuple(row[column] for column in COLUMNS))
    with sqlite3.connect(database) as connection:
        connection.row_factory = sqlite3.Row
        try:
            connection.execute('SELECT SQRT(9)')
        except sqlite3.OperationalError:
            connection.create_function('SQRT',1,lambda x: None if x is None or x<0 else math.sqrt(x),deterministic=True)
        connection.execute('DROP TABLE IF EXISTS traffic_raw')
        connection.execute('''CREATE TABLE traffic_raw (
            holiday TEXT,temp REAL,rain_1h REAL,snow_1h REAL,clouds_all INTEGER,
            weather_main TEXT,weather_description TEXT,date_time TEXT,traffic_volume INTEGER
        )''')
        connection.executemany('INSERT INTO traffic_raw VALUES (?,?,?,?,?,?,?,?,?)',rows)
        logger.info('Loaded %d unchanged CSV rows into %s',len(rows),database)
        sql = (ROOT / 'capstone_part1/sql/traffic_analysis.sql').read_text()
        results = {'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
                   'analysis_grain':'All supplied CSV rows unless explicitly labelled holiday-hour supplement',
                   'queries':{}}
        for name,body in re.findall(r'-- query: (\w+)\n(.*?)(?=-- query: |\Z)',sql,flags=re.S):
            cursor=connection.execute(body.strip())
            values=[dict(row) for row in cursor.fetchall()]
            results['queries'][name]=values
            if values:
                with (output/(name+'.csv')).open('w',newline='') as handle:
                    writer=csv.DictWriter(handle,fieldnames=list(values[0]),lineterminator='\n')
                    writer.writeheader();writer.writerows(values)
            logger.info('Executed SQL query %s: %d output rows',name,len(values))
        (output/'all_sql_results.json').write_text(json.dumps(results,indent=2)+'\n')
        return results


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--csv',type=Path,default=ROOT/'capstone_part2/data/raw/Metro_Interstate_Traffic_Volume.csv')
    parser.add_argument('--output',type=Path,default=ROOT/'capstone_part1/results/requested_raw_analysis')
    args=parser.parse_args(argv)
    try:
        logging.basicConfig(level=logging.INFO,
            format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
            handlers=[logging.StreamHandler(),logging.FileHandler(ROOT/'capstone_part1/requested_sql.log',encoding='utf-8')],force=True)
        run(args.csv,args.output)
        return 0
    except (OSError,csv.Error,ValueError,sqlite3.Error) as exc:
        logger.error('Requested SQL analysis failed: %s',exc,exc_info=True)
        return 1


if __name__=='__main__':
    raise SystemExit(main())
