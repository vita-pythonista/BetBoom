from typing import Callable, Dict

import jsonschema
from aiohttp import web


async def _extract_data(request: web.Request, extractor: str):
    if extractor == 'body':
        return await request.json()
    elif extractor == 'path':
        return \
            dict(request.match_info)
    elif extractor == 'query':
        return dict(request.query)


def validator_decorator(schema: Dict, extractor: str) -> Callable:
    def decorator(target: Callable):
        async def decorated(request: web.Request, *args, **kwargs):
            payload = await _extract_data(request, extractor)
            try:
                jsonschema.validate(payload, schema)
                return await target(request, *args, **kwargs)
            except jsonschema.ValidationError as error:
                return web.json_response({
                    'success': False,
                    'error': 'Invalid field %s. %s' % ('.'.join(error.absolute_path), error.message)
                }, status=400)

        return decorated

    return decorator
