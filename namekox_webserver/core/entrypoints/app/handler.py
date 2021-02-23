#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals

import sys
import six
import json


from eventlet.event import Event
from werkzeug.routing import Rule
from werkzeug.wrappers import Response
from namekox_core.exceptions import gen_exc_to_data
from namekox_webserver.exceptions import BadRequest
from namekox_core.core.friendly import as_wraps_partial
from namekox_core.core.service.entrypoint import Entrypoint
from namekox_webserver.core.messaging import get_message_headers


from .server import WebServer


class BaseWebServerHandler(Entrypoint):
    server = WebServer()

    def __init__(self, rule, methods=('GET',), **kwargs):
        self.rule = rule
        self.methods = methods
        super(BaseWebServerHandler, self).__init__(**kwargs)

    @property
    def url_rule(self):
        return Rule(self.rule, methods=self.methods, endpoint=self)

    def setup(self):
        self.server.register_extension(self)

    def stop(self):
        self.server.unregister_extension(self)
        self.server.wait_extension_stop()

    def handle_request(self, request):
        context, result, exc_info = None, None, None
        try:
            request.shallow = False
            ctxdata = get_message_headers(request)
            args, kwargs = (request,), request.path_values
            event = Event()
            res_handler = as_wraps_partial(self.res_handler, event)
            self.container.spawn_worker_thread(self, args, kwargs, 
                                               ctx_data=ctxdata,
                                               res_handler=res_handler)
            context, result, exc_info = event.wait()
        except Exception:
            exc_info = sys.exc_info()
        return context, result, exc_info

    @staticmethod
    def res_handler(event, context, result, exc_info):
        data = (context, result, exc_info)
        event.send(data)
        return result, exc_info

    def handle_response(self, request, context, result):
        raise NotImplementedError
    
    def handle_exception(self, request, context, exc_info):
        raise NotImplementedError


class WebServerHandler(BaseWebServerHandler):
    def handle_request(self, request):
        context, result, exc_info = super(WebServerHandler, self).handle_request(request)
        return (
            self.handle_response(request, context, result)
            if exc_info is None else
            self.handle_exception(request, context, exc_info)
        )

    def handle_response(self, request, context, result):
        if isinstance(result, Response):
            return result
        headers = None
        if isinstance(result, tuple):
            if len(result) == 3:
                payload, headers, status = result
            else:
                payload, status = result
        else:
            payload, status = result, 200
        return Response(payload, status=status, headers=headers)

    def handle_exception(self, request, context, exc_info):
        exc_type, exc_value, exc_trace = exc_info
        if isinstance(exc_value, BadRequest):
            status = 400
        else:
            status = 500
        headers = {'Content-Type': 'text/html; charset=utf-8'}
        exc_data = gen_exc_to_data(exc_value)
        payload = '''
        <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
        <title>{status} {exc_type}</title>
        <h1>{exc_type}</h1>
        <p>{exc_mesg}</p>'''.format(status=status, **exc_data)
        return Response(payload, status=status, headers=headers)


class ApiServerHandler(BaseWebServerHandler):
    def handle_request(self, request):
        context, result, exc_info = super(ApiServerHandler, self).handle_request(request)
        return (
            self.handle_response(request, context, result)
            if exc_info is None else
            self.handle_exception(request, context, exc_info)
        )
    
    def handle_response(self, request, context, result):
        headers = {'Content-Type': 'application/json'}
        call_id = context.call_id.split('.')[-1]
        payload = {
            'code': 'Request:Success',
            'errs': '',
            'data': result,
            'call_id': call_id,
        }
        payload = json.dumps(payload)
        return Response(payload, status=200, headers=headers)
    
    def handle_exception(self, request, context, exc_info):
        exc_type, exc_value, exc_trace = exc_info
        headers = {'Content-Type': 'application/json'}
        call_id = context.call_id.split('.')[-1]
        exc_name = exc_type.__name__
        payload = {
            'code': 'ServerError:{0}'.format(exc_name),
            'errs': six.text_type(exc_value),
            'data': None,
            'call_id': call_id,
        }
        payload = json.dumps(payload)
        return Response(payload, status=200, headers=headers)
