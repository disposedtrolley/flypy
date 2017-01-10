
class Trip:
    """This class defines an entire trip, and includes Legs for each
       segment of the trip."""

    def __init__(self, origin, dest, legs, cost, carrier):
        self.origin = origin
        self.dest = dest
        self.legs = []
        self.cost = cost
        self.carrier = carrier
