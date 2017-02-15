import iso8601
import csv
import json
from datetime import datetime


def convert_str_to_date(str_to_convert):
    """This function converts a string to a datetime object.
    Args:
        str_to_convert (string): The string to convert in the format of
                                 <YYYY>-<MM>-<DD>T<HH>:<MM>+<HH>:<MM>
    Returns:
        datetime: The input string converted to a datetime object.
    """

    output = iso8601.parse_date(str_to_convert)
    return output


def convert_str_to_date_tz_naive(str_to_convert):
    """This function converts a string to a datetime object.
    Args:
        str_to_convert (string): The string to convert in the format of
                                 <YYYY>-<MM>-<DD>
    Returns:
        datetime: The input string converted to a datetime object.
    """
    output = datetime.strptime(str_to_convert, "%Y-%m-%d")
    return output


def open_airport_list():
        """Opens the list of IATA codes for airports and cities, converted
        to a Python dictionary.

        Args:
            None.

        Returns:
            dict[]: an array of airports with IATA codes.
        """
        with open("flypy/data/airports.json") as file:
            airports = json.load(file)
        return airports


def open_airline_list():
    """Opens the list of IATA codes and names for airlines, converted
    to a Python dictionary.

    Args:
        None.

    Returns:
        dict[]: an array of airlines with IATA codes.
    """
    with open("flypy/data/airlines.json") as file:
        airlines = json.load(file)
    return airlines
