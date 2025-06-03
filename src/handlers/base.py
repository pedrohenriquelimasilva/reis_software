from abc import ABC, abstractmethod

class BaseHandler(ABC):
    def __init__(self, next_handler=None):
        self._next_handler = next_handler

    @abstractmethod
    def handle(self, request, session):
        pass

    def set_next(self, handler):
        self._next_handler = handler
        return handler