"""Sample module to illustrate how to use patch as a decorator"""
from datetime import datetime

import requests


def is_weekday():
    """Returns True if today is a weekday, False if today is a weekend day"""
    today = datetime.today()
    return 0 <= today.weekday() < 5


def get_holidays():
    """Access an *invented* API to get a dictionary of holidays as in
    `{"12/25": "Christmas", "7/4": "Independence Day"}`
    """
    r = requests.get("http://localhost/api/holidays") # pylint: disable=missing-timeout,invalid-name
    if r.status_code == 200:
        return r.json()
    return None
