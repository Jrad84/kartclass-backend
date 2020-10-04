from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.validators import EmailValidator
from django.contrib.postgres.fields import ArrayField
from django.db import models
import django.dispatch
from django.db.models.signals import pre_delete, post_save, pre_save
from django.dispatch.dispatcher import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from kc.users.managers import CustomUserManager
import jwt

from kc.core.models import Category, Customer, Base, Video
from django.conf import settings
import stripe
import decimal


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
    fname = models.CharField(_("first name"), max_length=80, default='')
    lname = models.CharField(_("last name"), max_length=80, default='')
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
    videos = ArrayField(ArrayField(models.IntegerField()), blank=True, null=True)
        
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
