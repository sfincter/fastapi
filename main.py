from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import uvicorn
from pydantic import BaseModel, EmailStr, field_validator

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем все домены
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все HTTP методы
    allow_headers=["*"],  # Разрешаем все заголовки
)

# Берем URL из переменной окружения
DATABASE_URL = "postgres://01955629-3eff-7fa2-b9ec-59979ded6f4f:7cbeeccc-cde6-46e8-9f9b-b42bc7adc5f1@eu-central-1.db.thenile.dev/getbetterDB"


@app.get('/')
def check_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("SELECT version();")
        result = cur.fetchone()
        cur.close()
        conn.close()
        return {"message": "✅ БД подключена"}
    except Exception as e:
        return {"error": f"❌ Ошибка подключения: {e}"}


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