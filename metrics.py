from datetime import date, timedelta
from garminconnect import Garmin
from notion_client import Client
from dotenv import load_dotenv
import pytz
import os

# Constants 

local_tz = pytz.timezone('America/Chicago')

# Load Env Variables

load_dotenv()
CONFIG = dotenv_values()

def get_max_metrics(garmin):
    today = datetime.today().date()
    return garmin.get_max_metrics(today.isoformat())
    stats = garmin.get_max_metrics(today)

    vo2max = stats[0]['generic']['vo2MaxPreciseValue']
   

    write_row(client, DB_ID, today, vo2max)
    
def main():
    load_dotenv()

    # Initialize Garmin and Notion clients using environment variables
    garmin_email = os.getenv("GARMIN_EMAIL")
    garmin_password = os.getenv("GARMIN_PASSWORD")
    notion_token = os.getenv("NOTION_TOKEN")
    database_id = os.getenv("NOTION_V_DB_ID")

    # Initialize Garmin client and login
    garmin = Garmin(garmin_email, garmin_password)
    garmin.login()
    client = Client(auth=notion_token)

if __name__ == '__main__':
    main()





