from shop.models import Product, Review, Deal, Addon
from django.db.models import Model
from django.http import JsonResponse
from django.core.paginator import Paginator
from services import deal_service


def insert_discount_in_products(products: [Product]):
    for product in products:
        product.discounted_price = deal_service.get_discounted_price(product)


class Context:
    def __init__(self, product, addons, deal):
        self.product = product
        self.addons = addons
        self.deal = deal

    def get_product(self) -> Product:
        return self.product

    def get_addons(self) -> Addon:
        return self.addons

    def get_deal(self) -> Deal:
        return self.deal


# context = everything related to a product page
def get_product_context(product_id) -> Context:
    try:
        product = Product.objects.get(id=product_id)
        addons = Addon.objects.filter(product=product.id)
        try:
            deal = Deal.objects.get(product=product.id)
        except Deal.DoesNotExist:
            deal = Deal()
            deal.percents = 0
        return Context(product, addons, deal)
    except Product.DoesNotExist as e:
        raise e


def get_random_products(quantity):
    products = Product.objects.all()
    if products.count() > quantity:
        products = products[0:quantity]
    return products


def get_products_page(name, page_num):
    items_per_page_count = 8
    paginator = Paginator(get_products(name), items_per_page_count)
    if page_num > paginator.num_pages or page_num < 1:
        raise IndexError("page number is above of existing count")
    return paginator.page(page_num)


def get_products(name):
    products = get_products_by_category_name(name)
    if not products.count():
        products = Product.objects.filter(name__icontains=name).order_by("name")
    return products


def get_products_by_category_name(name):
    return Product.objects.filter(category__name__iexact=name).order_by("category__name")


class Catalogue:

    @staticmethod
    def get_some_random_products() -> JsonResponse:
        products = get_random_products(quantity=20)
        return products


