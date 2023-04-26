from twilio.rest import Client
import requests
import psycopg2
import rich
import json
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta

current_date = datetime.now()
#day_before_yesterday_date = current_date - timedelta(days=2)
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
    
plt.bar(labels, values)

plt.xlabel('Tijd')
plt.ylabel('Prijs')

plt.title('Prijs per uur')
plt.savefig(f'./images/price_plot_{yesterday_date.strftime("%Y-%m-%d")}.png')

#plt.show()




# sla resultaat als dict in db.
# docker run -d --name postgres -e POSTGRES_PASSWORD=Password01 -e PGDATA=/var/lib/postgresql/data/pgdata -v /volume1/docker/postgres:/var/lib/postgresql/data -p 8081:5432 postgres
# con = psycopg2.connect(
#     database="postgres",
#     user="postgres",
#     password="Password01",
#     host="192.168.2.224",
#     port='8081'
# )
# CREATE TABLE energyprices(Price VARCHAR (10) UNIQUE NOT NULL, intervalType VARCHAR (10) UNIQUE NOT NULL, average VARCHAR (10) UNIQUE NOT NULL, fromDate VARCHAR (50) UNIQUE NOT NULL, tillDate VARCHAR (50) UNIQUE NOT NULL);
# curs_obj = con.cursor()
# curs_obj.execute("INSERT INTO energyprices (Price, intervalType, average, fromDate, tillDate) VALUES('1.15', '4', '1.5', '23-04-2023', '24-04-2023');")
# print("Data inserted successfully")
# con.commit()
# curs_obj.close()
# con.close()

# curs_obj.execute("SELECT * FROM energyprices")
# result = curs_obj.fetchall()
# print("Table's Data:", "\n", result)


##################################################
####### genreer SMS / MMS van deze laagste uren.
# '31639136509', '31624319319'                   #
##################################################
account_sid = 'AC45de5d39112710853e007fe7ed6ccd0e'
auth_token = '34ca9f7dedaeeb0e4579f36846cb227f'
client = Client(account_sid, auth_token)

phonenumbers = ['31614956656', '31614683243']

for number in phonenumbers:    
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=output, 
        media_url='https://raw.githubusercontent.com/dockerized-nl/energyprice/main/images/price_plot_2023-04-24.png',
        to=f"whatsapp:+{number}"
    )

print(message.sid)
