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
    conn = await aiosqlite.connect('./database.db')
    conn.row_factory = aiosqlite.Row
    return conn

def get_context():
    return ApplicationContext(
        get_database
    )

token = os.getenv('ACCESS_TOKEN')

if token is None:
    raise Exception('Missing ACCESS_TOKEN in environment variables')

app = ApplicationCore(get_context, token)

#Register components
from components.MainMenuComponent import MainMenuComponent
app.add_component(lambda x: MainMenuComponent(x))

from components.SearchByNameComponent import SearchByNameComponent
app.add_component(lambda x: SearchByNameComponent(x))

app.run()