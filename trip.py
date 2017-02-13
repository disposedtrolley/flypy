
class Trip:
    """This class defines an entire trip, which includes Journeys (e.g. onward
    and return), Legs within those Journeys (specifics for each flight), and
    Layovers within the Journeys (specifics for each layover between flights).
    """

    def __init__(self, query_response_data, query_response_trip_option):
        """This function initialises the Trip object.

        Args:
            query_response_data (dict): the JSON object representing the "data"
                                        object of the query response from QPX.
            query_response_trip_option (dict): the JSON object representing the
                                               "tripOption" object of the
                                               query response from QPX.

        Returns:
            None.

        """

        self.query_response_data = query_response_data
        self.query_response_trip_option = query_response_trip_option
        self.ap_list, self.ac_list, self.city_list, self.carrier_list = \
            self.extract_globals()

    def extract_globals(self):
        """Extracts details from the query response which are global to all
        trip options, e.g. the "data" object in the response.

        Args:
            None.

        Returns:
            ap_list (dict): listing of all of the airports mentioned in the
                            trip options, of the following schema:
                            {
                                "code": <string> the IATA code of the airport,
                                "name": <string> the name of the airport,
                                "city": <string> the IATA code of the city
                            }
            ac_list (dict): listing of all of the aircraft mentioned in the
                            trip options, of the following schema:
                            {
                                "code": <string> the IATA aircraft code,
                                "name": <string> the name of the aircraft
                            }
            city_list (dict): listing of all of the cities mentioned in the
                              trip options, of the following schema:
                              {
                                "code": <string> the IATA city code,
                                "name": <string> the name of the city
                              }
            carrier_list (dict): listing of all of the carriers mentioned in
                                 the trip options, of the following schema:
                                 {
                                    "code": <string> the IATA carrier code,
                                    "name": <string> the name of the carrier
                                 }
        """
        response_data_airport = query_response_data["airport"]
        ap_list = []
        for airport in response_data_airport:
            ap_list.append({
                    "code": airport["code"],
                    "name": airport["name"],
                    "city": airport["city"]
                })

        response_data_aircraft = query_response_data["aircraft"]
        ac_list = []
        for aircraft in response_data_aircraft:
            ac_list.append({
                    "code": aircraft["code"],
                    "name": aircraft["name"]
                })

        response_data_city = query_response_data["city"]
        city_list = []
        for city in response_data_city:
            city_list.append({
                    "code": city["code"],
                    "name": city["name"]
                })

        response_data_carrier = query_response_data["carrier"]
        carrier_list = []
        for carrier in response_data_carrier:
            carrier_list.append({
                    "code": carrier["code"],
                    "name": carrier["name"]
                })

        return ap_list, ac_list, city_list, carrier_list

    def get_legs(self):
        """This function returns the Leg objects of this Trip as an array.

        Args:
            None.

        Returns:
            Leg[]: An array of Leg objects for this Trip.

        """
        return self.legs

    def get_cost(self):
        """This function returns the total cost of this Trip as an integer.

        Args:
            None.

        Returns:
            int: The total cost of the trip

        """
        return int(self.cost)
