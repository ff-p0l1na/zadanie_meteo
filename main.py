import datetime
import requests
import csv
import re
# data YYYY-mm-dd w postaci regular expression
date_pattern = re.compile(r'^\d{4}-(?:0[1-9]|1[0-2])-([012]\d|3[01])$')
#
latitude = None
longitude = None
searched_date = None
today = datetime.date.today()
# walidacja daty, krok 1: sprawdzenie prawidlowosci formatu
date_valid = date_pattern.match(str(today))
# TODO krok 2 walidacji daty
#
while True:
    latitude = input("Wpisz wybraną szerokość geograficzną (xx.yy): \n")
    longitude = input("Wpisz wybraną długość geograficzną (xx.yy): \n")
    searched_date = input("Wpisz wybraną datę (YYYY-mm-dd): \n")
    if not searched_date:
        tomorrow = today + datetime.timedelta(days=1)
        searched_date = tomorrow
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&" \
          f"longitude={longitude}&hourly=rain&daily=rain_sum&timezone=" \
          f"Europe%2FLondon&start_date={searched_date}" \
          f"&end_date={searched_date}"
    response = requests.get(url)
    if not response.ok:
        print(f"Błąd. Kod błędu: [{response.status_code}]")
        quit()
    else:
        data = response.json()
        rain_sum = data['daily']['rain_sum'][0]  # bierzemy idx 0 listy rain_sum





