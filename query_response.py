from helper import convert_str_to_date
from leg import Leg
from trip import Trip
from layover import Layover


class QueryResponse:
    """This class stores a filtered set of data returned by a query. Trip and
    Leg objects are instantiated from data within this class.
    """

    def __init__(self, query_response):
        """Initialises the QueryResponse object by parsing the JSON response
        and extracting these key details from the "data" object:
            - airport
            - city
            - aircraft
            - carrier
        and the:
            - total cost
            - legs
        from the "tripOption" object.

        Args:
            query_response (dict): The JSON QPX query response as a Python
                                   dictionary.

        Returns:
            None.
        """
        self.query_response = query_response
        self.legs = self.create_legs()
        self.trip = self.create_trip()

    def get_airports(self):
        return self.airports

    def get_cities(self):
        return self.cities

    def get_aircraft(self):
        return self.aircraft

    def get_carriers(self):
        return self.carriers

    def create_legs(self):
        """This function returns all of the Legs present in the query response.

        Args:
            None.

        Returns:
            Legs[]: An array of Leg objects for this query response.

        """
        legs = []

        slice_data = self.query_response["trips"]["tripOption"][0]["slice"]
        data = self.query_response["trips"]["data"]

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

                # extract flight details
                leg_flight_carrier = segment["flight"]["carrier"]
                leg_flight_number = segment["flight"]["number"]
                leg_flight = {
                    "carrier": leg_flight_carrier,
                    "number": leg_flight_number,
                    "name": None
                }
                # get carrier name from "data" object
                trip_carrier = data["carrier"]
                for carrier in trip_carrier:
                    if carrier["code"] == leg_flight["carrier"]:
                        leg_flight["name"] = carrier["name"]

                # extract aircraft details
                leg_ac_code = leg_data["aircraft"]
                leg_aircraft = {
                    "code": leg_ac_code,
                    "name": None
                }
                # get aircraft name from "data" object
                trip_ac = data["aircraft"]
                for aircraft in trip_ac:
                    if aircraft["code"] == leg_ac_code:
                        leg_aircraft["name"] = aircraft["name"]

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

    def create_layovers(self):
        """Creates all Layover objects for this query response.
        """
        return None

    def create_trip(self):
        """This function returns a Trip object comprising of global trip details
        and individual Leg objects.

        Args:
            None.

        Returns:
            Trip: The Trip object corresponding to this query response.

        """

        trip_data = self.query_response["trips"]["data"]
        trip_option_data = self.query_response["trips"]["tripOption"][0]

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
        trip_legs = self.legs

        # create Trip object
        this_trip = Trip(trip_origin,
                         trip_dest,
                         trip_legs,
                         trip_cost,
                         trip_carrier)

        return this_trip
