import aiohttp_jinja2
import jinja2
from aiohttp import web

import api_handlers
import page_handlers
from middlewares import errors_handling_middleware

API_PATH_PREFIX = '/api/v1'


def create_application(*args) -> web.Application:
    app = web.Application(middlewares=[errors_handling_middleware])
    app.add_routes([
        web.post(
            API_PATH_PREFIX + '/user/registration',
            api_handlers.user_registration_handler
        ),
        web.post(
            API_PATH_PREFIX + '/user/login',
            api_handlers.user_login_handler
        ),
        web.get(
            API_PATH_PREFIX + '/user',
            api_handlers.user_get_handler
        ),
        web.post(
            API_PATH_PREFIX + '/user/contact',
            api_handlers.user_add_contact_handler
        ),
        web.delete(
            API_PATH_PREFIX + r'/user/contact/{contact_id:[0-9]{1,10}}',
            api_handlers.user_remove_contact_handler
        ),

        web.get('/session/{ssid}', page_handlers.user_page_handler)
    ])

    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('./page_handlers/templates'))

    return app
