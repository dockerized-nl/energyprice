from twilio.rest import Client
import requests
import psycopg2
import rich
import json
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta
import os

current_date = datetime.now()
yesterday_date = current_date - timedelta(days=1)


URL = f"https://api.energyzero.nl/v1/energyprices?fromDate={yesterday_date.strftime('%Y-%m-%d')}T00:00:00.000Z&tillDate={current_date.strftime('%Y-%m-%d')}T00:00:00.000Z&interval=4&usageType=1&inclBtw=true"
page = requests.get(URL)

output_page = page.json()

output = ""

for item in output_page['Prices']:
    output += f"Tijd: {item['readingDate'].split('T')[-1].replace('Z','')[:2]} Prijs: {item['price']}"
    output += "\n"

print(output)
labels = []
values = []

for item in output_page['Prices']:
    labels.append(item['readingDate'].split('T')[-1].replace('Z', '')[:2])
    values.append(item['price'])

##################################################
# Generate Whatsapp message.
##################################################
account_sid = os.environ['ACCOUNT_SID']
auth_token = os.environ['TWILIO_API_TOKEN']
client = Client(account_sid, auth_token)

twilio_number = os.environ.get('FROM_NUMBER')
print(twilio_number )
exit()

if ',' in os.environ['TEL_NUMBER']:
    phonenumbers = os.environ['TEL_NUMBER'].split(',')
else:
    phonenumbers = [os.environ['TEL_NUMBER']]

print(phonenumbers)

for number in phonenumbers:
    message = client.messages.create(
        from_= f"whatsapp:+{twilio_number}",
        body=output,
        media_url='https://raw.githubusercontent.com/dockerized-nl/energyprice/main/images/price_plot_2023-04-28.png',
        to=f"whatsapp:+{number}"
    )

print(message.sid)
