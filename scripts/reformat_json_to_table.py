import sys
import json
from datetime import datetime

if __name__ == '__main__':
    data = json.load(open("market_data_next_24h.json"))
    print("ok, loaded")
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
    site_contents = """
## Preise für die nächsten 24h der Leipziger Strom Börse (neue preise werden täglich um 14:00 veröffentlicht für den nächsten Tag)
letzte aktualisierung:""" + dt_string + """

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

    for i, datum in enumerate(data['data']):
        if i == min_ind:
            site_contents += "| **" + str(i) + "** | **" + str(datum['marketprice']) + "** | \n"
        else:
            site_contents += "| " + str(i) + " | " + str(datum['marketprice']) + " | \n"

    with open("README.md", "w") as f:
        f.write(site_contents)
    print("all done writing")