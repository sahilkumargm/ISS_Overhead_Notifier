import requests
from datetime import datetime as dt
from smtplib import SMTP
import time

MY_LAT = 13.348430
MY_LNG = 74.779390

######  FOR SMTP USE ######
# smtp.mail.yahoo.com
FROM_ADDRESS = "sahilkumargm@yahoo.com"
PASSWORD = "hssjazdfekgjfikn"
TO_ADDRESS = "sahilkumargm@gmail.com"
MESSAGE = "Subject:ISS Alert!\n\nISS in your proximity right now. Look up now!"

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()




def iss_is_overhead():
    """
    Function to check if the ISS is within +5 or -5 degrees of the current location.
    Function returns True if conditions are met.
    """

    parameters = {
        "lat": MY_LAT,
        "lng": MY_LNG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    # Your position is within +5 or -5 degrees of the ISS position.
    if iss_latitude + 5 <= MY_LAT <= iss_longitude - 5 and iss_longitude + 5 <= MY_LNG <= iss_longitude - 5:
        return True


def is_dark():
    """
    Function to check if it is currently dark outside.
    :return: True if dark outside
    """

    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = dt.now()
    hour_now = time_now.hour

    if hour_now >= sunset or hour_now <= sunrise:
        return True


# Checking if the iss is visible every 60 seconds:
while True:
    time.sleep(60)
    if iss_is_overhead() and is_dark():
        with SMTP("smtp.mail.yahoo.com") as smtp:
            smtp.starttls()
            smtp.login(user=FROM_ADDRESS, password=PASSWORD)
            smtp.sendmail(from_addr=FROM_ADDRESS, to_addrs=TO_ADDRESS, msg=MESSAGE)

# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.
