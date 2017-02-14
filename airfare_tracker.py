from query import Query
from query_response import QueryResponse
from helper import convert_str_to_date_tz_naive
import json


def load_test_data():
    """This function returns the JSON test data as a dictionary."""
    test_data = open('data/test_data_multi_leg.json', 'r')
    return json.loads(test_data.read())


def main():
    data = load_test_data()
    response = QueryResponse(data)

    # dept_date = convert_str_to_date_tz_naive("2017-07-09")
    # return_date = convert_str_to_date_tz_naive("2017-09-23")
    # query = Query()
    # print(query.add_origin("MEL"))
    # print(query.add_dest("PVG"))
    # print(query.add_dept_date(dept_date))
    # print(query.add_return_date(return_date))
    # print(query.add_pax(1))
    # print(query.add_airline("CA"))
    # print(query.add_max_stops(1, 1))
    # response = query.send()

    trips = response.get_trips()
    for trip in trips:
        for journey in trip.journeys:
            for leg in journey.legs:
                print(leg)
        print(trip.get_cost())

if __name__ == "__main__":
    main()
