from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import EventSourceResponse
import uvicorn
from pydantic import BaseModel, EmailStr, field_validator
import time

app = FastAPI()


@app.get("/events")
async def sse():
    def event_generator():
        while True:
            time.sleep(5)  # симуляция задержки
            yield f"data: {str(specialists)}\n\n"
    
    return EventSourceResponse(event_generator())


# Настройка CORS
origins = [
    "https://fastapi-frontend-three.vercel.app",  # Разрешаем доступ с локального фронтенда
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://fastapi-frontend-three.vercel.app"],  # Разрешаем все домены
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все HTTP методы
    allow_headers=["*"],  # Разрешаем все заголовки
)


specialists = [
    {
        'id': 1,
        'role': 'Психолог',
        'name': 'Иван',
        'email': 'ivan@gmail.ru'
    },
    {
        'id': 2,
        'role': 'Психотерапевт',
        'name': 'Наталья',
        'email': 'node@gmail'
    },
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



# Ручка для добавления нового специалиста
@app.post('/specialists')
def create_specialist(new_specialist: NewSpecialist):
    specialists.append({
        'id': len(specialists) + 1,
        'role': new_specialist.role,
        'name': new_specialist.name,
        'email': new_specialist.email,
    })
    return {'success': True, 'message': 'Специалист добавлен'}




@app.get('/', summary='Главная ручка', tags=['Основные ручки'])
def home():
    return 'Hello from fastapi'


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)