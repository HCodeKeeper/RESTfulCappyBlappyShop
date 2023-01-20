from django.urls import include, path
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register(r'cart', views.CartViewSet, basename='cart')

urlpatterns = router.urls

