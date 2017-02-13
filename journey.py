
class Journey:
    """This class defines a particular journey within a Trip. Trips typically
    have either a single journey (for a one-way ticket), and two journeys for
    a return fare.
    """

    def __init__(self, slice_data):
        """Initialises the Journey object.

        Args:
            slice_data (dict): a dictionary representing the JSON object of
                               a slice in the parent Trip.

        Returns:
            None.
        """
        self.slice_data = slice_data
