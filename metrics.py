from datetime import date, timedelta
from garminconnect import Garmin
from notion_client import Client
from dotenv import load_dotenv
import pytz
import os

# Constants 

local_tz = pytz.timezone('America/Chicago')

# Load Env Variables
"""
load_dotenv()


def get_max_metrics(garmin):
    startdate = date.today() - timedelta(days=1)
    daterange = [startdate + timedelta(days=x)
                for x in range((date.today() - startdate).days)]
    metrics = []
    for d in daterange: 
        metrics += garmin.get_max_metrics(d.isoformat(), d.isoformat())
    return metrics

    "properties":{
    'date': {'date': {'start': date}},
    "vo2max": {'number': vo2max},
    }

    write_row(client, DB_ID, today, vo2max)

def write_row(client, database_id, date, miles, vo2max, duration, effect):
    client.pages.create(
        **{
            "parent":{
                "database_id": database_id
            },
            "properties":{
                'date': {'date': {'start': date}},
                "vo2max": {'number': vo2max},
            }
        }
    )


    stats = garmin.get_max_metrics(today)

    vo2max = stats[0]['generic']['vo2MaxPreciseValue']

def main():
    load_dotenv()

    # Initialize Garmin and Notion clients using environment variables
    garmin_email = os.getenv("GARMIN_EMAIL")
    garmin_password = os.getenv("GARMIN_PASSWORD")
    notion_token = os.getenv("NOTION_TOKEN")
    database_id = os.getenv("NOTION_V_DB_ID")
    write_row(client, DB_ID, today, vo2max)

if __name__ == '__main__':
     main()

"""



