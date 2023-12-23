import requests
import pytz
from datetime import datetime, timedelta

BASEURL = "https://api.octopus.energy"
PRODUCT = "AGILE-FLEX-22-11-25"
TARIFF = "E-1R-AGILE-FLEX-22-11-25-B"
API_ENDPOINT = f"{BASEURL}/v1/products/{PRODUCT}/electricity-tariffs/{TARIFF}/standard-unit-rates/"

def fetch_rates():
    response = requests.get(API_ENDPOINT)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def convert_date(utc_time_str):
    utc_time = datetime.fromisoformat(utc_time_str.replace("Z", "+00:00"))
    timezone = pytz.timezone("Europe/London")
    time = utc_time.astimezone(timezone)
    return time

# New Function: Check if a time period is within the next 12 hours
def within_next_12_hours(from_time, to_time, current_time):
    twelve_hrs_later = current_time + timedelta(hours=12)
    return to_time <= twelve_hrs_later and (from_time is None or from_time > current_time)

# New Function: Check if a time period is within the next 24 hours
def within_next_24_hours(from_time, to_time, current_time):
    twelve_hrs_later = current_time + timedelta(hours=24)
    return to_time <= twelve_hrs_later and (from_time is None or from_time > current_time)

def get_rate():
    rates_data = fetch_rates()

    # Get current time in bst timezone
    current_time_converted = datetime.now(pytz.timezone("Europe/London"))

    for rate in rates_data["results"]:
        valid_from_converted = convert_date(rate["valid_from"])

        # Compare rate's validity period with the current time
        if valid_from_converted <= current_time_converted:
            valid_to = rate.get("valid_to", "Ongoing")
            
            if valid_to != "Ongoing":
                valid_to_converted = convert_date(valid_to)

                # If the rate is expired then skip this iteration
                if valid_to_converted < current_time_converted:
                    continue

            value_inc_vat = float(rate["value_inc_vat"])  # Ensure value is a float for comparison
            print(f"Current rate: {value_inc_vat}p/kWh")
            return value_inc_vat

def check_for_negative_rates():
    rates_data = fetch_rates()

    # Get current time in bst timezone
    current_time_converted = datetime.now(pytz.timezone("Europe/London"))
    
    negative_rates = []  # Stores the negative rates within the next 24 hrs

    for rate in rates_data["results"]:
        valid_from_converted = convert_date(rate["valid_from"])
        valid_to = rate.get("valid_to", "Ongoing")

        if valid_to != "Ongoing":
            valid_to_converted = convert_date(valid_to)
        else:
            valid_to_converted = None

        # Check if rate is valid in the next 24 hours
        if within_next_24_hours(valid_from_converted, valid_to_converted, current_time_converted):
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

def av_rate_results_table():
    # Get the average rates for a window size of 5 hours and create new table
    data = fetch_rates()
    result = []
    window_size = 10
    running_sum = 0
    data = data['results']

    # Sort data based on 'valid_from' date in ascending order
    data = sorted(data, key=lambda x: x['valid_from'])

    for i, row in enumerate(data):
        
        running_sum += int(round(row['value_inc_vat']))
        if i >= window_size:
            running_sum -= int(round(data[i - window_size]['value_inc_vat']))
            result.append({
                'valid_from': data[i - window_size + 1]['valid_from'],
                'valid_to': row['valid_to'],
                'value_inc_vat': int(round(row['value_inc_vat'])),
                'average_inc_vat': running_sum / window_size if window_size > 0 else None
            })
        elif i == window_size - 1:
            result.append({
                'valid_from': data[0]['valid_from'],
                'valid_to': row['valid_to'],
                'value_inc_vat': int(round(row['value_inc_vat'])),
                'average_inc_vat': running_sum / (i + 1)
            })
        else:
            result.append({
                'valid_from': data[0]['valid_from'],
                'valid_to': row['valid_to'],
                'value_inc_vat': int(round(row['value_inc_vat'])),
                'average_inc_vat': None
            })
    return result

def get_avg_rate():
    data = fetch_rates()
    rates_data = data['results']

    # Get current time in Europe/London timezone
    current_time_converted = datetime.now(pytz.timezone("Europe/London"))
    
    rates_next_12_hrs = []  # Stores the rates valid within the next 12 hrs

    for rate in rates_data:
        valid_from_converted = convert_date(rate["valid_from"])
        valid_to = rate.get("valid_to", "Ongoing")

        if valid_to != "Ongoing":
            valid_to_converted = convert_date(valid_to)
        else:
            valid_to_converted = None

        # Check if rate is valid in the next 12 hours
        if within_next_12_hours(valid_from_converted, valid_to_converted, current_time_converted):
            value_inc_vat = float(rate["value_inc_vat"])  # Ensure value is a float
            rates_next_12_hrs.append(value_inc_vat)  # Add rate to list

    # Compute average if list is not empty
    if rates_next_12_hrs:
        avg_rate_next_12_hrs = sum(rates_next_12_hrs) / len(rates_next_12_hrs)
        print(f"Average rate for the next 12 hours: {int(avg_rate_next_12_hrs)}p/kWh")
    else:
        print("No rates available for the next 12 hours.")
    return int(avg_rate_next_12_hrs)

def get_min_avg_rate():
    rates_data = av_rate_results_table()

    # Get current time in BST timezone
    current_time_converted = datetime.now(pytz.timezone("Europe/London"))

    min_avg_rate = float('inf')  # Initialize with positive infinity
    min_avg_rate_valid_from = None

    for rate in rates_data:
        valid_from_converted = convert_date(rate["valid_from"])
        valid_to = rate.get("valid_to", "Ongoing")

        if valid_to != "Ongoing":
            valid_to_converted = convert_date(valid_to)
        else:
            valid_to_converted = None

        # Check if rate is valid in the next 12 hours
        if within_next_12_hours(valid_from_converted, valid_to_converted, current_time_converted):
            average_inc_vat = float(rate["average_inc_vat"])  # Ensure value is a float

            # Update min_avg_rate and corresponding valid_from if a lower value is found
            if average_inc_vat < min_avg_rate:
                min_avg_rate = average_inc_vat
                min_avg_rate_valid_from = valid_from_converted
                min_avg_rate_valid_to = valid_to_converted
                min_avg_rate_average_inc_vat = average_inc_vat

    # Print the valid_from time for the row with the lowest average_inc_vat
    if min_avg_rate_valid_from:
        print(f"Valid_from time for the lowest average rate: {min_avg_rate_valid_from}")
    else:
        print("No valid_from time available for the lowest average rate.")

    return min_avg_rate_valid_from, min_avg_rate_valid_to, min_avg_rate_average_inc_vat