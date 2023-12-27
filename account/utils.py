import pyotp
from datetime import datetime, timedelta

# import resend
# import os

# resend.api_key = os.environ["RESEND_KEY"]
from .models import OneTimePassword, User


def send_otp(email: str):
    totp = pyotp.TOTP(pyotp.random_base32(), interval=1800)
    otp = totp.now()
    valid_date = datetime.now() + timedelta(minutes=30)
    # print(f"{otp} + {valid_date}")

    try:
        user = User.objects.get(email=email)
        get_otp = OneTimePassword.objects.get(user=user)
        if get_otp is not None:
            get_otp.date = str(valid_date)
            get_otp.code = otp
            get_otp.secrete = totp.secret
            get_otp.save()
        else:
            OneTimePassword.objects.create(
                user=user, code=otp, date=valid_date, secrete=totp.secret
            )
        print(f"pass a url for the user {totp.secret}")
        # params = {
        #     "from": "Acme <onboarding@resend.dev>",
        #     "to": f"{email}",
        #     "subject": f"Send OTP to {email}",
        #     "html": f"<strong>Your {otp} is</strong>",
        # }
        # email = resend.Emails.send(params)

        return {
            "otp": otp,
            "Secret": totp.secret,
            "valid_date": str(valid_date),
            "status": 200,
        }
    except User.DoesNotExist:
        return {"error": "User doesn't exist", "status": 400}


def validate(otp: str, email: str):
    try:
        user = User.objects.get(email=email)
        get_user_otp_details = OneTimePassword.objects.get(code=otp)
        totp = pyotp.TOTP(get_user_otp_details.secrete, interval=60)

        # Is User verified
        if user.is_verified:
            return {"error": "User is already valid", "status": 400}

        # Does the user email match the email otp
        if user.email != get_user_otp_details.user.email:
            return {"message": "Invalid User Otp", "status": 400}

        # Has the otp expired
        valid_until = datetime.fromisoformat(get_user_otp_details.date)
        if valid_until < datetime.now():
            return {"message": "OTP has expired", "status": 400}
        totp = pyotp.TOTP(get_user_otp_details.secrete, interval=1800)

        # Does the OTP match the generated OTP
        if not totp.verify(otp=otp):
            return {"message": "Invalid Otp or has expired", "status": 400}

        user.is_verified = True
        user.save()

        return {"message": "User is equal", "status": 200}

    except User.DoesNotExist:
        return {"error": "User doesn't exist", "status": 400}
    except OneTimePassword.DoesNotExist:
        return {"error": "OTP doesn't exist", "status": 400}
