
from datetime import date, datetime, timedelta
#from fastapi import Depends, FastAPI, HTTPException, Path, status, APIRouter
from fastapi import APIRouter, HTTPException, Depends, status, Path
from sqlalchemy.orm import Session

from database.db import get_db
from database.models import Contact, User
from schemas import ContactResponse, ContactSchema

from services.auth import get_current_user

router = APIRouter(prefix='/contacts', tags=["contacts"])

@router.get("/")
def main_root():
    return {"message": "Hello, fastapi application!"}

@router.post("/contacts/", response_model=ContactResponse)
async def create_contact(body: ContactSchema, db: Session = Depends(get_db)):
    #new_contact = Contact(**contact.dict())
    contact = db.query(Contact).filter_by(email=body.email).first()
    if contact:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Contact already exists!")
    contact=Contact(fullname=body.fullname, phone_number=body.phone_number, email=body.email, birthday =body.birthday)
    # Создаем новый контакт
    # new_contact = Contact(**body.dict())
    db.add(contact)
    db.commit()
    return contact

@router.get("/contacts", response_model=list[ContactResponse])
#async def get_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
async def get_contacts(db: Session = Depends(get_db)):
    contacts = db.query(Contact).all()
    return contacts

@router.get("/contacts/id/{contact_id}", response_model=ContactResponse)
async def get_contact_by_id(contact_id: int = Path(ge=1), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return contact

@router.get("/contacts/by_name/{contact_fullname}", response_model=ContactResponse)
async def get_contact_by_fullname(contact_fullname: str = Path(...), db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    contact = db.query(Contact).filter(Contact.fullname.ilike(f"%{contact_fullname}%")).first()
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

@router.get("/contacts/by_email/{contact_email}", response_model=ContactResponse)
async def get_contact_by_email(contact_email: str = Path(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    print("Searching for contact with name:", contact_email)
    contact = db.query(Contact).filter(Contact.email.ilike(f"%{contact_email}%")).first()
    print("Found contact:", contact)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

@router.get("/contacts/by_birthday/{get_birthday}", response_model=list[ContactResponse])
async def get_upcoming_birthdays(db: Session = Depends(get_db)):
    current_date = date.today()
    future_date = current_date + timedelta(days=7)
    contacts = db.query(Contact).filter(current_date >= Contact.birthday, Contact.birthday <= future_date).all()
    print(contacts)
    return contacts

@router.get("/contacts/get_new_day/{new_date}", response_model=list[ContactResponse])
async def get_upcoming_birthdays_from_new_date(new_date: str = Path(..., description="Current date in format YYYY-MM-DD"),db: Session = Depends(get_db)):
    new_date_obj = datetime.strptime(new_date,"%Y-%m-%d").date()
    future_date = new_date_obj + timedelta(days=7)
    contacts = db.query(Contact).filter(Contact.birthday >= new_date_obj, Contact.birthday <= future_date).all()
    
    print(contacts)
    return contacts

@router.put("/contacts/update/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactSchema, contact_id: int = Path(ge=1),db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    contact = db.query(Contact).filter_by(id = contact_id).first()
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    
    contact.fullname = body.fullname
    contact.email = body.email
    contact.phone_number = body.phone_number
    contact.birthday = body.birthday

    db.commit()
    return contact

@router.delete("/contacts/{contact_id}", response_model=ContactResponse)
async def delete_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    contact = db.query(Contact).filter_by(id = contact_id).first()
    if contact is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Contact does not exist or you do not have permission to delete it.")
    db.delete(contact)
    db.commit()
    return contact