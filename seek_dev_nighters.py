import json, requests, pytz
from datetime import datetime


def load_data_from_api(page_num):
    url = "https://devman.org/api/challenges/solution_attempts/"
    payload = {"page": page_num}

    response = requests.get(url, params=payload)

    return response.json()


def get_number_of_pages():
    page_data = load_data_from_api(1)
    return page_data['number_of_pages']


def load_attempts():
    pages = get_number_of_pages()

    for page in range(1, pages + 1):
        records = load_data_from_api(page)["records"]

        for attempt in records:
            yield attempt


def is_nighter(attempt):
    end_night_hour = 4

    if attempt["timestamp"] is None:
        return None

    attempt_timezone = pytz.timezone(attempt["timezone"])
    attempt_time = attempt_timezone.localize(datetime.fromtimestamp(attempt["timestamp"]))
    return attempt_time.hour < end_night_hour


def get_nighters():
    nighters = set()

    for attempt in load_attempts():
        if is_nighter(attempt):
            nighters.add(attempt["username"])

    return nighters


if __name__ == '__main__':
  for nighter in get_nighters():
    print(nighter)
