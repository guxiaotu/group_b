from app.dao import x_dao
from app.data_mining import data_mining


def save_data():
    x_dao.save_data(data_mining.get_data())
