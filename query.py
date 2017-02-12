
class Query:
    """This class represents a query sent to QPX.
    """

    def __init__(self, origin, dest, dept_date, return_date, pax, airline,
                 max_stops):
        """Initialises the Query object.

        Args:
            origin (string): The IATA code of the originating airport or city.
            dest (string): The IATA code of the destination airport or city.
            dept_date (datetime): The date of intended departure.
            return_date (datetime): The date of intended return (for round-trip
                                   flights), None for one-way.
            pax (dict): The number of passengers intending to fly, as a
                        dictionary of the following schema:
                        {
                            "adultCount": <int>,
                            "childCount": <int>,
                            "seniorCount": <int>,
                            "infantInLapCount": <int>,
                            "infantsInSeatCount": <int>
                        }
            airline (string): The IATA code of the requested airline,
                              None for no preference.
            max_stops (int[]): The maximum number of stops allowed for each
                               slice of the journey (i.e. depart and return
                               trip), as an array of integers where the index
                               is the slice and the value is the maximum stops.

        Returns:
            None.
        """
        self.origin = str(origin)
        self.dest = str(dest)
        self.dept_date = dept_date
        self.return_date = return_date
        self.pax = pax
        self.airline = airline
        self.max_stops = max_stops

    def send_query(self):
        return None

    def format_query(self):
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

    def validate_iata(self):
        return None
