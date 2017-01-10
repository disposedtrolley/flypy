import requests
from bs4 import BeautifulSoup
import json
from leg import Leg


def perform_search():
    base_url = 'https://www.googleapis.com/qpxExpress/v1/trips/search?key=AIzaSyABg87ZKo9OH5Xc7llvmbxBd8LlrZ0kiuM'
    payload = {
        "request": {
            "passengers": {
                "adultCount": "1"
            },
            "slice": [
                {
                    "origin": "PVG",
                    "destination": "MEL",
                    "date": "2017-02-08",
                    "maxStops": 0
                }
            ],
            "solutions": "1"
            }
        }

    r = requests.post(base_url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})

    soup = BeautifulSoup(r.text, 'html.parser')
    print(soup)


def load_test_data():
    """This function returns the JSON test data as a dictionary."""
    test_data = open('data/test_data.txt', 'r')
    return json.loads(test_data.read())


def create_legs(query_response):
    """This function returns all of the Legs present in the query response."""

    segment_data = query_response["trips"]["tripOption"][0]["slice"][0]["segment"][0]
    leg_data = segment_data["leg"][0]

    # extract origin
    leg_origin = leg_data["origin"]

    # extract destination
    leg_dest = leg_data["destination"]

    # extract departure and arrival time
    leg_deptTime = leg_data["departureTime"]
    leg_arrTime = leg_data["arrivalTime"]

    # extract flight details as dictionary
    leg_flight = segment_data["flight"]
    
    # extract aircraft details
    leg_aircraft = leg_data["aircraft"]

    # extract duration
    leg_duration = leg_data["duration"]

    # create new Leg object
    this_leg = Leg(leg_origin,
                   leg_dest,
                   leg_deptTime,
                   leg_arrTime,
                   leg_flight,
                   leg_aircraft,
                   leg_duration)
    return this_leg


def create_trip(query_response, legs):
    """This function returns a Trip object comprising of global trip details
    and individual Leg objects.
    
    Args:
        query_response (dict): The JSON QPX query response as a Python dictionary.
        legs (Leg[]): An array of Leg objects within this Trip.

    Returns:
        Trip: The Trip object corresponding to this query response.

    """
    

def main():
    data = load_test_data()
    create_legs(data)
    #perform_search()

if __name__ == "__main__":
    main()
