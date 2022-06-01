from typing import Dict

from aiohttp import web

import decorators
import models
import storage
from decorators import check_auth_decorator


@check_auth_decorator
@decorators.validator_decorator({
    "type": "object",
    "properties": {
        "contact": {
            "type": "object",
            "properties": {
                "type": {
                    "type": "string",
                    "enum": ["email", "phone"]
                },
                "content": {
                    "type": "string",
                    "maxLength": 25,
                    "minLength": 1
                }
            },
            "required": ["type", "content"]
        },
    }
}, 'body')
async def user_add_contact_handler(request: web.Request, session: Dict) -> web.Response:
    payload = await request.json()
    contact_data = payload.get('contact')

    created_contact: models.Contact = models.Contact(
        contact_type=contact_data.get('type'),
        content=contact_data.get('content'),
    )

    user: models.User = storage.USERS.get(session.get('login'))
    if not user.add_contact(created_contact):
        return web.json_response({
            'success': False,
            'error': 'Contact already exist'
        }, status=400)

    return web.json_response({
        'success': True,
        'result': {
            'user': user.api_mapping()
        }
    }, status=200)
