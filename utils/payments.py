import math
import calendar as cal
import datetime as dt
from dateutil.relativedelta import *

from utils import PAYMENTSPERSCHEDULE, PAYMENTSCHEDULEINCR, DATESTR, dates


def get_payments_per_month(debit_start_date, schedule_type):
    """Get the number of payments per month, used when figuring out how much each payment is"""
    payment_dates_in_month = dates.get_payments_in_month(debit_start_date, schedule_type)
    return len(payment_dates_in_month)


def get_payment_amount(loan, next_payment_date):
    """Get payment amount and round up to nearest cent"""
    monthly_payment_amount = loan['monthly_payment_amount']
    schedule_type = loan['schedule_type']

    payments_per_month = get_payments_per_month(next_payment_date, schedule_type)

    return math.ceil(
        float(
            f"{monthly_payment_amount / payments_per_month:.04f}"
        ) * 100
    ) / 100


