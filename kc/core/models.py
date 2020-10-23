from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User
from kc.users.managers import ChargeManager, CustomerManager
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField
import uuid
import stripe
from django.utils import timezone
from jsonfield.fields import JSONField
from kc.utils import CURRENCY_SYMBOLS
from django.utils.functional import cached_property
from kc.settings.base import STRIPE_SECRET_KEY, AUTH_USER_MODEL as auth_user
import json


stripe.api_key = STRIPE_SECRET_KEY


class Base(models.Model):
    """Base model.
    Contains fields:
    - `date_created`
    - `date_updated`
    """

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Uuid(models.Model):
    """UUID model.
    Contains fields:
    - `uuid`
    """

    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, verbose_name="UUID"
    )

    class Meta:
        abstract = True

        
class Category(models.Model):
    name = models.CharField(max_length=50)
    tier = models.CharField(max_length=50, null=True)
    description = models.TextField(max_length=1000, null=True)
    image = models.CharField(max_length=100, null=True)
    amount = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    trailer = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    # @property
    # def videos(self):
    #     return self.video_set.all()


class Driver(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Driver"
        verbose_name_plural = "Drivers"

    def __str__(self):
         return self.name


# class Tag(models.Model):
#     name = models.CharField(max_length=50)

#     class Meta:
#         verbose_name = "Tag"
#         verbose_name_plural = "Tags"

#     def __str__(self):
#         return self.name

class Video(models.Model):
    title = models.CharField(max_length=100)
    longdescription = models.TextField(max_length=9000, null=True)    
    description = models.CharField(max_length=150, null=True)
    category = models.ManyToManyField(Category, related_name='category')
    # tag = models.ManyToManyField(Tag, related_name='tag')
    duration = models.DecimalField(decimal_places=2, max_digits=9, null=True)
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    video_file = models.CharField(max_length=100, null=True)
    image_file = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "Videos"

    def __str__(self):
        return self.title

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)



class Article(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=150)
    image = models.CharField(max_length=100, null=True)
    document = models.CharField(max_length=500, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    name = models.CharField(max_length=50)
    comment = models.TextField()
    image = models.FileField(null=True)

    class Meta:
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"

    def __str__(self):
        return self.name


class StripeObject(models.Model):

    stripe_id = models.CharField(max_length=191, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class Plan(models.Model):
    stripe_id = models.CharField(max_length=191)
    amount = models.DecimalField(decimal_places=2, max_digits=9)
    currency = models.CharField(max_length=15, blank=False)
    sku = models.CharField(max_length=50, blank=True)
    interval = models.CharField(max_length=15)
    interval_count = models.IntegerField()
    name = models.CharField(max_length=150)
    statement_descriptor = models.TextField(blank=True)
    trial_period_days = models.IntegerField(null=True, blank=True)
    metadata = JSONField(null=True, blank=True)

    def __str__(self):
        return "{} ({}{})".format(self.name, CURRENCY_SYMBOLS.get(self.currency, ""), self.amount)

    def __repr__(self):
        return "Plan(pk={!r}, name={!r}, amount={!r}, currency={!r}, sku={!r}, interval={!r}, interval_count={!r}, trial_period_days={!r}, stripe_id={!r})".format(
            self.pk,
            self.name,
            self.amount,
            self.currency,
            self.sku,
            self.interval,
            self.interval_count,
            self.trial_period_days,
            self.stripe_id,
        )

    @property
    def stripe_plan(self):
        return stripe.Plan.retrieve(
            self.stripe_id,
        )

class Price(models.Model):
    stripe_id = models.CharField(max_length=191)
    product = models.ForeignKey(Plan, on_delete=models.CASCADE)
    unit_amount = models.DecimalField(decimal_places=2, max_digits=9)
    currency = models.CharField(max_length=15, default='aud', blank=False)

    def __str__(self):
        return "{} ({}{})".format(self.stripe_id, CURRENCY_SYMBOLS.get(self.currency, ""), self.unit_amount)

    def __repr__(self):
        return "Price(pk={!r}, unit_amount={!r}, currency={!r}, stripe_id={!r})".format(
            self.pk,
            self.unit_amount,
            self.currency,
            self.stripe_id,
        )

    @property
    def stripe_price(self):
        return stripe.Price.retrieve(
            self.stripe_id,
        )

class Customer(models.Model):

    user = models.OneToOneField(auth_user, null=True, blank=True, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=191)
    currency = models.CharField(max_length=10, default="aud", blank=True)
    delinquent = models.BooleanField(default=False)
    default_source = models.TextField(blank=True)
    date_purged = models.DateTimeField(null=True, blank=True, editable=False)

    objects = CustomerManager()

    @cached_property
    def stripe_customer(self):
        return stripe.Customer.retrieve(
            self.stripe_id,
        )

    def __str__(self):
        if self.user:
            return str(self.user)
        
        if self.stripe_id:
            return "No User(s) ({})".format(self.stripe_id)
        return "No User(s)"

    def __repr__(self):
        if self.user:
            return "Customer(pk={!r}, user={!r}, stripe_id={!r})".format(
                self.pk,
                self.user,
                self.stripe_id,
            )
        elif self.id:
            return "Customer(pk={!r}, users={}, stripe_id={!r})".format(
                self.pk,
                ", ".join(repr(user) for user in self.users.all()),
                self.stripe_id,
            )
        return "Customer(pk={!r}, stripe_id={!r})".format(self.pk, self.stripe_id)




class Card(models.Model):

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.TextField(blank=True)
    address_line_1 = models.TextField(blank=True)
    address_line_1_check = models.CharField(max_length=15)
    address_line_2 = models.TextField(blank=True)
    address_city = models.TextField(blank=True)
    address_state = models.TextField(blank=True)
    address_country = models.TextField(blank=True)
    address_zip = models.TextField(blank=True)
    address_zip_check = models.CharField(max_length=15)
    brand = models.TextField(blank=True)
    country = models.CharField(max_length=2, blank=True)
    cvc_check = models.CharField(max_length=15, blank=True)
    dynamic_last4 = models.CharField(max_length=4, blank=True)
    tokenization_method = models.CharField(max_length=15, blank=True)
    exp_month = models.IntegerField()
    exp_year = models.IntegerField()
    funding = models.CharField(max_length=15)
    last4 = models.CharField(max_length=4, blank=True)
    fingerprint = models.TextField()

    def __repr__(self):
        return "Card(pk={!r}, customer={!r})".format(
            self.pk,
            getattr(self, "customer", None),
        )

class Subscription(models.Model):

    STATUS_CURRENT = ["trialing", "active"]
    stripe_id = models.CharField(max_length=191, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    application_fee_percent = models.DecimalField(decimal_places=2, max_digits=3, default=None, null=True, blank=True)
    cancel_at_period_end = models.BooleanField(default=False)
    canceled_at = models.DateTimeField(null=True, blank=True)
    current_period_end = models.DateTimeField(null=True, blank=True)
    current_period_start = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    start = models.DateTimeField()
    status = models.CharField(max_length=25)  # trialing, active, past_due, canceled, or unpaid
    trial_end = models.DateTimeField(null=True, blank=True)
    trial_start = models.DateTimeField(null=True, blank=True)

    @property
    def stripe_subscription(self):
        return stripe.Subscription.retrieve(self.stripe_id, stripe_account=self.stripe_account_stripe_id)

    @property
    def total_amount(self):
        return self.plan.amount * self.quantity

    def plan_display(self):
        return self.plan.name

    def status_display(self):
        return self.status.replace("_", " ").title()

    def delete(self, using=None):
        """
        Set values to None while deleting the object so that any lingering
        references will not show previous values (such as when an Event
        signal is triggered after a subscription has been deleted)
        """
        super(Subscription, self).delete(using=using)
        self.status = None
        self.quantity = 0
        self.amount = 0

    def __repr__(self):
        return "Subscription(pk={!r}, customer={!r}, plan={!r}, status={!r}, stripe_id={!r})".format(
            self.pk,
            getattr(self, "customer", None),
            getattr(self, "plan", None),
            self.status,
            self.stripe_id,
        )


class Invoice(models.Model):
    
    created_at = models.DateTimeField(default=timezone.now)
    customer = models.ForeignKey(Customer, related_name="invoices", on_delete=models.CASCADE)
    amount_due = models.DecimalField(decimal_places=2, max_digits=9)
    attempted = models.NullBooleanField()
    attempt_count = models.PositiveIntegerField(null=True, blank=True)
    charge = models.ForeignKey("Charge", null=True, blank=True, related_name="invoices", on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, null=True, blank=True, on_delete=models.CASCADE)
    statement_descriptor = models.TextField(blank=True)
    currency = models.CharField(max_length=10, default="aud")
    closed = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    paid = models.BooleanField(default=False)
    receipt_number = models.TextField(blank=True)
    period_end = models.DateTimeField()
    period_start = models.DateTimeField()
    subtotal = models.DecimalField(decimal_places=2, max_digits=9)
    tax = models.DecimalField(decimal_places=2, max_digits=9, null=True, blank=True)
    tax_percent = models.DecimalField(decimal_places=2, max_digits=9, null=True, blank=True)
    total = models.DecimalField(decimal_places=2, max_digits=9)
    date = models.DateTimeField()
    webhooks_delivered_at = models.DateTimeField(null=True, blank=True)

    @property
    def status(self):
        return "Paid" if self.paid else "Open"

    @property
    def stripe_invoice(self):
        return stripe.Invoice.retrieve(
            self.stripe_id,
            stripe_account=self.stripe_account_stripe_id,
        )


class InvoiceItem(models.Model):

    stripe_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    invoice = models.ForeignKey(Invoice, related_name="items", on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=9)
    currency = models.CharField(max_length=10, default="aud")
    kind = models.CharField(max_length=25, blank=True)
    subscription = models.ForeignKey(Subscription, null=True, blank=True, on_delete=models.CASCADE)
    period_start = models.DateTimeField()
    period_end = models.DateTimeField()
    proration = models.BooleanField(default=False)
    line_type = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True)
    plan = models.ForeignKey(Plan, null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True, blank=True)

    def plan_display(self):
        return self.plan.name if self.plan else ""


class Charge(models.Model):
    
    customer = models.ForeignKey(Customer, null=True, blank=True, related_name="charges", on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, null=True, blank=True, related_name="charges", on_delete=models.CASCADE)
    source = models.CharField(max_length=100, blank=True)
    currency = models.CharField(max_length=10, default="aud")
    amount = models.DecimalField(decimal_places=2, max_digits=9, null=True, blank=True)
    amount_refunded = models.DecimalField(decimal_places=2, max_digits=9, null=True, blank=True)
    description = models.TextField(blank=True)
    paid = models.NullBooleanField(null=True, blank=True)
    disputed = models.NullBooleanField(null=True, blank=True)
    refunded = models.NullBooleanField(null=True, blank=True)
    captured = models.NullBooleanField(null=True, blank=True)
    receipt_sent = models.BooleanField(default=False)
    charge_created = models.DateTimeField(null=True, blank=True)

    # These fields are extracted from the BalanceTransaction for the
    # charge and help us to know when funds from a charge are added to
    # our Stripe account's balance.
    available = models.BooleanField(default=False)
    available_on = models.DateTimeField(null=True, blank=True)
    fee = models.DecimalField(
        decimal_places=2, max_digits=9, null=True, blank=True
    )
    fee_currency = models.CharField(max_length=10, default="aud", null=True, blank=True)

    transfer_group = models.TextField(null=True, blank=True)
    outcome = JSONField(null=True, blank=True)

    objects = ChargeManager()

    def __str__(self):
        info = []
        if not self.paid:
            info += ["unpaid"]
        if not self.captured:
            info += ["uncaptured"]
        if self.refunded:
            info += ["refunded"]
        currency = CURRENCY_SYMBOLS.get(self.currency, "")
        return "{}{}{}".format(
            currency,
            self.total_amount,
            " ({})".format(", ".join(info)) if info else "",
        )

    def __repr__(self):
        return "Charge(pk={!r}, customer={!r}, source={!r}, amount={!r}, captured={!r}, paid={!r}, stripe_id={!r})".format(
            self.pk,
            self.customer,
            self.source,
            self.amount,
            self.captured,
            self.paid,
            self.stripe_id,
        )

    @property
    def total_amount(self):
        amount = self.amount if self.amount else 0
        amount_refunded = self.amount_refunded if self.amount_refunded else 0
        return amount - amount_refunded
    total_amount.fget.short_description = "Σ amount"

    @property
    def stripe_charge(self):
        return stripe.Charge.retrieve(
            self.stripe_id,
            stripe_account=self.stripe_account_stripe_id,
            expand=["balance_transaction"]
        )

    @property
    def card(self):
        return Card.objects.filter(stripe_id=self.source).first()

# class Charges(models.Model):

#     object = ArrayField(models.CharField(max_length=50))
#     data = models.ManyToManyField(Charge)
#     has_more = models.BooleanField(default=False)
#     url = models.CharField(max_length=100)

# class PaymentIntent(models.Model):

#     amount = models.IntegerField()
#     client_secret = models.CharField(max_length=100, blank=True)
#     charges = models.ForeignKey(Charges, null=True, blank=True, related_name="charges", on_delete=models.CASCADE)
#     currency = models.CharField(max_length=3, default="aud")
#     customer = models.ForeignKey(Customer, blank=True, related_name="customer", on_delete=models.CASCADE)
#     description = models.CharField(max_length=100, blank=True)
#     created = models.DateTimeField(null=True, blank=True)
#     payment_method = models.ForeignKey(Card, related_name="card", on_delete=models.CASCADE)
#     receipt_email = models.EmailField(blank=True)
#     status = 



# from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
# from django.core.exceptions import PermissionDenied, ValidationError
# from django.core.validators import EmailValidator

# import django.dispatch
# from django.db.models.signals import pre_delete, post_save, pre_save
# from django.dispatch.dispatcher import receiver

# from django.utils.translation import gettext_lazy as _
# from kc.accounts.managers import CustomUserManager
# import jwt



# import decimal


# class CustomUser(AbstractBaseUser, PermissionsMixin, Base):
#     """Custom user model that extends `AbstractUser`, `Base`, `Uuid`.
#     Contains fields:
#     - `email: str`
#     - `name: str`
#     - `is_staff: bool`
#     - `is_active: bool`
#     """

#     email_validator = EmailValidator()

#     username = None
#     email = models.EmailField(
#         _("email address"),
#         unique=True,
#         validators=[email_validator],
#         error_messages={"unique": _("A user with that email already exists.")}, 
#     )
#     name = models.CharField(_("full name"), max_length=80)
#     is_staff = models.BooleanField(
#         _("staff status"),
#         default=False,
#         help_text=_("Designates whether the user can log into this admin site."),
#     )
#     is_active = models.BooleanField(
#         _("active"),
#         default=True,
#         help_text=_(
#             "Designates whether this user should be treated as active. "
#             "Unselect this instead of deleting accounts."
#         ),
#     )
#     is_member = models.BooleanField(
#         _("member"),
#         default=False,  
#         help_text=_("Designates whether a user is a paid member or not"),
#     )
#     # Need to test this
#     category = models.ForeignKey(
#         Category, null=True, 
#         on_delete=models.SET_NULL,
#         help_text=_("Designates what category a user is in")
#     )
#     # category = models.IntegerField(null=True)
#     stripe_id = models.CharField(
#         max_length=300,
#         null = True,
#         blank = True,
#         help_text=_("Stripe user id")
#     )
#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = []
#     objects = CustomUserManager()

#     class Meta:
#         verbose_name = _("custom user")
#         verbose_name_plural = _("custom users")

#     def clean(self):
#         super().clean()
#         self.email = self.__class__.objects.normalize_email(self.email)

#     def __str__(self):
#         return self.email

# # Make sure superuser can't be deleted
# @receiver(pre_delete, sender=CustomUser)
# def delete_user(sender, instance, **kwargs):
#     # Prevent superuser deletion.
#     if instance.is_superuser:
#         raise PermissionDenied
