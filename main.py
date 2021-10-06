import sys
from pathlib import Path
# Добавляем пути глобальных модулей/моделей
sys.path.append((Path(__file__).parent / 'globals').as_posix())

from dotenv import load_dotenv
load_dotenv()

import asyncio

from aiohttp import web
from rest_api import create_app
from logger import log
from services.config_loader import load_config


if __name__ == '__main__':
    log.info('Start')
    loop = asyncio.get_event_loop()

    config = load_config()

    app = create_app(config.get('api'))
    runner = web.AppRunner(app)

    loop.run_until_complete(runner.setup())
    site = web.TCPSite(runner, host=app['config'].get('host'), port=app['config'].get('port'))

    # Run app
    loop.run_until_complete(site.start())
    loop.run_forever()
