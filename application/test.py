import requests

def all_countries():
    r = requests.get("https://corona.lmao.ninja/v2/countries/")
    r.raise_for_status()
    payload = r.json()
    countries = []
    for c in payload:
        countries.append((c['countryInfo']['iso3'], c['country']))
    return countries

c = all_countries()

for key,value in c:
    print(key)





