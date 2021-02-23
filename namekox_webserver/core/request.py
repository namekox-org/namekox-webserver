#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals


from werkzeug.wrappers import Request
from werkzeug.wrappers.json import JSONMixin
from namekox_webserver.exceptions import BadRequest


class BaseRequest(Request):
    def is_valid(self, raise_exception=False):
        pass


class JsonRequest(JSONMixin, BaseRequest):
    def __init__(self, request):
        self.request = request
        super(JsonRequest, self).__init__(request.environ)

    def is_valid(self, raise_exception=False):
        if raise_exception and not self.is_json:
            msg = 'unsupported mimetype {0}'.format(self.request.content_type)
            raise BadRequest(msg)
        return self.is_json
