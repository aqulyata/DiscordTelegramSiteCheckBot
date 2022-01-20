from enum import Enum


class SiteState(Enum):  # описание класса enum для состояния сайтов
    NOT_READY = 0  # статус неработоспособности
    READY = 1  # cтатус работоспособности
    UNDEFINDED = 2  # неопрделенный статус сайта
