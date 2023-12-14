import pyotp
from datetime import datetime, timedelta

# import resend
# import os
from .models import User

# resend.api_key = os.environ["RESEND_KEY"]
# from .models import OneTimePassword, User


def send_otp(email: str):
    totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
    otp = totp.now()
    valid_date = datetime.now() + timedelta(minutes=1)
    # print(f"{otp} + {valid_date}")

    try:
        user = User.objects.get(email=email)
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


def validate(otp: str, secrete: str, expiring_date: datetime, email: str):
    try:
        user = User.objects.get(email=email)
        totp = pyotp.TOTP(secrete, interval=60)

        if user.is_verified:
            return {"error": "User is already valid", "status": 400}

        if secrete and expiring_date is not None:
            valid_until = datetime.fromisoformat(expiring_date)
            if valid_until > datetime.now():
                totp = pyotp.TOTP(secrete, interval=60)
                if totp.verify(otp):
                    user.is_verified = True
                    user.save()
                    return {
                        "valid": True,
                        "status": 200,
                    }
                else:
                    return {
                        "error": "Invalid data",
                        "status": 400,
                    }
            else:
                return {
                    "error": "Session as expired",
                    "status": 400,
                }
        return {
            "error": "Un identified",
            "status": 400,
        }
    except User.DoesNotExist:
        return {"error": "User doesn't exist", "status": 400}
