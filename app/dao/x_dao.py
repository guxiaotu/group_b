from typing import List

from app.config.database import get_session
from app.model.entity import X


def save_data(x_list: List[X]):
    session = get_session()
    with session as s:
        s.add_all(x_list)
        s.commit()
