from smtplib import SMTPException

from django.contrib.auth.models import User
from django.db.utils import DatabaseError
from django.contrib.auth import login as login_user
from django.contrib.auth import authenticate
from django.core.paginator import Paginator
from . import mailing
from .session import RegistrationData, TemporalRegistrationStorage
from user_profiles.models import Profile, Telephone
from custom_exceptions.account import ProfileAlreadyExistException
from django.core.exceptions import ObjectDoesNotExist
from helpers.responsibilit_chain import AbstractHandler


def login(request, username, password):
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login_user(request, user)
        return True
    return False


def register(registration_data: RegistrationData):
    add_user_to_db(registration_data)
    user = lookup_user(registration_data.email)
    if user is None:
        raise ObjectDoesNotExist()
    add_profile_to_user(user)


def add_user_to_db(registration_data: RegistrationData):
    try:
        User.objects.create_user(registration_data.username, registration_data.email, registration_data.password)
    except DatabaseError:
        raise


def add_profile_to_user(user: User):
    try:
        Profile.objects.create(email=user.email, user=user)
    except DatabaseError as e:
        raise ProfileAlreadyExistException(
            "Tried to attach profile to user who already has another profile attached, or has same telephone number as another profile( Telephone table)"
        ) from e


def lookup_user(email: str):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = None
    return user


def update_password(email, password):
    user = lookup_user(email)
    if user is None:
        raise DatabaseError("User with this email doesn't exist")
    else:
        user.set_password(password)


def get_profile_from_request(request):
    username = request.user.get_username()
    try:
        profile = Profile.objects.get(user__username=username)
    except Profile.DoesNotExist:
        raise
    return profile


def add_telephone_with_profile(profile: Profile, number):
    try:
        telephone = Telephone.objects.get(profile=profile)
        telephone.number = number
        telephone.save()
    except Telephone.DoesNotExist:
        telephone = Telephone.objects.create(number=number, user=profile.user)
        profile.telephone = telephone
        profile.save()


def update_profile(profile: Profile, first_name, second_name, telephone):
    if first_name:
        profile.first_name = first_name
    if second_name:
        profile.second_name = second_name
    profile.save()
    if telephone:
        add_telephone_with_profile(profile, telephone)


class RegistrationCreditsCachingHandler(AbstractHandler):
    def __init__(self, request, email, username, password, token):
        super().__init__()
        self.request = request
        self.email = email
        self.username = username
        self.password = password
        self.token = token

    def handle(self):
        storage = TemporalRegistrationStorage(self.request)
        storage.put(self.email, self.username, self.password, self.token)
        self.try_next()


class RegistrationTokenSendingHandler(AbstractHandler):
    def __init__(self, email, token):
        super().__init__()
        self.email = email
        self.token = token

    def handle(self):
        try:
            mailing.send_registration_token(self.email, self.token)
        except SMTPException:
            raise
        else:
            self.try_next()