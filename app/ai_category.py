# app/ai_category.py

import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

async def categorize_complaint(text: str) -> str:
    prompt = (
        f'Определи категорию жалобы: "{text}". '
        'Варианты: техническая, оплата, другое. Ответ только одним словом.'
    )

    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=10
        )
        category = response.choices[0].message.content.strip().lower()

        # Безопасная проверка
        if category in ["техническая", "оплата", "другое"]:
            return category
        return "другое"

    except Exception as e:
        print(f"Ошибка OpenAI: {e}")
        return "другое"
