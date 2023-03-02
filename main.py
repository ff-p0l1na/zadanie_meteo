import csv
import datetime
import os
import pandas
import re
import requests
# data YYYY-mm-dd w postaci regular expression
date_pattern = re.compile(r'^\d{4}-(?:0[1-9]|1[0-2])-([012]\d|3[01])$')
#
if not os.path.isfile('fallback.csv'):
    with open('fallback.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(["latitude", "longitude", "searched_date", "rain_sum"])
#
today = datetime.date.today()
#
while True:
    witam_zegnam = input("Kontynuuj (enter) żeby sprawdzić czy w danym miejscu będzie padać,"
                         "lub napisz \"adios\" żeby wyjść.\n")
    if witam_zegnam == "adios":
        break
    if not witam_zegnam:
        latitude = input("Wpisz wybraną szerokość geograficzną (np. 60.39): \n")
        longitude = input("Wpisz wybraną długość geograficzną (np. 5.32): \n")
        searched_date = input("Wpisz wybraną datę w formacie YYYY-mm-dd: \n")
        if not searched_date:
            tomorrow = today + datetime.timedelta(days=1)
            searched_date = tomorrow
        date_valid = date_pattern.match(str(searched_date))
        if date_valid:
            pass
        else:
            print("Nieprawidłowa data, spróbuj ponownie.\n")
            continue
        # najpierw sprawdzamy czy wprowadzone dane istnieją w pliku:
        gathered_data = pandas.read_csv("fallback.csv")
        checker = (gathered_data['latitude'] == float(latitude)) & \
                  (gathered_data['longitude'] == float(longitude)) & \
                  (gathered_data['searched_date'] == str(searched_date))
        matching_data = gathered_data.loc[checker]
        if not matching_data.empty:
            rain_sum = float(matching_data.iloc[0]['rain_sum'])
            if rain_sum == 0:
                print("Nie będzie padać.")
            elif rain_sum > 0:
                print("Będzie padać.")
            else:
                print("Nie wiem.")
        else:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&" \
                  f"longitude={longitude}&hourly=rain&daily=rain_sum&timezone=" \
                  f"Europe%2FLondon&start_date={searched_date}" \
                  f"&end_date={searched_date}"
            response = requests.get(url)
            if not response.ok:
                print(f"Błąd. Kod błędu: [{response.status_code}]")
                quit()
            elif response:
                print("Wysyłanie zapytania do API...")
                data = response.json()
                rain_sum = data['daily']['rain_sum'][0]  # bierzemy idx 0 listy rain_sum
                with open('fallback.csv', 'a') as file:
                    writer = csv.writer(file)
                    writer.writerow([latitude, longitude, searched_date, rain_sum])
                    if float(rain_sum) == 0:
                        print("Nie będzie padać.")
                    elif float(rain_sum) > 0:
                        print("Będzie padać.")
                    else:
                        print("Nie wiem.")
