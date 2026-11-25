import requests
import csv
import time
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")

LIMIT = 1000
DS = datetime.today()

def run_stock_job():
    DS = datetime.now().strftime('%Y-%m-%d')
    url = f'https://api.massive.com/v3/reference/tickers?market=stocks&active=true&order=asc&limit={LIMIT}&sort=ticker&apiKey={POLYGON_API_KEY}'
    response = requests.get(url)
    tickers = []

    data = response.json()
    for ticker in data['results']:
        ticker['ds'] = DS
        tickers.append(ticker)

    while 'next_url' in data:
        print('requesting next page...')
        time.sleep(14)
        response = requests.get(data['next_url'] + f'&apiKey={POLYGON_API_KEY}')
        data = response.json()
        for ticker in data['results']:
            ticker['ds'] = DS
            tickers.append(ticker)

    example_ticker =  {
        'ticker': 'ZWS', 
        'name': 'Zurn Elkay Water Solutions Corporation', 
        'market': 'stocks', 
        'locale': 'us', 
        'primary_exchange': 'XNYS', 
        'type': 'CS', 
        'active': True, 
        'currency_name': 'usd', 
        'cik': '0001439288', 
        'composite_figi': 'BBG000H8R0N8', 	'share_class_figi': 'BBG001T36GB5', 	
        'last_updated_utc': '2025-09-11T06:11:10.586204443Z',
        'ds': '2025-09-25'
    }

    fieldnames = list(example_ticker.keys())
    output_filename = f'stock_tickers_{DS}.csv'

    load_to_csv(tickers, fieldnames, output_filename)
    print(f'Loaded {len(tickers)} rows to {output_filename}')


def load_to_csv(rows, fieldnames, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()

        for row in rows:
            conformed_row = {k: row.get(k, None) for k in fieldnames}
            writer.writerow(conformed_row)


if __name__ == '__main__':
    run_stock_job()