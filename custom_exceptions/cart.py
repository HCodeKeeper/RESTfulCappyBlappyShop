class EmptyCartException(Exception):
    def __int__(self):
        super().__init__()

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    __doc__ = "Raised when a user tries to checkout with empty cart"
