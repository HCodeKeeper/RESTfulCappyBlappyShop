class EmptyTemporalRegistrationStorage(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    __doc__ = "Raised when trying to get registration data, although user haven't sent any"