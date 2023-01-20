from django.urls import path
from . import views

urlpatterns = [
    path(r'', views.create_checkout_session, name='create_checkout_session'),
    path(r'success', views.succeed, name='checkout_succeed'),
    path(r'cancel', views.cancel, name='checkout_cancelled')
]