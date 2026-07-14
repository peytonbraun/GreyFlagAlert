from datetime import datetime, timezone, timedelta
from resuspension_alert.gfs import check_wind
from resuspension_alert.snow import check_snow
from resuspension_alert.soil_moisture import check_soil_moisture
from resuspension_alert.email import send_email

def send_alert():
    run_date = datetime.now(timezone.utc)
    
    model_date = (run_date.replace(minute=0, second=0, microsecond=0)- timedelta(hours=1))
    
    wind_ok = check_wind(model_date)
    snow_ok = check_snow(run_date)
    soil_moisture_ok = check_soil_moisture(model_date)
    
    if wind_ok[0] and snow_ok and soil_moisture_ok[0]:
        send_email(date)

if __name__ == '__send_alert__':
    send_alert()