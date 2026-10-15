import pika
import time
from bson import ObjectId
from db import init_db
from models import Contact

def callback(ch, method, properties, body):
    contact_id = body.decode('utf-8')
    contact = Contact.objects(id=ObjectId(contact_id)).first()
    
    if contact:
        # Функція-заглушка: імітація відправки SMS
        print(f"[ SMS ] Надсилання повідомлення на номер: {contact.fullname} ({contact.phone})...")
        time.sleep(1)
        
        contact.is_sent = True
        contact.save()
        print(f"[ OK ] Статус контакту {contact_id} змінено на True")
        
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    init_db()
    
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='sms_queue')
    
    channel.basic_consume(queue='sms_queue', on_message_callback=callback)
    
    print('[*] Очікування повідомлень в sms_queue. Для виходу натисніть CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    main()
