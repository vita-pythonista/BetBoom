from typing import Callable

from aiohttp import web

import storage


def check_auth_decorator(decorable: Callable) -> Callable:
    def decorator(request: web.Request):
        session = storage.SESSIONS.get(request.headers['ssid'])

        if not session:
            return web.json_response({
                'success': False,
                'error': 'User is not authorized'
            }, status=401)

        return decorable(request, session=session)

    return decorator
