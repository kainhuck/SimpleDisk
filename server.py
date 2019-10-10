#!/usr/bin/python3
# -*- coding: utf-8 -*-

import config

from application import Application

from tornado import ioloop, httpserver, options

if __name__ == '__main__':
    application = Application()
    http_server = httpserver.HTTPServer(application)
    http_server.bind(config.options['port'])
    http_server.start(1)

    ioloop.IOLoop.current().start()