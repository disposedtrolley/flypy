
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
        self.conn_time = conn_time
        self.airport = self.set_layover_airpot()
        self.arr_terminal = self.set_arr_terminal()
        self.dept_terminal = self.set_dept_terminal()

    def set_layover_airpot(self):
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
                    "city": <string> the name of the origin city,
                    "terminal": <int>
                 }
        """
        return self.arr_leg.dest

    def set_arr_terminal(self):
        """Returns the terminal of the arriving flight to the layover airport.

        Args:
            None.

        Returns:
            int: the arrival terminal.
        """
        return self.arr_leg.dest["terminal"]

    def set_dept_terminal(self):
        """Returns the terminal of the dpearting flight from the layover
        airport.

        Args:
            None.

        Returns:
            int: the departing terminal.
        """
        return self.dept_leg.origin["terminal"]

    def get_layover_airport(self):
        return self.airport

    def get_layover_dur(self):
        return self.conn_time

    def get_arr_terminal(self):
        return self.arr_terminal

    def get_dept_terminal(self):
        return self.dept_terminal
