from django.urls import include, path
from django.contrib import admin
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
    path(r'api/', include('shop.urls')),
    path(r'api/auth/', include('authentication.urls')),
    path(r'api/account/', include('accounts.urls')),
    path('api/', include('cart.urls')),
    path('api/checkout/', include('checkout.urls')),
    path('api/event/', include('events.urls')),
    path('api/admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
