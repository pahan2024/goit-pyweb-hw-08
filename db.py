import os
import certifi
from mongoengine import connect
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

def init_db():
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        raise ValueError("Помилка: MONGO_URI не знайдено у файлі .env")
    
    # Подключаемся, используя certifi для избежания ошибок SSL-сертификатов
    connect(host=mongo_uri, tlsCAFile=certifi.where())
    print("Успішно підключено до хмарної бази MongoDB Atlas!")
