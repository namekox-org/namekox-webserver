#! -*- coding: utf-8 -*-

# author: forcemain@163.com


import eventlet
import werkzeug
import eventlet.wsgi


from werkzeug import Request
from eventlet import wsgi, wrap_ssl
from werkzeug.routing import Rule, Map
from namekox_core.core.service.entrypoint import EntrypointProvider
from namekox_webserver.constants import WEBSERVER_CONFIG_KEY, DEFAULT_WEBSERVER_HOST, DEFAULT_WEBSERVER_PORT


class WsgiApp(object):
    def __init__(self, server):
        self.server = server
        self.urlmap = server.gen_urls_map()

    def __call__(self, environ, start_response):
        request = Request(environ)
        adapter = self.urlmap.bind_to_environ(environ)
        try:
            entrypoint, pvalues = adapter.match()
            request.path_values = pvalues
            response = entrypoint.handle_request(request)
        except werkzeug.exceptions.HTTPException as e:
            response = e
        return response(environ, start_response)


class WebServer(EntrypointProvider):
    SSL_ARGS = [
        'keyfile', 'certfile', 'server_side', 'cert_reqs',
        'ssl_version', 'ca_certs',
        'do_handshake_on_connect', 'suppress_ragged_eofs',
        'ciphers'
    ]

    def __init__(self, *args, **kwargs):
        self.gt = None
        self.host = None
        self.port = None
        self.ev_sock = None
        self.ev_serv = None
        self.accpted = True
        self.sslargs = None
        self.srvargs = None
        self.started = False
        super(WebServer, self).__init__(*args, **kwargs)

    @property
    def _key(self):
        return self.__class__.__name__
    
    def setup(self):
        if self.host is not None and self.port is not None and self.sslargs is not None and self.srvargs is not None:
            return
        config = self.container.config.get(WEBSERVER_CONFIG_KEY, {}).copy()
        self.host = config.pop('host', DEFAULT_WEBSERVER_HOST) or DEFAULT_WEBSERVER_HOST
        self.port = config.pop('port', DEFAULT_WEBSERVER_PORT) or DEFAULT_WEBSERVER_PORT
        self.sslargs = {k: config.pop(k) for k in config if k in self.SSL_ARGS}
        self.sslargs and self.sslargs.update({'server_side': True})
        self.srvargs = config
        self.srvargs and self.srvargs.update({'debug': True})

    def bind(self, container, name):
        ins = container.shared_providers.get(self._key, None)
        if ins is None:
            ins = super(WebServer, self).bind(container, name)
            container.shared_providers[self._key] = ins
        return ins

    def start(self):
        if not self.started:
            self.started = True
            self.ev_sock = eventlet.listen((self.host, self.port))
            self.ev_sock.settimeout(None)
            self.ev_serv = self.get_wsgi_srv()
            self.gt = self.container.spawn_manage_thread(self.handle_connect)

    def stop(self):
        self.accpted = False
        self.gt.kill()
        self.ev_sock.close()

    def handle_connect(self):
        while self.accpted:
            sock, addr = self.ev_sock.accept()
            sock.settimeout(self.ev_serv.socket_timeout)
            self.container.spawn_manage_thread(self.handle_request, args=(sock, addr))

    def handle_request(self, sock, addr):
        connection = [addr, sock, wsgi.STATE_IDLE]
        self.ev_serv.process_request(connection)

    def get_wsgi_app(self):
        return WsgiApp(self)

    def get_wsgi_srv(self):
        sock = self.ev_sock if not self.sslargs else wrap_ssl(self.ev_sock, **self.sslargs)
        addr = self.ev_sock.getsockname()
        return wsgi.Server(sock, addr, self.get_wsgi_app(), **self.srvargs)

    def gen_urls_map(self):
        url_map = Map()
        for entrypoint in self.entrypoints:
            rule = Rule(entrypoint.rule, methods=entrypoint.methods, endpoint=entrypoint)
            url_map.add(rule)
        return url_map

    @staticmethod
    def get_context_from_header(request):
        # TODO: headers to context
        return {}
