import dotenv
import os
import logging
import aiosqlite

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

dotenv.load_dotenv()

from components.application import ApplicationContext, ApplicationCore

async def get_database():
    return await aiosqlite.connect('./database.db')

def get_context():
    return ApplicationContext(
        get_database
    )

token = os.getenv('ACCESS_TOKEN')

if token is None:
    raise Exception('Missing ACCESS_TOKEN in environment variables')

app = ApplicationCore(get_context, token)

#Register components

app.run()