from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _
from kc.users.models import CustomUser



@admin.register(CustomUser)
class CustomUserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model."""

    list_display = (
        "email",
        "date_created",
        "is_staff",
    )
    search_fields = (
        "fname",
        "lname",
        "email",
    )
    fieldsets = (
        (None, {"fields": ("email", "password", "id",)}),
        (_("Personal info"), {"fields": ("fname", "lname")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_created",)},),
    )
    readonly_fields = (
        "id",
        "date_created",
    )
    ordering = ("lname",)

    def get_fieldsets(self, request, obj=None, *args, **kwargs):
        # Non superuser fieldsets.
        fieldsets = (
            (None, {"fields": ("password", "id",)}),
            (_("Personal info"), {"fields": ("fname", "lname", "email",)}),
            (_("Important dates"), {"fields": ("last_login", "date_created",)},),
        )

        add_fieldsets = (
            (
                None,
                {
                    "classes": ("wide",),
                    "fields": ("fname", "lname", "email", "password1", "password2",),
                },
            ),
        )

        if not obj:
            return add_fieldsets

        if not request.user.is_superuser:
            return fieldsets

        return super(CustomUserAdmin, self).get_fieldsets(request, obj, *args, **kwargs)

    def get_readonly_fields(self, request, obj=None, *args, **kwargs):
        readonly_fields = [
            "id",
            "date_created",
            "last_login",
        ]

        if not request.user.is_superuser:
            # Disable fields if user is a superuser.
            if obj and obj.is_superuser:
                readonly_fields.extend(["fname", "lname", "email"])

            return tuple(readonly_fields)

        return super(CustomUserAdmin, self).get_readonly_fields(
            request, obj, *args, **kwargs
        )