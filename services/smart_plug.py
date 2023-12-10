import requests
import os
# from PyP100 import PyP100
from dotenv import load_dotenv
import pytz
from datetime import datetime

# Load values from .env
load_dotenv()

# Access the API key
# API_KEY = os.environ["OCTOPUS_API_KEY"]

# BASEURL = "https://api.octopus.energy"
# PRODUCT = "AGILE-FLEX-22-11-25"
# TARIFF = "E-1R-AGILE-FLEX-22-11-25-B"
# API_ENDPOINT = f"{BASEURL}/v1/products/{PRODUCT}/electricity-tariffs/{TARIFF}/standard-unit-rates/"
# EMAIL = os.environ["EMAIL"]
# PASSWORD = os.environ["PASSWORD"]
# SMART_PLUG_IP = os.environ["SMART_PLUG_IP"]
WEBHOOK = os.environ["DISCORD_WEBHOOK"]
# LOG_FILE = "/var/log/cron.log"
# MAXIMUM_RATE = 16 # Set your desired maximum rate here.

def post_to_discord(message):
    data = {
        "content": message
    }
    response = requests.post(WEBHOOK, data=data)
    return response.status_code

def control_smart_plug(action):

    # Get current time in bst timezone
    current_time_bst = datetime.now(pytz.timezone("Europe/London"))

    # Parse into a datetime object
    dt = datetime.fromisoformat(str(current_time_bst))

    # Format the datetime object
    formatted_dt = dt.strftime("%Y-%m-%d %H:%M")

    try:
        # Create a P100 plug object
        #plug = PyP100.P100(SMART_PLUG_IP, EMAIL, PASSWORD)

        #plug.handshake() #Creates the cookies required for further methods
        #plug.login() #Sends credentials to the plug and creates AES Key and IV for further methods

        # Access the API key
        access_token = os.environ["HOME_API"]

        # Home Assistant API endpoint
        api_endpoint = f"http://homeassistant.local:8123/api/services/switch/turn_{action}"

        # Entity ID of your plug switch
        entity_id = "switch.kuga"

        # Headers for the API request
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        # Data for the API request
        data = {
            "entity_id": entity_id,
        }
        
        # Control the smart plug based on the action
        if action == "on":
            #plug.turnOn()
            response = requests.post(api_endpoint, headers=headers, json=data)
            message = f"Plug turned ON at {formatted_dt}!"
            post_to_discord(message)
        elif action == "off":
            #plug.turnOff()
            response = requests.post(api_endpoint, headers=headers, json=data)
            message = f"Plug turned OFF at {formatted_dt}!"
            post_to_discord(message)
    except Exception as e:
        message = f"Failed to control the smart plug. Exception of type {type(e).__name__} occurred: {e}"
        post_to_discord(message)
    return