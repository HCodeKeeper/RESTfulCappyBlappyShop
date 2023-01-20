from dataclasses import dataclass
from user_profiles.models import Profile
from services.account import get_profile_from_request
import stripe


@dataclass
class CustomerDetails:
    email: str
    name: str
    phone: str

    @staticmethod
    def get_from_db(profile: Profile):
        email = profile.user.email
        first_name = str(profile.first_name or '')
        second_name = str(profile.second_name or '')
        if first_name and second_name:
            name = f"{first_name} {second_name}"
        else:
            name = ''
        tel = profile.telephone
        phone = ''
        if tel:
            phone = tel.number
        return CustomerDetails(email=email, name=name, phone=phone)

    def get_dict(self):
        return {
            "email": self.email,
            "name": self.name,
            "phone": self.phone,
        }


def get_customer(request) -> dict or None:
    if not request.user.is_authenticated:
        return None
    else:
        try:
            profile = get_profile_from_request(request)
            customer_details = CustomerDetails.get_from_db(profile)
            return stripe.Customer.create(email=customer_details.email,
                                          name=customer_details.name,
                                          phone=customer_details.phone,
                                          )
        except Profile.DoesNotExist:
            raise
