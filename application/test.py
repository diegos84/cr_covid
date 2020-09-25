# Testing app only, not connected to the rest of the project
import requests
from bs4 import BeautifulSoup
import csv

# Using .text at the end or else .get will return only the response code from the server
source = requests.get('https://ticotimes.net/post-covid-19-updates').text
# Using lxml parser for beautiful soup
soup = BeautifulSoup(source, 'lxml')
# Create a list to append all the scrapped data and return it
news = []
# Iterate through segment and find all the tags with relevant data
# Must use an underscore after the word 'class' to differentiate from the keyword for classes in Python
for segment in soup.find_all('div', class_='poster size-normal size-350'):
    # Must use [] to get the value from an attribute in a tag
    link = segment.find('a', class_='poster-image mt-radius')['href']
    photo = segment.find('img')['src']
    headline = segment.find('h2').text
    timestamp = segment.find('span', class_='color-silver-light mt-pl-d').text
    
    # Using .strip() to remove leading and trailing whitespaces
    content = [headline.strip(), link, timestamp.strip(), photo]
    news.append(content)
print(news)
