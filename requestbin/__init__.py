from requestbin import api, views
from requestbin.filters import *
from werkzeug.middleware.proxy_fix import ProxyFix
import os
from io import StringIO

from flask import Flask
from flask_cors import CORS

import requestbin.config as config

class WSGIRawBody(object):
    def __init__(self, application):
        self.application = application

    def __call__(self, environ, start_response):

        length = environ.get('CONTENT_LENGTH', '0')
        length = 0 if length == '' else int(length)

        body = environ['wsgi.input'].read(length)
        environ['raw'] = body
        environ['wsgi.input'] = StringIO(body.decode())

        # Call the wrapped application
        app_iter = self.application(environ, self._sr_callback(start_response))

        # Return modified response
        return app_iter

    def _sr_callback(self, start_response):
        def callback(status, headers, exc_info=None):

            # Call upstream start_response
            start_response(status, headers, exc_info)
        return callback


app = Flask(__name__)

if os.environ.get('ENABLE_CORS', config.ENABLE_CORS):
    cors = CORS(app, resources={r"*": {
        "origins": os.environ.get('CORS_ORIGINS', config.CORS_ORIGINS)
    }})

app.wsgi_app = WSGIRawBody(ProxyFix(app.wsgi_app))

app.debug = config.DEBUG
app.secret_key = config.FLASK_SESSION_SECRET_KEY

app.jinja_env.filters['status_class'] = status_class
app.jinja_env.filters['friendly_time'] = friendly_time
app.jinja_env.filters['friendly_size'] = friendly_size
app.jinja_env.filters['to_qs'] = to_qs
app.jinja_env.filters['approximate_time'] = approximate_time
app.jinja_env.filters['exact_time'] = exact_time
app.jinja_env.filters['short_date'] = short_date

from .views import views
from .api import api
app.register_blueprint(views)
app.register_blueprint(api)
