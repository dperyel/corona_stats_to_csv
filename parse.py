import requests
import pandas as pd
import os
import os.path
from datetime import date, timedelta

def main():
    if not os.path.exists("./stats"):
        os.mkdir("./stats")

    iso_date = date.today().isoformat()
    yesterday = date.today() - timedelta(days=1)
    iso_date_yesterday = yesterday.isoformat()
    path_with_date = to_path(iso_date)
    path_with_date_yesterday = to_path(iso_date_yesterday)

    if os.path.exists(path_with_date):
        print('You already have the data for today')
        return

    print('Starting the get HTML from https://www.worldometers.info')
    stats_page = requests.get("https://www.worldometers.info/coronavirus/")

    print(f'Data received with status code {stats_page.status_code}')
    if stats_page.status_code == 200:
        all_tables = pd.read_html(stats_page.content)
        print(len(all_tables))
        data_frame = all_tables[0]
        date_frame_yesterday = all_tables[1]
        remove_if_exists(path_with_date_yesterday)

        path_to_current = to_path('current')
        remove_if_exists(path_to_current)

        print('Saving files:')
        data_frame.to_csv(path_to_current, encoding="utf-8", index=False)
        print('\t' + path_to_current)
        data_frame.to_csv(path_with_date, encoding="utf-8", index=False)
        print('\t' + path_with_date)
        date_frame_yesterday.to_csv(path_with_date_yesterday, encoding="utf-8", index=False)
        print('\t' + path_with_date_yesterday)

def to_path(name):
    return f'./stats/{name}.csv'

def remove_if_exists(path):
    if os.path.exists(path):
        os.remove(path)

if __name__ == "__main__":
    main()
