from django.urls import path
from . import views

urlpatterns = [
    path('checkout_succeeded/', views.checkout_webhook, name='api_event_checkout_succeeded')
]
