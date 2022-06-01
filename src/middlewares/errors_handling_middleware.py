from typing import Callable

from aiohttp import web


@web.middleware
async def errors_handling_middleware(request: web.Request, handler: Callable):
    try:
        return await handler(request)
    except web.HTTPError as http_error:
        return web.json_response({
            'success': False,
            'error': str(http_error)
        }, status=http_error.status)
    except Exception:
        return web.json_response({
            'success': False,
            'error': 'Unexpected server error'
        }, status=500)
