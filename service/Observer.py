from abc import abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')


class Observer(Generic[T]):
    @abstractmethod
    def update(self, check_res, loop):
        ...
