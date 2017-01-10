
class Leg:
    """This class defines a particular Leg of a Trip."""
    def __init__(self,
                 origin,
                 dest,
                 departureTime,
                 arrivalTime,
                 flight,
                 aircraft,
                 duration):
        self.origin = origin
        self.dest = dest
        self.departureTime = departureTime
        self.arrivalTime = arrivalTime
        self.flight = flight
        self.aircraft = aircraft
        self.duration = duration
