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
from kc.core.models import Category, Base, Video
from django.conf import settings
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
    first_name = models.CharField(_("first name"), max_length=80, default='')
    last_name = models.CharField(_("last name"), max_length=80, default='')
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
        help_text=_("Designates whether a user is a paid member or not")
    )
    
    category = ArrayField(models.IntegerField(), default=list, null=True)
    temp_cat = models.IntegerField(null=True, blank=True)
    s3_key = models.CharField(max_length=100, null=True, blank=True)
    s3_id = models.CharField(max_length=100, null=True, blank=True)
    token = models.CharField(max_length=400, blank=True, null=True)
    checkout = models.CharField(max_length=250, blank=True, null=True)
    popupMyChron = models.IntegerField(null=True, default=0, blank=True)
    purchasedChampions = models.DateTimeField(null=True)
  
    mail_list = models.BooleanField(
                default=False, 
                help_text=_("Designates whether user has signed up to mailing list")
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
