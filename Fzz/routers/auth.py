from fastapi import FastAPI, APIRouter, Depends, status , Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Annotated
from datab import SessionLocal
from models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


@router.get("/auth")
async def get_user():
    return {'user': 'authenticated'}


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


# this function will authenticate user against the record in db

def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return True


@router.post("/auth", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency,
                      create_user_request: CreateUserRequest):
    # we cannot directly use he model because we take in the password from the user
    # but stored onlyt he hashed password.
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True
    )

    # return create_user_model
    db.add(create_user_model)
    db.commit()


# token is whatt we are going to return back to the user with all the details
"""
if we use the below code , there is no way for us to accept a username and password 

@router.post("/token")
async def login_for_access_token():
    return 'token'
"""


# python multi part lets you allow OAuth2 password request form

@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return 'Failed Authentication'

    return 'successful authentication'
