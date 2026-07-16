from resuspension_alert.hrrr import check_wind
from resuspension_alert.snow import check_snow
from resuspension_alert.soil_moisture import check_soil_moisture
import smtplib
from email.message import EmailMessage
from datetime import datetime, timezone, timedelta
import os

def send_email(date):
    run_date = date.replace(tzinfo=None)
    model_date = (run_date.replace(minute=0, second=0, microsecond=0)- timedelta(hours=2)).replace(tzinfo=None)
    wind_ok = check_wind(model_date)
    snow_ok = check_snow()
    soil_moisture_ok = check_soil_moisture(model_date)
    
    sender = os.environ['EMAIL_ADDRESS']
    recipient = os.environ['RECIPIENT_EMAIL']
    app_password = os.environ['EMAIL_PASSWORD']

    msg = EmailMessage()
    msg["Subject"] = "Gray Flag Alert - HRRR"
    msg["From"] = sender
    msg["To"] = recipient
    
    msg.set_content(f"""
    Conditions for resuspension met on {run_date.strftime('%Y-%m-%d %H')} Z.
    
    Wind speed = {wind_ok[1]} knots
    Wind direction = {wind_ok[2]} degrees
    Snow depth =  0 in
    Soil moisture = {soil_moisture_ok[1]}%
    
    MSH webcam: https://volcview.wr.usgs.gov/ashcam-gui/webcam.html?webcam=msh-edifice
    """)
    
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender, app_password)
        smtp.send_message(msg)
