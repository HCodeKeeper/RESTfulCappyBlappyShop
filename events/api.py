from django.views.decorators.csrf import csrf_exempt
from helpers.datetime_utils import get_current_datetime_with_tz
from services.order_service import fulfill_order
from django.db import transaction
from django.db.utils import DatabaseError
import stripe
from django.http import HttpResponse

endpoint_secret = "whsec_a1f6b7a036ad4eaec4bdad6c2e628b9d45a3038c6a948c1501d353fa06fa8b45"


@csrf_exempt
@transaction.atomic
def checkout_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    if event["type"] == 'checkout.session.completed':
        session = event['data']['object']
        session_id = session['id']
        line_items = stripe.checkout.Session.list_line_items(session_id)
        payment_time_created = event["created"]
        payment_date = get_current_datetime_with_tz(payment_time_created)
        try:
            fulfill_order(session, payment_date, line_items)
        except DatabaseError as e:
            raise e

    # Passed signature verification
    return HttpResponse(status=200)
