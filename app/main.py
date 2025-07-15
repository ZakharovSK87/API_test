from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from . import models, schemas, database, sentiment, spam, geolocation
from .openai_utils import classify_category
from fastapi.middleware.cors import CORSMiddleware
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Разрешаем CORS для Swagger UI и тестов
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

# Зависимость для получения сессии БД
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
    try:
        # Валидация входных данных
        if not complaint.text or len(complaint.text.strip()) == 0:
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        if len(complaint.text) > 1000:
            raise HTTPException(status_code=400, detail="Text too long (max 1000 characters)")

        # 1. Анализ тональности через APILayer
        try:
            sentiment_result = await sentiment.analyze_sentiment(complaint.text)
        except Exception as e:
            logger.error(f"Sentiment analysis error: {e}")
            sentiment_result = "unknown"

        # 2. Геолокация по IP клиента
        try:
            client_ip = request.client.host
            country = await geolocation.get_country_by_ip(client_ip)
        except Exception as e:
            logger.error(f"Geolocation error: {e}")
            country = "unknown"

        # 3. Спам-фильтр через API Ninjas
        try:
            spam_flag = await spam.is_spam_text(complaint.text)
        except Exception as e:
            logger.error(f"Spam detection error: {e}")
            spam_flag = False

        # 4. Создание записи без категории
        new_complaint = models.Complaint(
            text=complaint.text,
            sentiment=sentiment_result,
            country=country,
            is_spam=spam_flag
        )
        db.add(new_complaint)
        db.commit()
        db.refresh(new_complaint)

        # 5. Категория через OpenAI
        try:
            category_result = await classify_category(complaint.text)
            new_complaint.category = category_result
            db.commit()
            db.refresh(new_complaint)
        except Exception as e:
            logger.error(f"OpenAI classification error: {e}")
            new_complaint.category = "другое"
            db.commit()

        # 6. Возврат ответа
        return schemas.ComplaintResponse(
            id=new_complaint.id,
            status=new_complaint.status,
            sentiment=new_complaint.sentiment,
            category=new_complaint.category,
            country=new_complaint.country,
            is_spam=new_complaint.is_spam
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in create_complaint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
