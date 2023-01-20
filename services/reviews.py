import django.core.paginator
from django.core.paginator import Paginator, EmptyPage
from shop.models import Review
from services.user import get_name_by_id
from django.core.exceptions import MultipleObjectsReturned
from django.contrib.auth.models import User
import json


def get_reviews(product_id, page):
    per_request_items = 8
    try:
        reviews = Review.objects.filter(product_id=product_id).order_by("upvotes")
    except Review.DoesNotExist or EmptyPage:
        return {"reviews": []}
    else:
        paginator = Paginator(reviews, per_request_items)
        _page = paginator.page(page)
        next_page = 1
        previous_page = 1
        paginated_reviews = _page.object_list
        if _page.has_next():
            next_page = _page.next_page_number()
        if _page.has_previous():
            previous_page = _page.previous_page_number()
        try:
            _dict = {
                "current_page": _page.number,
                "next_page": next_page,
                "previous_page": previous_page,
                "last_page": paginator.num_pages,
                "reviews":
                    [{
                    "user":{"name": get_name_by_id(review_obj.id)},
                    "rating": review_obj.rating,
                    "self": review_obj.text}
                    for review_obj in paginated_reviews]
            }
        except User.DoesNotExist or MultipleObjectsReturned:
            raise
        return _dict


def add_review(product_id):
    pass