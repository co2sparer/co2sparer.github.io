import sys
import json
import pytz
import argparse
from datetime import datetime, date, timedelta
from dateutil import tz
import time

import requests
import matplotlib.pyplot as plt
import seaborn as sns

def plot_and_save_bar_plot(label_list, data_list, date_as_string):
    p = sns.barplot(x=label_list, y=data_list, color="cornflowerblue")
    # sns.despine(trim=True, offset=2)

    p.set_xticklabels(label_list, rotation=90, ha="center")
    p.set_title("Strompreis Überblick:" + date_as_string, fontsize=20)
    p.set_xlabel("Stunde", fontsize=20)
    p.set_ylabel("Preis", fontsize=20)
    sns.set(rc={'figure.figsize': (20, 10)})
    plt.tight_layout()
    plt.savefig("../imgs/strompreis_uebersicht.png")

def request_data(base_request_url):
    ## TODO(nik): Add correct utc to berlin local time conversion here!
    ## looks like pandas could be convenient?
    ## https://stackoverflow.com/questions/37614303/in-pandas-how-to-get-a-utc-timestamp-at-a-given-hour-from-a-datetime
    ## https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html
    tomorrows_date = date.today() + timedelta(days=1)
    unix_time = time.mktime(tomorrows_date.timetuple()) * 1000
    request_url = base_request_url + "?start=" + str(unix_time)
    r = requests.get(request_url)
    json_test = r.json()
    with open('market_data_next_24h.json', 'w') as f:
        json.dump(json_test, f, indent=2)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Performs Request, and creates github page update.')
    parser.add_argument('base_request_url', type=str,
                        help='base request url')
    args = parser.parse_args()
    request_data(args.base_request_url)

    data = json.load(open("market_data_next_24h.json"))
    print("ok, loaded")
    now = datetime.now()
    dt_string = now.strftime("%d.%m.%Y %H:%M")
    date_tomorrow = (date.today() + timedelta(days=1)).strftime("%d.%m.%Y")
    site_contents = """
## Strompreise für den """ + date_tomorrow + """

Niedrige Preise deuten auf viel Sonnen und Windenergieerzeugung hin, ein hoher Anteil an erneuerbaren Energien bedeuted weniger CO2 Verbrauch!

![Strompreis übersicht](imgs/strompreis_uebersicht.png)

| Stunde | Preis in Cent/kWh |
|---|---|
"""
    min_val = sys.maxsize
    min_ind = -1
    for i, datum in enumerate(data['data']):
        current_val = float(datum['marketprice'])
        if current_val < min_val:
            min_ind = i
            min_val = current_val

    data_list = []
    label_list = []
    for i, datum in enumerate(data['data']):
        timestamp_start_cet_sec = datetime.utcfromtimestamp(datum['start_timestamp'] / 1000).replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Europe/Berlin'))
        timestamp_stop_cet_sec = datetime.utcfromtimestamp(datum['end_timestamp'] / 1000).replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Europe/Berlin'))

        hours = timestamp_start_cet_sec.strftime('%d.%m. %Hh') + " - " + timestamp_stop_cet_sec.strftime(' %Hh')
        price = float(datum['marketprice'])
        price = price / 10 # conversion from Euro/MWh to Cent/kWh
        label_list.append(hours)
        data_list.append(price)
        if i == min_ind:
            site_contents += "| **" + hours + "** | **" + str(price) + "** | \n"
        else:
            site_contents += "| " + hours + " | " + str(price) + " | \n"

    plot_and_save_bar_plot(label_list, data_list, date_tomorrow)
    site_contents += """
Preise der EPEX Spot ® Strombörse (neue Preise werden täglich um 14:00 veröffentlicht für den kompletten nächsten Tag).

letzte Aktualisierung:""" + dt_string
    with open("README.md", "w") as f:
        f.write(site_contents)
    print("all done writing")
