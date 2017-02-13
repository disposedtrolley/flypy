from helper import convert_str_to_date
from trip import Trip


class QueryResponse:
    """This class stores a filtered set of data returned by a query. Trip and
    Leg objects are instantiated from data within this class.
    """

    def __init__(self, query_response):
        """Initialises the QueryResponse object.

        Args:
            query_response (dict): The JSON QPX query response as a Python
                                   dictionary.

        Returns:
            None.
        """
        self.query_response = query_response
        self.trips = self._create_trips()

    def _create_trips(self):
        """Returns an array of Trip objects for each trip option in this
        query response.

        Args:
            None.

        Returns:
            Trip[]: an array of Trip objects corresponding to each trip option
            in this query response.
        """
        trips = []

        data = self.query_response["trips"]["data"]
        if "tripOption" in self.query_response["trips"]:
            trip_options = self.query_response["trips"]["tripOption"]
            for option in trip_options:
                trip = Trip(data, option)
                trips.append(trip)

        return trips

    def get_trips(self):
        return self.trips
