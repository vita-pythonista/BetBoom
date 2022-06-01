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
async def user_registration_handler(request: web.Request) -> web.Response:
    payload = await request.json()

    registered_user: models.User = models.User(
        login=payload.get('user').get('login'),
        password=payload.get('user').get('password'),
    )

    if registered_user.login in storage.USERS:
        return web.json_response({
            'success': False,
            'error': 'User already exist',
        }, status=400)

    storage.USERS[registered_user.login] = registered_user

    return web.json_response({
        'success': True,
        'result': {
            'user': registered_user.api_mapping()
        }
    }, status=201)
