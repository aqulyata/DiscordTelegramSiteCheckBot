from abc import ABC, abstractmethod

from Observer import Observer


class Publisher(ABC):

    @abstractmethod
    def attach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def notify(self, check_res) -> None:
        pass
