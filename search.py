import redis
import json
from db import init_db
from models import Author, Quote

# Підключаємося до локального сервера Redis у Docker
redis_client = redis.Redis(host="localhost", port=6379, db=0)


def get_cached_result(cache_key):
    """Отримує дані з кешу Redis, якщо вони там є."""
    cached_data = redis_client.get(cache_key)
    if cached_data:
        # Декодуємо з bytes у рядок та парсимо JSON назад у список
        return json.loads(cached_data.decode("utf-8"))
    return None


def set_cached_result(cache_key, data_list):
    """Зберігає результати в кеш Redis у форматі JSON на 1 годину (3600 секунд)."""
    # Замість redis_client.setex використовуємо сучасний redis_client.set з параметром ex
    redis_client.set(cache_key, json.dumps(data_list, ensure_ascii=False), ex=3600)


def search_loop():
    init_db()
    print("\n🚀 CLI Пошук цитат з КЕШУВАННЯМ Redis та регулярками!")
    print("name:st        -> Пошук за початком імені (наприклад, Steve Martin)")
    print("tag:li         -> Пошук за скороченим тегом (наприклад, life)")
    print("tags:life,live -> Пошук за декількома повними тегами")
    print("exit           -> Вихід з програми\n")

    while True:
        try:
            user_input = input("Введіть команду: ").strip()

            if user_input.lower() == "exit":
                print("Завершення роботи пошуку.")
                break

            if ":" not in user_input:
                print("Помилка: невірний формат. Використовуйте 'команда: значення'")
                continue

            command, value = user_input.split(":", 1)
            command = command.strip().lower()
            value = value.strip()

            # Формуємо унікальний ключ для кешу, наприклад: "query:name:st"
            cache_key = f"query:{command}:{value.lower()}"

            # --- 1. ПЕРЕВІРКА КЕШУ REDIS ---
            cached_results = get_cached_result(cache_key)
            if cached_results is not None:
                print(
                    f"\n⚡ [Взято з КЕШУ Redis] Знайдено цитат: {len(cached_results)}"
                )
                for q in cached_results:
                    print(
                        f"[{q['author']}]: {q['quote']} (Теги: {', '.join(q['tags'])})"
                    )
                print("-" * 50)
                continue

            # --- 2. ПОШУК У MONGODB (якщо в кеші порожньо) ---
            quotes_found = []

            if command == "name":
                # Використовуємо регулярний вираз __icontains для пошуку за частиною імені без урахування регістру
                authors = Author.objects(fullname__icontains=value)
                if not authors:
                    print(f"Автора, що містить '{value}', не знайдено.")
                    continue
                # Збираємо цитати для всіх знайдених за маскою авторів
                quotes_found = Quote.objects(author__in=authors)

            elif command == "tag":
                # Використовуємо регулярний вираз для пошуку за частиною тегу
                quotes_found = Quote.objects(tags__icontains=value)

            elif command == "tags":
                tags_list = [t.strip() for t in value.split(",")]
                quotes_found = Quote.objects(tags__in=tags_list)

            else:
                print(f"Невідома команда '{command}'. Доступні: name, tag, tags, exit")
                continue

            # --- 3. ОБРОБКА ТА КЕШУВАННЯ РЕЗУЛЬТАТІВ ---
            if not quotes_found:
                print("За вашим запитом нічого не знайдено.")
            else:
                # Трансформуємо об'єкти бази даних у простий список словників для JSON
                formatted_results = []
                for q in quotes_found:
                    formatted_results.append(
                        {"author": q.author.fullname, "quote": q.quote, "tags": q.tags}
                    )

                # Зберігаємо отриманий результат у Redis для майбутніх повторних запитів
                set_cached_result(cache_key, formatted_results)

                print(
                    f"\n🍃 [Взято з бази MongoDB Atlas] Знайдено цитат: {len(formatted_results)}"
                )
                for q in formatted_results:
                    output = (
                        f"[{q['author']}]: {q['quote']} (Теги: {', '.join(q['tags'])})"
                    )
                    print(output.encode("utf-8").decode("utf-8"))
                print("-" * 50)

        except Exception as e:
            print(f"Виникла помилка під час пошуку: {e}")


if __name__ == "__main__":
    search_loop()
