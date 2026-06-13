


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models.profile import Profile
from .models.user import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = (
        "id",
        "phone_number",
        "email",
        "email_verified",
        "phone_verified",
        "is_active",
        "is_staff",
        "date_joined",
    )

    list_filter = (
        "is_active",
        "is_staff",
        "is_superuser",
        "email_verified",
        "phone_verified",
    )

    search_fields = (
        "phone_number",
        "email",
    )

    ordering = ("-date_joined",)
    list_display_links = ("phone_number",)

    fieldsets = (
        ("Authenticate:", {"fields": ("phone_number", "password")}),
        ("Personal Info:", {"fields": ("email",)}),
        ("Verification:", {"fields": ("email_verified", "phone_verified")}),
        ("Permissions:", {"fields": (
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
        )}),
        
    )

    add_fieldsets = (
        (
            "Authenticate:",
            {
                "classes": ("wide",),
                "fields": ("phone_number", "email", "password1", "password2"),
            },
        ),
    )
    readonly_fields = ("last_login", "date_joined")

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "first_name",
        "last_name",
    )

    search_fields = (
        "user__phone_number",
        "first_name",
        "last_name",
    )

    list_select_related = ("user",)

    fieldsets = (
        (
            "User Relation",
            {"fields": ("user",)},
        ),
        (
            "Personal Info",
            {"fields": ("first_name", "last_name", "bio")},
        ),
    )
    list_display_links = ("user",)
    