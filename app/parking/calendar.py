import calendar


class ParkingCalendar:
    def __init__(self):
        self.Calendar = calendar.Calendar()

    def get_days(self, month, year):
        return self.Calendar.monthdatescalendar(year, month)
