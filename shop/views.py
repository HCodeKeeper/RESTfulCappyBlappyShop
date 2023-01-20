from rest_framework import viewsets
from .serializers import ProductPreviewSerializer, ProductCompoundSerializer
from .models import Product
from rest_framework.permissions import AllowAny


class CatalogueViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]

    queryset = Product.objects.all()
    serializer_class = ProductPreviewSerializer


class ProductPageViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]

    queryset = Product.objects.all()
    serializer_class = ProductCompoundSerializer
