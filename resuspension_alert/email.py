from resuspension_alert.hrrr import check_wind
from resuspension_alert.snow import check_snow
from resuspension_alert.soil_moisture import check_soil_moisture
import smtplib
from email.message import EmailMessage
from datetime import datetime
import os

def send_email(date):
    date = date.replace(tzinfo=None)
    wind_ok = check_wind(date)
    snow_ok = check_snow(date)
    soil_moisture_ok = check_soil_moisture(date)
    
    sender = os.environ['email_address']
    recipient = os.environ['test_recipient_email']
    app_password = os.environ['email_password']

    msg = EmailMessage()
    msg["Subject"] = "Gray Flag Alert - GFS"
    msg["From"] = sender
    msg["To"] = recipient
    
    msg.set_content(f"""
    Conditions for resuspension met on {date} Z.
    
    Wind speed = {wind_ok[1]} knots
    Wind direction = {wind_ok[2]} degrees
    Snow depth =  0 in
    Soil moisture = {soil_moisture_ok[1]}%
    
    MSH webcam: https://volcview.wr.usgs.gov/ashcam-gui/webcam.html?webcam=msh-edifice
    """)
    
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender, app_password)
        smtp.send_message(msg)
