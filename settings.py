import asyncio
import logging
from os import getenv, makedirs, mkdir, remove
from os.path import dirname, exists, join, splitext

import aiohttp
import asyncpg
from dotenv import load_dotenv
from tornado.web import escape, HTTPError
from tornado.ioloop import IOLoop

# Configuring logging to show timestamps
logging.basicConfig(format='[%(asctime)s] p%(thread)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG
)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

PG_CONFIG = {
    'user': getenv('DB_USER'),
    'pass': getenv('DB_PASS'),
    'host': getenv('DB_HOST'),
    'database': getenv('DB_NAME'),
    'port': getenv('DB_PORT')
}
PG_CONFIG['dsn'] = "postgres://%s:%s@%s:%s/%s" % (PG_CONFIG['user'], PG_CONFIG['pass'],
                                                  PG_CONFIG['host'], PG_CONFIG['port'], PG_CONFIG['database'])


################################################################################################################################


async def get_config():
    return {
        'template_path': join(dirname(__file__), 'template'),
        'static_path': join(dirname(__file__), 'static'),
        'pool': await asyncpg.create_pool(PG_CONFIG['dsn']),
        'log': logging.getLogger()
    }
################################################################################################################################


