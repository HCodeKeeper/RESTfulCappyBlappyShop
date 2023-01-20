from django.urls import include, path
from . import views

urlpatterns = [
    path('login/', views.get_login_page, name="login_page"),
    path('register/', views.get_registration_page, name="registration_page"),
    path('register/email_user', views.register_email, name='register_email'), # #!why its not usable with slash
    path('register/verificate/perform', views.verificate, name='verificate'),
    path('register/verificate/', views.get_token_verification_page, name='get_token_verification_page'),
    path('login/perform/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('update_password/verify_email', views.update_password_email, name="update_password_verify_email"),
    path('update_password/credits', views.update_password, name="update_password_credits"),
    path('update_password/perform', views.update_password_perform, name="update_password_perform"),
]
