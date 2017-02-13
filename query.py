import requests
import json
from query_response import QueryResponse
from api_key import API_KEY


class Query:
    """This class represents a query sent to QPX.
    """

    BASE_URL = "https://www.googleapis.com/qpxExpress/v1/trips/search{}{}" \
        .format("?key=", API_KEY)

    def __init__(self, origin, dest, dept_date, return_date, pax, airline,
                 max_stops):
        """Initialises the Query object.

        Args:
            origin (string): The IATA code of the originating airport or city.
            dest (string): The IATA code of the destination airport or city.
            dept_date (datetime): The date of intended departure.
            return_date (datetime): The date of intended return (for round-trip
                                   flights), None for one-way.
            pax (dict): The number of passengers intending to fly, as a
                        dictionary of the following schema:
                        {
                            "adultCount": <int>,
                            "childCount": <int>,
                            "seniorCount": <int>,
                            "infantInLapCount": <int>,
                            "infantsInSeatCount": <int>
                        }
            airline (string): The IATA code of the requested airline,
                              None for no preference.
            max_stops (int[]): The maximum number of stops allowed for each
                               slice of the journey (i.e. depart and return
                               trip), as an array of integers where the index
                               is the slice and the value is the maximum stops.

        Returns:
            None.
        """
        self.origin = str(origin)
        self.dest = str(dest)
        self.dept_date = dept_date
        self.return_date = return_date
        self.pax = pax
        self.airline = airline
        self.max_stops = max_stops

    def send(self):
        """Sends the query to QPX and returns a QueryResponse object with the
        response data.

        Args:
            None.

        Returns:
            QueryResponse: the response data of the query.
        """
        base_url = "https://www.googleapis.com/qpxExpress/v1/trips/search?key=AIzaSyABg87ZKo9OH5Xc7llvmbxBd8LlrZ0kiuM"  # NOQA
        payload = self._format_query()

        r = requests.post(Query.BASE_URL,
                          data=json.dumps(payload),
                          headers={'Content-Type': 'application/json'})
        r = r.text

        text_file = open("data/test_data_multi_leg.json", "w")
        text_file.write(r)
        text_file.close()

        query_response = QueryResponse(json.loads(r))

        return query_response

    def _format_query(self):
        """Formats the input parameters into a valid QPX query object.

        Args:
            None.

        Returns:
            string: A valid QPX query string.
        """

        # slice
        trip_slice = [
            {
                "origin": self.origin,
                "destination": self.dest,
                "date": "{:%Y-%m-%d}".format(self.dept_date),
                "maxStops": self.max_stops[0]
            }
        ]
        if self.return_date is not None:
            trip_slice.append({
                    "origin": self.dest,
                    "destination": self.origin,
                    "date": "{:%Y-%m-%d}".format(self.return_date),
                    "maxStops": self.max_stops[1]
                })
        if self.airline:
            for trip in trip_slice:
                trip["permittedCarrier"] = self.airline

        query = {
            "request": {
                "passengers": self.pax,
                "slice": trip_slice,
                "solutions": "1"
            }
        }
        return query

    def add_origin(self, origin):
        """Validates and adds an origin airport to the query.

        Args:
            origin (string): the IATA code of the originating airport.

        Returns:
            string: the name of the validated origin airport, or None if not
                    found.
        """

    def add_dest(self, dest):
        """Validates and adds a destination airport to the query.

        Args:
            origin (string): the IATA code of the destination airport.

        Returns:
            string: the name of the validated destination airport, or None
                    if not found.
        """

    def add_dept_date(self, dept_date):
        """Validates and adds a departure date to the query.

        Args:
            dept_date (datetime): a datetime object of the intended departure
                                  date.

        Returns:
            string: the validated departure date in the format YYYY-MM-DD.
        """

    def add_return_date(self, return_date):
        """Validates and adds a return date to the query. This is optional
        and only specified if a return journey is requested.

        Args:
            dept_date (datetime): a datetime object of the intended return
                                  date.

        Returns:
            string: the validated return date in the format YYYY-MM-DD.
        """

    def add_pax_adult(self, pax_adult):
        """Validates and adds adult passengers to the query.

        Args:
            pax_adult (int): the number of adult passengers travelling.

        Returns:
            string: the validated adult passenger count.
        """

    def add_pax_child(self, pax_child):
        """Validates and adds child passengers to the query.

        Args:
            pax_child (int): the number of child passengers travelling.

        Returns:
            string: the validated child passenger count.
        """

    def add_pax_senior(self, pax_senior):
        """Validates and adds senior passengers to the query.

        Args:
            pax_senior (int): the number of senior passengers travelling.

        Returns:
            string: the validated senior passenger count.
        """

    def add_pax_infant_lap(self, pax_infant_lap):
        """Validates and adds infant in lap passengers to the query.

        Args:
            pax_infant_lap (int): the number of infant in lap passengers
            travelling.

        Returns:
            string: the validated infant in lap passenger count.
        """

    def add_pax_infant_seat(self, pax_infant_seat):
        """Validates and adds infant in seat passengers to the query.

        Args:
            pax_infant_seat (int): the number of infant in seat passengers
            travelling.

        Returns:
            string: the validated infant in seat passenger count.
        """

    def add_airline(self, airline):
        """Adds a preferred airline to the query. Optional.

        Args:
            airline (string): the IATA code of the preferred airline.

        Returns:
            string: the validated airline name.
        """

    def add_max_stops(self, max_stops_dept, max_stops_return):
        """Adds a restriction on the maximum layovers for the onward and return
        journey.

        Args:
            max_stops_dept (int): the maximum allowed layovers for the
                                  departing flight.
            max_stops_return (int): the maximum allowed layovers for the
                                    returning flight.

        Returns:
            string: the validated airline name.
        """

    def _validate_iata(self):
        return None
