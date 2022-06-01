from aiohttp import web

from .application import create_application

web.run_app(create_application(), port=8080)
