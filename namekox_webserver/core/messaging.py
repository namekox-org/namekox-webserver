#! -*- coding: utf-8 -*-

# author: forcemain@163.com


import six
import anyjson


from namekox_xmlrpc.constants import DEFAULT_XMLRPC_H_PREFIX


def gen_message_headers(context):
    headers = {}
    for k, v in six.iteritems(context):
        k = '{}-'.format(DEFAULT_XMLRPC_H_PREFIX) + k
        headers.update({k: anyjson.serialize(v)})
    return headers


def get_message_headers(message):
    headers = {}
    for k, v in six.iteritems(message.headers):
        p = '{}-'.format(DEFAULT_XMLRPC_H_PREFIX)
        k.startswith(p) and headers.update({k[len(p):]: anyjson.deserialize(v)})
    return headers
