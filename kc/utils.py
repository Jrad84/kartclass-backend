from __future__ import unicode_literals
from django.contrib.auth import authenticate
from kc.users.models import CustomUser
import os
import random
from rest_framework.exceptions import AuthenticationFailed
import datetime
import decimal
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import timezone


def send_email(data):
    
    email = EmailMessage(subject=data['email_subject'], 
                body=data['email_body'], to=data['to_email'])
    email.send()

def generate_username(name):

    username = "".join(name.split(' ')).lower()
    if not CustomUser.objects.filter(username=username).exists():
        return username
    else:
        random_username = username + str(random.randint(0, 1000))
        return generate_username(random_username)

def register_social_user(provider, user_id, email, name):
    filtered_user_by_email = CustomUser.objects.filter(email=email)

    if filtered_user_by_email.exists():

        if provider == filtered_user_by_email[0].auth_provider:

            registered_user = authenticate(
                email=email, password=os.environ.get('SOCIAL_SECRET'))

            return {
                'username': registered_user.username,
                'email': registered_user.email,
                'tokens': registered_user.tokens()}

        else:
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

    else:
        user = {
            'username': generate_username(name), 'email': email,
            'password': os.environ.get('SOCIAL_SECRET')}
        user = CustomUser.objects.create_user(**user)
        user.is_verified = True
        user.auth_provider = provider
        user.save()

        new_user = authenticate(
            email=email, password=os.environ.get('SOCIAL_SECRET'))
        return {
            'email': new_user.email,
            'username': new_user.username,
            'tokens': new_user.tokens()
        }

def convert_tstamp(response, field_name=None):
    tz = timezone.utc if settings.USE_TZ else None

    if field_name and response.get(field_name):
        return datetime.datetime.fromtimestamp(
            response[field_name],
            tz
        )
    if response is not None and not field_name:
        return datetime.datetime.fromtimestamp(
            response,
            tz
        )


# currencies those amount=1 means 100 cents
# https://support.stripe.com/questions/which-zero-decimal-currencies-does-stripe-support
ZERO_DECIMAL_CURRENCIES = [
    "bif", "clp", "djf", "gnf", "jpy", "kmf", "krw",
    "mga", "pyg", "rwf", "vuv", "xaf", "xof", "xpf",
]


def convert_amount_for_db(amount, currency="aud"):
    if currency is None:  # @@@ not sure if this is right; find out what we should do when API returns null for currency
        currency = "aud"
    return (amount / decimal.Decimal("100")) if currency.lower() not in ZERO_DECIMAL_CURRENCIES else decimal.Decimal(amount)


def convert_amount_for_api(amount, currency="aud"):
    if currency is None:
        currency = "aud"
    return int(amount * 100) if currency.lower() not in ZERO_DECIMAL_CURRENCIES else int(amount)


def update_with_defaults(obj, defaults, created):
    if not created:
        for key in defaults:
            setattr(obj, key, defaults[key])
        obj.save()
    return obj


CURRENCY_SYMBOLS = {
    "aud": "\u0024",
    "cad": "\u0024",
    "chf": "\u0043\u0048\u0046",
    "cny": "\u00a5",
    "eur": "\u20ac",
    "gbp": "\u00a3",
    "jpy": "\u00a5",
    "myr": "\u0052\u004d",
    "sgd": "\u0024",
    "usd": "\u0024",
}


def obfuscate_secret_key(secret_key):
    return "*" * 20 + secret_key[-4:]
