#
Создание системы для обработки жалоб клиентов с интеграцией публичных API

---
Сервис для приёма и анализа жалоб клиентов с интеграцией публичных API:  
Sentiment Analysis, OpenAI, Spam-фильтр, Геолокация по IP и автоматизация в n8n.

📦 Стек

- 🐍 FastAPI + SQLAlchemy
- 💾 SQLite
- 🌍 Sentiment Analysis by APILayer
- 🤖 OpenAI (GPT-3.5)
- 🛡 Spam Check by API Ninjas (опционально)
- 🗺 IP API (геолокация)
- 🔁 Автоматизация: n8n + Telegram + Google Sheets
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
OPENAI_API_KEY=your_api_ninjas_key_here

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

# 9 Автоматизация через n8n
https://darkcoder87.app.n8n.cloud/workflow/0oIAlCSgwVCQbgfN
Каждый час n8n:

Проверяет открытые жалобы за последний час

Отправляет в Telegram технические

Записывает в Google Sheets платёжные

Закрывает статус жалоб

#  10 Cкриншоты в папке docks в проекте.





