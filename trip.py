
class Trip:
    """This class defines an entire trip, and includes Legs for each
    segment of the trip."""

    def __init__(self, origin, dest, legs, cost, carrier):
        """This function initialises the Trip object.

        Args:
            origin (dict): The trip origin as a dictionary of the following
                           schema:
                           {
                                "airport_code": <string>,
                                "airport_name": <string>,
                                "city_name": <string>,
                                "city_code": <string>
                           }
            dest (dict): The trip destination as a dictionary of the following
                         schema:
                         {
                            "airport_code": <string>,
                            "airport_name": <string>,
                            "city_name": <string>,
                            "city_code": <string>
                         }
            legs (Leg[]): An array of Leg objects within this Trip.
            cost (string): The total cost of the trip.
            carrier (dict[]): An array of dictionaries describing the carriers
                              present on this trip. Each dictionary is of the
                              following schema:
                              {
                                "carrier_code": <string>,
                                "carrier_name": <string>
                              }

        Returns:
            None.

        """

        self.origin = origin
        self.dest = dest
        self.legs = legs
        self.cost = cost
        self.carrier = carrier

    def get_origin(self):
        """This function returns the origin of this Trip as a dictionary.

        Args:
            None.

        Returns:
            dict: The origin data as a dictionary of the same schema
                  as the input.

        """
        return self.origin

    def get_dest(self):
        """This function returns the destination of this Trip as a dictionary.

        Args:
            None.

        Returns:
            dict: The destination data as a dictionary of the same schema
                  as the input.

        """
        return self.dest

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

    def get_carrier(self):
        """This function returns the carriers of this Trip as an array
           of dictionaries.

        Args:
            None.

        Returns:
            dict[]: The list of carriers on this Trip. Each dictionary is
                    of the same schema as the input.

        """
        return self.carrier
