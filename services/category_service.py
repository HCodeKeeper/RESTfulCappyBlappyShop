from shop.models import Category


def get_categories(path) -> dict:
    categories_dict = {}
    for category in Category.objects.all():
        link = path + category.name
        categories_dict[category.name] = link
    return categories_dict
