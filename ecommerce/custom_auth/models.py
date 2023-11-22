import uuid as uuid

from django.conf import settings
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils import timezone
from model_utils import Choices
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField

from ecommerce.custom_auth.managers import ApplicationUserManager
from ecommerce.attachments.models import Attachment
from ecommerce.custom_auth.mixins import UserPhotoMixin
from ecommerce.custom_auth.utils import set_password_reset_expiration_time


class ApplicationUser(
    AbstractBaseUser,
    UserPhotoMixin,
    PermissionsMixin
):
    USER_TYPES = Choices(
        ("users","Users"),
        ("seller","Seller"),
    )

    GENDER_TYPES = Choices(
        ("male","Male"),
        ("female","Female"),
    )

    #uuid = universal unique identification
    username_validator = UnicodeUsernameValidator()
    uuid = models.UUIDField(
        verbose_name=_('uuid'),
        unique=True,
        help_text=_('Required. A 32 hexadecimal digits number as specified in RFC 4122'),
        error_messages={
            'unique': _('A user with that uuid already exists.'),
        },
        default=uuid.uuid4,
    )

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        blank=True,
        null=True,
        help_text=('Required. 150 characters or fewer. Lettres , digits and @/./+/-/ only .'),
        validators=[username_validator],
        error_messages={
            'unique': _('A user with that username already exists.'),
        }
    )

    email = models.EmailField(
        _('email address'),
        null=True,
        blank=True,
        unique=True,
        error_messages={
            'unique': _('A user with that email address  already exists.'),
        }
    )

    is_email_verified = models.BooleanField(
        _('email verified'),
        default=True,
    )
    first_name = models.CharField(
        _('first name'),
        max_length=30,
        blank=True,
    )

    last_name = models.CharField(
        _('last name'),
        max_length=150,
        blank=True,
    )

    fullname = models.CharField(
        _('full name'),
        max_length=300,
        blank=True,
        help_text=_('Full name as it was returned by social media provider.'),
    )

    about = models.TextField(
        _('about me'),
        max_length=1000,
        blank=True,
    )

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_('Designates whether the user should be treated as active.'
                      'Unselect this instead of deleting account.'),
    )

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    last_modified = models.DateTimeField(_('last modified'),auto_now=True)
    last_user_activity = models.DateTimeField(_('last activity'),default=timezone.now)
    phone = PhoneNumberField(_('Phone'),null=True, blank=True, unique=True,
                             error_messages={
            'unique': _('A user with that phone number already exists.'),
        })
    gender = models.CharField(max_length=10,choices=GENDER_TYPES, default=GENDER_TYPES.male)
    date_of_birth = models.DateField(_('date of birth'), null=True, blank=True)
    city = models.CharField(_('city'), max_length=100, null=True, blank=True)
    is_deliver_orders = models.BooleanField(_('do you want to deliver orders?'), default=False)
    delivery_region = models.CharField(_('delivery region'), max_length=255, null=True, blank=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default=USER_TYPES.users)

    attachments = GenericRelation(Attachment, verbose_name=_("Attachments"), null=True, blank=True)

    objects = ApplicationUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.username or self.fullname or self.email or self.first_name or self.str(uuid)


    @property
    def attachment(self):
        return self.attachments.order_by('-added_at')

    def save(self, *args, **kwargs):
        if self.photo and (not self.width_photo or not self.height_photo):
            self.width_photo = self.photo.width
            self.height_photo = self.photo.height

        if self.email:
            self.email = self.__class__.objects.normalize_email(self.email)

        if not self.username:
            new_username = self.email.split('@')[0] if self.email else ''

            if self._meta.model._default_manager.filter(username=new_username).exists() or new_username == '':
                postfix = timezone.now().strftime('%Y%m%d%H%M%S')

                while self._meta.model._default_manager.filter(username=new_username + postfix).exists():
                    postfix = timezone.now().strftime('%Y%m%d%H%M%S')

                new_username += postfix

            self.username = new_username


        # full name assignment
        if not self.fullname.strip():
            if self.first_name and self.last_name:
                self.assign_full_name_to_the_object()

        if self.fullname:
            self.assign_first_last_name_to_the_object()

        return super(ApplicationUser, self).save(*args, **kwargs)

    def assign_full_name_to_the_object(self):
        self.fullname = f'{self.first_name} {self.last_name}'.strip()

    def assign_first_last_name_to_the_object(self):
        fullname = self.fullname.split(' ')
        self.first_name = fullname[0]
        if len(fullname) > 1:
            self.last_name = fullname[1]
        else:
            self.last_name = fullname[0]


    def update_last_activity(self):
        now = timezone.now()

        print(self.last_user_activity)
        self.last_user_activity = now
        self.save(update_fields=('last_user_activity','last_modified'))


class PasswordResetId(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    expiration_time = models.DateTimeField(default=set_password_reset_expiration_time)

    class Meta:
        verbose_name = 'Password reset id'


class Address(TimeStampedModel):
    ADDRESS_TYPES = Choices(
        ('home', 'Home'),
        ('work', 'Work'),
        ('other', 'Other'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(_('Full Name'), blank=True, max_length=300)
    phone = PhoneNumberField(_('Phone'), blank=True, null=True)
    street_address = models.CharField(_('Street Address'), blank=True, max_length=300)
    street_address_two = models.CharField(_('Street Address 2'), blank=True, max_length=300)
    city = models.CharField(_('City'), blank=True, null=True, max_length=100)
    state = models.CharField(_('State/Province/Region'), blank=True, null=True, max_length=100)
    zipcode = models.CharField(_('Zip Code'), blank=True, null=True, max_length=100)
    latitude = models.DecimalField(_('Latitude'), blank=True, null=True, max_digits=9, decimal_places=6)
    longitude = models.DecimalField(_('Longitude'), blank=True, null=True, max_digits=9, decimal_places=6)
    address_type = models.CharField(choices=ADDRESS_TYPES, max_length=10, default=ADDRESS_TYPES.home)

    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')

    def __str__(self):
        return f'{self.user.username}'




