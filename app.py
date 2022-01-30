import json
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound

from utils import validation, payments, dates, DATESTR

class App(object):

    def __init__(self):
        self.url_map = Map(
            [
                Rule("/", endpoint=""),
                Rule("/get_next_debit", endpoint="get_next_debit")
            ]
        )


    def dispatch_request(self, request):
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            return getattr(self, f"on_{endpoint}")(request, **values)
        except NotFound:
            return self.error_404()
        except HTTPException as e:
            return e

    def on_get_next_debit(self, request):
        body = request.get_json()
        response = {}

        try:
            # Basic checks for input
            if not validation.input_valid(body):
                response = { "Error": "Invalid input detected.  Check logs for details" }
            else:
                next_payment_date = dates.get_next_payment_date(body['loan']) # get expected next payment date
                payment_amount = payments.get_payment_amount(body['loan'], next_payment_date) # get amount based on this original date

                # Pushes out payment date until next business day if next_payment_date is a holiday
                # Does not impact payment amount
                next_payment_date = dates.handle_holidays(next_payment_date, body['loan']['schedule_type'])

                response = {
                    "debit": {
                        "amount": payment_amount,
                        "date": next_payment_date.strftime(DATESTR)
                    }
                }

        except Exception as exc:
            err_msg = "Unable to return next debit information.  See logs for details."
            response = {"ERROR": err_msg}

        return Response(json.dumps(response), mimetype='application/json')

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)
        response = {}

        if body is None:
            response = { "Error": "No JSON body provided" }
        elif not validation.input_valid(body):
            response = { "Error": "Invalid input detected.  Check logs for details" }
        else:
            next_payment_date = dates.get_next_payment_date(body['loan'])

        ##############
        # START HERE #
        ##############


        return Response(json.dumps(response), mimetype='application/json')


    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)


    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)


def create_app():
    app = App()
    return app


if __name__ == '__main__':
    from werkzeug.serving import run_simple

    app = create_app()
    run_simple('0.0.0.0', 5000, app, use_debugger=True, use_reloader=True)
