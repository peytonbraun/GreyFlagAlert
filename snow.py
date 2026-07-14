import requests
import pandas as pd
from datetime import datetime

def check_snow(date):
    '''Checks whether the Spirit Lake SNOTEL station had any snow on the selected date. Returns True if there is NO snow, False if there IS snow. Date must be input as a datetime.'''
    url = 'https://wcc.sc.egov.usda.gov/awdbRestApi/services/v1/data'
    station_ID = '777:WA:SNTL'
    params = {
        "stationTriplets": station_ID,
        "elements": "SNWD",
        "duration": "DAILY",
        "beginDate": date,
        "endDate": date,
        "periodRef": "END",
        "returnFlags": "false",
        "returnOriginalValues": "false",
        "returnSuspectData": "false"
        }
    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise Exception(f"API error: {response.status_code}")

    data = response.json()
    snow_depth = data[0]["data"][0]["values"][0]["value"]

    if snow_depth == 0:
        return True
    else:
        return False