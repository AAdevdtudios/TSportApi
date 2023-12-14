from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializer import (
    UserRegisterSerializer,
    ResendOneTimePasswordRequest,
    ValidateOneTimePasswordRequest,
    LoginSerializer,
    PasswordResetRequest,
    SetNewPasswordSerializer,
    LogOutSerializer,
)
from rest_framework.response import Response
from rest_framework import status
from .utils import send_otp, validate
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.permissions import IsAuthenticated

from .models import User

# Create your views here.


class ResendOtp(GenericAPIView):
    serializer_class = ResendOneTimePasswordRequest

    # send new Otp
    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)

        if not serializer.is_valid(raise_exception=True):
            return Response(serializer.error_messages, status=400)

        info = serializer.data
        sent_data = send_otp(info["email"])
        return Response(sent_data, status=sent_data["status"])


class VerifyOtp(GenericAPIView):
    serializer_class = ValidateOneTimePasswordRequest

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)

        if not serializer.is_valid(raise_exception=True):
            return Response(serializer.error_messages, status=400)

        info = serializer.data
        print(info)
        valid = validate(
            otp=info["otp"],
            secrete=info["secrete"],
            expiring_date=info["date"],
            email=info["email"],
        )
        return Response(valid, status=valid["status"])


class RegisterUserView(GenericAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        user_data = request.data
        serializer = self.serializer_class(data=user_data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.data
            sentInfo = send_otp(user["email"])
            first_name = user["first_name"]

            # Send email function
            return Response(
                {
                    "data": user | sentInfo,
                    "message": f"Hi {first_name} thanks for signing up a pass code has been sent to your email",
                },
                status=200,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUser(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=serializer.data["status_code"])


class PasswordResetView(GenericAPIView):
    serializer_class = PasswordResetRequest

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        return Response({"message": serializer.data}, status=200)


class PasswordResetConfirmView(GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response(
                    {"message": "Token is invalid or as expired"}, status=400
                )
            return Response({"message": "Token is valid"}, status=200)
        except DjangoUnicodeDecodeError:
            Response({"message": "Token is invalid or as expired"}, status=400)


class SetNewPasswordView(GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"message": "Password is set"}, status=200)


class LogOutView(GenericAPIView):
    serializer_class = LogOutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=204)
