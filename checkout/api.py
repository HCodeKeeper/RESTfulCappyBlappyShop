from django.shortcuts import redirect
from django.urls import reverse
from rest_framework.reverse import reverse
import stripe
from rest_framework.permissions import AllowAny

from services.cart_service import Cart
from cappy_blappy_shop.settings import DOMAIN
from helpers.checkout import generate_product_line
from rest_framework.decorators import api_view, permission_classes
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_400_BAD_REQUEST
from rest_framework.response import Response


@api_view(['POST'])
@permission_classes([AllowAny])
def create_checkout_session(request):
    cart = Cart(request.session)

    if not cart.has_any():
        return Response({"Exception": "Your cart is empty. Checkout is impossible"}, HTTP_400_BAD_REQUEST)
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=generate_product_line(request),
            mode='payment',
            success_url=DOMAIN + reverse('checkout_success'),
            cancel_url=DOMAIN + reverse('checkout_cancel'),
        )
    except Exception as e:
        raise e
        return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'Proceed to checkout in a browser': checkout_session.url})
