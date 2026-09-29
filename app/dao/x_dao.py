from app.config.database import AsyncSessionLocal
from app.model.entity import X


async def save_data(x_list: list[X]):
    # 离线版操作，只能使用AsyncSessionLocal()，yield只能使用路由版Depends依赖注入
    async with AsyncSessionLocal() as s:
        try:
            s.add_all(x_list)
            await s.commit()
        except Exception:
            await s.rollback()
            raise
