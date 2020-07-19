from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.validators import EmailValidator
from django.db import models
import django.dispatch
from django.db.models.signals import pre_delete, post_save, pre_save
from django.dispatch.dispatcher import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from accounts.managers import CustomUserManager
from pinax.stripe.actions import customers
from pinax.stripe.models import Customer
import jwt

from core.models import Category

from django.conf import settings
from core.models import Base, Uuid
import stripe
import decimal

stripe.api_key = settings.PINAX_STRIPE_SECRET_KEY

class CustomUser(AbstractBaseUser, PermissionsMixin, Base):
    """Custom user model that extends `AbstractUser`, `Base`, `Uuid`.
    Contains fields:
    - `email: str`
    - `name: str`
    - `is_staff: bool`
    - `is_active: bool`
    """

    email_validator = EmailValidator()

    username = None
    email = models.EmailField(
        _("email address"),
        unique=True,
        validators=[email_validator],
        error_messages={"unique": _("A user with that email already exists.")}, 
    )
    name = models.CharField(_("full name"), max_length=80)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_member = models.BooleanField(
        _("member"),
        default=False,  
        help_text=_("Designates whether a user is a paid member or not"),
    )
    # Need to test this
    category = models.ForeignKey(
        Category, null=True, 
        on_delete=models.SET_NULL,
        help_text=_("Designates what category a user is in")
    )
    stripe_id = models.CharField(
        max_length=300,
        null = True,
        blank = True,
        help_text=_("Stripe user id")
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        verbose_name = _("custom user")
        verbose_name_plural = _("custom users")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def __str__(self):
        return self.email

# Make sure superuser can't be deleted
@receiver(pre_delete, sender=CustomUser)
def delete_user(sender, instance, **kwargs):
    # Prevent superuser deletion.
    if instance.is_superuser:
        raise PermissionDenied

# Create a Stripe customer after User saved in db
# @receiver(post_save, sender=CustomUser)
# def create_stripe_user(sender, instance, created, **kwargs):
#     if created:
#         customer = customers.create(user=instance)
#         customer.save()
#         CustomUser.stripe_id = customer.stripe_id
#         CustomUser.save()
