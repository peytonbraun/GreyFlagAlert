from datetime import datetime, timezone, timedelta
from resuspension_alert.hrrr import check_wind
from resuspension_alert.snow import check_snow
from resuspension_alert.soil_moisture import check_soil_moisture
from resuspension_alert.email import send_email
from resuspension_alert.github_state import (alert_exists, create_alert_issue, close_alert_issue)

def send_alert():
    run_date = datetime.now(timezone.utc)
    
    model_date = (run_date.replace(minute=0, second=0, microsecond=0)- timedelta(hours=2)).replace(tzinfo=None)
    
    wind_ok = check_wind(model_date)
    try:
        snow_ok = check_snow()
    except Exception as e:
        print(f'Snow check failed: {e}')
        snow_ok = False
    soil_moisture_ok = check_soil_moisture(model_date)

    alert = wind_ok[0] and snow_ok and soil_moisture_ok[0]

    if alert:
        if not alert_exists():
            send_email(run_date)
            create_alert_issue(f"""Grey Flag Alert""")
            print(f'\U00002705 Conditions met. Alert sent!')
    else:
        close_alert_issue()
        print(f'\u274C Conditions not met.')
        print(f'Winds: {wind_ok[0]}')
        print(f'Snow: {snow_ok()}')
        print(f'Soil moisture: {soil_moisture_ok[0]}')

if __name__ == "__main__":
    send_alert()
