from abc import ABC, abstractmethod

class RandBase(ABC):

    @abstractmethod
    def generate(self): pass

class RandDeterministic(RandBase):
    def __init__(self, number):
        self.__number = number

    def generate(self):
        return self.__number
