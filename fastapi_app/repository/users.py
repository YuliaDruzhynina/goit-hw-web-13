
from fastapi import Depends
from libgravatar import Gravatar
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from fastapi_project.fastapi_app.database.db import get_db
from fastapi_project.fastapi_app.database.models import User
from fastapi_project.fastapi_app.schemas import UserModel


async def get_user_by_email(email: str, db: AsyncSession = Depends(get_db)):
        stmt = select(User).filter_by(email=email)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        return user

# async def get_user_by_email(email: str, db: Session) -> User:
#     return db.query(User).filter(User.email == email).first()

async def create_user(body: UserModel, db: Session) -> User:
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.dict(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    user.refresh_token = token
    db.commit()