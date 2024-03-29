# main.py

from datetime import datetime
import requests
from bs4 import BeautifulSoup
import arrow

from ics import Calendar, Event
from fastapi import FastAPI, Response, responses
from fastapi_utils.tasks import repeat_every

from caching import Caching

app = FastAPI()


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
                mtch['result'] = link.text
                mtch['match_id'] = href.split("/")[-1]
            elif 'www.google.com/calendar/event' in href:
                mtch['google_calendar'] = href
            else:
                print(' nem feldolgozott sor: ', link)
    return competition


def generate_calendar(competition_id: str, teamname: str):
    base_url = "https://mvlsz.webpont.com"
    competition_url = 'http://mvlsz.webpont.com/bajnoksagok/?szures[bajnoksag_id]=' + competition_id
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
        is_game_finished = match['result'] != '0-0'
        result = (': ' + match['result']) if is_game_finished else ''
        event.name = f'{match["teams"][0]} - {match["teams"][1]}{result}'
        if not is_game_finished:
            live_link = f'\n<a href="http://waterpololive.webpont.com/?{match["match_id"]}">Élő közvetítés</a>' if "match_id" in match else ""
        else:
            live_link = ""
        event.description = f'<a href="{base_url}{match["match_url"]}">Adatlap</a>\n<a href="{competition_url}">Bajnokság</a>{live_link}'
        event.begin = arrow.get(match['date_str'], "YYYY. MMM. D. H:mm", locale="hu", tzinfo="CET")
        event.duration = {'hours': 1}
        event.last_modified = datetime.now()
        event.location = match['location']
        calendar.events.add(event)
    return calendar.serialize()


cache = Caching(24*60*60, generate_calendar)


@repeat_every(seconds=4*60*60)
async def update_cache() -> None:
    cache.update_all_values()


@app.get("/waterpolo/{competition_id}/{teamname}")
async def read_item(competition_id: str, teamname: str):
    return Response(content=cache.get((competition_id, teamname)), media_type="text/calendar")


@app.get("/cached_calendars")
async def cached_calendars() -> responses.JSONResponse:
    retval = list()
    for key, cal in cache.get_cache().items():
        retval.append({'tournament': key[0], 'team': key[1], 'size': len(cal)})
    return responses.JSONResponse(retval)


@app.get("/")
async def index_page() -> responses.HTMLResponse:
    cache_size = len(cache.get_cache())
    return responses.HTMLResponse(f"""
    <htnk>
        <body>
            <p>
                <a href="cached_calendars">Cached calendars</a>
            </p>
            <p>cache size: {cache_size}</p>
            <div>
                <h2>Example calendars</h2>
                <ul>
                    <li><a href="waterpolo/758/KSI">KSI Országos serdülő bajnokság</a></li>
                    <li><a href="waterpolo/768/KSI">KSI Budapest serdülő bajnokság</a></li>
                <ul>
                <p>You can add these url-s to your calendar feeds. Further help to add to your calendar <a href="https://support.google.com/calendar/answer/37100">Add URL to your Google Calendar</a></p>
            </div>
        </body>
    <htnk>
    """)


# @app.get("/index.html")
# async def read_html():
#    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
#    with open(file_path, encoding='utf-8') as f:
#        return f.read()
