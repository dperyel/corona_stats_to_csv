""" Saving a statistics about COVID-19 from the worldometers """

from datetime import date, timedelta
import os
import requests
import pandas as pd

def main():
    """ Main """
    if not os.path.exists("./stats"):
        os.mkdir("./stats")

    iso_date = date.today().isoformat()
    yesterday = date.today() - timedelta(days=1)
    iso_date_yesterday = yesterday.isoformat()
    path_with_date = to_path(iso_date)
    path_with_date_yesterday = to_path(iso_date_yesterday)

    if os.path.exists(path_with_date):
        logger('You already have the data for today')
        return

    logger('Starting the get HTML from https://www.worldometers.info')
    stats_page = requests.get("https://www.worldometers.info/coronavirus/")

    logger(f'Data received with status code {stats_page.status_code}')
    if stats_page.status_code == 200:
        all_tables = pd.read_html(stats_page.content)
        data_frame = all_tables[0]
        date_frame_yesterday = all_tables[1]
        remove_if_exists(path_with_date_yesterday)

        path_to_current = to_path('current')
        remove_if_exists(path_to_current)

        to_csv(data_frame, path_to_current)
        to_csv(data_frame, path_with_date)
        to_csv(date_frame_yesterday, path_with_date_yesterday)

def to_csv(data_frame, path):
    """ Will save data frame data to the files to a given path """
    logger(f'Saving {path}')
    data_frame.to_csv(path, encoding="utf-8", index=False)

def logger(message, logger_callback=print):
    """ Loggin data, by default print it to a standard out """
    logger_callback(message)

def to_path(name, path='./stats'):
    """ Makes a relative path to a csv """
    return f'{path}/{name}.csv'

def remove_if_exists(path):
    """ Checks if file already exists and removes it """
    if os.path.exists(path):
        logger(f'Removing {path}')
        os.remove(path)

if __name__ == "__main__":
    main()
