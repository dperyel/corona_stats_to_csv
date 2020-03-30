import requests
import pandas as pd
import os
import os.path
from time import time
from datetime import date

def main():
    if not os.path.exists("./stats"):
        os.mkdir("./stats")

    iso_date = date.fromtimestamp(time()).isoformat()
    path_with_date = f'./stats/{iso_date}.csv'

    if os.path.exists(path_with_date):
        print('You already have the data for today')
        return

    print('Starting the get HTML from https://www.worldometers.info')
    stats_page = requests.get("https://www.worldometers.info/coronavirus/")

    print(f'Data received with status code {stats_page.status_code}')
    if stats_page.status_code == 200:
        all_tables = pd.read_html(stats_page.content)
        data_frame = all_tables[0]

        path_to_current = f'./stats/current.csv'
        removeIfExists(path_to_current)

        print('Saving files:')
        data_frame.to_csv(path_to_current, encoding="utf-8", index=False)
        print('\t' + path_to_current)
        data_frame.to_csv(path_with_date, encoding="utf-8", index=False)
        print('\t' + path_with_date)

def removeIfExists(path):
    if os.path.exists(path):
        os.remove(path)

if __name__ == "__main__":
    main()
