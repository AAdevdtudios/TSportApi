from rest_framework import serializers
from django.contrib.auth import authenticate
from account.models import User
from rest_framework.exceptions import AuthenticationFailed
import datetime
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_str, smart_bytes, force_str
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    password2 = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "password",
            "password2",
        ]

    def validate(self, attrs):
        password = attrs.get("password", "")
        password2 = attrs.get("password2", "")

        if password != password2:
            raise serializers.ValidationError("Password doesn't match")
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            password=validated_data["password"],
        )

        return user


class ResendOneTimePasswordRequest(serializers.Serializer):
    email = serializers.EmailField(max_length=256)


class ValidateOneTimePasswordRequest(serializers.Serializer):
    email = serializers.EmailField(max_length=256)
    otp = serializers.CharField(max_length=10)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=256, required=False)
    password = serializers.CharField(max_length=68, write_only=True)
    full_name = serializers.CharField(max_length=256, read_only=True)
    access_token = serializers.CharField(max_length=256, read_only=True)
    refresh_token = serializers.CharField(max_length=256, read_only=True)
    status_code = serializers.IntegerField(read_only=True)
    message = serializers.CharField(max_length=256, read_only=True)
    is_subscribed = serializers.BooleanField(read_only=True)
    is_verified = serializers.BooleanField(read_only=True)
    subscriber_number = serializers.CharField(max_length=256, read_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "full_name",
            "access_token",
            "refresh_token",
            "status_code",
            "is_subscribed",
            "is_verified",
            "subscriber_number",
            "message",
        ]

    def validate(self, attrs):
        request = self.context.get("request")
        email = attrs.get("email")
        password = attrs.get("password")

        if email is None:
            return {"message": "Email cant be empty", "status_code": 400}

        if password is None:
            return {"message": "Password cant be empty", "status_code": 400}

        try:
            user = User.objects.get(email=email)
            if not user.check_password(password):
                return {"message": "User password is incorrect", "status_code": 400}

            if not user.is_verified:
                return {"message": "User is not verified", "status_code": 400}

            user_tokens = user.tokens()
            user.lastLogin = datetime.datetime.now()
            user.save()

            return {
                "email": user.email,
                "full_name": user.get_full_name,
                "is_subscribed": user.is_subscribed,
                "subscriber_number": user.subscriber_number,
                "is_verified": user.is_verified,
                "access_token": user_tokens.get("access"),
                "refresh_token": user_tokens.get("refresh"),
                "status_code": 200,
                "message": "User logged in",
            }
        except User.DoesNotExist:
            return {"message": "User doesn't exist", "status_code": 400}


class PasswordResetRequest(serializers.Serializer):
    email = serializers.EmailField(max_length=256)

    class Meta:
        fields = ["email"]

    def validate(self, attrs):
        email = attrs.get("email")
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            request = self.context.get("request")
            site_domain = get_current_site(request=request).domain
            retrieve_lik = reverse(
                "password-reset-confirm", kwargs={"uidb64": uid64, "token": token}
            )
            absLink = f"http://{site_domain}{retrieve_lik}"
            print(absLink)
            return super().validate(attrs)


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    password2 = serializers.CharField(max_length=68, min_length=6, write_only=True)
    uidb64 = serializers.CharField(max_length=256, write_only=True)
    token = serializers.CharField(max_length=256, write_only=True)

    class Meta:
        fields = ["password", "password2", "uidb64", "token"]

    def validate(self, attrs):
        try:
            password = attrs.get("password")
            password2 = attrs.get("password2")
            uidb64 = attrs.get("uidb64")
            token = attrs.get("token")

            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed("Reset link is invalid")
            if password != password2:
                raise AuthenticationFailed("Password doesn't match")
            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            return AuthenticationFailed("Link is invalid")


class LogOutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    default_error_messages = {"bad_token": ("Token is invalid or has expired")}

    def validate(self, attrs):
        self.token = attrs.get("refresh_token")
        return super().validate(attrs)

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            return self.fail("Bad token")


class UserDataSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=256)
    get_full_name = serializers.ReadOnlyField()
    subscriber_number = serializers.CharField(max_length=256, read_only=True)
    is_subscribed = serializers.BooleanField(read_only=True)
    is_verified = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "get_full_name",
            "subscriber_number",
            "is_subscribed",
            "is_verified",
        ]
