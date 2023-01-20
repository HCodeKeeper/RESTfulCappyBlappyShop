from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Product, Deal, Category, Addon
from django.core.exceptions import ObjectDoesNotExist


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class DiscountSerializer(ModelSerializer):
    class Meta:
        model = Deal
        fields = '__all__'


class AddonSerializer(ModelSerializer):
    class Meta:
        model = Addon
        fields = '__all__'


class DiscountFromProductMixin:
    discount = SerializerMethodField()

    def get_discount(self, obj):
        try:
            discount = Deal.objects.get(product_id=obj.id)
        except ObjectDoesNotExist:
            return None
        return DiscountSerializer(discount).data


class CategoryFromProductMixin:
    category = SerializerMethodField()

    def get_category(self, obj):
        try:
            category = Category.objects.get(id=obj.category_id)
        except ObjectDoesNotExist:
            return None
        return CategorySerializer(category).data


class AddonFromProductMixin:
    addons = SerializerMethodField()

    def get_addons(self, obj):
        try:
            addons = Addon.objects.filter(product_id=obj.id)
        except ObjectDoesNotExist:
            return None
        return AddonSerializer(addons, many=True).data


class ProductPreviewSerializer(ProductSerializer, DiscountFromProductMixin, CategoryFromProductMixin):
    discount = SerializerMethodField()
    category = SerializerMethodField()

    class Meta(ProductSerializer.Meta):
        fields = ['id', 'name', 'rating', 'manufacturer',
                  'price', 'image_src', 'discount', 'category']


class ProductCompoundSerializer(ProductSerializer,
                                DiscountFromProductMixin,
                                CategoryFromProductMixin,
                                AddonFromProductMixin):
    discount = SerializerMethodField()
    category = SerializerMethodField()
    addons = SerializerMethodField()

    class Meta(ProductSerializer.Meta):
        fields = ['id', 'name', 'rating',
                  'manufacturer', 'price', 'image_src',
                  'discount', 'category', 'addons']