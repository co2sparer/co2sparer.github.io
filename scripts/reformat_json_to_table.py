import sys
import json
import pytz
from datetime import datetime, timedelta
from dateutil import tz

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

if __name__ == '__main__':
    data = json.load(open("market_data_next_24h.json"))
    print("ok, loaded")
    now = datetime.now()
    dt_string = now.strftime("%d.%m.%Y %H:%M")
    dt_with_hour_string = now.strftime("%d.%m.%Y %Hh")
    # tomorrows_date = (now + timedelta(days=1)).strftime("%d.%m.%Y")
    site_contents = """
## Strompreise für die nächsten 24h, stand: """ + dt_string + """

Niedrige Preise deuten auf viel Sonnen und Windenergieerzeugung hin, ein hoher Anteil an erneuerbaren Energien bedeuted weniger CO2 Verbrauch!

![Strompreis übersicht](imgs/strompreis_uebersicht.png)

| Stunde | Preis in Eur/MWh |
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
        label_list.append(hours)
        data_list.append(price)
        if i == min_ind:
            site_contents += "| **" + hours + "** | **" + str(price) + "** | \n"
        else:
            site_contents += "| " + hours + " | " + str(price) + " | \n"

    plot_and_save_bar_plot(label_list, data_list, dt_with_hour_string)
    site_contents += """
Preise der EPEX Spot ® Strombörse (neue Preise werden täglich um 14:00 veröffentlicht für den kompletten nächsten Tag).

letzte Aktualisierung:""" + dt_string
    with open("README.md", "w") as f:
        f.write(site_contents)
    print("all done writing")
