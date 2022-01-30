import holidays


DATESTR = "%Y-%m-%d"

VALIDSCHEDULETYPES = [
    'monthly',
    'biweekly',
    'weekly'
]

PAYMENTSPERSCHEDULE = {
    "monthly": 1,
    "biweekly": 2,
    "weekly": 4
}

PAYMENTSCHEDULEINCR = {
    "monthly": 4,
    "biweekly": 2,
    "weekly": 1
}

BANKINGHOLIDAYNAMES = [
    "New Year's Day",
    "Martin Luther King Jr. Day",
    "Washington's Birthday",
    "Memorial Day",
    "Juneteenth National Independence Day",
    "Independence Day",
    "Labor Day",
    "Columbus Day",
    "Veterans Day",
    "Thanksgiving Day",
    "Christmas Day",
]

