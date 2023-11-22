from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin,ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.viewsets import GenericViewSet
from unicef_restlib.views import MultiSerializerViewSetMixin

from ecommerce.custom_auth.models import ApplicationUser
from ecommerce.registrations.serializers import RegistrationSerializer, CheckUserDataSerializer, CheckPhoneSerializer,CheckOtp


class RegistrationViewSet(
    MultiSerializerViewSetMixin,
    CreateModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    queryset = ApplicationUser.objects.all().order_by('-date_joined')
    serializer_class = RegistrationSerializer
    serializer_action_classes = {
        # 'check_user_data': CheckUserDataSerializer,
        'send_sms': CheckPhoneSerializer,
        'check_otp_with_number': CheckOtp,
    }
    permission_classes = (AllowAny,)

    @action(methods=['post'], permission_classes=(AllowAny,), url_name='check',
            url_path='check', detail=False, serializer_class=CheckUserDataSerializer)
    def check_user_data(self, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


        #send SMS code

        return Response(serializer.data)

    @action(permission_classes=(AllowAny,), methods=['post'], url_name='send_sms_code',
            url_path='send-sms-code', detail=False)
    def send_sms(self, *args, **kwargs):
        '''
        For manual sms code sending
        '''

        serializer = self.get_serializer(data=self.request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


        #send SMS code
        otp = "1234"
        # return Response(serializer.data)
        return Response({"otp": otp})


    @action(permission_classes=(AllowAny,), methods=['post'], url_name='check_otp_with_number',
            url_path='check_otp_with_number', detail=False)
    def check_otp_with_number(self, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        otp = "1234"

        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        if otp == serializer.data['otp']:
            return Response({"success": "Successfully registered!!"}, status=HTTP_200_OK)
        return Response({"error": "Enter valid otp"}, status=HTTP_400_BAD_REQUEST)

