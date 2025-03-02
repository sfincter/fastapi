from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'postgres://01955629-3eff-7fa2-b9ec-59979ded6f4f:7cbeeccc-cde6-46e8-9f9b-b42bc7adc5f1@eu-central-1.db.thenile.dev/getbetterDB'

# Создаём движок SQLAlchemy
engine = create_engine(DATABASE_URL)

# Создаём сессию для работы с БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Функция для создания всех таблиц (использует модели из models.py)
def create_tables():
    from models import User
    User.metadata.create_all(bind=engine)
