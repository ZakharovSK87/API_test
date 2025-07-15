import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def classify_category(text: str) -> str:
    try:
        prompt = (
            f'Определи категорию жалобы: "{text}". '
            'Варианты: техническая, оплата, другое. Ответ только одним словом.'
        )

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=10
        )

        result = response.choices[0].message.content.strip().lower()

        if result in ["техническая", "оплата", "другое"]:
            return result
        return "другое"

    except Exception as e:
        print(f"[OpenAI ERROR] {e}")
        return "другое"
