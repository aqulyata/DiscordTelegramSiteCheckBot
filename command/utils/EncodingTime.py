class EncoderTime: # класс перевода времени в красивый формат

    def encod(self, time_parametr): # метод превода времени

        remainder_without_nanosec = int(str(time_parametr).split(".")[0]) # перевод времени в удобную структуру данных

        if time_parametr < 3600: # првоерка на количетсво времени

            sec = remainder_without_nanosec % 60 # получение секунд
            minutes = remainder_without_nanosec // 60 # поулчение минут
            result = f"MINUTES:{minutes}  SECONDS:{sec}" # запись результата
            return result

        elif 3600 < time_parametr <= 86400: # проверка
            hour = remainder_without_nanosec // 3600 # получение часов
            remainder_after_hours = remainder_without_nanosec - (hour * 3600) # получение минут
            min = int(remainder_after_hours) // 60 # получение минут
            result = f"HOURS:{hour}  MINUTES:{min}" # запись в результат
            return result

        else:
            day = remainder_without_nanosec // 86400 # получение дней
            remainder_after_day = remainder_without_nanosec - (day * 86400) # получение остатка времени
            hours = remainder_after_day // 3600 # получение часов
            remainder_after_hour = remainder_without_nanosec - ((hours * 3600) + (day * 86400)) # получение остатка минут
            minutes = remainder_after_hour // 60 # получение минут
            result = f" DAY:{day} HOURS:{hours}  MINUTES:{minutes}" # получение результат
            return result
