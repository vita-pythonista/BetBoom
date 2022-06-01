from typing import Dict

import aiohttp_jinja2
from aiohttp import web

import models
import storage


def user_page_handler(request: web.Request):
    ssid: str = request.match_info.get('ssid')

    session: Dict = storage.SESSIONS.get(ssid)
    if not session:
        return aiohttp_jinja2.render_template(
            'user_page_error.html', request, {'error': 'Session %s is not exist' % ssid})

    user: models.User = storage.USERS.get(session.get('login'))
    if not user:
        return aiohttp_jinja2.render_template(
            'user_page_error.html', request, {'error': 'User with login %s not found' % user.login})

    return aiohttp_jinja2.render_template('user_page.html', request, {'user': user})
