from services.cart_service import Cart
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.reverse import reverse
from django.http.response import HttpResponseRedirect
from .serializers import ItemSerializer
from rest_framework.status import HTTP_422_UNPROCESSABLE_ENTITY


class CartViewSet(ViewSet):

    def list(self, request):
        cart_formed_data = Cart(request.session).get_data()
        context = {
            "items": cart_formed_data["items"],
            "sub_total_price": cart_formed_data["sub_total_price"],
            "items_count": cart_formed_data["items_count"]
        }
        return Response(context)

    @action(detail=False, methods=['POST'], name='Add Item')
    def item(self, request):
        item_serializer = ItemSerializer(data=request.data)
        if item_serializer.is_valid():
            item_data = item_serializer.data
            cart = Cart(request.session)
            cart.add(item_data["product_id"], item_data["count"], item_data["addon_id"])
            return HttpResponseRedirect(redirect_to=reverse('cart-list'))
        return Response(item_serializer.errors, status=HTTP_422_UNPROCESSABLE_ENTITY)

    @item.mapping.delete
    def remove_from_cart(self, request, item_pk):
        cart = Cart(request.session)
        cart.remove_item(item_pk)
        return HttpResponseRedirect(redirect_to=reverse('cart-list'))

    def put(self, request):
        cart = Cart(request.session)
        cart.clear()
        return HttpResponseRedirect(redirect_to=reverse('cart-list'))



