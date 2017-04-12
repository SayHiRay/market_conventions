class DayCountConvention(object):
    r"""
    An abstract class containing the most common components of
    frequently used day count conventions.

    Parameters
    ----------
    date_beg : datetime.datetime
        The beginning date considered when computing accrual factor.
    date_end : datetime.datetime
        The end date considered when computing accrual factor.

    """
    def __init__(self, date_beg, date_end):
        self._date_1 = date_beg
        self._date_2 = date_end
        self._D1 = date_beg.day
        self._D2 = date_end.day
        self._M1 = date_beg.month
        self._M2 = date_end.month
        self._Y1 = date_beg.year
        self._Y2 = date_end.year

    @property
    def convention_name(self):
        r"""str: An abstract property for the name of the convention.

        """
        raise NotImplementedError

    @property
    def accrual_factor(self):
        r"""float: An abstract property for the accrual factor.

        """
        raise NotImplementedError

    def _date_equal(self, date_1, date_2):
        if date_1.year == date_2.year and date_1.month == date_2.month and date_1.day == date_2.day:
            return True
        return False
