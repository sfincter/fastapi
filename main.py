from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel, EmailStr, field_validator
from database import create_tables
from databases import Database

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем все домены
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все HTTP методы
    allow_headers=["*"],  # Разрешаем все заголовки
)

DATABASE_URL = 'postgres://01955629-3eff-7fa2-b9ec-59979ded6f4f:7cbeeccc-cde6-46e8-9f9b-b42bc7adc5f1@eu-central-1.db.thenile.dev/getbetterDB'

database = Database(DATABASE_URL)


# Создание таблиц и другие действия с БД
def create_tables():
    from models import Base
    Base.metadata.create_all(bind=database)

@app.on_event("startup")
async def startup():
    try:
        await database.connect()  # Подключаемся к базе данных
        create_tables()  # Создание таблиц при запуске
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при подключении или создании таблиц: {str(e)}")

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()  # Отключаемся от базы данных

@app.get("/")
def check_db():
    return {"message": "✅ БД подключена и таблицы созданы"}


specialists = [
    {'id': 1, 'role': 'Психолог', 'name': 'Иван', 'email': 'ivan@dbtplus.ru'},
    {'id': 2, 'role': 'Психотерапевт', 'name': 'Наталья', 'email': 'node@dbtplus.ru'},
]

@app.get('/specialists', tags=['Специалисты 👨‍⚕️'], summary='Показать всех специалистов')
def all_specialists():
    return specialists

@app.get('/specialists/{spec_id}', tags=['Специалисты 👨‍⚕️'], summary='Найти конкретного специалиста')
def get_specialist(spec_id: int):
    for specialist in specialists:
        if specialist['id'] == spec_id:
            return specialist
    raise HTTPException(status_code=404, detail='Специалист не найден')

class NewSpecialist(BaseModel):
    role: str
    name: str
    email: EmailStr

    @field_validator("email")
    @classmethod
    def validate_email_domain(cls, value: str):
        if not value.endswith("@dbtplus.ru"):
            raise ValueError("Email должен заканчиваться на @dbtplus.ru")
        return value

@app.post('/specialists', tags=['Специалисты 👨‍⚕️'], summary='Добавить специалиста')
def create_specialist(new_specialist: NewSpecialist):
    new_id = len(specialists) + 1
    specialist = {
        'id': new_id,
        'role': new_specialist.role,
        'name': new_specialist.name,
        'email': new_specialist.email,
    }
    specialists.append(specialist)
    return {'success': True, 'message': 'Специалист добавлен', 'id': new_id}

@app.delete('/specialists/{spec_id}', tags=['Специалисты 👨‍⚕️'], summary='Удалить специалиста')
def delete_specialist(spec_id: int):
    global specialists
    for specialist in specialists:
        if specialist['id'] == spec_id:
            specialists = [s for s in specialists if s['id'] != spec_id]
            return {'success': True, 'message': f'Специалист с ID {spec_id} удален'}
    raise HTTPException(status_code=404, detail='Специалист не найден')

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True) 