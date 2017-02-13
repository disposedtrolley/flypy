from datetime import datetime
from query import Query
from query_response import QueryResponse
from helper import convert_str_to_date


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

    response = test_query.send()
    # data = load_test_data()
    # response = QueryResponse(data)
    trips = response.get_trips()
    for trip in trips:
        for journey in trip.journeys:
            for leg in journey.legs:
                print(leg)
        print(trip.get_cost())

if __name__ == "__main__":
    main()
