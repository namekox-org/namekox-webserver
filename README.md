# Install
```shell script
pip install -U namekox-webserver
```

# Example
> ping.py
```python
#! -*- coding: utf-8 -*-

# author: forcemain@163.com
from __future__ import unicode_literals


from namekox_webserver.core.entrypoints.app import app


class Ping(object):
    name = 'ping'

    @app.api('/api/ping', methods=['GET'])
    def api_ping(self, request):
        return {'success': True}

    @app.web('/web/ping', methods=['GET'])
    def web_ping(self, request):
        return 'success'
```

# Running
> namekox run ping
```shell script
2020-09-19 11:13:14,217 DEBUG load service classes from ping
2020-09-19 11:13:14,375 DEBUG load container class from namekox_core.core.service.container:ServiceContainer
2020-09-19 11:13:14,376 DEBUG starting services ['ping']
2020-09-19 11:13:14,376 DEBUG starting service ping entrypoints [ping:namekox_webserver.core.entrypoints.app.server.WebServer:server, ping:namekox_webserver.core.entrypoints.app.handler.ApiServerHandler:api_ping, ping:namekox_webserver.core.entrypoints.app.handler.WebServerHandler:web_ping]
2020-09-19 11:13:14,379 DEBUG spawn manage thread handle ping:namekox_webserver.core.entrypoints.app.server:handle_connect(args=(), kwargs={}, tid=handle_connect)
2020-09-19 11:13:14,379 DEBUG service ping entrypoints [ping:namekox_webserver.core.entrypoints.app.server.WebServer:server, ping:namekox_webserver.core.entrypoints.app.handler.ApiServerHandler:api_ping, ping:namekox_webserver.core.entrypoints.app.handler.WebServerHandler:web_ping] started
2020-09-19 11:13:14,379 DEBUG starting service ping dependencies []
2020-09-19 11:13:14,379 DEBUG service ping dependencies [] started
2020-09-19 11:13:14,380 DEBUG services ['ping'] started
2020-09-19 11:13:20,118 DEBUG spawn manage thread handle ping:namekox_webserver.core.entrypoints.app.server:handle_request(args=(<eventlet.greenio.base.GreenSocket object at 0x105e98850>, ('127.0.0.1', 52535)), kwargs={}, tid=handle_request)
2020-09-19 11:13:20,143 DEBUG spawn worker thread handle ping:api_ping(args=(<Request 'http://127.0.0.1/api/ping' [GET]>,), kwargs={}, context={})
127.0.0.1 - - [19/Sep/2020 11:13:20] "GET /api/ping HTTP/1.1" 200 250 0.003394
2020-09-19 11:13:24,085 DEBUG spawn worker thread handle ping:web_ping(args=(<Request 'http://127.0.0.1/web/ping' [GET]>,), kwargs={}, context={})
127.0.0.1 - - [19/Sep/2020 11:13:24] "GET /web/ping HTTP/1.1" 200 147 0.000966
2020-09-19 11:13:28,714 DEBUG stopping services ['ping']
2020-09-19 11:13:28,714 DEBUG stopping service ping entrypoints [ping:namekox_webserver.core.entrypoints.app.server.WebServer:server, ping:namekox_webserver.core.entrypoints.app.handler.ApiServerHandler:api_ping, ping:namekox_webserver.core.entrypoints.app.handler.WebServerHandler:web_ping]
2020-09-19 11:13:28,715 DEBUG wait service ping entrypoints [ping:namekox_webserver.core.entrypoints.app.server.WebServer:server, ping:namekox_webserver.core.entrypoints.app.handler.ApiServerHandler:api_ping, ping:namekox_webserver.core.entrypoints.app.handler.WebServerHandler:web_ping] stop
2020-09-19 11:13:28,715 DEBUG service ping entrypoints [ping:namekox_webserver.core.entrypoints.app.server.WebServer:server, ping:namekox_webserver.core.entrypoints.app.handler.ApiServerHandler:api_ping, ping:namekox_webserver.core.entrypoints.app.handler.WebServerHandler:web_ping] stopped
2020-09-19 11:13:28,715 DEBUG stopping service ping dependencies []
2020-09-19 11:13:28,716 DEBUG service ping dependencies [] stopped
2020-09-19 11:13:28,716 DEBUG services ['ping'] stopped
2020-09-19 11:13:28,716 DEBUG killing services ['ping']
2020-09-19 11:13:28,716 DEBUG service ping already stopped
2020-09-19 11:13:28,717 DEBUG services ['ping'] killed
```
