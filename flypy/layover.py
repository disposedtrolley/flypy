
class Layover:
    """This class defines a layover period between two legs of a trip.
    """

    def __init__(self, arr_leg, dept_leg, conn_time):
        """Initialises the Layover object.

        Args:
            arr_leg (Leg): the leg on which pax arrived at the
                           layover airport.
            dept_leg (Leg): the leg on which pax will depart from the
                            layover airport.
            conn_time (int): the total layover time in minutes.

        Returns:
            None.
        """

        self.arr_leg = arr_leg
        self.dept_leg = dept_leg
        self.start_time = arr_leg.arr_time
        self.end_time = dept_leg.dept_time
        self.conn_time = conn_time
        self.airport = self._set_layover_airpot()

    def _set_layover_airpot(self):
        """Returns the airport where the layover will take place.

        Args:
            None.

        Returns:
            dict: A dictionary describing the origin of the leg, of
                  the following schema:
                  {
                    "code": <string> the IATA code of the origin
                            airport,
                    "name": <string> the name of the origin
                            airport,
                    "city": <string> the name of the origin city
                 }
        """
        return self.arr_leg.dest

    def get_layover_airport(self):
        return self.airport

    def get_layover_dur(self):
        return self.conn_time

    def get_layover_start(self):
        return self.start_time

    def get_layover_end(self):
        return self.end_time

    def __str__(self):
        return "\t\t[Layover] DUR: {} minutes at {}. START: {}. END: {}.".format(
                self.get_layover_dur(),
                self.get_layover_airport()["name"],
                self.start_time,
                self.end_time)
