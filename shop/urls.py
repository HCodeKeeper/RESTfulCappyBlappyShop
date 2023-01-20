from django.urls import include, path
from rest_framework.routers import SimpleRouter
from .views import CatalogueViewSet, ProductPageViewSet
router = SimpleRouter()
router.register(r'products', CatalogueViewSet)
router.register(r'product', ProductPageViewSet)
urlpatterns = router.urls
