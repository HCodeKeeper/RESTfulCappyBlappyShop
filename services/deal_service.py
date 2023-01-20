from shop.models import Deal, Product
from decimal import Decimal


def get_random_json():
    return deal_to_json(
        get_random()
    )


def get_random():
    random_deal = Deal.objects.order_by('?').first()
    return random_deal


def deal_to_json(deal):
    return {
        deal.title: f"/product/{deal.product.id}"
    }


def get_discounted_price(product: Product):
    price = Decimal(product.price)
    try:
        discount = Deal.objects.get(product=product)
    except Deal.DoesNotExist:
        pass
    else:
        price -= price * Decimal(int(discount.percents) / 100)
        price = round(price, 2)
    return price
