import os
import uuid

from django.conf import settings


def get_user_photo_random_filename(instance,filename):
    extension = os.path.splitext(filename)[1]
    return '{}/{}/{}{}'.format(settings.IMAGES_PATH_USER_PHOTOS, uuid.uuid4(), uuid.uuid4(), extension)


def get_document_path(instance,filename):
    return '{}/{}/{}'.format(settings.DOCUMENTS_PATH, uuid.uuid4(), filename)


def get_product_photo_path(instance,filename):
    return '{}/{}/{}'.format(settings.PRODUCTS_IMAGE_PATH, uuid.uuid4(), filename)






















