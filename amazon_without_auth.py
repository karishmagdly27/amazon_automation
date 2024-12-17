import requests
import json
import time
from datetime import datetime
import pytz

# Define the URL and payload
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

# Headers with authorization token
headers = {
    "Content-Type": "application/json",
    "Accept": "*/*"
}

def get_token():
    """Prompt the user to enter a new token."""
    new_token = input("Enter a new Authorization token: ")
    global headers
    headers["Authorization"] = f"Bearer {new_token}"
    return time.time()

def is_token_expired(token_time):
    """Check if the token has expired (valid for 1 hour)."""
    return (time.time() - token_time) >= 3600  # 1 hour in seconds

# Function to check for jobs
def check_for_jobs():
    token_generation_time = None

    while True:
        # Check if token is set and valid
        if "Authorization" not in headers or not headers["Authorization"] or is_token_expired(token_generation_time):
            token_generation_time = get_token()

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            data = response.json()
            job_cards = data.get("data", {}).get("searchJobCardsByLocation", {}).get("jobCards", [])

            if job_cards:
                # Get current time in Kitchener's timezone
                kitchener_tz = pytz.timezone("America/Toronto")
                current_time = datetime.now(kitchener_tz).strftime("%Y-%m-%d %H:%M:%S %Z")
                print(f"Job Cards Found: {current_time}")
                print(json.dumps(job_cards, indent=2))
                break
            else:
                print("-----------------------------------------------No jobs found")
        else:
            print(f"Failed to fetch data. HTTP Status Code: {response.status_code}")
            print("Response:", response.text)

        # time.sleep(10)

# Start the job check loop
if __name__ == "__main__":
    check_for_jobs()
