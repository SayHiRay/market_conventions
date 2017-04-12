from abc import DayCountConvention
from calendar import monthrange, isleap
from datetime import timedelta, datetime


class DCC30360(DayCountConvention):
    r"""*30/360* Day Count Convention. As defined in 4.16(f) in 2006
    ISDA Definitions.

    Also known as 30/360 US, 30U/360, Bond basis, 30/360 or 360/360.
    The last three terms are the ones used in the 2006 ISDA Definitions.
    This class is a subclass of DayCountConvention.
    See :py:class:`daycountconventions.abc.DayCountConvention` for the
    superclass of this class.

    """
    @property
    def convention_name(self):
        r"""str: A property for the name of the convention.

        This property has a constant value ``30/360``.

        """
        return "30/360"

    @property
    def accrual_factor(self):
        r"""float: A property which gives the accrual factor.

        Notes
        -----
        The computation of accrual factor follows the following formula:

        .. math:: \frac{360(Y_2-Y_1)+30(M_2-M_1)+(D_2-D_1)}{360}

        where the date adjustment rules are the following:

        * If :math:`D_1` is 31, then change :math:`D_1` to 30.
        * If :math:`D_2` is 31 and :math:`D_1` is 30 or 31, then change
          :math:`D_2` to 30.

        """
        self._adjust_dates()
        return (360. * (self._Y2 - self._Y1) + 30. * (self._M2 - self._M1) + self._D2 - self._D1)/360.

    def _adjust_dates(self):
        new_D1 = 30 if self._D1 == 31 else self._D1
        new_D2 = 30 if self._D2 == 31 and (self._D1 == 30 or self._D1 == 31) else self._D2
        self._D1, self._D2 = new_D1, new_D2


class DCC30E360(DayCountConvention):
    r"""*30E/360* Day Count Convention. As defined in 4.16(g) in 2006
    ISDA Definitions.

    Also known as *Eurobond basis*.

    """
    @property
    def convention_name(self):
        r"""str: A property for the name of the convention.

        This property has a constant value ``30E/360``.

        """
        return "30E/360"

    @property
    def accrual_factor(self):
        r"""float: A property which gives the accrual factor.

        Notes
        -----
        The computation of accrual factor follows the following formula:

        .. math:: \frac{360(Y_2-Y_1)+30(M_2-M_1)+(D_2-D_1)}{360}

        where the date adjustment rules are the following:

        * If :math:`D_1` is 31, then change :math:`D_1` to 30.
        * If :math:`D_2` is 31, then change :math:`D_2` to 30.

        """
        self._adjust_dates()
        return (360. * (self._Y2 - self._Y1) + 30. * (self._M2 - self._M1) + self._D2 - self._D1)/360.

    def _adjust_dates(self):
        new_D1 = 30 if self._D1 == 31 else self._D1
        new_D2 = 30 if self._D2 == 31 else self._D2
        self._D1, self._D2 = new_D1, new_D2


class DCC30E360ISDA(DayCountConvention):
    r"""*30E/360 ISDA* Day Count Convention. As defined in 4.16(h) in 2006
    ISDA Definitions.

    Parameters
    ----------
    date_beg : datetime.datetime
        The beginning date considered when computing accrual factor.
    date_end : datetime.datetime
        The end date considered when computing accrual factor.
    termination_date : datetime.datetime
        The termination date considered when computing accrual factor.

    """
    def __init__(self, date_beg, date_end, termination_date):
        super(DCC30E360ISDA, self).__init__(date_beg, date_end)
        self._termination_date = termination_date

    @property
    def convention_name(self):
        r"""str: A property for the name of the convention.

        This property has a constant value ``30E/360 ISDA``.

        """
        return "30E/360 ISDA"

    @property
    def accrual_factor(self):
        r"""float: A property which gives the accrual factor.

        Notes
        -----
        The computation of accrual factor follows the following formula:

        .. math:: \frac{360(Y_2-Y_1)+30(M_2-M_1)+(D_2-D_1)}{360}

        where the date adjustment rules are the following:

        * If :math:`D_1` is 31, then change :math:`D_1` to 30.
        * If :math:`D_2` is the last day of February but not the termination
          date, or `D_2` is 31, then change :math:`D_2` to 30.

        """
        self._adjust_dates()
        return (360. * (self._Y2 - self._Y1) + 30. * (self._M2 - self._M1) + self._D2 - self._D1)/360.

    def _adjust_dates(self):
        new_D1 = 30 if self._D1 == monthrange(self._Y1, self._M1)[1] else self._D1
        new_D2 = 30 if self._D2 == 31 or (self._M2 == 2 and self._D2 == monthrange(self._Y2, self._M2)[1]
                                          and not self._date_equal(self._date_2, self._termination_date)) else self._D2
        self._D1, self._D2 = new_D1, new_D2


class DCC30EP360ISDA(DayCountConvention):
    r"""*30E+/360 ISDA* Day Count Convention. As defined in 4.16(g) in 2006
    ISDA Definitions.

    Also known as *30E+/360*.

    """
    @property
    def convention_name(self):
        r"""str: A property for the name of the convention.

        This property has a constant value ``30E+/360 ISDA``.

        """
        return "30E+/360 ISDA"

    @property
    def accrual_factor(self):
        r"""float: A property which gives the accrual factor.

        Notes
        -----
        The computation of accrual factor follows the following formula:

        .. math:: \frac{360(Y_2-Y_1)+30(M_2-M_1)+(D_2-D_1)}{360}

        where the date adjustment rules are the following:

        * If :math:`D_1` is 31, then change :math:`D_1` to 30.
        * If :math:`D_2` is 31, then change :math:`D_2` to 1 and
          :math:`M_2` to :math:`M_2+1`.

        """
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
    r"""*ACT/360* Day Count Convention. As defined in 4.16(e) in 2006
    ISDA Definitions.

    Also known as *Money Market basis*, *Actual 360*, *French*.

    """
    @property
    def convention_name(self):
        r"""str: A property for the name of the convention.

        This property has a constant value ``ACT/360``.

        """
        return "ACT/360"

    @property
    def accrual_factor(self):
        r"""float: A property which gives the accrual factor.

        Notes
        -----
        The computation of accrual factor follows the following formula:

        .. math:: \frac{d_2-d_1}{360}

        where :math:`d_1` and :math:`d_2` are the beginning date and end
        date considered respectively.

        """
        return (self._date_2 - self._date_1).days/360.


class DCCACT365Fixed(DayCountConvention):
    r"""*ACT/365 Fixed* Day Count Convention. As defined in 4.16(d) in 2006
    ISDA Definitions.

    Also known as *English Money Market basis*.

    """
    @property
    def convention_name(self):
        r"""str: A property for the name of the convention.

        This property has a constant value ``ACT/365 Fixed``.

        """
        return "ACT/365 Fixed"

    @property
    def accrual_factor(self):
        r"""float: A property which gives the accrual factor.

        Notes
        -----
        The computation of accrual factor follows the following formula:

        .. math:: \frac{d_2-d_1}{365}

        where :math:`d_1` and :math:`d_2` are the beginning date and end
        date considered respectively.

        """
        return (self._date_2 - self._date_1).days/365.


class DCCACT365L():
    r"""*ACT/365 L* Day Count Convention. As defined in ICMA Rule 251.1(i).

    Also known as *ACT/365 Leap Year*. This day count convention was originally
    designed for Euro-Sterling floating rate notes. It is used only to compute
    the accrual factor of a coupon.

    Parameters
    ----------
    date_1 : datetime.datetime
        The coupon start date.
    date_2 : datetime.datetime
        The accrual factor date.
    date_3 : datetime.datetime
        The coupon end date.
    coupon_type : {'semi-annual', 'annual'}
        The coupon type considered (The default is 'semi-annual').

    """
    def __init__(self, date_1, date_2, date_3, coupon_type='semi-annual'):
        self._date_1 = date_1
        self._date_2 = date_2
        self._date_3 = date_3
        self.coupon_type = coupon_type

    @property
    def convention_name(self):
        r"""str: A property for the name of the convention.

        This property has a constant value ``ACT/365 L``.

        """
        return "ACT/365 L"

    @property
    def accrual_factor(self):
        r"""float: A property which gives the accrual factor.

        Notes
        -----
        The computation of the factor requires three dates: coupon start
        date :math:`d_1`, accrual factor date :math:`d_2`, and the coupon
        end date :math:`d_3`

        For semi-annual coupons (the type of coupons for which it was
        originally designed for), the accrual factor follows:

        .. math:: \frac{d_2-d_1}{DaysInTheYearOfY_3}

        For annual coupons, the accrual factor follows:

        .. math:: \frac{d_2-d_1}{Denominator}

        where

        .. math::
           Denominator = \begin{cases}
               366 & \text{if 29 February is between $d_1$ (exclusive) and $d_3$ (inclusive)} \\
               365 & \text{otherwise}
           \end{cases}

        """
        if self.coupon_type == 'semi-annual':
            return (self._date_2 - self._date_1).days/(365. + 1*isleap(self._date_3.year))
        elif self.coupon_type == 'annual':
            if isleap(self._date_1.year) and self._date_1 < datetime(self._date_1.year, 2, 29) <= self._date_3:
                denominator = 366.
            elif isleap(self._date_3.year) and self._date_1 < datetime(self._date_3.year, 2, 29) <= self._date_3:
                denominator = 366.
            else:
                denominator = 365.
            return (self._date_2 - self._date_1).days/denominator
        else:
            raise ValueError('The parameter "coupon_type" can only be either "semi-annual" or "annual"')


class DCCACT365A(DayCountConvention):
    r"""*ACT/365 A* Day Count Convention.

    Also known as *ACT/365 Actual*.

    """
    @property
    def convention_name(self):
        r"""str: A property for the name of the convention.

        This property has a constant value ``ACT/365 A``.

        """
        return "ACT/365 A"

    @property
    def accrual_factor(self):
        r"""float: A property which gives the accrual factor.

        Notes
        -----
        The accrual factor follows:

        .. math:: \frac{d_2-d_1}{Denominator}

        where

        .. math::
           Denominator = \begin{cases}
               366 & \text{if 29 February is between $d_1$ (exclusive) and $d_2$ (inclusive)} \\
               365 & \text{otherwise}
           \end{cases}

        """
        if isleap(self._date_1.year) and self._date_1 < datetime(self._date_1.year, 2, 29) <= self._date_2:
            denominator = 366.
        elif isleap(self._date_2.year) and self._date_1 < datetime(self._date_2.year, 2, 29) <= self._date_2:
            denominator = 366.
        else:
            denominator = 365.
        return (self._date_2 - self._date_1).days / denominator


class DCCNL365(DayCountConvention):
    r"""*NL/365* Day Count Convention.

    Also known as *ACT/365 No Leap Year*.

    """
    @property
    def convention_name(self):
        r"""str: A property for the name of the convention.

        This property has a constant value ``NL/365``.

        """
        return "NL/365"

    @property
    def accrual_factor(self):
        r"""float: A property which gives the accrual factor.

        Notes
        -----
        The accrual factor follows:

        .. math:: \frac{Numerator}{365}

        where

        .. math::
           Numerator = \begin{cases}
               d_2-d_1-1 & \text{if 29 February is between $d_1$ (exclusive) and $d_2$ (inclusive)} \\
               d_2-d_1 & \text{otherwise}
           \end{cases}

        """
        if isleap(self._date_1.year) and self._date_1 < datetime(self._date_1.year, 2, 29) <= self._date_2:
            numerator = (self._date_2 - self._date_1).days - 1
        elif isleap(self._date_2.year) and self._date_1 < datetime(self._date_2.year, 2, 29) <= self._date_2:
            numerator = (self._date_2 - self._date_1).days - 1
        else:
            numerator = (self._date_2 - self._date_1).days
        return numerator / 365.


class DCCACTACTISDA(DayCountConvention):
    r"""*ACT/ACT ISDA* Day Count Convention. As defined in definition
    4.16(b) in 2016 ISDA Definitions.

    """
    @property
    def convention_name(self):
        r"""str: A property for the name of the convention.

        This property has a constant value ``ACT/ACT ISDA``.

        """
        return "ACT/ACT ISDA"

    @property
    def accrual_factor(self):
        r"""float: A property which gives the accrual factor.

        Notes
        -----
        The accrual factor follows:

        .. math:: \frac{DaysInNonLeapYears}{365}+\frac{DaysInLeapYears}{366}

        where :math:`DaysInNonLeapYears` represents the number of days in
        non-leap years between :math:`d_1` and :math:`d_2`, and
        :math:`DaysInLeapYears` represents the number of days in leap years
        between :math:`d_1` and :math:`d_2`. When computing these two
        numbers, :math:`d_1` is included, and :math:`d_2` is excluded. For
        example:

        * For :math:`d_1=30-Dec-2010` and :math:`d_2=2-Jan-2011`,
          :math:`DaysInNonLeapYears=3` and :math:`DaysInLeapYears=0`.
        * For :math:`d_1=30-Dec-2011` and :math:`d_2=2-Jan-2012`,
          :math:`DaysInNonLeapYears=2` and :math:`DaysInLeapYears=1`.

        """
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


# class DCCACTACTICMA():
#     def __init__(self):
#         raise NotImplementedError
#
#
# class DCCBusiness252():
#     def __init__(self):
#         raise NotImplementedError
