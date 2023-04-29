from twilio.rest import Client
import requests
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta
import os

current_date = datetime.now()
tomorrow = current_date + timedelta(days=1)


URL = f"https://api.energyzero.nl/v1/energyprices?fromDate={current_date.strftime('%Y-%m-%d')}T21:00:00.000Z&tillDate={tomorrow.strftime('%Y-%m-%d')}T20:00:00.000Z&interval=4&usageType=1&inclBtw=true"
page = requests.get(URL)

output_page = page.json()

output = ""

for item in output_page['Prices']:
    output += f"Tijd: {item['readingDate'].split('T')[-1].replace('Z','')[:2]} Prijs: {item['price']}"
    output += "\n"

labels = []
values = []

for item in output_page['Prices']:
    labels.append(item['readingDate'].split('T')[-1].replace('Z', '')[:2])
    values.append(item['price'])

##################################################
# Generate Whatsapp
##################################################
account_sid = os.environ['ACCOUNT_SID']
auth_token = os.environ['TWILIO_API_TOKEN']
client = Client(account_sid, auth_token)

twilio_number = os.environ['FROM_NUMBER']

if ',' in os.environ['TEL_NUMBER']:
    phonenumbers = os.environ['TEL_NUMBER'].split(',')
else:
    phonenumbers = [os.environ['TEL_NUMBER']]

print(phonenumbers)

for number in phonenumbers:
    message = client.messages.create(
        from_ = f"whatsapp:+{twilio_number}",
        body=output,
        media_url=f"https://raw.githubusercontent.com/dockerized-nl/energyprice/main/images/price_plot_{current_date.strftime('%Y-%m-%d')}.png",
        to=f"whatsapp:+{number}"
    )

print(message.sid)
