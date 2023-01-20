from django.core.mail import send_mail
from django.shortcuts import reverse
from smtplib import SMTPException
from cappy_blappy_shop.settings import EMAIL_HOST_USER, DOMAIN


def get_registration_token_html(token):
    html = f'''
<h1>To submit your registration,</h1><p1> click on this <a href="{DOMAIN + reverse("get_token_verification_page")}">link</a></p1>
<h3>And enter this token:</h3><br><h1>{token}</h1>
'''
    return html


def get_password_update_token_html(token):
    html = f'''
<h1>To update your password,</h1>
<h3>And enter this token:</h3><br><h1>{token}</h1>
'''
    return html


def send_registration_token(user_email, token):
    html_message = get_registration_token_html(token)
    try:
        is_sent = bool(send_mail("ClappyBlappyShop: Submit your registration", "",
                                 recipient_list=[user_email], html_message=html_message, from_email=EMAIL_HOST_USER))
    except SMTPException:
        raise
    return is_sent


def send_password_update_token(user_email, token):
    html_message = get_password_update_token_html(token)
    try:
        is_sent = bool(send_mail("ClappyBlappyShop: Complete updating your password", "",
                                 recipient_list=[user_email], html_message=html_message, from_email=EMAIL_HOST_USER))
    except SMTPException:
        raise
    return is_sent
