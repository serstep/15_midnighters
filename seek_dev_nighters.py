import json, requests, pytz
from datetime import datetime


def load_data_from_api(page_num):
    url = "https://devman.org/api/challenges/solution_attempts/"
    payload = {"page": page_num}

    response = requests.get(url, params=payload)

    return response.json()


def load_attempts():
    first_page = load_data_from_api(1)
    pages = first_page["number_of_pages"]
    attempts = first_page["records"]

    for page in range(2, pages + 1):
        records = load_data_from_api(page)["records"]
        attempts.extend(records)

    return attempts


def is_nighter(attempt):
    end_night_hour = 4

    if attempt["timestamp"] is None:
        return None

    attempt_timezone = pytz.timezone(attempt["timezone"])
    attempt_time = attempt_timezone.localize(datetime.fromtimestamp(attempt["timestamp"]))
    return attempt_time.hour < end_night_hour


def get_nighters():
    return set([attempt["username"] for attempt in load_attempts() if is_nighter(attempt)])


if __name__ == '__main__':
    for nighter in get_nighters():
        print(nighter)
