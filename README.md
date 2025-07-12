# Система обработки жалоб клиентов (FastAPI + SQLite + API интеграции)

Простое API для приёма и обработки жалоб клиентов с интеграцией анализа тональности, фильтрации спама и определением геолокации по IP.

---

📦 Стек

- [FastAPI](https://fastapi.tiangolo.com/)
- SQLite + SQLAlchemy
- Sentiment Analysis API (APILayer)
- Spam Filter API (API Ninjas)
- IP Geolocation API (ip-api.com)

---

## ⚙️ Установка и запуск

 ## 1 Клонируй репозиторий  

   В терминале пишем команду: 
git clone https://github.com/ZakharovSK87/API_test
cd API_TEST

## 2 Создай виртуальное окружение

python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows


## 3. Установи зависимости

pip install -r requirements.txt

## 4 Настройка .env

Создай файл .env в корне проекта:

APILAYER_API_KEY=your_apilayer_key_here
NINJAS_API_KEY=your_api_ninjas_key_here


## 5  Запуск приложения

В терминале пишем команду:

uvicorn app.main:app --reload

## 6 

Приложение будет доступно на:
📍 http://localhost:8000

Документация Swagger:
📘 http://localhost:8000/docs

## 7  Пример запроса через curl

curl -X POST http://localhost:8000/complaints \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"Не работает оплата на сайте\"}"

  Ответ:

    json

  {
    "id": 1,
    "status": "open",
    "sentiment": "negative",
    "category": "другое",
    "country": "Argentina",
    "is_spam": false
}


## 8 Пример запроса через Postman

    Метод: POST

    URL: http://localhost:8000/complaints

    Headers:

    Content-Type: application/json

    Body (raw JSON):


    {
     "text": "Не приходит код подтверждения"
    }







