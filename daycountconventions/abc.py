from util import raiseNotDefined


class DayCountConvention(object):
    def __init__(self, date_beg, date_end):
        self._date_1 = date_beg
        self._date_2 = date_end
        self._D1 = date_beg.day
        self._D2 = date_end.day
        self._M1 = date_beg.month
        self._M2 = date_end.month
        self._Y1 = date_beg.year
        self._Y2 = date_end.year

    def convention_name(self):
        raiseNotDefined()

    def accrual_factor(self):
        raiseNotDefined()

    def _date_equal(self, date_1, date_2):
        if date_1.year == date_2.year and date_1.month == date_2.month and date_1.day == date_2.day:
            return True
        return False
