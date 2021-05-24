from model import Apartment
from deta import Deta
from dotenv import PROJECT_KEY


def create_db():
    client = Deta(PROJECT_KEY)
    db = client.Base("wahlinf")

    def insert(apt: Apartment):
        try:
            doc = {
                "key": apt.object_number,
                "link": apt.link,
                "title": apt.title,
                "area": apt.area,
                "object_number": apt.object_number,
            }
            db.insert(doc)
        except Exception as e:
            raise e

    return insert
