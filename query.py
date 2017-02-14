import requests
import json
from query_response import QueryResponse
from helper import convert_str_to_date
from api_key import API_KEY
import csv
import datetime


class Query:
    """This class represents a query sent to QPX.
    """

    BASE_URL = "https://www.googleapis.com/qpxExpress/v1/trips/search{}{}" \
        .format("?key=", API_KEY)
    AIRPORT_LIST = None
    AIRLINE_LIST = None

    def __init__(self):
        """Initialises the Query object.

        Args:
            None.

        Returns:
            None.
        """
        Query.AIRPORT_LIST = self._open_airport_list()
        Query.AIRLINE_LIST = self._open_airline_list()
        self.origin = None
        self.dest = None
        self.dept_date = None
        self.return_date = None
        self.pax = None
        self.airline = None
        self.max_stops = None
        self.max_stops_return = None

    def _open_airport_list(self):
        """Opens the list of IATA codes for airports and cities, converted
        to a Python dictionary.

        Args:
            None.

        Returns:
            dict[]: an array of airports with IATA codes.
        """
        reader = csv.DictReader(open("data/airports.csv", "rb"))
        dict_list = []
        for line in reader:
            dict_list.append(line)
        return dict_list

    def _open_airline_list(self):
        """Opens the list of IATA codes and names for airlines, converted
        to a Python dictionary.

        Args:
            None.

        Returns:
            dict[]: an array of airlines with IATA codes.
        """
        with open("data/airlines.json") as file:
            airlines = json.load(file)
        return airlines

    def send(self):
        """Sends the query to QPX and returns a QueryResponse object with the
        response data.

        Args:
            None.

        Returns:
            QueryResponse: the response data of the query.
        """
        if self._validate_params_exist():
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
            print("All mandatory parameters not supplied.")
            return False

    def _validate_params_exist(self):
        """Validates that mandatory parameters have been supplied for a basic
        query to run.

        Args:
            None.

        Returns:
            bool: False if some mandatory params are missing, True otherwise.
        """
        validated = True
        mandatory_params = [self.origin,
                            self.dest,
                            self.dept_date,
                            self.pax]

        for param in mandatory_params:
            if param is None:
                validated = False
        return validated

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
                "date": "{:%Y-%m-%d}".format(self.dept_date)
            }
        ]
        if self.return_date is not None:
            trip_slice.append({
                    "origin": self.dest,
                    "destination": self.origin,
                    "date": "{:%Y-%m-%d}".format(self.return_date)
                })
        if self.airline:
            for trip in trip_slice:
                trip["permittedCarrier"] = self.airline
        if self.max_stops:
            trip_slice[0]["maxStops"] = self.max_stops
        if self.max_stops_return:
            trip_slice[1]["maxStops"] = self.max_stops_return

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
        ap = self._validate_iata_airport(dest)
        if ap:
            self.dest = ap["iata_code"]
            return "DEST: " + ap["name"]
        else:
            return "Invalid IATA code."

    def add_dept_date(self, dept_date):
        """Validates and adds a departure date to the query.

        Args:
            dept_date (datetime): a datetime object of the intended departure
                                  date.

        Returns:
            string: the validated departure date in the format YYYY-MM-DD.
        """
        if dept_date > datetime.datetime.now():
            self.dept_date = dept_date
            return "DEPT_DATE: " + "{:%Y-%m-%d}".format(dept_date)
        else:
            return "Date must be in the future."

    def add_return_date(self, return_date):
        """Validates and adds a return date to the query. This is optional
        and only specified if a return journey is requested.

        Args:
            dept_date (datetime): a datetime object of the intended return
                                  date.

        Returns:
            string: the validated return date in the format YYYY-MM-DD.
        """
        if return_date > datetime.datetime.now() and \
                return_date > self.dept_date:
            self.return_date = return_date
            return "RETURN_DATE: " + "{:%Y-%m-%d}".format(return_date)
        else:
            return "Date must be in the future and after the departure date."

    def add_pax(self,
                adult=None,
                child=None,
                senior=None,
                infant_lap=None,
                infant_seat=None):
        """Validates and adds passenger counts to the query.

        Args:
            adult (int): number of adult passengers.
            child (int): number of child passengers.
            senior (int): number of senior passengers.
            infant_lap (int): number of infant in lap passengers.
            infant_seat (int): number of infant in seat passengers.

        Returns:
            dict: passenger counts.
        """
        if (adult or child or senior or infant_lap or infant_seat) > 0:
            pax = {
                "adultCount": adult,
                "childCount": child,
                "infantInLapCount": infant_lap,
                "infantInSeatCount": infant_seat,
                "seniorCount": senior
            }
            self.pax = pax
            return "PAX: " + str(pax)
        else:
            return "At least one type of passenger must be travelling."

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
        self.max_stops = max_stops_dept
        self.max_stops_return = max_stops_return
        return "MAX_STOPS: " + str(max_stops_dept) + ", " + \
            str(max_stops_return)

    def _validate_iata_airport(self, code):
        for ap in Query.AIRPORT_LIST:
            if ap["iata_code"] == code:
                return ap
        return False
