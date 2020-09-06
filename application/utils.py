import requests
import csv
from flask import  url_for
from flask_mail import Message
from application import mail
from bs4 import BeautifulSoup


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', 
                sender='noreply-crcovidtracker@outlook.com', 
                recipients=[user.email])
    # Embedded text must not be indented, or else the indentation will show on the email sent to the user
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
            "cases": payload["cases"],
            "active": payload["active"],
            "critical": payload["critical"],
            "deaths": payload["deaths"],
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


def get_the_news():
    # Using .text at the end or else .get will return only the response code from the server
    source = requests.get('https://ticotimes.net/post-covid-19-updates').text
    # Using lxml parser for beautiful soup
    soup = BeautifulSoup(source, 'lxml')
    # Create a list to append all the scrapped data and return it
    news = []
    # Iterate through segment and find all the tags with relevant data
    # Must use an underscore after the word 'class' to differenciate from the keyword for classes in Python
    for segment in soup.find_all('div', class_='poster size-normal size-350'):
        # Must use [] to get the value from an attribute in a tag
        link = segment.find('a', class_='poster-image mt-radius')['href']
        photo = segment.find('img')['src']
        headline = segment.find('h2').text
        timestamp = segment.find('span', class_='color-silver-light mt-pl-d').text
        # Using .strip() to remove leading and trailing whitespaces
        content = [headline.strip(), link, photo, timestamp.strip()]
        news.append(content)

    return(news)


