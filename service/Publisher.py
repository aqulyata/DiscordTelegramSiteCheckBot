from abc import abstractmethod
from typing import TypeVar, Generic

from service.Observer import Observer
# импорт зависимостей
T = TypeVar('T')
# инициализация типа generic


class Publisher(Generic[T]): # описание класса издателя

    @abstractmethod
    def attach(self, observer: Observer[T]) -> None: # метод подписки
        pass

    @abstractmethod
    def detach(self, observer: Observer[T]) -> None: # метод отписки
        pass

    @abstractmethod
    def notify(self, check_res: T) -> None: # метод уведомления
        pass
