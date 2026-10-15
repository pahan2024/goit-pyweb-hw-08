import os
import certifi
from mongoengine import connect
from dotenv import load_dotenv

# Завантаження змінних з .env
load_dotenv()

def init_db():
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        raise ValueError("Помилка: MONGO_URI не знайдено у файлі .env")
    
    # Підключення до MongoDB Atlas із сертифікатом certifi
    connect(host=mongo_uri, tlsCAFile=certifi.where())
    print("Успішно підключено до хмарної бази MongoDB Atlas!")
