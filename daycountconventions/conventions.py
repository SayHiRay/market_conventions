from abc import DayCountConvention
from calendar import monthrange, isleap
from datetime import timedelta, datetime
from util import raiseNotDefined


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


class DCCACT360(DayCountConvention):
    @property
    def convention_name(self):
        return "ACT/360"

    @property
    def accrual_factor(self):
        return (self._date_2 - self._date_1).days/360.


class DCCACT365Fixed(DayCountConvention):
    @property
    def convention_name(self):
        return "ACT/365 Fixed"

    @property
    def accrual_factor(self):
        return (self._date_2 - self._date_1).days/365.


class DCCACT365L():
    def __init__(self, date_1, date_2, date_3, coupon_type='semi-annual'):
        self._date_1 = date_1
        self._date_2 = date_2
        self._date_3 = date_3
        self.coupon_type = coupon_type

    @property
    def convention_name(self):
        return "ACT/365 L"

    @property
    def accrual_factor(self):
        if self.coupon_type == 'semi-annual':
            return (self._date_2 - self._date_1).days/(365 + 1*isleap(self._date_3.year))
        elif self.coupon_type == 'annual':
            if isleap(self._date_1) and self._date_1 < datetime(self._date_1.year, 2, 29) < self._date_3:
                denominator = 366.
            elif isleap(self._date_3) and self._date_1 < datetime(self._date_3.year, 2, 29) < self._date_3:
                denominator = 366.
            else:
                denominator = 365.
            return (self._date_2 - self._date_1).days/denominator
        else:
            raise ValueError('The parameter "coupon_type" can only be either "semi-annual" or "annual"')


class DCCACT365A(DayCountConvention):
    @property
    def convention_name(self):
        return "ACT/365 A"

    @property
    def accrual_factor(self):
        if isleap(self._date_1) and self._date_1 < datetime(self._date_1.year, 2, 29) < self._date_2:
            denominator = 366.
        elif isleap(self._date_2) and self._date_1 < datetime(self._date_2.year, 2, 29) < self._date_2:
            denominator = 366.
        else:
            denominator = 365.
        return (self._date_2 - self._date_1).days / denominator


class DCCNL365(DayCountConvention):
    @property
    def convention_name(self):
        return "NL/365"

    @property
    def accrual_factor(self):
        if isleap(self._date_1) and self._date_1 < datetime(self._date_1.year, 2, 29) < self._date_2:
            numerator = (self._date_2 - self._date_1).days - 1
        elif isleap(self._date_2) and self._date_1 < datetime(self._date_2.year, 2, 29) < self._date_2:
            numerator = (self._date_2 - self._date_1).days - 1
        else:
            numerator = (self._date_2 - self._date_1).days
        return numerator / 365.


class DCCACTACTISDA(DayCountConvention):
    @property
    def convention_name(self):
        return "ACT/ACT ISDA"

    @property
    def accrual_factor(self):
        leapyear_days = 0
        nonleapyear_days = 0

        if self._date_1.year < self._date_2.year:
            if isleap(self._date_1.year):
                leapyear_days += (datetime(self._date_1.year, 12, 31) - self._date_1).days + 1
            else:
                nonleapyear_days += (datetime(self._date_1.year, 12, 31) - self._date_1).days + 1
            for year in range(self._date_1.year+1, self._date_2.year):
                if isleap(year):
                    leapyear_days += 366
                else:
                    nonleapyear_days += 365
            if isleap(self._date_2.year):
                leapyear_days += (self._date_2 - datetime(self._date_2.year, 1, 1)).days
            else:
                nonleapyear_days += (self._date_2 - datetime(self._date_2.year, 1, 1)).days
        else:
            if isleap(self._date_1.year):
                leapyear_days += (self._date_2 - self._date_1).days
            else:
                nonleapyear_days += (self._date_2 - self._date_1).days

        return leapyear_days / 366. + nonleapyear_days / 365.


class DCCACTACTICMA():
    def __init__(self):
        raiseNotDefined()


class DCCBusiness252():
    def __init__(self):
        raiseNotDefined()
