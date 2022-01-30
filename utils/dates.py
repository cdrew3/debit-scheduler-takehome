import datetime as dt
from dateutil.relativedelta import *
import calendar as cal
import holidays

from utils import PAYMENTSPERSCHEDULE, PAYMENTSCHEDULEINCR, DATESTR, BANKINGHOLIDAYNAMES


# Get number of payments in a month to determine how much each payment should be
def get_payments_in_month(debit_start_date, schedule_type):
    """Get all payments in a month in an array"""

    payment_dates = []
    if schedule_type.lower() == "monthly":
        payment_dates.append(debit_start_date)
    else:

        # Capture month of payments and go to last payment of previous month
        this_month = debit_start_date.month
        while debit_start_date.month == this_month:
            debit_start_date -= relativedelta(weeks=PAYMENTSCHEDULEINCR[schedule_type])

        # Increment by one payment to get first payment of this month
        debit_start_date += relativedelta(weeks=PAYMENTSCHEDULEINCR[schedule_type])
        while debit_start_date.month == this_month:
            payment_dates.append(debit_start_date) # Add payment to list
            debit_start_date += relativedelta(weeks=PAYMENTSCHEDULEINCR[schedule_type]) # increment by schedule type

    return payment_dates


def validate_start_date(start_date, day_of_week):
    """Verify dates and days passed in make sense.  Doesn't try to assume anything if things don't match up."""

    errs = []
    start_date = dt.datetime.strptime(start_date, "%Y-%m-%d")
    start_date_day_num = start_date.weekday()
    start_date_day_str = list(cal.day_name)[start_date.weekday()]

    if start_date_day_num in [5,6]:
        errs.append(f"ERROR: Start date ({start_date.strftime(DATESTR)})( falls on a {start_date_day_str}.  It must fall during a weekday.")

    if start_date_day_str.lower() != day_of_week.lower():
        errs.append(f"ERROR: Provided start day ({day_of_week.title()}) does not match calculated day of start date ({start_date.strftime(DATESTR)} - {start_date_day_str.title()})")

    if len(errs) > 0:
        print("\n".join(errs))
        raise Exception("Input errors detected")


def handle_holidays(debit_start_date, schedule_type):
    """Check if debit date falls on a holiday and move it to next business day"""

    # Get all banking holiday dates
    banking_holiday_dates = [date for date, name in holidays.US(years=debit_start_date.year).items() if name.replace(" (Observed)", "") in BANKINGHOLIDAYNAMES]

    # Pause payment until next business day
    while debit_start_date.date() in banking_holiday_dates or debit_start_date.weekday() in [5, 6]:
        debit_start_date += relativedelta(days=1)

    return debit_start_date


def get_next_payment_date(loan):
    """
    High level function for calculating the next debit date
    """

    debit_start_date = loan['debit_start_date']
    debit_day_of_week = loan['debit_day_of_week']
    schedule_type = loan['schedule_type']

    validate_start_date(debit_start_date, debit_day_of_week)

    # Calculate increment based on schedule type
    td_incr = relativedelta(months=1)
    if "weekly" in schedule_type:
        td_incr = relativedelta(weeks=PAYMENTSCHEDULEINCR[schedule_type])

    debit_start_date = dt.datetime.strptime(debit_start_date, "%Y-%m-%d")

    # Move start date up to be in the future while keeping payment day of week and weekly increments correct
    todays_date = dt.datetime.today()
    while debit_start_date <= todays_date:
        debit_start_date += td_incr

    #debit_start_date = handle_holidays(debit_start_date, schedule_type)
    return debit_start_date

