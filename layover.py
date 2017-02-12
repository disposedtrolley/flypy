
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
        # should = arr_leg's dest
        return None

    def set_arr_terminal(self):
        # should = arr_leg's dest terminal
        return None

    def set_dept_terminal(self):
        # should = dept_leg's origin terminal
        return None

    def get_layover_airport(self):
        return self.airport

    def get_layover_dur(self):
        return self.conn_time

    def get_arr_terminal(self):
        return self.arr_terminal

    def get_dept_terminal(self):
        return self.dept_terminal
