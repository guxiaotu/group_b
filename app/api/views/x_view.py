from sqlmodel import select

from app.config.database import get_session
from app.model.entity.x import X
from app.model.view import x_view
from app.model.view.x_view import XView


def find_entity():
    session = get_session()
    with session as s:
        statement = select(X)
        x_list = session.exec(statement).all()
        return x_list


def get_view() -> XView:
    x_list = find_entity()
    return XView(
        month=[x.month for x in x_list],
        count=[x.count for x in x_list],
        ratios=[x.ratios for x in x_list],
        sample_count=[x.sample_count for x in x_list],
    )