from abc import ABC, abstractmethod

class BaseDecorator(ABC):
    def __init__(self, mediator, show_data_func):
        self._mediator = mediator
        self._show_data_func = show_data_func

    @abstractmethod
    def __call__(self):
        pass