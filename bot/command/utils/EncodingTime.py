class EncoderTime:

    def __init__(self) -> None:
        super().__init__()

    def encod(self, time_parametr):
        remainder_without_nanosec = int(str(time_parametr).split(".")[0])

        if time_parametr < 3600:

            sec = remainder_without_nanosec % 60
            minutes = remainder_without_nanosec // 60
            result = f"MINUTES:{minutes}  SECONDS:{sec}"
            return result
        elif time_parametr > 3600 and time_parametr <= 86400:
            hour = remainder_without_nanosec // 3600
            remainder_after_hours = remainder_without_nanosec - (hour * 3600)
            min = int(remainder_after_hours) // 60
            result = f"HOURS:{hour}  MINUTES:{min}"
            return result
        else:
            day = remainder_without_nanosec // 86400
            remainder_after_day = remainder_without_nanosec - (day * 86400)
            hours = remainder_after_day // 3600
            remainder_after_hour = remainder_without_nanosec - ((hours * 3600) + (day * 86400))
            minutes = remainder_after_hour // 60
            result = f" DAY:{day} HOURS:{hours}  MINUTES:{minutes}"
            return result

