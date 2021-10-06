from aiohttp import web
from .routes import setup_routes
from logger import log


def create_app(config):
    app = web.Application()
    app['config'] = config
    setup_routes(app)
    app.on_startup.append(on_start)
    app.on_cleanup.append(on_shutdown)
    return app


async def on_start(app: web.Application):
    log.info('Bound api on %s:%s', app["config"].get("host"), app["config"].get("port"))


async def on_shutdown(app: web.Application):
    log.info('Unbound api on %s:%s', app["config"].get("host"), app["config"].get("port"))
