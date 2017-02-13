
class Leg:
    """This class defines a particular Leg of a Trip."""

    def __init__(self, origin, dest, dept_time, arr_time, flight, aircraft,
                 duration):
        """This function initialises the Leg object.

        Args:
            origin (dict): A dictionary describing the origin of the leg, of
                           the following schema:
                           {
                                "code": <string> the IATA code of the origin
                                        airport,
                                "name": <string> the name of the origin
                                        airport,
                                "city": <string> the name of the origin city,
                                "terminal": <int>
                           }
            dest (dict): A dictionary describing the destination of the leg, of
                         the following schema:
                         {
                            "code": <string> the IATA code of the destination
                                    airport,
                            "name": <string> the name of the destination
                                    airport,
                            "city": <string> the name of the destination city,
                            "terminal": <int>
                         }
            dept_time (datetime): The departure date and time, including time
                                  zone.
            arr_time (datetime): The arrival date and time, including time
                                 zone.
            flight (dict): A dictionary describing flight details, of the
                           following schema:
                           {
                                "carrier": <string> the IATA code of the
                                           airline,
                                "number": <string>,
                                "name": <string> the name of the airline
                           }
            aircraft (dict): A dictionary describing the aircraft details, of
                             the following schema:
                             {
                                "code": <string> the IATA code of the aircraft,
                                "name": <string>
                             }
            duration (string): The duration of the leg in minutes.

        Return:
            None.

        """

        self.origin = origin
        self.dest = dest
        self.dept_time = dept_time
        self.arr_time = arr_time
        self.flight = flight
        self.aircraft = aircraft
        self.duration = duration

    def __str__(self):
        """This function defines the pretty printing of the Leg object.

        The output format is similar to the following:
            MU737 from PVG to MEL. DUR: 600. AC: 773.

        Args:
            None.

        Returns:
            None.
        """

        return "{}{} from {} to {}. DUR: {}. AC: {}. DEPT: {}. ARR: {}".format(
                                    self.flight["carrier"],
                                    self.flight["number"],
                                    self.origin["code"],
                                    self.dest["code"],
                                    self.duration,
                                    self.aircraft["code"],
                                    self.dept_time,
                                    self.arr_time)

    def get_origin(self):
        """This function returns the IATA code of the origin of the Leg.

        Args:
            None

        Returns:
            string: The IATA code of the origin of the Leg.

        """
        return self.origin

    def get_dest(self):
        """This function returns the IATA code of the destination of the Leg.

        Args:
            None.

        Returns:
            string: The IATA code of the destination of the Leg.

        """
        return self.dest

    def get_dept_time(self):
        """This function returns the departure date and time of the Leg

        Args:
            None.

        Returns:
            datetime: The departure date and time of the Leg, including
                      time zone offset.

        """
        return self.dept_time

    def get_arr_time(self):
        """This function returns the arrival date and time of the Leg

        Args:
            None.

        Returns:
            datetime: The arrival date and time of the Leg, including
                      time zone offset.

        """
        return self.dept_time

    def get_flight(self):
        """This function returns the flight code of the Leg.

        Args:
            None.

        Returns:
            string: The flight code of the Leg, comprised of the carrier code
                    and flight number. e.g. MU737.

        """
        return self.flight

    def get_aircraft(self):
        """This function returns the IATA aircraft code for this Leg.

        Args:
            None.

        Returns:
            string: The IATA code of the aircraft used on this Leg.

        """
        return self.aircraft

    def get_duration(self):
        """This function returns the duration of this Leg in minutes.

        Args:
            None.

        Returns:
            int: The duration of this Leg in minutes.

        """
        return int(self.duration)
