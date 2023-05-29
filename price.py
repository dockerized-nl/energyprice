import requests
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta
import numpy as np
import pytz


current_date = datetime.now(pytz.timezone('GMT'))
yesterday = current_date + timedelta(days=-1)


URL = f"https://api.energyzero.nl/v1/energyprices?fromDate={yesterday.strftime('%Y-%m-%d')}T22:00:00.000Z&tillDate={current_date.strftime('%Y-%m-%d')}T22:00:00.000Z&interval=4&usageType=1&inclBtw=true"
page = requests.get(URL)

output_page = page.json()

average = output_page['average']

output = ""


labels = []
values = []

for item in output_page['Prices']:
    hour = int(item['readingDate'].split('T')[-1].replace('Z', '')[:2])
    hour += 2
    if hour == 24:
        hour = 00
    elif hour == 25:
        hour = 1
    labels.append(hour)
    values.append(item['price'])
plt.bar(labels, values)
plt.xlabel('Tijd')
plt.xticks(np.arange(0, 24, 1))
plt.ylabel('Prijs')
plt.title('Prijs per uur')
plt.axhline(y=float(average), color='orange',
            linestyle='--', linewidth=3, label='Avg')
plt.savefig(
    f'/volume1/Shared/Energie/images/price_plot_{current_date.strftime("%Y-%m-%d")}.png')
