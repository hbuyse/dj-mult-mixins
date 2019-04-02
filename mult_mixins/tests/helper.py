#! /usr/bin/env python
# coding=utf-8

"""Generate objects."""

# Standard library
import logging
import sys
from datetime import date, datetime, timedelta
from importlib import import_module, reload
from unittest.mock import MagicMock, PropertyMock

# Django
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.base import ModelBase
from django.urls.base import clear_url_caches

logger = logging.getLogger(__name__)


class HelperAttributeNotConfigured(Exception):
    pass


class HelperAttributeImproperlyConfigured(Exception):
    pass


class Helper(object):

    defaults = {}
    iter_fields = list()
    model = None

    def __init__(self, *args, **kwargs):
        """Constructor.

        Set default first and then we update the defaults.
        """
        super().__init__()  # TypeError: object.__init__() takes no arguments

        # Set the default fields
        for k, v in self.get_defaults().items():
            setattr(self, k, v)

        # Overload the fields
        for k, v in kwargs.items():
            setattr(self, k, v)
        self._object = None

    def __iter__(self):
        for key in self.get_iter_fields():
            if issubclass(type(getattr(self, key)), Helper):
                yield (key, getattr(self, key).object)
            else:
                yield (key, getattr(self, key))

    def get_defaults(self):
        if not getattr(self, "defaults"):
            raise HelperAttributeNotConfigured("'defaults' field not set. You have to set it.")
        elif not isinstance(self.defaults, dict):
            raise HelperAttributeImproperlyConfigured("'defaults' field has to be a dict.")
        return self.defaults

    def get_model(self):
        """."""
        if not getattr(self, "model"):
            raise HelperAttributeNotConfigured("'model' field not set. You have to set it.")
        elif not isinstance(self.model, ModelBase):
            raise HelperAttributeImproperlyConfigured("'model' field has to be a django.db.models.base.ModelBase.")
        return self.model

    def get_iter_fields(self):
        """."""
        if not getattr(self, "iter_fields"):
            raise HelperAttributeNotConfigured("'iter_fields' field not set. You have to set it.")
        elif not isinstance(self.iter_fields, (list, tuple)):
            raise HelperAttributeImproperlyConfigured("'iter_fields' field has to be a list or a tuple.")
        return self.iter_fields

    def create(self):
        self._object = self.get_model().objects.create(**dict(self))

    def update(self):
        self.get_model().objects.filter(pk=self._object.pk).update(**dict(self))
        self._object.refresh_from_db()

    def destroy(self):
        self.get_model().objects.get(pk=self._object.pk).delete()

    def get(self, attr):
        if self._object is None:
            self.create()
        return getattr(self._object, attr)

    @property
    def datas_for_form(self):
        for key in self.get_iter_fields():
            if issubclass(type(getattr(self, key)), Helper):
                yield (key, getattr(self, key).get('pk'))
            else:
                yield (key, getattr(self, key))

    @property
    def object(self):
        if self._object is None:
            self.create()
        return self._object

    @property
    def pk(self):
        return self.get('pk')

    def refresh_from_db(self):
        if self._object is None:
            self.create()
        self._object.refresh_from_db()


class UserHelper(Helper):
    """Create a User object and save it in the DB."""

    defaults = {
        'username': 'toto',
        'password': "hello-world",
        'first_name': "Toto",
        'last_name': "Tata",
        'is_staff': False,
        'is_superuser': False,
        'email': 'toto@example.com',
    }
    model = get_user_model()
    iter_fields = ['username', 'password', 'first_name', 'last_name', 'email', 'is_staff']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if ('is_staff' in kwargs and kwargs['is_staff']) or ('is_superuser' in kwargs and kwargs['is_superuser']):
            self.is_staff = True
        self.create()

    def create(self):
        if self.is_superuser:
            self._object = self.get_model().objects.create_superuser(**dict(self))
        else:
            self._object = self.get_model().objects.create_user(**dict(self))

    def get_credentials(self):
        for key in ['username', 'password']:
            yield (key, getattr(self, key))

    def get_username(self):
        return self._object.get_username()
