
class Journey:
    """This class defines a particular journey within a Trip. Trips typically
    have either a single journey (for a one-way ticket), and two journeys for
    a return fare.
    """

    def __init__(self, slice_data, ac_list, ap_list, city_list, carrier_list):
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
        self.slice_data = slice_data
        self.ac_list, self.ap_list, self.city_list, self.carrier_list = \
            ac_list, ap_list, city_list, carrier_list

