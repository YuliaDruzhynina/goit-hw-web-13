#uvicorn main:app --host 127.0.0.1 --port 8000 --reload
from fastapi import FastAPI
from dotenv import load_dotenv

from routes.contact_router import router as contact_router
from routes.auth_router import router as user_router
from routes.mail_router import router as mail_router
from config import config

load_dotenv()

app = FastAPI()

app.include_router(contact_router, prefix="/contacts", tags=["contacts"])
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(mail_router, prefix="/mail", tags=["mail"])


@app.get("/")
def main_root():
    return {"message": "Hello, fastapi application! Goit-HW modul 13."}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host=config.HOST, port=config.PORT)
    