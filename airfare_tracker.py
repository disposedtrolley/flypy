import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup
import iso8601
from leg import Leg
from trip import Trip
from query import Query


def perform_search(query):
    base_url = 'https://www.googleapis.com/qpxExpress/v1/trips/search?key=AIzaSyABg87ZKo9OH5Xc7llvmbxBd8LlrZ0kiuM'
    payload = query

    r = requests.post(base_url, data=json.dumps(payload),
                      headers={'Content-Type': 'application/json'})
    r = r.text

    text_file = open("data/test_data_multi_leg.json", "w")
    text_file.write(r)
    text_file.close()
    return json.loads(r)


def load_test_data():
    """This function returns the JSON test data as a dictionary."""
    test_data = open('data/test_data_multi_leg.json', 'r')
    return json.loads(test_data.read())


def create_legs(query_response):
    """This function returns all of the Legs present in the query response.

    Args:
        query_response (dict): The JSON QPX query response as a Python
                               dictionary.

    Returns:
        Legs[]: An array of Leg objects for this query response.

    """

    legs = []

    slice_data = query_response["trips"]["tripOption"][0]["slice"]

    for slice in slice_data:

        segment_data = \
            slice["segment"]

        for segment in segment_data:

            leg_data = segment["leg"][0]

            # extract origin
            leg_origin = leg_data["origin"]

            # extract destination
            leg_dest = leg_data["destination"]

            # extract departure and arrival time
            leg_dept_time = convert_str_to_date(leg_data["departureTime"])
            leg_arr_time = convert_str_to_date(leg_data["arrivalTime"])
            # extract flight details as dictionary
            leg_flight = segment["flight"]

            # extract aircraft details
            leg_aircraft = {
                "code": leg_data["aircraft"],
                "name": None
            }

            # extract duration
            leg_duration = leg_data["duration"]

            # create new Leg object
            this_leg = Leg(leg_origin,
                           leg_dest,
                           leg_dept_time,
                           leg_arr_time,
                           leg_flight,
                           leg_aircraft,
                           leg_duration)

            legs.append(this_leg)

    return legs


def create_trip(query_response, legs):
    """This function returns a Trip object comprising of global trip details
    and individual Leg objects.

    Args:
        query_response (dict): The JSON QPX query response as a Python
                               dictionary.
        legs (Leg[]): An array of Leg objects within this Trip.

    Returns:
        Trip: The Trip object corresponding to this query response.

    """

    trip_data = query_response["trips"]["data"]
    trip_option_data = query_response["trips"]["tripOption"][0]

    # extract origin and dest as dictionary (airport code, airport name,
    #                                        city code, city name)
    trip_origin = {
                "airport_code": trip_data["airport"][1]["code"],
                "airport_name": trip_data["airport"][1]["name"],
                "city_name": trip_data["city"][1]["name"],
                "city_code": trip_data["city"][1]["code"]
            }
    trip_dest = {
                "airport_code": trip_data["airport"][0]["code"],
                "airport_name": trip_data["airport"][0]["name"],
                "city_name": trip_data["city"][0]["name"],
                "city_code": trip_data["city"][0]["code"]
            }

    # extract cost
    trip_cost = trip_option_data["saleTotal"]

    # extract carrier as dictionary
    trip_carrier = {
                "carrier_code": trip_data["carrier"][0]["code"],
                "carrier_name": trip_data["carrier"][0]["name"]
            }

    # get legs
    trip_legs = legs

    # create Trip object
    this_trip = Trip(trip_origin,
                     trip_dest,
                     trip_legs,
                     trip_cost,
                     trip_carrier)

    return this_trip


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


def parse_results(query_response):
    """Parses the query response to create Trip and Leg objects. Returns an
    error if no flights were returned by QPX.

    Args:
        query_response (dict): The JSON QPX query response as a Python
                               dictionary.

    Returns:
        Trip: The Trip object corresponding to this query response.
    """

    if "tripOption" in query_response["trips"]:
        legs = create_legs(query_response)
        trip = create_trip(query_response, legs)
        return trip
    else:
        return None


def main():
    dept_date = convert_str_to_date("2017-07-10")
    return_date = convert_str_to_date("2017-07-24")
    pax = {
        "adultCount": 2,
        "childCount": 0,
        "seniorCount": 0,
        "infantInLapCount": 0,
        "infantsInSeatCount": 0
    }
    max_stops = [10, 10]
    test_query = Query("MEL",
                       "PEK",
                       dept_date,
                       return_date,
                       pax,
                       None,
                       max_stops)

    print(test_query.format_query())

    data = perform_search(test_query.format_query())
    # data = load_test_data()

    trip = parse_results(data)

    if trip:
        for i in trip.legs:
            print(i)
        print(trip.cost)
    else:
        print("No flights found.")


if __name__ == "__main__":
    main()
