class ProfileAlreadyExistException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    __doc__ = "Is raised when trying to add Profile to User, although it already has a Profile attached"
