from db import init_db
from models import Author, Quote

def search_loop():
    init_db()
    print("\nCLI Пошук цитат активовано. Доступні команди:")
    print("name: Ім'я Автора  -> Пошук цитат за автором")
    print("tag: тег          -> Пошук цитат за одним тегом")
    print("tags: тег1,тег2   -> Пошук за декількома тегами (через кому без пробілів)")
    print("exit              -> Вихід з програми\n")
    
    while True:
        try:
            user_input = input("Введіть команду: ").strip()
            
            if user_input.lower() == 'exit':
                print("Завершення роботи пошуку.")
                break
                
            if ':' not in user_input:
                print("Помилка: невірний формат. Використовуйте 'команда: значення'")
                continue
                
            command, value = user_input.split(':', 1)
            command = command.strip().lower()
            value = value.strip()
            
            if command == 'name':
                # Поиск автора (можно использовать регулярное выражение для поиска по подстроке без учета регистра)
                author = Author.objects(fullname__iexact=value).first()
                if not author:
                    print(f"Автора '{value}' не знайдено в базі.")
                    continue
                quotes = Quote.objects(author=author)
                
            elif command == 'tag':
                # Mongoengine автоматически ищет элемент внутри списка ListField
                quotes = Quote.objects(tags__iexact=value)
                
            elif command == 'tags':
                # Разбиваем строку тегов по запятой
                tags_list = [t.strip() for t in value.split(',')]
                # Оператор 'in' в Mongoengine находит документы, содержащие любой тег из списка
                quotes = Quote.objects(tags__in=tags_list)
                
            else:
                print(f"Невідома команда '{command}'. Доступні: name, tag, tags, exit")
                continue

            # Вывод результатов
            if not quotes:
                print("За вашим запитом нічого не знайдено.")
            else:
                print(f"\nЗнайдено цитат: {len(quotes)}")
                for q in quotes:
                    # Обеспечиваем вывод строго в utf-8 декорированием/принтом
                    output = f"[{q.author.fullname}]: {q.quote} (Теги: {', '.join(q.tags)})"
                    print(output.encode('utf-8').decode('utf-8'))
                print("-" * 50)
                
        except Exception as e:
            print(f"Виникла помилка: {e}")

if __name__ == '__main__':
    search_loop()
