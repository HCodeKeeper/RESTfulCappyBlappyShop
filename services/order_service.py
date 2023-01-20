from shop.models import Order, OrderItem, Product, Addon, DOESNT_EXIST_ID
from helpers.checkout import int_to_price
from django.db.utils import DatabaseError, ConnectionDoesNotExist
from django.core.exceptions import ObjectDoesNotExist
from typing import List


class StripeProduct:
    def __init__(self, product, count, addon, unit_price):
        self.product = product
        self.count = count
        self.addon = addon
        self.unit_price = unit_price

    @staticmethod
    def create_with_line_item(line_item):
        count = line_item["quantity"]
        unit_price = int_to_price(line_item["price"]["unit_amount"])
        product_id = line_item["price"]["metadata"]["self_id"]
        addon_id = line_item["price"]["metadata"]["addon_id"]
        try:
            product = Product.objects.get(id=product_id)
            addon = None
            if addon_id != DOESNT_EXIST_ID:
                addon = Addon.objects.get(id=addon_id)
        except (ObjectDoesNotExist, ConnectionDoesNotExist):
            raise
        except DatabaseError:
            raise

        return StripeProduct(product, count, addon, unit_price)

    def add_to_db(self, order):
        order_item = OrderItem(
            product=self.product,
            addon=self.addon,
            quantity=self.count,
            unit_price=self.unit_price,
            order=order
        )
        order_item.save()


class StripeOrder:
    def __init__(self, products: List[StripeProduct], user_email: str, payment_date, total_price):
        self.payment_date = payment_date
        self.products = products
        self.email = user_email
        self.total_price = total_price

    @staticmethod
    def create_with_session(session, payment_date, line_items):
        user_email = session["customer_details"]["email"]
        products = []
        total_price = int_to_price(session["amount_total"])

        for item in line_items:
            product = StripeProduct.create_with_line_item(item)
            products.append(product)

        return StripeOrder(products, user_email, payment_date, total_price)

    def add_to_db(self):
        order = Order(
            creation_date=self.payment_date,
            email=self.email,
            price=self.total_price
            )
        order.save()
        for order_item in self.products:
            order_item.add_to_db(order)


def fulfill_order(session, payment_date, line_items):
    stripe_order = StripeOrder.create_with_session(session, payment_date, line_items)
    try:
        stripe_order.add_to_db()
    except DatabaseError as e:
        raise e
