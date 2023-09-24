import requests
import os
import pytz
from datetime import datetime
from dotenv import load_dotenv

# Load values from .env
load_dotenv()

# Access the API key
API_KEY = os.environ["OCTOPUS_API_KEY"]

BASEURL = "https://api.octopus.energy"
PRODUCT = "AGILE-FLEX-22-11-25"
TARIFF = "E-1R-AGILE-FLEX-22-11-25-B"
API_ENDPOINT = f"{BASEURL}/v1/products/{PRODUCT}/electricity-tariffs/{TARIFF}/standard-unit-rates/"

def fetch_rates():
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    response = requests.get(API_ENDPOINT, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def convert_to_bst(utc_time_str):
    utc_time = datetime.fromisoformat(utc_time_str.replace("Z", "+00:00"))
    bst_timezone = pytz.timezone("Europe/London")
    bst_time = utc_time.astimezone(bst_timezone)
    return bst_time

def get_rate():
    rates_data = fetch_rates()

    # Get current time in bst timezone
    current_time_bst = datetime.now(pytz.timezone("Europe/London"))

    for rate in rates_data["results"]:
        valid_from_bst = convert_to_bst(rate["valid_from"])

        # Compare rate's validity period with the current time
        if valid_from_bst <= current_time_bst:
            valid_to = rate.get("valid_to", "Ongoing")
            
            if valid_to != "Ongoing":
                valid_to_bst = convert_to_bst(valid_to)

                # If the rate is expired then skip this iteration
                if valid_to_bst < current_time_bst:
                    continue

            value_inc_vat = float(rate["value_inc_vat"])  # Ensure value is a float for comparison
            print(f"Current rate: {value_inc_vat}p/kWh")
            return value_inc_vat