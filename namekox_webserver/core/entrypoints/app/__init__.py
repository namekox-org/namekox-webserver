#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals


from .handler import WebServerHandler, ApiServerHandler


app = type(__name__, (object,), {'web': WebServerHandler.decorator, 'api': ApiServerHandler.decorator})
