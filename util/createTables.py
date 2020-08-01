track_work = '''
CREATE TABLE track_work(
    ID SERIAL NOT NULL,
    date_created TIMESTAMP WITH TIME ZONE DEFAULT (now() AT TIME ZONE 'UTC') NOT NULL,
    dp INTEGER DEFAULT 0 NOT NULL,
    graphs INTEGER DEFAULT 0 NOT NULL,
    others INTEGER DEFAULT 0 NOT NULL,
    os BOOLEAN DEFAULT FALSE NOT NULL,
    sys_des BOOLEAN DEFAULT FALSE NOT NULL,
    ml BOOLEAN DEFAULT FALSE NOT NULL,
    PRIMARY KEY (ID)
);
'''

async def addDatabaseTables(pool):
    async with pool.acquire() as connection:
        async with connection.transaction():
            await connection.execute(track_work)


async def main(PG_CONFIG):
    pool = await asyncpg.create_pool(PG_CONFIG['dsn'])
    await addDatabaseTables(pool)

import asyncio
import asyncpg
from dotenv import load_dotenv
from os import getenv
from os.path import dirname, join, exists

import aiohttp
dotenv_path = join(dirname(__file__), '../.env')
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

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(PG_CONFIG))
