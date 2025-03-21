import datetime
import json
import logging
import os
import sys
from notion_client import Client
from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def authenticate_garmin(email, password):
    """
    Authenticate with Garmin Connect.
    
    Args:
        email (str): Garmin Connect email
        password (str): Garmin Connect password
        
    Returns:
        Garmin: Authenticated Garmin client object
    """
    try:
        client = Garmin(email, password)
        
        client.login()
        return client
    
    except (
        GarminConnectConnectionError,
        GarminConnectAuthenticationError,
        GarminConnectTooManyRequestsError,
    ) as err:
        logger.error(f"Authentication error: {err}")
        sys.exit(1)

def get_body_battery(client, date=None):
    """
    Get body battery data for a specific date.
    
    Args:
        client (Garmin): Authenticated Garmin client
        date (datetime.date, optional): Date to fetch data for. Defaults to today.
        
    Returns:
        dict: Body battery data
    """
    if date is None:
        date = datetime.date.today()
    
    try:
        # Format date for the API call
        formatted_date = date.strftime("%Y-%m-%d")
        
        # Get body battery data
        logger.info(f"Getting body battery data for {formatted_date}")
        body_battery_data = client.get_body_battery(formatted_date)
        
        return body_battery_data
    
    except (
        GarminConnectConnectionError,
        GarminConnectAuthenticationError,
        GarminConnectTooManyRequestsError,
    ) as err:
        logger.error(f"Error fetching body battery data: {err}")
        return None
def write_metrics_to_notion(notion_token, notion_db_id, charged_value, drained_value, timestamp):

    Write body battery metrics to a Notion database.
"""
    Args:
        notion_token (str): Notion API token
        notion_db_id (str): Notion database ID
        charged_value (float): Body battery charged value
        drained_value (float): Body battery drained value
        timestamp (str): Timestamp of the reading
 """   
    Returns:
        bool: True if successful, False otherwise
  
    try:
        notion = Client(auth=notion_token)
        
        notion.pages.create(
            parent={"database_id": notion_db_id},
            properties={
                "Body Battery Charged Value": {
                    "number": charged_value
                },
                "Body Battery Drained Value": {
                    "number": drained_value
                },
                "Timestamp": {
                    "rich_text": [
                        {
                            "text": {
                                "content": timestamp
                            }
                        }
                    ]
                },
                "Name": {
                    "title": [
                        {
                            "text": {
                                "content": f"Body Battery Metrics {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                            }
                        }
                    ]
                }
            }
        )
        
        logger.info(f"Successfully wrote body battery metrics to Notion")
        return True
        
    except Exception as e:
        logger.error(f"Error writing to Notion: {e}")
        return False

def main():
    """Main function to execute the script."""
    # Get Notion credentials from environment variables
    notion_token = os.getenv("NOTION_TOKEN")
    notion_db_id = os.getenv("NOTION_V_DB_ID")
    
    # Garmin Connect credentials from environment variables
    email = os.getenv("GARMIN_EMAIL")
    password = os.getenv("GARMIN_PASSWORD")
    
    # Authenticate with Garmin Connect
    client = authenticate_garmin(email, password)
    
    # Get today's body battery data
    today = datetime.date.today()
    body_battery_data = get_body_battery(client, today)
    
    if body_battery_data:
        # Print the data in a readable format
        print("\nBody Battery Data:")
        print("==================")
        print(f"Date: {today.strftime('%Y-%m-%d')}")
        
        # Pretty print the JSON response
        print("\nDetailed data:")
        print(json.dumps(body_battery_data, indent=4))
        
        # Extract and display key metrics if available
        if body_battery_data:
            try:
                # Get the latest reading
                latest = body_battery_data[-1]
                print("\nLatest Body Battery Reading:")
                print(f"Timestamp: {latest.get('timestamp', 'N/A')}")
                print(f"Battery Level: {latest.get('bodyBatteryValue', 'N/A')}%")
                print(f"Charged: {latest.get('bodyBatteryChargeValue', 'N/A')}%")
                print(f\"Drained: {latest.get('bodyBatteryDrainValue', 'N/A')}%\")
                
                # Write metrics to Notion if credentials are available
                if notion_token and notion_db_id:
                    charged_value = latest.get('bodyBatteryChargeValue', 0)
                    drained_value = latest.get('bodyBatteryDrainValue', 0)
                    timestamp = latest.get('timestamp', datetime.datetime.now().isoformat())
                    
                    success = write_metrics_to_notion(
                        notion_token, 
                        notion_db_id, 
                        charged_value, 
                        drained_value, 
                        timestamp
                    )
                    
                    if success:
                        print("Successfully wrote metrics to Notion")
                    else:
                        print("Failed to write metrics to Notion")
                else:
                    logger.warning("Notion credentials not provided. Skipping write to Notion.")
                
                # Calculate daily stats
                if len(body_battery_data) > 0:
                    max_value = max(item.get('bodyBatteryValue', 0) for item in body_battery_data)
                    min_value = min(item.get('bodyBatteryValue', 100) for item in body_battery_data)
                    
                    print("\nDaily Summary:")
                    print(f"Max Battery: {max_value}%")
                    print(f"Min Battery: {min_value}%")
                    print(f"Range: {max_value - min_value}%")
            except (IndexError, KeyError, ValueError) as e:
                logger.error(f"Error processing body battery data: {e}")
    else:
        print("No body battery data available for today.")

if __name__ == "__main__":
    main()
