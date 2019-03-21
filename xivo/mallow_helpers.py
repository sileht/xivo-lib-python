# -*- coding: utf-8 -*-
# Copyright 2016-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from functools import wraps

import marshmallow

from .mallow import fields, validate
from .rest_api_helpers import APIException


class ValidationError(APIException):

    def __init__(self, errors):
        super(ValidationError, self).__init__(
            status_code=400,
            message='Sent data is invalid',
            error_id='invalid-data',
            details=errors
        )


def handle_validation_exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except marshmallow.ValidationError as e:
            raise ValidationError(e.messages)
    return wrapper


class ListSchema(marshmallow.Schema):
    default_sort_column = None
    sort_columns = []
    searchable_columns = []

    direction = fields.String(validate=validate.OneOf(['asc', 'desc']), missing='asc')
    order = fields.String()
    limit = fields.Integer(validate=validate.Range(min=0), missing=None)
    offset = fields.Integer(validate=validate.Range(min=0), missing=0)
    search = fields.String(missing=None)

    class Meta:
        strict = True

    def on_bind_field(self, field_name, field_obj):
        if field_name == 'order':
            self._set_order_parameters(field_obj)

    def _set_order_parameters(self, field_obj):
        field_obj.validators = [validate.OneOf(self.sort_columns)]
        field_obj.missing = self.default_sort_column
        if self.default_sort_column is None:
            field_obj.allow_none = True
        else:
            field_obj.allow_none = False

    @marshmallow.post_load(pass_original=True)
    def add_searchable_fields(self, data, original_data):
        for key, value in original_data.items():
            if key in self.searchable_columns:
                data.setdefault(key, value)

        return data


class Schema(marshmallow.Schema):

    class Meta:
        ordered = True
        strict = True   # Always strict in marshmallow 3

    # This behavior is fixed in marshmallow 3
    @marshmallow.pre_load
    def ensure_dict(self, data):
        return data or {}
