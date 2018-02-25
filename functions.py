# coding=utf-8

"""
Function module. Here are defined all
needed tool functions for main window.
This module is independent module.
"""

import json
from time import timezone
from urllib import request

# URL string to get API data from. Is a global readonly variable
# so it can be updated easily if changes happen.
api_url = "https://rata.digitraffic.fi/api/v1/"


def convert_date_format(date):
    """Returns a list containing the date and time
    formatted into separate strings from API data.
    Also adds current timezone difference."""
    # from: yyyy-mm-ddT00:00:00.000Z
    # to: [["yyyy","mm","dd"], ["00","00","00"]]

    assert str(date)  # Assertion: date is a string
    date = str(date)
    date = date.replace(".000Z", "").split("T")

    hour_str = date[1][0] + date[1][1]
    hour = int(hour_str)
    diff = int(-timezone / 3600)  # Get timezone from local system

    if hour < (24 - diff):
        hour += diff
    elif hour == (24 - diff):
        hour = 0
    else:
        hour = (hour + diff) - 24

    hour = str(hour)
    if len(hour) < 2:
        hour = "0" + hour

    date[1] = date[1].replace(hour_str, hour, 1)
    date[0] = date[0].split("-")
    date[1] = date[1].split(":")
    return date


def get_station_names():
    """Reads stations from a local json file.
    Parses and returns them in a proper format.
    :return: station dict, format: {long_name: shortname}
    """
    stations = {}
    with open("stationList.txt", encoding="utf-8") as f:
        data = json.load(f)
    for val in data:
        if val["id"].lower() == "null":
            continue
        if "[" in val["value"]:
            continue
        key = val["value"]
        value = val["id"].upper()
        stations[key] = value

    # Return format: {"Station code": "ABR"}
    return stations


def get_station_data(station, departing):
    """Function that extracts train fata from
    a specific station and returns it.
    :param station : the station to get data for
    :param departing : departing or arriving trains to get
    :return station_data : data of the specific station
    """

    # Get different data for departing and arriving trains
    if departing:
        part = "live-trains/station/" + station \
               + "?minutes_before_departure=240&" \
                 "minutes_after_departure=0&" \
                 "minutes_before_arrival=0&" \
                 "minutes_after_arrival=0&" \
                 "include_nonstopping=false"
    else:
        part = "live-trains/station/" + station \
               + "?minutes_before_departure=0&" \
                 "minutes_after_departure=0&" \
                 "minutes_before_arrival=240&" \
                 "minutes_after_arrival=0&" \
                 "include_nonstopping=false"

    # Form url and fetch data from it with proper encoding
    url = api_url + part
    with request.urlopen(url) as r:
        data = json.loads(r.read().decode("utf-8"))

    return data
