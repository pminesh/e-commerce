import phonenumbers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from unicef_restlib.serializers import UserContextSerializerMixin

from ecommerce.attachments.models import Attachment
from ecommerce.custom_auth.models import Address
from ecommerce.utils.serializers import ReadOnlySerializerMixin

User = get_user_model()


class AccessTokenSerializer(ReadOnlySerializerMixin, serializers.Serializer):
    access_token = serializers.CharField(max_length=1024)


class UserAuthSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    password = serializers.CharField()

    def validate(self, attrs):
        validate_data = super().validate(attrs)
        if 'username' not in validate_data:
            if 'email' not in validate_data and 'phone' not in validate_data:
                raise ValidationError(_('Username, email or phone should be provided'))

        return validate_data


class UserPhotoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    image = serializers.ImageField(source='photo', allow_null=True)
    width = serializers.ReadOnlyField(source='width_photo', allow_null=True)
    height = serializers.ReadOnlyField(source='height_photo', allow_null=True)

    class Meta:
        model = User
        fields = ('id', 'image', 'width', 'height')


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ('id', 'file', 'added_at')
        read_only_fields = fields


class BaseUserSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)
    attachments = AttachmentSerializer(read_only=True, many=True)
    country_code = serializers.SerializerMethodField()
    phone_number = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'uuid', 'first_name', 'last_name', 'fullname', 'email', 'phone', 'about', 'photo', 'user_type',
            'gender', 'password', 'attachments', 'country_code', 'phone_number',
        )
        read_only_fields = ('uuid', )

    def get_photo(self, obj):
        photo = obj.photo
        if not photo:
            return
        return UserPhotoSerializer(obj).data

    def get_country_code(self, obj):
        try:
            phone = phonenumbers.parse(str(obj.phone))
            return f'+{phone.country_code}'
        except phonenumbers.NumberParseException:
            return None

    def get_phone_number(self, obj):
        try:
            phone = phonenumbers.parse(str(obj.phone))
            return f'+{phone.national_number}'
        except phonenumbers.NumberParseException:
            return None

    def save(self, **kwargs):
        password = self.validated_data.pop('password', None)

        user = super().save(**kwargs)

        if password:
            user.set_password(password)
            user.save(update_fields=['password'])

        return user


class UserStatisticSerializerMixin:
    filter_amount = serializers.ReadOnlyField()

    class Meta:
        fields = ('filter_amount',)


class PasswordValidationSerializer(serializers.Serializer):
    password = serializers.CharField()

    def validate_password(self, password):
        try:
            validate_password(password)
        except DjangoValidationError as ex:
            raise ValidationError(ex.messages)
        return password


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, attrs):
        validate_data = super().validate(attrs)
        print(attrs)
        if validate_data['old_password'] == validate_data['new_password']:
            raise ValidationError(_('Aww don\'t use the same password! for security reasons, please use a different password to your old one'))
        elif not self.context['request'].user.check_password(validate_data['old_password']):
            raise ValidationError(_('You have entered incorrect password, please try again'))

        return validate_data


class AddressSerializer(UserContextSerializerMixin, serializers.ModelSerializer):
    user = BaseUserSerializer(read_only=True)
    country_code = serializers.SerializerMethodField()
    phone_number = serializers.SerializerMethodField()

    class Meta:
        model = Address
        fields = ('id', 'name', 'phone', 'street_address', 'street_address_two', 'city', 'state', 'zipcode',
                  'latitude', 'longitude', 'country_code', 'phone_number', 'user',)
        extra_kwargs = {
            'name': {'required': True},
            'phone': {'required': True},
            'street_address': {'required': True},
            'street_address_two': {'required': True},
            'city': {'required': True},
            'state': {'required': True},
            'zipcode': {'required': True},
            'latitude': {'required': True},
            'longitude': {'required': True},
        }

    def get_country_code(self, obj):
        try:
            phone = phonenumbers.parse(str(obj.phone))
            return f'+{phone.country_code}'
        except phonenumbers.NumberParseException:
            return None

    def get_phone_number(self, obj):
        try:
            phone = phonenumbers.parse(str(obj.phone))
            return f'+{phone.national_number}'
        except phonenumbers.NumberParseException:
            return None

    def create(self, validated_data):
        user = self.get_user()
        validated_data['user'] = user
        return super().create(validated_data)

    def validate(self, attrs):
        address = Address.objects.filter(user=self.context['request'].user)
        for add in address:
            if add.street_address == attrs['street_address'] and add.street_address_two == attrs['street_address_two'] and add.city == attrs['city'] and add.state == attrs['state'] and add.zipcode == attrs['zipcode']:
                raise ValidationError('address is same')
        print(attrs['street_address'])
        print(attrs['street_address_two'])
        return super().validate(attrs)