import sqlalchemy

from fastapi import APIRouter, Body, HTTPException, Response

from src.exceptions import EmailAlreadyExistsException
from src.schemas_API.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService
from src.api.dependencies import UserIdDep, DBDep

router = APIRouter(prefix='/auth', tags=['Авторизация и аутентификация'])

@router.post(
    '/register',
     summary='Регистрация пользователей',
     description='Тут можно зарегистрировать нового пользователя, введя эл. почту и пароль'
)
async def register_user(db: DBDep, data: UserRequestAdd = Body(openapi_examples={
    '1': {
        'summary': 'Тестовый вариант',
        'value': {
            'email': 'balesiy@mail.ru',
            'password': '123456789'
          }
        }
})
):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    try:
        await db.users.register_user(new_user_data)
    except EmailAlreadyExistsException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)
    await db.commit()
    return {'status': 'OK'}

@router.post(
    '/login',
     summary='Аутентификация пользователя',
     description='Тут можно аутентифицировать пользователя, введя эл. почту и пароль'
)
async def login_user(db: DBDep, response: Response, data: UserRequestAdd = Body(openapi_examples={
    '1': {
        'summary': 'Тестовый вариант',
        'value': {
            'email': 'balesiy@mail.ru',
            'password': '123456789'
          }
        }
})
):
    user = await db.users.get_user_with_hashed_password(email=data.email)
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь с таким email не зарегистрирован")
    if not AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Пароль неверный")
    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie('access_token', access_token)
    return {"access_token": access_token}

@router.get(
    '/me',
    summary='Получаем данные об аутентифицированном пользователе'
)
async def get_me(db: DBDep, user_id: UserIdDep):
    user_data = await db.users.get_one_or_none(id=user_id)
    return user_data

@router.get(
    '/logout',
    summary='Удаляем JWT-токен после того, как пользователь разлогинился'
)
async def delete_jwt_token(response: Response):
    response.delete_cookie(key='access_token')
    return {'status': 'OK'}