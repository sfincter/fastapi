from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel, EmailStr

app = FastAPI()

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



@app.post('/specialists', tags=['Специалисты 👨‍⚕️'], summary='Добавить специалиста')
def create_specialist(new_specialist: NewSpecialist):
    specialists.append ({
        'id': len(specialists) + 1,
        'role': new_specialist.role,
        'name': new_specialist.name,
        'email': new_specialist.email,
    })
    return {'success':True, 'message': 'Специалист добавлен'}



@app.get('/', summary='Главная ручка', tags=['Основные ручки'])
def home():
    return 'Hello from fastapi'


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)