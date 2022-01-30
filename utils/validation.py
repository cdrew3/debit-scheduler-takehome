from utils import VALIDSCHEDULETYPES

def input_valid(body):
    errs = []
    warns = []

    if body is None:
        print("ERROR: Loan body is empty")
        return False

    if "loan" not in body:
        errs.append("ERROR: Missing 'loan' from request body")

    err_keys = [
        "monthly_payment_amount",
        "schedule_type",
        "debit_start_date",
        "debit_day_of_week"
    ]

    for err_key in err_keys:
        if err_key not in body['loan']:
            errs.append(f"ERROR: Missing required key ({err_key}) from loan body")

    if 'schedule_type' in body['loan'] and body['loan']['schedule_type'] not in VALIDSCHEDULETYPES:
        errs.append(f"ERROR: The schedule type provided ({body['loan']['schedule_type']}) is not valid.  Please use one of the following: {', '.join(VALIDSCHEDULETYPES)}")

    warn_keys = [
        "payment_due_day"
    ]

    for warn_key in warn_keys:
        if warn_key not in body['loan']:
            warns.append(f"WARNING: Missing key ({warn_key}) from loan body")

    if len(warns) > 0: print("\n".join(warns))

    if len(errs) > 0:
        print("\n".join(errs))
        return False

    return True

