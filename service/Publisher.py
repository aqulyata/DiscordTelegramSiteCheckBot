from abc import abstractmethod
from typing import TypeVar, Generic

from service.Observer import Observer

T = TypeVar('T')


class Publisher(Generic[T]):

    @abstractmethod
    def attach(self, observer: Observer[T]) -> None:
        pass

    @abstractmethod
    def detach(self, observer: Observer[T]) -> None:
        pass

    @abstractmethod
    def notify(self, check_res: T) -> None:
        pass
