import pika
import time
from bson import ObjectId
from db import init_db
from models import Contact

def callback(ch, method, properties, body):
    # Отримуємо ID контакту з черги
    contact_id = body.decode('utf-8')
    
    # Знаходимо контакт у MongoDB
    contact = Contact.objects(id=ObjectId(contact_id)).first()
    
    if contact:
        # Функція-заглушка: імітація відправки email
        print(f"[ Email ] Надсилання листа для: {contact.fullname} ({contact.email})...")
        time.sleep(1) # Імітація затримки мережі
        
        # Оновлюємо статус у базі даних
        contact.is_sent = True
        contact.save()
        print(f"[ OK ] Статус контакту {contact_id} змінено на True")
        
    # Підтверджуємо успішну обробку повідомлення
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    init_db()
    
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='email_queue')
    
    # Налаштовуємо слухача черги
    channel.basic_consume(queue='email_queue', on_message_callback=callback)
    
    print('[*] Очікування повідомлень в email_queue. Для виходу натисніть CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    main()
