from fastapi import FastAPI, HTTPException
import asyncio
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel, EmailStr, field_validator

app = FastAPI()


# Переменная для отслеживания изменений
data_updated = False

# Пример ручки для long polling
@app.get("/long-poll")
async def long_poll():
    global data_updated

    # Ждем, пока данные не изменятся
    while not data_updated:
        await asyncio.sleep(1)  # Пауза между проверками (если нужно)

    # Как только данные обновляются, отправляем ответ
    data_updated = False  # Сбрасываем флаг изменений
    return {"specialists": specialists}



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
@app.post("/specialists")
async def add_specialist(name: str, role: str):
    new_id = len(specialists) + 1
    specialists.append({"id": new_id, "name": name, "role": role})

    # Помечаем, что данные обновились
    global data_updated
    data_updated = True

    return {"message": "Специалист добавлен"}




@app.get('/', summary='Главная ручка', tags=['Основные ручки'])
def home():
    return 'Hello from fastapi'


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)