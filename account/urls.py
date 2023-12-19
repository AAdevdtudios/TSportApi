from django.urls import path
from .views import (
    RegisterUserView,
    ResendOtp,
    VerifyOtp,
    LoginUser,
    PasswordResetView,
    PasswordResetConfirmView,
    SetNewPasswordView,
    LogOutView,
    GetData,
)

urlpatterns = [
    path("data/", GetData.as_view(), name="GetData"),
    path("register/", RegisterUserView.as_view(), name="register"),
    path("login/", LoginUser.as_view(), name="login"),
    path("logout/", LogOutView.as_view(), name="logout"),
    # path("reset-password/", PasswordResetView.as_view(), name="reset-password"),
    path("resendOtp/", ResendOtp.as_view(), name="Send-OTP"),
    path("validateOtp/", VerifyOtp.as_view(), name="Verify-OTP"),
    path("password-reset/", PasswordResetView.as_view(), name="password-reset"),
    path(
        "password-reset-confirm/<uidb64>/<token>",
        PasswordResetConfirmView.as_view(),
        name="password-reset-confirm",
    ),
    path("set-new-password/", SetNewPasswordView.as_view(), name="set-new-password"),
    # path("otp/<str:id>", ShowOTP.as_view(), name="OTP"),
]
