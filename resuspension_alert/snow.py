import requests
import pandas as pd
from datetime import datetime, timedelta, timezone

def check_snow():
    '''Checks whether the Spirit Lake SNOTEL station had any snow on the selected date. Returns True if there is NO snow, False if there IS snow. Date must be input as a datetime.'''
    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=7)
    url = 'https://wcc.sc.egov.usda.gov/awdbRestApi/services/v1/data'
    station_ID = '777:WA:SNTL'
    params = {
        "stationTriplets": station_ID,
        "elements": "SNWD",
        "duration": "DAILY",
        "beginDate": start_date.strftime("%Y-%m-%d"),
        "endDate": end_date.strftime("%Y-%m-%d"),
        "periodRef": "END",
        "returnFlags": "false",
        "returnOriginalValues": "false",
        "returnSuspectData": "false"
        }
    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise Exception(f"API error: {response.status_code}")

    data = response.json()
    observations = data[0]["data"]
    observations = [
        obs for obs in observations
        if obs["values"][0]["value"] is not None
        ]

    snow_depth = observations[-1]["values"][0]["value"]

    if snow_depth == 0:
        return True
    else:
        return False
