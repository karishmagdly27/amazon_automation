import requests
import json
import time
from twilio.rest import Client
from datetime import datetime
import pytz

# Twilio configuration
TWILIO_ACCOUNT_SID = "ACf01efbb20d1f40444fabd1b7b51f7e8f"
TWILIO_AUTH_TOKEN = "034988fc028958c7a28f2647044cab58"
TWILIO_PHONE_NUMBER = "+17754875108"
RECIPIENT_PHONE_NUMBER = "+14376793891"

# GraphQL API details
url = "https://e5mquma77feepi2bdn4d6h3mpu.appsync-api.us-east-1.amazonaws.com/graphql"
payload = {
    "operationName": "searchJobCardsByLocation",
    "variables": {
        "searchJobRequest": {
            "locale": "en-CA",
            "country": "Canada",
            "keyWords": "",
            "equalFilters": [],
            "containFilters": [
                {
                    "key": "isPrivateSchedule",
                    "val": [
                        "false"
                    ]
                }
            ],
            "rangeFilters": [],
            "orFilters": [],
            "dateFilters": [
                {
                    "key": "firstDayOnSite",
                    "range": {
                        "startDate": "2024-12-07"
                    }
                }
            ],
            "sorters": [],
            "pageSize": 100,
            "geoQueryClause": {
                "lat": 50.926163435,
                "lng": -84.74493,
                "unit": "km",
                "distance": 150
            }
        }
    },
    "query": "query searchJobCardsByLocation($searchJobRequest: SearchJobRequest!) {\n  searchJobCardsByLocation(searchJobRequest: $searchJobRequest) {\n    nextToken\n    jobCards {\n      jobId\n      language\n      dataSource\n      requisitionType\n      jobTitle\n      jobType\n      employmentType\n      city\n      state\n      postalCode\n      locationName\n      totalPayRateMin\n      totalPayRateMax\n      tagLine\n      bannerText\n      image\n      jobPreviewVideo\n      distance\n      featuredJob\n      bonusJob\n      bonusPay\n      scheduleCount\n      currencyCode\n      geoClusterDescription\n      surgePay\n      jobTypeL10N\n      employmentTypeL10N\n      bonusPayL10N\n      surgePayL10N\n      totalPayRateMinL10N\n      totalPayRateMaxL10N\n      distanceL10N\n      monthlyBasePayMin\n      monthlyBasePayMinL10N\n      monthlyBasePayMax\n      monthlyBasePayMaxL10N\n      jobContainerJobMetaL1\n      virtualLocation\n      poolingEnabled\n      __typename\n    }\n    __typename\n  }\n}\n"
}
headers = {"Content-Type": "application/json", "Accept": "*/*"}

# Function to send a call using Twilio
def make_call(message):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    call = client.calls.create(
        to=RECIPIENT_PHONE_NUMBER,
        from_=TWILIO_PHONE_NUMBER,
        twiml=f'<Response><Say>{message}</Say></Response>'
    )
    print(f"Call initiated: {call.sid}")

# Function to prompt user for token
def get_token():
    new_token = input("Enter a new Authorization token: ")
    global headers
    headers["Authorization"] = new_token
    return time.time()

# Function to check if the token is expired
def is_token_expired(token_time):
    isExpired = (time.time() - token_time) >= 3600
    if(isExpired):
        make_call(token_expired_message)
    
    return isExpired

# Function to check for jobs
def check_for_jobs():

    token_generation_time = None

    while True:
        # Ensure token is valid
        if "Authorization" not in headers or not headers["Authorization"] or is_token_expired(token_generation_time):
            token_generation_time = get_token()

        response = requests.post(url, headers=headers, json=payload)
        current_time = datetime.now(pytz.timezone("America/Toronto")).strftime("%Y-%m-%d %H:%M:%S")

        if response.status_code == 200:
            data = response.json()
            job_cards = data.get("data", {}).get("searchJobCardsByLocation", {}).get("jobCards", [])

            if job_cards:
                print(f"Job Cards Found: {current_time}")
                print(json.dumps(job_cards, indent=2))
                make_call(job_found_message)
                break
            else:
                print(f"--------------------------------------No jobs found!!! - {current_time}")
        else:
            print(f"Failed to fetch data. HTTP Status Code: {response.status_code}")
            print("Response:", response.text)
            make_call(error_message)
            break

        # time.sleep(10)

if __name__ == "__main__":

    job_found_message = "Jobs found"
    token_expired_message = "Token expired"
    error_message = "Execution stopped"

    check_for_jobs()
