
class AbstractHandler:
    def __init__(self):
        self.next: AbstractHandler = None

    def set_next(self, handler):
        self.next = handler
        return self

    def has_next(self):
        return self.next is not None

    def try_next(self):
        if self.has_next():
            return self.next.handle()

    def handle(self):
        pass
