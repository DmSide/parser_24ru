import uuid

import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, MetaData, Column, Table, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import sessionmaker

from const import CONNECTION_STRING, MAIN_URL
from schema import Jobs


def create_db():
    db = create_engine(CONNECTION_STRING)
    meta = MetaData()

    jobs = Table(
        'jobs',
        meta,
        Column("uuid", UUID(as_uuid=True), default=uuid.uuid4(), primary_key=True),
        Column("title", String(128), nullable=False),
        Column("link", String(128), nullable=False),
        Column("description", String(1024), nullable=False),
        Column("money", String(128), nullable=True),
        Column("countries", String(256), nullable=False),
        Column("published", String(128), nullable=False),
    )
    meta.create_all(db)


def write_data_to_database():
    db = create_engine(CONNECTION_STRING)
    Session = sessionmaker(db)
    session = Session()

    r = requests.get(MAIN_URL)

    soup = BeautifulSoup(r.text, "html.parser")

    page_numbers = list(filter(None,
                               soup.find("div", id="pagePaginator").find("div").text.replace("\t", "").replace("\r",
                                                                                                               "").replace(
                                   "...", "").split("\n")))
    last_page_number = int(page_numbers[-2])

    for i in range(last_page_number):
        r = requests.get(f"{MAIN_URL}?page={i + 1}")

        soup = BeautifulSoup(r.text, "html.parser")

        vacations_list = soup.findAll("a", class_="adv")
        # print(len(vacations_list))
        for vacation in vacations_list:
            link = vacation.get("href")
            # print(link)
            title = vacation.find("span").text
            # print(title)
            description = vacation.find("div", class_="text").text
            description = description.replace("\t", "").replace("\r", "").replace("\n", "").replace("\xa0", "").strip()
            # print(description)
            money = vacation.find("div", class_="money")
            money = money.text if money else None
            # print(money)
            countries = []
            for country in vacation.findAll("div", class_="country"):
                countries.append("".join(c for c in country.text if c.isalpha()))
            countries = ",".join(countries)
            published = vacation.find("div", class_="time").text
            published = "".join(c for c in published if c.isdigit() or c == ".")
            # print(published)

            job = Jobs(
                uuid=uuid.uuid4(),
                title=title,
                link=link,
                description=description,
                money=money,
                countries=countries,
                published=published,
            )
            session.add(job)
            session.commit()


def read_data_from_database():
    db = create_engine(CONNECTION_STRING)
    Session = sessionmaker(db)
    session = Session()

    jobs = session.query(Jobs)
    for job in jobs:
        print(job.title)


def read_counties_number():
    db = create_engine(CONNECTION_STRING)
    Session = sessionmaker(db)
    session = Session()

    query = "SELECT COUNT(*), c.country " \
            "FROM (" \
            "SELECT uuid, title, link, description, money, regexp_split_to_table(countries, '\s*,\s*') as country, published " \
            "FROM public.jobs" \
            ") as c " \
            "GROUP BY c.country;"
    res = session.query(query)
    print(res)


if __name__ == '__main__':
    # create_db()
    # write_data_to_database()
    # read_data_from_database()
    read_counties_number()
