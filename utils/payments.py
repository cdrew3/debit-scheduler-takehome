import math
import calendar as cal
import datetime as dt
from dateutil.relativedelta import *

from utils import PAYMENTSPERSCHEDULE, PAYMENTSCHEDULEINCR, DATESTR, dates


def get_payments_per_month(debit_start_date, schedule_type):
    payment_dates_in_month = dates.get_payments_in_month(debit_start_date, schedule_type)
    return len(payment_dates_in_month)

def get_payments_per_month2(debit_start_date, schedule_type):
    # Easy case
    if schedule_type.lower() == "monthly":
        return 1

    # Get number of days in the month and the 1st weekday_number of the month
    dow, days_in_month = cal.monthrange(debit_start_date.year, debit_start_date.month)

    # Short circuit easy case
    if days_in_month <= 28:
        return PAYMENTSPERSCHEDULE[schedule_type]

    # Create array of 1-3 dates where if a payment occurs it would mean an extra payment that month
    possible_5_dow_dates = [dt.datetime(debit_start_date.year, debit_start_date.month, i+1) for i in range(days_in_month-28)]

    # Stay in the same month
    payment_month = debit_start_date.month
    print(debit_start_date.month, possible_5_dow_dates)
    while debit_start_date.month == payment_month:
        print(debit_start_date.month, payment_month)
        debit_start_date -= relativedelta(weeks=PAYMENTSCHEDULEINCR[schedule_type]) # Decrement payment start date by the scheduled payment increment

        # Add 1 extra payment to normal number if a payment date lands
        # on any of the days of the month where 5 days of that week would occur
        if debit_start_date in possible_5_dow_dates:
            return PAYMENTSPERSCHEDULE[schedule_type] + 1

    return PAYMENTSPERSCHEDULE[schedule_type]


# Round cent up from 4 decimal places
def get_payment_amount(loan, next_payment_date):
    monthly_payment_amount = loan['monthly_payment_amount']
    schedule_type = loan['schedule_type']

    payments_per_month = get_payments_per_month(next_payment_date, schedule_type)

    return math.ceil(
        float(
            f"{monthly_payment_amount / payments_per_month:.04f}"
        ) * 100
    ) / 100


