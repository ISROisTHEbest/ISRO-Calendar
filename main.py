import requests
from ics import Calendar, Event
from ics.grammar.parse import ContentLine

calendar = Calendar()
calendar.scale = 'Gregorian'
calendar.extra.append(ContentLine(name="X-WR-CALNAME", value="ISRO Launches"))
calendar.extra.append(ContentLine(name="X-PUBLISHED-TTL", value="PT1H"))
calendar.extra.append(ContentLine(name="REFRESH-INTERVAL;VALUE=DURATION", value="PT1H"))


base_url = 'https://ll.thespacedevs.com/2.3.0/'

data = requests.get(base_url+'launches/upcoming', params={'format':'json', 'mission__agency__ids':31}).json()

for launch in data['results']:
    event = Event()
    event.uid = launch['id']
    event.name = launch['name']
    if launch['window_start'] != launch['window_end']:
        event.begin = str(launch['window_start']).replace('T', ' ').replace('Z', '')
        event.end = str(launch['window_end']).replace('T', ' ').replace('Z', '')
    else:
        event.begin = str(launch['window_start']).replace('T', ' ').replace('Z', '')
        event.make_all_day()
    event.description = launch['rocket']['configuration']['full_name']
    event.location = launch['pad']['name']

    calendar.events.add(event)

with open('docs/isro_launches.ics', 'w') as file:
    file.writelines(calendar.serialize_iter())

