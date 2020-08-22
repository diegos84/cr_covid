import requests
from flask import  url_for
from flask_mail import Message
from application import mail

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', 
                sender='noreply-crcovidtracker@outlook.com', 
                recipients=[user.email])
    msg.body = f'''Please visit the following link to resert your password:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request, please just ignore this email to prevent any account chages to take place.
'''
    mail.send(msg)


def api_call(country):
    # Contact COVID API
    try:
        r = requests.get(f"https://corona.lmao.ninja/v2/countries/{country}")
        r.raise_for_status()
    except requests.RequestException:
        return None  
    # Parse response
    try:
        payload = r.json()
        return {
            "country": payload["country"],
            "flag": payload["countryInfo"]["flag"],
            "cases": payload["cases"],
            "active": payload["active"],
            "critical": payload["critical"],
            "deaths": payload["deaths"],
            "tests": payload["tests"],
            "cases_per_million": payload["casesPerOneMillion"],
            "deaths_per_million": payload["deathsPerOneMillion"],
            "tests_per_million": payload["testsPerOneMillion"]
        }
    except (KeyError, TypeError, ValueError):
        return None

def all_countries():
    r = requests.get("https://corona.lmao.ninja/v2/countries/")
    r.raise_for_status()
    payload = r.json()
    countries = []
    for c in payload:
        countries.append((c['countryInfo']['iso3'], c['country']))
    return countries