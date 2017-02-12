
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

    def get_airports(self):
        return self.airports

    def get_cities(self):
        return self.cities

    def get_aircraft(self):
        return self.aircraft

    def get_carriers(self):
        return self.carriers

    def create_legs(self):
        """Creates all Leg objects for this query response.
        """
        return None

    def create_layovers(self):
        """Creates all Layover objects for this query response.
        """
        return None

    def create_trip(self):
        """Creates the consolidated Trip object for this query response.
        """
        return None
