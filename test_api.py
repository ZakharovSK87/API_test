import requests
import json

def test_api():
    """Тестирование API жалоб"""
    
    # URL API
    base_url = "http://localhost:8000"
    
    # Тест 1: Проверка здоровья сервиса
    print("1. Тестирование health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Тест 2: Создание жалобы
    print("2. Тестирование создания жалобы...")
    test_complaint = {
        "text": "У меня проблема с оплатой заказа #12345"
    }
    
    try:
        response = requests.post(
            f"{base_url}/complaints",
            json=test_complaint,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   Response: {json.dumps(result, indent=2, ensure_ascii=False)}")
        else:
            print(f"   Error Response: {response.text}")
            
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Тест 3: Тест с пустым текстом
    print("3. Тестирование с пустым текстом...")
    empty_complaint = {
        "text": ""
    }
    
    try:
        response = requests.post(
            f"{base_url}/complaints",
            json=empty_complaint,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")

if __name__ == "__main__":
    test_api() 