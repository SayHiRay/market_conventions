from abc import DayCountConvention
from calendar import monthrange
from datetime import timedelta


class DCC30360(DayCountConvention):
    @property
    def convention_name(self):
        return "30/360"

    @property
    def accrual_factor(self):
        self._adjust_dates()
        return (360. * (self._Y2 - self._Y1) + 30. * (self._M2 - self._M1) + self._D2 - self._D1)/360.

    def _adjust_dates(self):
        new_D1 = 30 if self._D1 == 31 else self._D1
        new_D2 = 30 if self._D2 == 31 and (self._D1 == 30 or self._D1 == 31) else self._D2
        self._D1, self._D2 = new_D1, new_D2


class DCC30E360(DayCountConvention):
    @property
    def convention_name(self):
        return "30E/360"

    @property
    def accrual_factor(self):
        self._adjust_dates()
        return (360. * (self._Y2 - self._Y1) + 30. * (self._M2 - self._M1) + self._D2 - self._D1)/360.

    def _adjust_dates(self):
        new_D1 = 30 if self._D1 == 31 else self._D1
        new_D2 = 30 if self._D2 == 31 else self._D2
        self._D1, self._D2 = new_D1, new_D2


class DCC30E360ISDA(DayCountConvention):
    def __init__(self, date_beg, date_end, termination_date):
        super(DCC30E360ISDA, self).__init__(date_beg, date_end)
        self._termination_date = termination_date

    @property
    def convention_name(self):
        return "30E/360 ISDA"

    @property
    def accrual_factor(self):
        self._adjust_dates()
        return (360. * (self._Y2 - self._Y1) + 30. * (self._M2 - self._M1) + self._D2 - self._D1)/360.

    def _adjust_dates(self):
        new_D1 = 30 if self._D1 == monthrange(self._Y1, self._M1)[1] else self._D1
        new_D2 = 30 if self._D2 == 31 or (self._M2 == 2 and self._D2 == monthrange(self._Y2, self._M2)[1]
                                          and not self._date_equal(self._date_2, self._termination_date)) else self._D2
        self._D1, self._D2 = new_D1, new_D2


class DCC30EP360ISDA(DayCountConvention):
    @property
    def convention_name(self):
        return "30E+/360 ISDA"

    @property
    def accrual_factor(self):
        self._adjust_dates()
        return (360. * (self._Y2 - self._Y1) + 30. * (self._M2 - self._M1) + self._D2 - self._D1)/360.

    def _adjust_dates(self):
        new_D1 = 30 if self._D1 == 31 else self._D1
        if self._D2 == 31:
            new_date_2 = self._date_2 + timedelta(days=1)
            new_D2, new_M2, new_Y2 = new_date_2.day, new_date_2.month, new_date_2.year
            self._D2, self._M2, self.Y2, self._date_2 = new_D2, new_M2, new_Y2, new_date_2
        self._D1 = new_D1
