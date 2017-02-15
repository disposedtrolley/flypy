from leg import Leg
from layover import Layover
from helper import convert_str_to_date


class Journey:
    """This class defines a particular journey within a Trip. Trips typically
    have either a single journey (for a one-way ticket), and two journeys for
    a return fare.
    """

    def __init__(self, slice_data, ap_list, ac_list, city_list, carrier_list):
        """Initialises the Journey object.

        Args:
            slice_data (dict): a dictionary representing the JSON object of
                               a slice in the parent Trip.
            ap_list (dict[]): listing of all of the airports mentioned in this
                              slice, of the following schema:
                            {
                                "code": <string> the IATA code of the airport,
                                "name": <string> the name of the airport,
                                "city": <string> the IATA code of the city
                            }
            ac_list (dict[]): listing of all of the aircraft mentioned in this
                              slice, of the following schema:
                            {
                                "code": <string> the IATA aircraft code,
                                "name": <string> the name of the aircraft
                            }
            city_list (dict[]): listing of all of the cities mentioned in this
                              slice, of the following schema:
                              {
                                "code": <string> the IATA city code,
                                "name": <string> the name of the city
                              }
            carrier_list (dict[]): listing of all of the carriers mentioned in
                                   this slice, of the following schema:
                                 {
                                    "code": <string> the IATA carrier code,
                                    "name": <string> the name of the carrier
                                 }

        Returns:
            None.
        """
        self.segment_data = slice_data["segment"]
        self.ap_list, self.ac_list, self.city_list, self.carrier_list = \
            ap_list, ac_list, city_list, carrier_list
        self.legs = self._create_legs(self.segment_data)
        self.layovers = self._create_layovers(self.segment_data)

    def _create_legs(self, segment_data):
        """Creates the Leg objects for this journey using segments in the
        slice data.

        Args:
            segment_data (dict): the "segment" object of the query response.

        Returns:
            Leg[]: an array of Leg objects for this Journey.
        """
        legs = []

        for segment in segment_data:

            leg_data = segment["leg"][0]

            # extract origin
            leg_origin = {
                "code": leg_data["origin"],
                "name": None,
                "city": None
            }
            for airport in self.ap_list:
                if airport["code"] == leg_origin["code"]:
                    leg_origin["name"] = airport["name"]
                    for city in self.city_list:
                        if city["code"] == airport["city"]:
                            leg_origin["city"] = city["name"]

            # extract destination
            leg_dest = {
                "code": leg_data["destination"],
                "name": None,
                "city": None
            }
            for airport in self.ap_list:
                if airport["code"] == leg_dest["code"]:
                    leg_dest["name"] = airport["name"]
                    for city in self.city_list:
                        if city["code"] == airport["city"]:
                            leg_dest["city"] = city["name"]

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
            for carrier in self.carrier_list:
                if carrier["code"] == leg_flight["carrier"]:
                    leg_flight["name"] = carrier["name"]

            # extract aircraft details
            leg_ac_code = leg_data["aircraft"]
            leg_aircraft = {
                "code": leg_ac_code,
                "name": None
            }
            # get aircraft name from "data" object
            for aircraft in self.ac_list:
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

    def _create_layovers(self, segment_data):
        """Creates Layover objects for this Journey.

        Args:
            Segment_data (dict): the "segment" object of the query response.

        Returns:
            Layover[]: an array of Layover objects for this Journey.
        """
        layovers = []
        segments = segment_data
        for i in range(len(segments) - 1):
            if "connectionDuration" in segments[i]:
                duration = segments[i]["connectionDuration"]
                layover = Layover(self.legs[i], self.legs[i+1], duration)
                layovers.append(layover)

        return layovers

    def get_legs(self):
        return self.legs

    def get_layovers(self):
        return self.layovers

    def __str__(self):
        return "\t[Journey] {} to {}.".format(
                                    self.legs[0].get_origin()["code"],
                                    self.legs[-1].get_origin()["code"])
