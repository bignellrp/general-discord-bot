import os
from dotenv import load_dotenv
import requests

# Load values from .env
load_dotenv()

# Access the API key
access_token = os.environ["HOME_API"]

# Home Assistant API endpoint
api_endpoint = f"http://homeassistant.local:8123/api/services/switch/turn_off"

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

# Make the API request to turn off the plug switch
response = requests.post(api_endpoint, headers=headers, json=data)

# Check the response status
if response.status_code == 200:
    print("Plug switch turned off successfully.")
else:
    print(f"Failed to turn off plug switch. Status code: {response.status_code}")
    print(response.text)