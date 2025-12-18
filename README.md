# origin-revenue-ingestion

Pulls monthly revenue tables from the legacy Origin endpoint:

https://oldapi.originmedia.tv/report/revenue?time=YYYYMM

## What it does
- Iterates through the last 48 months
- Scrapes the revenue table
- Normalizes into a single CSV
- Adds a Report Month column

## Usage
```bash
pip install -r requirements.txt
python src/fetch_revenue.py
