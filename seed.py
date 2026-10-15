import json
from db import init_db
from models import Author, Quote

def load_data():
    # Инициализируем подключение к базе
    init_db()
    
    # Очищаем коллекции перед повторным запуском (совет ментора для надежности)
    Author.objects.delete()
    Quote.objects.delete()
    
    # 1. Загружаем и сохраняем авторов
    with open('authors.json', 'r', encoding='utf-8') as f:
        authors_data = json.load(f)
        
    for auth_info in authors_data:
        author = Author(
            fullname=auth_info['fullname'],
            born_date=auth_info['born_date'],
            born_location=auth_info['born_location'],
            description=auth_info['description']
        )
        author.save()
    print("Авторів успішно імпортовано.")

    # 2. Загружаем и сохраняем цитаты
    with open('quotes.json', 'r', encoding='utf-8') as f:
        quotes_data = json.load(f)
        
    for q_info in quotes_data:
        # Ищем автора в базе по имени, чтобы получить его ObjectID
        author_obj = Author.objects(fullname=q_info['author']).first()
        
        if author_obj:
            quote = Quote(
                tags=q_info['tags'],
                author=author_obj, # Передаем объект автора (Mongoengine сам подставит Reference)
                quote=q_info['quote']
            )
            quote.save()
            
    print("Цитати успішно імпортовано.")

if __name__ == '__main__':
    load_data()
