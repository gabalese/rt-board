import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi
import tornado.gen
import django.core.handlers.wsgi
import json
import os
import time

import rtboard.wsgi
from haas.models import *


class ListMessages(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self, last_id):
        response = yield tornado.gen.Task(self.get_updates, last_id)

        output_dictionary = [{"title": message.title,
                              "author": message.author.name,
                              "text": message.text,
                              "id": message.pk}
                             for message in response]

        self.write(json.JSONEncoder().encode(output_dictionary))
        self.finish()

    def get_updates(self, last_id, callback):
        messages = Message.objects.filter(id__gt=last_id)
        if len(messages) == 0:
            tornado.ioloop.IOLoop.instance().add_timeout(time.time()+0.01, lambda: self.get_updates(last_id, callback))
        else:
            callback(messages)

wsgi_app = tornado.wsgi.WSGIContainer(
    django.core.handlers.wsgi.WSGIHandler())

application = tornado.web.Application([
    (r'/update/(.+)', ListMessages),  # Long polling handler to Tornado, manage updates
    (r'.*', tornado.web.FallbackHandler, dict(fallback=wsgi_app))  # Handler for Django: everything else - see urls.py
], debug=True)

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    port = int(os.environ.get("PORT", 5000))
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()
