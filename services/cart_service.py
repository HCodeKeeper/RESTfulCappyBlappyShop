import decimal

from django.http import HttpRequest
from shop.models import Product, Addon, Deal, DOESNT_EXIST_ID
from services.deal_service import get_discounted_price


class Cart:
    def __init__(self, session):
        self.session = session
        if not self.__assert_cart_exists():
            self.__insert_cart_in_session()
        self.session_cart: dict = self.session["cart"]

    def add(self, product_id, count: int, addon_id=DOESNT_EXIST_ID):
        self.session_cart[product_id] = {"self": product_id, "count": count, "addon_id": addon_id}
        self.session.modified = True

    def set(self, product_id, count: int = None, addon_id=None):
        if count is not None:
            self.session_cart[product_id]["count"] = count
        if addon_id is not None:
            self.session_cart[product_id]["addon_id"]

    def update_multiple_count(self, id_counts: [str, int]):
        for entry in id_counts:
            self.session_cart[entry[0]]["count"] = entry[1]
        self.session.modified = True

    def get_data(self) -> dict:
        items = {}
        items_count = 0
        sub_total_price = 0
        for product_id in self.session_cart.values():
            product_items_price = 0
            product = Product.objects.get(id=product_id["self"])
            addon = None
            if product_id["addon_id"] != DOESNT_EXIST_ID:
                addon = Addon.objects.get(id=product_id["addon_id"])
                product_items_price += decimal.Decimal(addon.price)
            else:
                addon = Addon(id=DOESNT_EXIST_ID, product=product)
            count = product_id["count"]
            items_count += int(count)
            product_discounted_price = get_discounted_price(product)
            product_items_price += product_discounted_price * int(count)
            sub_total_price += product_items_price
            items[product_id["self"]] = {
                "self": {"id": product.id, "name": product.name, "price": product.price},
                "count": count,
                "addon": {"id": addon.id, "name": addon.name, "price": addon.price},
                "product_discounted_price": product_discounted_price
            }
        return {"items": items, "sub_total_price": sub_total_price, "items_count": items_count}

    def has_any(self):
        return bool(len(self.session_cart))

    def remove_item(self, product_id):
        self.session_cart.pop(product_id)
        self.session.modified = True

    def remove_addon(self, product_id):
        self.session_cart[product_id]["addon_id"] = "-1"

    def clear(self):
        self.__insert_cart_in_session()

    def __assert_cart_exists(self):
        cart = self.session.get("cart", None)
        if cart is None:
            return False
        return True

    def item_exists(self, product_id):
        return bool(self.session_cart.get(product_id, False))

    def __insert_cart_in_session(self):
        self.session["cart"] = {}


# Deprecated method from cart which is used to form stripe products
def get_data_for_checkout(session_cart) -> dict:
    items = {}
    items_count = 0
    sub_total_price = 0
    for product_id in session_cart.values():
        product_items_price = 0
        product = Product.objects.get(id=product_id["self"])
        addon = None
        if product_id["addon_id"] != DOESNT_EXIST_ID:
            addon = Addon.objects.get(id=product_id["addon_id"])
            product_items_price += decimal.Decimal(addon.price)
        else:
            addon = Addon(id=DOESNT_EXIST_ID, product=product)
        count = product_id["count"]
        items_count += int(count)
        product_discounted_price = get_discounted_price(product)
        product_items_price += product_discounted_price * int(count)
        sub_total_price += product_items_price
        items[product_id["self"]] = {
            "self": product,
            "count": count,
            "addon": addon,
            "product_discounted_price": product_discounted_price
        }
    return {"items": items, "sub_total_price": sub_total_price, "items_count": items_count}