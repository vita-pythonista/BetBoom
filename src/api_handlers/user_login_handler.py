import uuid

from aiohttp import web

import decorators
import models
import storage


@decorators.validator_decorator({
    "type": "object",
    "properties": {
        "user": {
            "type": "object",
            "properties": {
                "login": {
                    "type": "string",
                    "maxLength": 50,
                    "minLength": 3
                },
                "password": {
                    "type": "string",
                    "maxLength": 25,
                    "minLength": 5
                }
            },
            "required": ["login", "password"]
        },
    },
}, 'body')
async def user_login_handler(request: web.Request) -> web.Response:
    payload = await request.json()

    user_data = payload.get('user')
    found_user: models.User = storage.USERS.get(user_data.get('login'))

    if not found_user:
        return web.json_response({
            'success': False,
            'error': 'User not found'
        })
    elif not found_user.check_password(user_data.get('password')):
        return web.json_response({
            'success': False,
            'error': 'Incorrect password'
        })

    session_id = str(uuid.uuid4())

    storage.SESSIONS[session_id] = {'login': found_user.login}

    return web.json_response({
        'success': True,
        'result': {
            'ssid': session_id,
            'user': found_user.api_mapping(),
        },
    })
