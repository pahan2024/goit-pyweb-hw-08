import pika
import random
from faker import Faker
from db import init_db
from models import Contact

fake = Faker('uk_UA')

def main():
    init_db()
    
    # Підключення до RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    
    # Оголошення двох окремих черг для email та sms
    channel.queue_declare(queue='email_queue')
    channel.queue_declare(queue='sms_queue')
    
    print("Генерація контактів...")
    
    # Генеруємо 20 випадкових контактів
    for _ in range(20):
        method = random.choice(['email', 'sms'])
        contact = Contact(
            fullname=fake.name(),
            email=fake.email(),
            phone=fake.phone_number(),
            preferred_method=method
        )
        contact.save()
        
        # Передаємо в чергу тільки ObjectID контакту як рядок
        message = str(contact.id)
        
        if method == 'email':
            channel.basic_publish(exchange='', routing_key='email_queue', body=message)
            print(f"[+] Відправлено в email_queue: ID {message}")
        else:
            channel.basic_publish(exchange='', routing_key='sms_queue', body=message)
            print(f"[+] Відправлено в sms_queue: ID {message}")
            
    connection.close()
    print("Всі контакти успішно згенеровані та розподілені по чергах!")

if __name__ == '__main__':
    main()
