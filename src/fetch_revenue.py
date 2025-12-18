import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.relativedelta import relativedelta

BASE_URL = "https://oldapi.originmedia.tv/report/revenue?time={}"
MONTHS_BACK = 48

def generate_months(months_back=48):
    start = datetime.today().replace(day=1)
    return [
        (start - relativedelta(months=i)).strftime("%Y%m")
        for i in range(months_back)
    ]

def fetch_month(ym):
    url = BASE_URL.format(ym)
    print(f"Fetching {ym}")

    r = requests.get(url, timeout=30)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "lxml")
    table = soup.find("table")

    if table is None:
        print(f"⚠️ No table for {ym}")
        return None

    df = pd.read_html(str(table))[0]
    df["Report Month"] = ym
    return df

def main():
    frames = []

    for ym in generate_months(MONTHS_BACK):
        df = fetch_month(ym)
        if df is not None:
            frames.append(df)

    if not frames:
        raise RuntimeError("No data collected")

    final_df = pd.concat(frames, ignore_index=True)
    final_df["Time"] = pd.to_datetime(final_df["Time"], errors="coerce")

    output = "origin_revenue_last_48_months.csv"
    final_df.to_csv(output, index=False)

    print(f"✅ Saved {output}")

if __name__ == "__main__":
    main()
