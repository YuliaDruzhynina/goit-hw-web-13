#from typing import List
import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class ContactSchema(BaseModel):
    fullname: str
    email: EmailStr
    phone_number:str
    birthday: datetime.date
    #birthdate: str

    class Config:
        from_attributes = True

class ContactResponse(ContactSchema):
    id: int
   

    class Config:
        from_attributes = True 
        orm_mode=True
        #orm_mode = True

class UserModel(BaseModel):
    username: str
    password: str
    refresh_token: Optional[str] = None
 
    class Config:
        from_attributes = True  

class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class Config:
        orm_mode = True        

class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"        
    

class RequestEmail(BaseModel):
    email: EmailStr

class EmailSchema(BaseModel):
    email: EmailStr

class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


# class ContactUpdate(BaseModel):
#     fullname: Optional[str]
#     email: Optional[EmailStr]
#     phone_number: Optional[str]
#     birthday: Optional[datetime.date]

#     class Config:
#         orm_mode = True