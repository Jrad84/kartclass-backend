from django.contrib.auth.models import BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        mail = extra_fields.get('mail_list')
        return self._create_user(email, password, mail, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


# class CustomerManager(models.Manager):

#     def started_during(self, year, month):
#         return self.exclude(
#             subscription__status="trialing"
#         ).filter(
#             subscription__start__year=year,
#             subscription__start__month=month
#         )

#     def active(self):
#         return self.filter(
#             subscription__status="active"
#         )

#     def canceled(self):
#         return self.filter(
#             subscription__status="canceled"
#         )

#     def canceled_during(self, year, month):
#         return self.canceled().filter(
#             subscription__canceled_at__year=year,
#             subscription__canceled_at__month=month,
#         )

#     def started_plan_summary_for(self, year, month):
#         return self.started_during(year, month).values(
#             "subscription__plan"
#         ).order_by().annotate(
#             count=models.Count("subscription__plan")
#         )

#     def active_plan_summary(self):
#         return self.active().values(
#             "subscription__plan"
#         ).order_by().annotate(
#             count=models.Count("subscription__plan")
#         )

#     def canceled_plan_summary_for(self, year, month):
#         return self.canceled_during(year, month).values(
#             "subscription__plan"
#         ).order_by().annotate(
#             count=models.Count("subscription__plan")
#         )

#     def churn(self):
#         canceled = self.canceled().count()
#         active = self.active().count()
#         return decimal.Decimal(str(canceled)) / decimal.Decimal(str(active))




