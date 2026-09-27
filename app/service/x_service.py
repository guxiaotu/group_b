import asyncio

from app.dao import x_dao
from app.data_mining import data_mining


async def save_data():
    await x_dao.save_data(await data_mining.read_data())
