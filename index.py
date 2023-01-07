# main.py

import requests
from bs4 import BeautifulSoup
import arrow

from ics import Calendar, Event
from fastapi import FastAPI, Response

from caching import Caching

app = FastAPI()


# @app.get("/")
# async def read_root():
#    return {"Hello": "World"}


def sniff_date_from_webpage(competition_url: str) -> list:
    competition = list()

    page = requests.get(competition_url, timeout=10)
    #soup = BeautifulSoup(page.content, 'html-parser')
    soup = BeautifulSoup(page.content, 'html5lib')
    matches = soup.find_all("tr", class_='gamerow')

    for match in matches:
        mtch = {'teams': []}
        competition.append(mtch)
        mtch['rawdata'] = mtch
        #location = match.td
        for i, row in enumerate(match.find_all('td')):
            if row.text.startswith("202"):
                mtch['date_str'] = row.text.strip()
            elif i == 6 and row.text.strip() != '':
                mtch['location'] = row.text.strip()
        for link in match.find_all("a"):
            href = link['href']
            if '/csapat/' in href:
                mtch['teams'].append(link.text)
            elif '/MatchReturnData' in href:
                mtch['report_url'] = href
            elif '/meccs/' in href:
                mtch['match_url'] = href
                mtch['results'] = link.text
            elif 'www.google.com/calendar/event' in href:
                mtch['google_calendar'] = href
            else:
                print(' nem feldolgozott sor: ', link)
    return competition


def generate_calendar(competition_id: str, teamname: str):
    competition_url = 'https://waterpolo.hu/bajnoksagok/?szures[bajnoksag_id]=' + competition_id
    competition = sniff_date_from_webpage(competition_url)

    for match in competition:
        if len(match) < 5:
            del match

    def filter_competition_by_team(competition: list, team: str) -> list:
        filtered = list()
        for match in competition:
            if len(match) > 3:
                for t in match['teams']:
                    if team in t:
                        filtered.append(match)
                        break
        return filtered

    competition_filtered = filter_competition_by_team(competition, teamname)

    calendar = Calendar()

    for match in competition_filtered:
        event = Event()
        event.name = f'{match["teams"][0]} - {match["teams"][1]}: {match["results"]}'

        event.begin = arrow.get(match['date_str'], "YYYY. MMM. D. H:mm", locale="hu")
        event.duration = {'hours': 1}

        event.location = match['location']
        calendar.events.add(event)
    return calendar.serialize()


cache = Caching(4*60*60, generate_calendar)


@app.get("/waterpolo/{competition_id}/{teamname}")
async def read_item(competition_id: str, teamname: str):

    return Response(content=cache.get((competition_id, teamname)), media_type="text/calendar")
    # return Response(content=generate_calendar(competition_id, teamname), media_type="text/calendar")


# @app.get("/index.html")
# async def read_html():
#    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
#    with open(file_path, encoding='utf-8') as f:
#        return f.read()
