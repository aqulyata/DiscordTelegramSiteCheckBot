from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar('T')


class Observer(Generic[T]):
    @abstractmethod
    def update(self, check_res, loop):
        ...
