import requests
from icalendar import Calendar, Event
from datetime import datetime
import os

calendar_path = 'docs/isro_launches.ics'
base_url = 'https://ll.thespacedevs.com/2.3.0/'

if os.path.exists(calendar_path):
    with open(calendar_path, 'rb') as file:
        calendar = Calendar.from_ical(file.read())
else:
    calendar = Calendar()
    calendar.calendar_name = 'ISRO Launches'
    calendar.add('scale', 'Gregorian')
    calendar.add('x-published-ttl', 'PT1H')
    calendar.add('refresh-interval', value='PT1H', parameters={'value': 'DURATION'})

data = requests.get(base_url+'launches/upcoming', params={'format':'json', 'lsp__id':'31,1051'}).json()

for launch in data['results']:
    i = 0
    for subcomponent in calendar.subcomponents:
        if subcomponent.name == 'VEVENT':
            if launch['id'] == str(subcomponent.get('uid')):
                calendar.subcomponents.remove(subcomponent)
                break
        i += 1
    else:
        i = None
    event = Event()
    event.add('uid', launch['id'])
    event.add('summary', launch['name'])
    window_start = datetime.strptime(launch['window_start'], '%Y-%m-%dT%H:%M:%S%z')
    if launch['window_start'] != launch['window_end']:
        event.add('dtstart', window_start)
        event.add('dtend', datetime.strptime(launch['window_end'], '%Y-%m-%dT%H:%M:%S%z'))
    else:
        event.add('dtstart', window_start.date())
    try:
        desc = str(launch['mission']['description']).replace('\r', '')
        event.add('description', f"[{launch['launch_service_provider']['name']}]\n{launch['rocket']['configuration']['full_name']}\n\n{desc}")
    except:
        event.add('description', f"[{launch['launch_service_provider']['name']}]\n{launch['rocket']['configuration']['full_name']}")
    
    event.add('location', launch['pad']['name'])
    if i == None:
        calendar.subcomponents.append(event)
    else:
        calendar.subcomponents.insert(i, event)

with open('docs/isro_launches.ics', 'wb') as file:
    file.write(calendar.to_ical())

