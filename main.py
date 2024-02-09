import requests
from datetime import datetime
from smtplib import SMTP

MY_LAT = 51.507351  # Your latitude
MY_LONG = -0.127758  # Your longitude
MARGIN = 5
MY_EMAIL = "ixdul3004@gmail.com"
MY_PASSWORD = "rbpc prwc wmvj yryw"
OTHER_EMAIL = "ixdul3004@gmail.com"

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

# Your position is within +5 or -5 degrees of the ISS position.


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.now()
time_hour = time_now.hour

# If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.

if sunset <= time_hour < sunrise:
    if MY_LAT - MARGIN <= iss_latitude <= MY_LAT + MARGIN:
        with SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL, to_addrs=OTHER_EMAIL,
                                msg=f"Subject: Hey look up at the sky\n\nLook up")
            print("Email sent")
