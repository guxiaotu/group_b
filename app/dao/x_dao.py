from app.config.database import SessionLocal
from app.model.entity import X


def save_data(x_list: list[X]):
    # 离线版得手工注入数据
    with SessionLocal() as s:
        s.add_all(x_list)
        s.commit()
