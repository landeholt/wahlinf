from typing import List, Callable
from dotenv import TEST_API, PROD_API


class FormDetails:
    pass


class Environment:
    def __init__(
        self, name: str, base_url: str, filters: List[Callable], form_details: FormDetails, pb_api: str
    ):
        self.name = name
        self.base_url = base_url
        self.filters = filters
        self.form_details = form_details
        self.pb_api = pb_api


Environment.Production = Environment(
    "production",
    "https://wahlinfastigheter.se/",
    [],  # [lambda a: any([street in a.title for street in ["Tegelmästargatan"]])],
    FormDetails,
    PROD_API,
)

Environment.Test = Environment(
    "test",
    "http://web.archive.org/web/20210123212910/https://wahlinfastigheter.se/",
    [],
    FormDetails,
    TEST_API,
)
