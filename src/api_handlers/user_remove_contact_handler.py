from typing import Dict

from aiohttp import web

import models
import storage
import decorators


@decorators.check_auth_decorator
async def user_remove_contact_handler(request: web.Request, session: Dict) -> web.Response:
    contact_id: int = int(request.match_info.get('contact_id'))

    user: models.User = storage.USERS.get(session.get('login'))
    if not user.remove_contact(contact_id):
        return web.json_response({
            'success': False,
            'error': 'Nothing to remove'
        }, status=400)

    return web.json_response({
        'success': True,
        'result': {
            'user': user.api_mapping()
        }
    }, status=200)
