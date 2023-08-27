import calendar


class ParkingCalendar:
    def __init__(self):
        self.year = 2023
        self.Calendar = calendar.Calendar()

    def get_days(self, month):
        return self.Calendar.monthdatescalendar(self.year, month)
