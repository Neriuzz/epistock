class Event:
    """
    Represents a tuple (E, T) where E is the event type
    and T is the time at which the event occured.
    """

    def __init__(self, symbol, time):
        self.type = symbol
        self.time = time
