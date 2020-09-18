import requests
from requests import get
from bs4 import BeautifulSoup
from time import sleep
from random import randint

track = ''
date = ''
names = []
race_num = []
position = []
diff = []
best_time = []
best_lap = []
total_laps = []
top_speed = []

headers = {"Accept-Language": "en-US, en;q=0.5"}

url = 'https://speedhive.mylaps.com/Sessions/5883889'
response = requests.get(url)

data = BeautifulSoup(response.text, 'html.parser')
divs = data.findAll('div', class_='data-loading session-detail-results')
# print(divs)

for div in divs:
    track = div.findAll('span', class_='info-location toggle-on-small hide-it')
    date = div.findAll('span', class_='info-date')
    name = div.findAll('span', class_='competitorName')
    names.append(name)

    num = div.findAll('div', class_='row-event-racenumber')
    race_num.append(num)

    pos = div.findAll('div', class_='row-event-position')
    position.append(pos)

    d = div.findAll('div', class_='row-event-diff')
    diff.append(d)

    time = div.findAll('div', class_='row-event-besttime')
    best_time.append(time)

    lap = div.findAll('div', class_='row-event-bestlap')
    best_lap.append(lap)

    speed = div.findAll('div', class_='row-event-topspeed')
    top_speed.append(speed)

    laps = div.findAll('div', class_='row-event-laps')
    total_laps.append(laps)

