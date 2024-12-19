from html.entities import html5
from http.client import HTTPException
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import BaseModel, EmailStr
from decouple import config

class EmailSchema(BaseModel):
    name: str
    email: EmailStr
    message: str

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

conf = ConnectionConfig(
    MAIL_USERNAME = config("MAIL_USERNAME"),
    MAIL_PASSWORD = config("MAIL_PASSWORD"),
    MAIL_FROM = config("MAIL_FROM"),
    MAIL_PORT = config("MAIL_PORT", cast=int),
    MAIL_SERVER = config("MAIL_SERVER"),
    MAIL_STARTTLS = config("MAIL_STARTTLS", cast=bool),
    MAIL_SSL_TLS = config("MAIL_SSL_TLS", cast=bool),
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/contact")
async def simple_send(email: EmailSchema, background_tasks: BackgroundTasks):

    try:
        body = f"""
            <h3> Nuevo Mensaje desde tu portafolio </h3>
            <p> <strong>Nombre:</strong> {email.name} </p>
            <p> <strong>Mail:</strong> {email.email} </p>
            <p> <strong>Mensaje:</strong> {email.message} </p>
            """
        message = MessageSchema(
            subject="Nuevo mensaje desde el portafolio",
            recipients=["az57445@gmail.com"],
            body=body,
            subtype='html'
        )

        fm = FastMail(conf)
        background_tasks.add_task(fm.send_message, message)
        return {"message": "Email enviado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))