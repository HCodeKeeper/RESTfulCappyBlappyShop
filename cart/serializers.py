from rest_framework import serializers
from django.db import models
from shop.models import Product, Addon


# Workaround  for ItemSerializer. Doesn't really appear in the database
class Item:
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    addon_id = models.ForeignKey(Addon, on_delete=models.CASCADE)
    count = models.IntegerField()


class ItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    addon_id = serializers.IntegerField()
    count = serializers.IntegerField()
