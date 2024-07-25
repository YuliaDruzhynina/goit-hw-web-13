#uvicorn main:app --host 127.0.0.1 --port 8000 --reload
import sys 
import os
from dotenv import load_dotenv
from fastapi import FastAPI

from fastapi_project.config import config
from fastapi_project.fastapi_app.routes.auth_router import router as user_router
from fastapi_project.fastapi_app.routes.contact_router import router as contact_router
from fastapi_project.fastapi_app.routes.email_router import router as mail_router
    
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

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
    