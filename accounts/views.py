import jwt
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import HttpResponseBadRequest
from django.urls import reverse_lazy
from services.account import *
from cappy_blappy_shop.settings import SECRET_KEY
from helpers.validators import validate_phone_number
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, reverse, render
from django.views.decorators.cache import cache_page
from rest_framework import generics
from user_profiles.models import Profile
from .serializers import ProfileSerializer
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED


@login_required(login_url=reverse_lazy('login_page'))
def account(request):
    username = request.user.get_username()
    try:
        profile = Profile.objects.get(user__username=username)
    except Profile.DoesNotExist:
        # will also logout you from admin site
        return redirect(reverse('logout'))
    telephone_number = profile.telephone.number if profile.telephone else 'Not set'
    return render(request, 'account.html', context={
        "first_name": profile.first_name,
        "second_name": profile.second_name,
        "email": profile.email,
        "premium_active": profile.has_premium,
        "telephone": telephone_number
    })


@login_required(login_url=reverse_lazy('login_page'))
@cache_page(15*60)
def get_edit_profile_page(request):
    return render(request, "change_profile_credits.html")


@login_required(login_url=reverse_lazy('login_page'))
def edit_profile(request):
    if request.method == 'POST':
        profile = get_profile_from_request(request)
        first_name = request.POST.get("first_name")
        second_name = request.POST.get("second_name")
        telephone = request.POST.get("telephone")
        if telephone and not validate_phone_number(telephone):
            return HttpResponseBadRequest("Your telephone number is invalid", content_type="text/plain")
        update_profile(profile, first_name, second_name, telephone)

        return redirect(reverse('account'))
    return HttpResponseBadRequest()


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer

    def get_object(self):
        try:
            jwt_authenticator = JWTAuthentication()
            user, _ = jwt_authenticator.authenticate(self.request)
        except jwt.ExpiredSignatureError:
            raise
        except KeyError:
            raise
        except TypeError:
            raise
        try:
            return Profile.objects.get(user=user)
        except ObjectDoesNotExist:
            raise

