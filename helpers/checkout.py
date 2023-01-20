import decimal

from services.cart_service import Cart, get_data_for_checkout
import stripe
from django.urls import reverse
from shop.models import DOESNT_EXIST_ID
from cappy_blappy_shop.settings import DOMAIN


def price_to_int(price):
    return int(price*100)


def int_to_price(value):
    return value/100


def generate_product_line(request):
    cart = Cart(request.session)
    raw_products = list()
    items_for_checkout = get_data_for_checkout(cart.session_cart)["items"]
    for product_data in items_for_checkout.values():
        raw_products.append(product_data.values())

    line_products = []
    for product, count, addon, discounted_price in raw_products:
        addon_price = 0
        product_name = product.name
        if addon.id != DOESNT_EXIST_ID:
            product_name += f" + {addon.name}"
            addon_price = addon.price
        metadata = {"self_id": product.id, "addon_id": addon.id}
        try:
            price = stripe.Price.create(
                currency="usd", unit_amount=price_to_int(decimal.Decimal(discounted_price) + addon_price),
                product_data={"name": product_name, "metadata": metadata},
                metadata=metadata
            )
        except stripe.error.StripeError:
            raise
        else:
            line_products.append(
                {
                    "price": price.stripe_id,
                    "quantity": count
                }
            )

    return line_products


def create_session(request):
    session = stripe.checkout.Session.create(
        line_items=generate_product_line(request),
        mode='payment',
        success_url=DOMAIN + reverse('checkout_succeed'),
        cancel_url=DOMAIN + reverse('checkout_cancelled'),
    )
    return session
