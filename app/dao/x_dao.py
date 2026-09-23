from app.config.database import get_session
from app.model.x import X


def save_data(x_list: list[X]):
    session = get_session()
    with session as s:
        s.add_all(x_list)
        s.commit()
