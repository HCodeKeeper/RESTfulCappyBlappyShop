from django.urls import path
from . import views


urlpatterns = [path(r'', views.ProfileView.as_view(), name="profile")]
