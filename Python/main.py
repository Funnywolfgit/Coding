import datetime
import pandas as pd
import bs4
import re
import requests
from bs4 import BeautifulSoup

url = "https://andelenergi.dk/kundeservice/aftaler-og-priser/timepris/"
response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    for ele in soup.find_all('a', href=re.compile("^https://")):
        if not "csv" in ele["href"]:
            continue
        else:
            csv_url = ele.get("href")

df = pd.read_csv(csv_url)
energi_pris_liste = pd.DataFrame()
energi_pris_liste = pd.concat([energi_pris_liste,df]).drop_duplicates()

time_status = str(datetime.datetime.now())
current_month = time_status[:10]
current_hour = time_status[11:13]+":00"
current_price = df.loc[df["Date"] == current_month][current_hour]
current_kwh_price = float(current_price.reset_index(drop=True)[0].replace(",", "."))

if current_kwh_price <= 3 :
    print(f"Low cost power at {current_kwh_price} kr/kwh")
else :
    print(f"High cost power at {current_kwh_price} kr/kwh")