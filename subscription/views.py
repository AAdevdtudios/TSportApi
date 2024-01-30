from rest_framework.generics import GenericAPIView
from rest_framework.decorators import api_view
from .serializer import SubscribePlan, WebhookResponse
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .services import SubscribeUser, EventActions, CheckReference
from django.core.mail import send_mail
from django.conf import settings


@api_view(["POST"])
def TestDataUserRes(request):
    # call = request.data
    # res = CheckReference(call["ref"])
    # return Response({"message": res}, status=200)
    data = request.data
    message = data["message"]
    email = data["email"]
    send_mail(
        "Test info",
        message,
        settings.EMAIL_HOST_USER,
        [email],
    )
    return Response(
        {
            "message": "Message sent successfully",
        },
    )


# Create your views here.
class CreateSubscription(GenericAPIView):
    serializer_class = SubscribePlan
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        # serializer.email = str(request.user)
        if not serializer.is_valid(raise_exception=True):
            return Response(serializer.error_messages, status=400)
        plan = serializer.data
        data = SubscribeUser(request.user, plan["planName"])
        return Response({"message": data}, status=200)


class WebHookListener(GenericAPIView):
    serializer_class = WebhookResponse

    def post(self, request):
        res = EventActions(request.data["event"], request.data)

        return Response({"success": res}, status=200)
