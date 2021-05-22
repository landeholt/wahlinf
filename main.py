from environment import Environment
from model import Apartment, Refs
import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
from pushbullet import Pushbullet
from deta import app


def get_n_apartments(soup: bs) -> int:
    try:
        result = soup.select_one(Refs.n_vacant_apartments).get_text()
        return int(result)
    except Exception as e:
        pprint(e)
        return 0


def extract_one(soup: bs, selector_string: str):
    return soup.select_one(selector_string).get_text().strip()


def get_apartments(soup: bs):
    try:
        apartments = soup.select_one(Refs.apartment)

        for apt in apartments.select("div.block-item.semi.carousel-cell div.block div.block-content"):
            title = extract_one(apt, "h3.block-title a")
            object_number = extract_one(apt, "div.post-info strong:nth-child(1) span.data")
            area = extract_one(apt, "div.post-info strong:nth-child(2) span.data")
            link = apt.select_one("div.link-wrapper a")["href"]
            yield Apartment(title, object_number, area, link)

    except Exception as e:
        pprint(e)


class WahlinSession:
    def __init__(self, environment: Environment):
        pprint("Session started..")
        self.environment = environment
        self.pushbullet = Pushbullet(environment.pb_api)
        self.apartments = []

    def get(self, endpoint: str) -> requests.models.Response:
        url = self.environment.base_url + endpoint
        return requests.get(url)

    def post(self, endpoint: str, payload: dict) -> requests.models.Response:
        pass

    def push(self, payload):
        self.pushbullet.push_note(
            f"{payload.title}",
            f"{payload.link}\n\narea: {payload.area}",
        )

    def accept(self, apartment: Apartment) -> bool:
        return all(f(apartment) for f in self.environment.filters)

    def find_apartments(self):
        response = self.get("lediga-objekt/lagenheter/")
        soup = bs(response.content, "html.parser")
        self.n_apartments = get_n_apartments(soup)
        if self.n_apartments > 0:
            pprint(f"{self.n_apartments} apartments founds")
            for apt in get_apartments(soup):
                if self.accept(apt):
                    self.push(apt)
            pprint("Apartments pushed")


@app.lib.cron()
def main(event):
    session = WahlinSession(Environment.Production)
    session.find_apartments()
    pprint("Session over")
    return "Session over"