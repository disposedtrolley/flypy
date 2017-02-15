from journey import Journey


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
        self.query_response_slice = query_response_trip_option["slice"]
        self.ap_list, self.ac_list, self.city_list, self.carrier_list = \
            self._extract_globals(self.query_response_data)
        self.journeys = self._create_journeys(self.query_response_slice)
        self.cost = query_response_trip_option["saleTotal"]

    def _extract_globals(self, data):
        """Extracts details from the query response which are global to all
        trip options, e.g. the "data" object in the response.

        Args:
            data (dict): the "data" object of the query response.

        Returns:
            ap_list (dict[]): listing of all of the airports mentioned in the
                            trip options, of the following schema:
                            {
                                "code": <string> the IATA code of the airport,
                                "name": <string> the name of the airport,
                                "city": <string> the IATA code of the city
                            }
            ac_list (dict[]): listing of all of the aircraft mentioned in the
                            trip options, of the following schema:
                            {
                                "code": <string> the IATA aircraft code,
                                "name": <string> the name of the aircraft
                            }
            city_list (dict[]): listing of all of the cities mentioned in the
                              trip options, of the following schema:
                              {
                                "code": <string> the IATA city code,
                                "name": <string> the name of the city
                              }
            carrier_list (dict[]): listing of all of the carriers mentioned in
                                 the trip options, of the following schema:
                                 {
                                    "code": <string> the IATA carrier code,
                                    "name": <string> the name of the carrier
                                 }
        """
        response_data_airport = data["airport"]
        ap_list = []
        for airport in response_data_airport:
            ap_list.append({
                    "code": airport["code"],
                    "name": airport["name"],
                    "city": airport["city"]
                })

        response_data_aircraft = data["aircraft"]
        ac_list = []
        for aircraft in response_data_aircraft:
            ac_list.append({
                    "code": aircraft["code"],
                    "name": aircraft["name"]
                })

        response_data_city = data["city"]
        city_list = []
        for city in response_data_city:
            city_list.append({
                    "code": city["code"],
                    "name": city["name"]
                })

        response_data_carrier = data["carrier"]
        carrier_list = []
        for carrier in response_data_carrier:
            carrier_list.append({
                    "code": carrier["code"],
                    "name": carrier["name"]
                })

        return ap_list, ac_list, city_list, carrier_list

    def _create_journeys(self, slices):
        """Creates a Journey object for each slice in this trip.

        Args:
            slices (dict[]): an array of "slice" objects from the query
                             response.

        Returns:
            Journey[]: an array of Journey objects, each representing a slice
                       on this trip.
        """
        journeys = []
        for slice in slices:
            journey = Journey(slice, self.ap_list, self.ac_list,
                              self.city_list, self.carrier_list)
            journeys.append(journey)

        return journeys

    def get_journeys(self):
        return self.journeys

    def get_cost(self):
        """This function returns the total cost of this Trip as an integer.

        Args:
            None.

        Returns:
            string: The total cost of the trip including currency.
        """
        return self.cost

    def __str__(self):
        return "[Trip] JOURNEYS: {}. COST: {}.".format(len(self.journeys),
                                                       self.cost)
