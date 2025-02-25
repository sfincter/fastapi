from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel, EmailStr, field_validator
from typing import List

app = FastAPI()


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


# Храним список активных WebSocket соединений
active_connections: List[WebSocket] = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """ WebSocket для автоматического обновления списка специалистов. """
    await websocket.accept()
    active_connections.append(websocket)

    try:
        while True:
            await websocket.receive_text()  # Ожидание сообщений (не используется)
    except:
        active_connections.remove(websocket)



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



@app.post('/specialists')
async def create_specialist(new_specialist: NewSpecialist):
    new_data = {
        'id': len(specialists) + 1,
        'role': new_specialist.role,
        'name': new_specialist.name,
        'email': new_specialist.email,
    }
    specialists.append(new_data)

    # Логируем перед отправкой
    print("📡 Отправка обновлений через WebSocket:", specialists)

    # Отправляем обновленный список клиентам
    for connection in active_connections:
        await connection.send_json(specialists)

    return {'success': True, 'message': 'Специалист добавлен'}




@app.get('/', summary='Главная ручка', tags=['Основные ручки'])
def home():
    return 'Hello from fastapi'


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)