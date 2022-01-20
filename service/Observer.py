from abc import abstractmethod
from typing import TypeVar, Generic

# имортирование зависимотсей

T = TypeVar('T')


# инициализация переменной типа generic

class Observer(Generic[T]): # описание класса подписчика
    @abstractmethod
    def update(self, check_res, loop): # метод при обновлении события 
        ...
