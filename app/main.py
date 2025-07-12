from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from . import models, schemas, database, sentiment
from .spam import is_spam_text
from .geolocation import get_country_by_ip
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/complaints", response_model=schemas.ComplaintResponse)
async def create_complaint(
    complaint: schemas.ComplaintCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    # 1. Анализ тональности через APILayer
    sentiment_result = await sentiment.analyze_sentiment(complaint.text)

    # 2. Геолокация клиента по IP
    client_ip = request.client.host
    country = await get_country_by_ip(client_ip)

    # 3. Проверка на спам
    spam = await is_spam_text(complaint.text)

    # Можно логировать или обрабатывать
    print(f"IP: {client_ip}, Country: {country}, Spam: {spam}")

    new_complaint = models.Complaint(
        text=complaint.text,
        sentiment=sentiment_result,
        # ты можешь сюда добавить поля country / is_spam, если они есть в модели
    )

    db.add(new_complaint)
    db.commit()
    db.refresh(new_complaint)

    return schemas.ComplaintResponse(
        id=new_complaint.id,
        status=new_complaint.status,
        sentiment=new_complaint.sentiment,
        category=new_complaint.category
    )
