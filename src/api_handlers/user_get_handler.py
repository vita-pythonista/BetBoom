from typing import Dict

from aiohttp import web

import models
import storage
from decorators import check_auth_decorator


@check_auth_decorator
async def user_get_handler(request: web.Request, session: Dict) -> web.Response:
    user: models.User = storage.USERS.get(session.get('login'))

    return web.json_response({
        'success': True,
        'result': {
            'user': user.api_mapping(),
        }
    })
