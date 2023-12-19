from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .manager import UserManager
from rest_framework_simplejwt.tokens import RefreshToken


AUTH_PROVIDERS = {
    "email": "email",
    "google": "google",
    "apple": "apple",
    "facebook": "facebook",
}


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        max_length=255, unique=True, verbose_name=_("Email Address")
    )
    first_name = models.CharField(max_length=255, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=255, verbose_name=_("Last Name"))
    phone_number = models.CharField(max_length=255, verbose_name=_("Phone Number"))
    subscriber_number = models.CharField(
        max_length=255, unique=True, verbose_name=_("Subscriber Number")
    )
    is_subscribed = models.BooleanField(default=False, verbose_name=_("Subscribed"))
    subscriptionDate = models.DateTimeField(
        auto_now=True, verbose_name=_("Subscription Date")
    )
    nextSubscriptionDate = models.DateTimeField(
        auto_now=True, verbose_name=_("Next Date")
    )
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    dateJoined = models.DateTimeField(auto_now_add=True)
    lastLogin = models.DateTimeField(auto_now=True)
    auth_provider = models.CharField(max_length=50, default=AUTH_PROVIDERS.get("email"))

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    objects = UserManager()

    def __str__(self) -> str:
        return self.email

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}


# class OneTimePassword(models.Model):
#     user = models.OneToOneRel(User, on_delete=models.CASCADE)
#     code = models.CharField(max_length=6, unique=True)
#     date = models.DateTimeField(auto_now=True)

#     def __str__(self) -> str:
#         return f"{self.user.first_name} {self.user.last_name}- pass code"
