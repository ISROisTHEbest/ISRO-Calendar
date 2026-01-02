import requests
from ics import Calendar, Event
from ics.grammar.parse import ContentLine
import os

calendar_path = 'docs/isro_launches.ics'
base_url = 'https://ll.thespacedevs.com/2.3.0/'

if os.path.exists(calendar_path):
    with open(calendar_path, 'r', encoding='utf-8', errors='replace') as file:
        calendar = Calendar(file.read())
else:
    calendar = Calendar()
    calendar.scale = 'Gregorian'
    calendar.extra.append(ContentLine(name="X-WR-CALNAME", value="ISRO Launches"))
    calendar.extra.append(ContentLine(name="X-PUBLISHED-TTL", value="PT1H"))
    calendar.extra.append(ContentLine(name="REFRESH-INTERVAL;VALUE=DURATION", value="PT1H"))

data = requests.get(base_url+'launches/upcoming', params={'format':'json', 'lsp__id':'31,1051'}).json()

for launch in data['results']:
    for event in calendar.events:
        if launch['id'] == event.uid:
            calendar.events.discard(event)
            break
    event = Event()
    event.uid = launch['id']
    event.name = launch['name']
    if launch['window_start'] != launch['window_end']:
        event.begin = str(launch['window_start']).replace('T', ' ').replace('Z', '')
        event.end = str(launch['window_end']).replace('T', ' ').replace('Z', '')
    else:
        event.begin = str(launch['window_start']).replace('T', ' ').replace('Z', '')
        event.make_all_day()
    try:
        desc = str(launch['mission']['description']).replace('\r', '')
        event.description = f"[{launch['launch_service_provider']['name']}]\n{launch['rocket']['configuration']['full_name']}\n\n{desc}"
    except:
        event.description = f"[{launch['launch_service_provider']['name']}]\n{launch['rocket']['configuration']['full_name']}"
    
    event.location = launch['pad']['name']

    calendar.events.add(event)

with open('docs/isro_launches.ics', 'w', encoding='utf-8') as file:
    file.writelines(calendar.serialize_iter())

