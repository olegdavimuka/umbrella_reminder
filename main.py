import requests
import os
from twilio.rest import Client

MY_LAT = 48.598538
MY_LON = 22.274249
OWM_ENDPOINT = "https://api.openweathermap.org/data/2.5/onecall"
OWM_API_KEY = os.environ.get("OWM_API_KEY")
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_SENDER_PHONE = "+18456713421"
TWILIO_RECIPIENT_PHONE = "+380505193622"
TWILIO_MESSAGE = "It's going to rain today. Remember to bring an ☔️"

weather_params = {
    "lat": MY_LAT,
    "lon": MY_LON,
    "appid": OWM_API_KEY,
    "exclude": "current,minutely,daily"
}

response = requests.get(OWM_ENDPOINT, params=weather_params)
response.raise_for_status()
weather_data = response.json()

will_rain = False

for hour_data in weather_data["hourly"][:12]:
    if int(hour_data["weather"][0]["id"]) < 700:
        will_rain = True

if will_rain:

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f"{TWILIO_MESSAGE}",
        from_=f"{TWILIO_SENDER_PHONE}",
        to=f"{TWILIO_RECIPIENT_PHONE}"
    )
    print(message.status)
