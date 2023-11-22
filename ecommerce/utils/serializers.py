from copy import copy
from typing import Type, Any

from pkg_resources import _
from rest_framework import serializers


class ReadCreateOnlySerializerMixin(object):
    create_not_allowed_message = _('This serializer is not suitable to create instance.')

    @classmethod
    def create(cls, validate_data):
        raise NotImplementedError(cls.create_not_allowed_message)


class ReadUpdateOnlySerializerMixin(object):
    update_not_allowed_message = _('This serializer is not suitable to update instance.')

    @classmethod
    def update(cls, instance, validate_data):
        raise NotImplementedError(cls.update_not_allowed_message)


class ReadOnlySerializerMixin(ReadUpdateOnlySerializerMixin, ReadCreateOnlySerializerMixin):
    pass


def add_serializer_mixin(original: Type[serializers.Serializer], mixin: Any) -> Type[serializers.Serializer]:
    print("add_serializer_mixin")
    if not hasattr(original, 'Meta'):
        return original

    meta = type('NewMeta', (original.Meta,), {})

    for key, value in mixin.Meta.__dict__.items():
        if key.startswith('__'):
            continue

        if key == 'fields':
            meta.fields = meta.fields + value
        elif key == 'read_only_fields':
            if value == serializers.ALL_FIELDS:
                meta.read_only_fields = copy(meta.fields)
            else:
                meta.read_only_fields = meta.read_only_fields = meta.fields + value
        else:
            raise NotImplementedError('Please specify desired behavior for {}'.format(key))

    extra_kwargs = {
        key: value for key, value in mixin.__dict__.items() if not key.startswith('__') and key != 'Meta'
    }
    extra_kwargs['Meta'] = meta
    print("last")

    return type('{}with{}'.format(original.__name__, mixin.__name__), (original,), extra_kwargs)
