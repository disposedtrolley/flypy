import requests
import json
from query_response import QueryResponse
from api_key import API_KEY
import csv


class Query:
    """This class represents a query sent to QPX.
    """

    BASE_URL = "https://www.googleapis.com/qpxExpress/v1/trips/search{}{}" \
        .format("?key=", API_KEY)

    IATA_LIST = None

    def __init__(self):
        """Initialises the Query object.

        Args:
            None.

        Returns:
            None.
        """
        Query.IATA_LIST = self.open_iata_list()
        self.origin = None
        self.dest = None
        self.dept_date = None
        self.return_date = None
        self.pax = None
        self.airline = None
        self.max_stops = None

    def open_iata_list(self):
        """Opens the list of IATA codes for airports and cities, converted
        to a Python dictionary.

        Args:
            None.

        Returns:
            dict[]: an array of airports with IATA codes.
        """
        reader = csv.DictReader(open("data/airports_filtered.csv", "rb"))
        dict_list = []
        for line in reader:
            dict_list.append(line)
        return dict_list

    def send(self):
        """Sends the query to QPX and returns a QueryResponse object with the
        response data.

        Args:
            None.

        Returns:
            QueryResponse: the response data of the query.
        """
        if self._validate_params_exist:
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
        else:
            return "Mandatory parameters not supplied."

    def _validate_params_exist(self):
        """Validates that mandatory parameters have been supplied for a basic
        query to run.

        Args:
            None.

        Returns:
            bool: True if some mandatory params are missing, False otherwise.
        """
        mandatory_left_blank = False
        mandatory_params = [self.origin,
                            self.dest,
                            self.dept_date,
                            self.pax]

        for param in mandatory_params:
            if param is None:
                mandatory_left_blank = True
        return mandatory_left_blank

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
            string: the name of the validated origin airport.
        """
        ap = self._validate_iata_airport(origin)
        if ap:
            self.origin = ap["iata_code"]
            return "ORIGIN: " + ap["name"]
        else:
            return "Invalid IATA code."

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
        journey. Optional.

        Args:
            max_stops_dept (int): the maximum allowed layovers for the
                                  departing flight.
            max_stops_return (int): the maximum allowed layovers for the
                                    returning flight.

        Returns:
            string: the validated airline name.
        """

    def _validate_iata_airport(self, code):
        for ap in Query.IATA_LIST:
            if ap["iata_code"] == code:
                return ap
        return False
