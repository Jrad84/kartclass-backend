import importlib

from django.conf import settings  # noqa
from django.core.exceptions import ImproperlyConfigured

import stripe
from appconf import AppConf


def load_path_attr(path):
    i = path.rfind(".")
    module, attr = path[:i], path[i + 1:]
    try:
        mod = importlib.import_module(module)
    except ImportError as e:
        raise ImproperlyConfigured(
            "Error importing {0}: '{1}'".format(module, e)
        )
    try:
        attr = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured(
            "Module '{0}' does not define a '{1}'".format(module, attr)
        )
    return attr


class PinaxStripeAppConf(AppConf):

    PUBLIC_KEY = "pk_test_51GwHkBD9jmvAZt96xvln9VxxqrK0OR1ylOW6RLt7PkuQYsO0BsHzSpxj8LwSd91RIZRuVaq5rvF60s1tLWazlB4b00Lj5TaYar"
    SECRET_KEY = "sk_test_51GwHkBD9jmvAZt96KpjcouKUOWsePIa6G2i42kPoldiMIaSQ0OM4waIlPYIs8Qv2PVeYpqaqc5Wf11zjYFKt4B4Z00FSo6Gx3L"
    API_VERSION = "2015-10-16"
    INVOICE_FROM_EMAIL = "jaredtaback@gmail.com"
    DEFAULT_PLAN = None
    HOOKSET = "pinax.stripe.hooks.DefaultHookSet"
    SEND_EMAIL_RECEIPTS = True
    SUBSCRIPTION_REQUIRED_EXCEPTION_URLS = []
    SUBSCRIPTION_REQUIRED_REDIRECT = None
    SUBSCRIPTION_TAX_PERCENT = None
    DOCUMENT_MAX_SIZE_KB = 20 * 1024 * 1024

    class Meta:
        prefix = "pinax_stripe"
        required = ["PUBLIC_KEY", "SECRET_KEY", "API_VERSION"]

    def configure_api_version(self, value):
        stripe.api_version = value
        return value

    def configure_secret_key(self, value):
        stripe.api_key = value
        return value

    def configure_hookset(self, value):
        return load_path_attr(value)()