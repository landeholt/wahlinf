from dataclasses import dataclass


class Refs:
    n_vacant_apartments = ".ojects-term-list > li:nth-child(2) > a:nth-child(1) > span:nth-child(1)"
    apartment = ".posts-wrapper-block > div:nth-child(2)"


@dataclass
class Apartment:
    title: str
    object_number: str
    area: str
    link: str
