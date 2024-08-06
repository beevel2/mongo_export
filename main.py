import asyncio
import os
import json

from motor.motor_asyncio import (AsyncIOMotorClient, AsyncIOMotorDatabase)

import config


def _connect_to_db() -> AsyncIOMotorDatabase:
    client = AsyncIOMotorClient(config.mongo_uri)
    db = client[config.db_name]
    return db

db_connection = _connect_to_db()


async def main():
    col = db_connection[config.col_name]

    try:
        os.remove(f'{config.field_name}.json')
    except Exception as e:
        pass
    
    output_data = [i[config.field_name] for i in (await col.find().to_list(999999999999999999))]

    with open(f'{config.field_name}.json', 'w') as file:
        json.dump(output_data, file)


asyncio.run(main())
