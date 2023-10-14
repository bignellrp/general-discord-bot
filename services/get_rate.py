import requests
import os
import pytz
from datetime import datetime, timedelta
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

# New Function: Check if a time period is within the next 12 hours
def within_next_12_hours(from_time, to_time, current_time):
    twelve_hrs_later = current_time + timedelta(hours=12)
    return from_time <= twelve_hrs_later and (to_time is None or to_time > current_time)

# New Function: Check if a time period is within the next 12 hours
def within_next_24_hours(from_time, to_time, current_time):
    twelve_hrs_later = current_time + timedelta(hours=24)
    return from_time <= twelve_hrs_later and (to_time is None or to_time > current_time)

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

def get_avg_rate():
    rates_data = fetch_rates()

    # Get current time in bst timezone
    current_time_bst = datetime.now(pytz.timezone("Europe/London"))
    
    rates_next_12_hrs = []  # Stores the rates valid within the next 12 hrs

    for rate in rates_data["results"]:
        valid_from_bst = convert_to_bst(rate["valid_from"])
        valid_to = rate.get("valid_to", "Ongoing")

        if valid_to != "Ongoing":
            valid_to_bst = convert_to_bst(valid_to)
        else:
            valid_to_bst = None

        # Check if rate is valid in the next 12 hours
        if within_next_12_hours(valid_from_bst, valid_to_bst, current_time_bst):
            value_inc_vat = float(rate["value_inc_vat"])  # Ensure value is a float
            rates_next_12_hrs.append(value_inc_vat)  # Add rate to list

    # Compute average if list is not empty
    if rates_next_12_hrs:
        avg_rate_next_12_hrs = sum(rates_next_12_hrs) / len(rates_next_12_hrs)
        print(f"Average rate for the next 12 hours: {avg_rate_next_12_hrs}p/kWh")
    else:
        print("No rates available for the next 12 hours.")
    return int(avg_rate_next_12_hrs)

def check_for_negative_rates():
    rates_data = fetch_rates()

    # Get current time in bst timezone
    current_time_bst = datetime.now(pytz.timezone("Europe/London"))
    
    negative_rates = []  # Stores the negative rates within the next 24 hrs

    for rate in rates_data["results"]:
        valid_from_bst = convert_to_bst(rate["valid_from"])
        valid_to = rate.get("valid_to", "Ongoing")

        if valid_to != "Ongoing":
            valid_to_bst = convert_to_bst(valid_to)
        else:
            valid_to_bst = None

        # Check if rate is valid in the next 24 hours
        if within_next_24_hours(valid_from_bst, valid_to_bst, current_time_bst):
            value_inc_vat = float(rate["value_inc_vat"])  # Ensure value is a float

            if value_inc_vat < 0:    # Check if the rate is negative
                negative_rates.append(value_inc_vat)  # Add negative rate to its list

    # Check for negative rates
    if negative_rates:
        print("There are some negative rates in the next 24 hours.")
        result = True
    else:
        print("There are no negative rates in the next 24 hours.")
        result = False

    return result

def get_optimal_time():
    rates_data = fetch_rates()

    # Get current time in bst timezone
    current_time_bst = datetime.now(pytz.timezone("Europe/London"))
    
    results = rates_data["results"]
    future_results = [rate for rate in results if convert_to_bst(rate["valid_from"]) > current_time_bst]

    optimal_period_end_time = None
    lowest_average = float('inf')

    for i in range(len(future_results) - 9):  # loop until the last possible 5hr block ends
        five_hour_period = future_results[i:i+10]  # get the next 5hr block of rates
        five_hour_average = sum(float(rate["value_inc_vat"]) for rate in five_hour_period) / 10  # calculate average

        if five_hour_average < lowest_average:  # check if the current block has a lower average than previous
            lowest_average = five_hour_average
            optimal_period_end_time = convert_to_bst(five_hour_period[0]["valid_from"])

    if optimal_period_end_time:
        print(f"Optimal period end time (BST): {optimal_period_end_time}")
    else:
        print("No optimal period found in the future.")

    return optimal_period_end_time

def get_optimal_time12():
    rates_data = fetch_rates()

    # Get current time in bst timezone
    current_time_bst = datetime.now(pytz.timezone("Europe/London"))
    
    results = rates_data["results"]
    future_results = [
        rate for rate in results 
        if within_next_12_hours(
            convert_to_bst(rate["valid_from"]),
            convert_to_bst(rate.get("valid_to")) if rate.get("valid_to") != "Ongoing" else None,
            current_time_bst
        )
    ]

    optimal_period_end_time = None
    lowest_average = float('inf')

    for i in range(len(future_results) - 9):  # loop until the last possible 5hr block ends
        five_hour_period = future_results[i:i+10]  # get the next 5hr block of rates
        five_hour_average = sum(float(rate["value_inc_vat"]) for rate in five_hour_period) / 10  # calculate average

        if five_hour_average < lowest_average:  # check if the current block has a lower average than previous
            lowest_average = five_hour_average
            optimal_period_end_time = convert_to_bst(five_hour_period[0]["valid_from"])

    if optimal_period_end_time:
        print(f"Optimal period end time (BST): {optimal_period_end_time}")
    else:
        print("No optimal period found in the next 12 hours.")

    return optimal_period_end_time

def get_optimal_time24():
    rates_data = fetch_rates()

    # Get current time in bst timezone
    current_time_bst = datetime.now(pytz.timezone("Europe/London"))
    
    results = rates_data["results"]
    future_results = [
        rate for rate in results 
        if within_next_24_hours(
            convert_to_bst(rate["valid_from"]),
            convert_to_bst(rate.get("valid_to")) if rate.get("valid_to") != "Ongoing" else None,
            current_time_bst
        )
    ]

    optimal_period_end_time = None
    lowest_average = float('inf')

    for i in range(len(future_results) - 9):  # loop until the last possible 5hr block ends
        five_hour_period = future_results[i:i+10]  # get the next 5hr block of rates
        five_hour_average = sum(float(rate["value_inc_vat"]) for rate in five_hour_period) / 10  # calculate average

        if five_hour_average < lowest_average:  # check if the current block has a lower average than previous
            lowest_average = five_hour_average
            optimal_period_end_time = convert_to_bst(five_hour_period[0]["valid_from"])

    if optimal_period_end_time:
        print(f"Optimal period end time (BST): {optimal_period_end_time}")
    else:
        print("No optimal period found in the next 24 hours.")

    return optimal_period_end_time