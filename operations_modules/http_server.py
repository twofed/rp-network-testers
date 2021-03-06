"""
    'KootNet Ethernet Testers' is a collection of scripts and programs
    to test Ethernet cables and or network routes.
    Copyright (C) 2018  Chad Ermacora  chad.ermacora@gmail.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from time import sleep
from flask import Flask
from flask_compress import Compress
from gevent.pywsgi import WSGIServer
from operations_modules import http_server_routes
from operations_modules.app_variables import flask_http_ip, flask_http_port


class CreateHTTPServer:
    def __init__(self):
        app = Flask(__name__)
        Compress(app)
        app.register_blueprint(http_server_routes.http_routes)

        try:
            http_server = WSGIServer((flask_http_ip, flask_http_port), app)
            http_server.serve_forever()
        except Exception as error:
            print("\nError Starting HTTP Server: " + str(error) + "\n")
            while True:
                sleep(600)
