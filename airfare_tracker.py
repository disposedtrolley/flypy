import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup
from query import Query
from query_response import QueryResponse
from helper import convert_str_to_date


def perform_search(query):
    base_url = "https://www.googleapis.com/qpxExpress/v1/trips/search?key=AIzaSyABg87ZKo9OH5Xc7llvmbxBd8LlrZ0kiuM"  # NOQA
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


def main():
    dept_date = convert_str_to_date("2017-07-10")
    return_date = None
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

    # print(test_query.format_query())

    # data = perform_search(test_query.format_query())
    data = load_test_data()
    response = QueryResponse(data)
    trips = response.get_trips()
    for trip in trips:
        for journey in trip.journeys:
            for leg in journey.legs:
                print(leg)
        print(trip.get_cost())

if __name__ == "__main__":
    main()
