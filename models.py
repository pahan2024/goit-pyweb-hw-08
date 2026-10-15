from mongoengine import Document, StringField, ListField, ReferenceField, BooleanField, CASCADE

class Author(Document):
    meta = {'collection': 'authors'} # Явно указываем имя коллекции
    
    fullname = StringField(required=True, unique=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class Quote(Document):
    meta = {'collection': 'quotes'}
    
    tags = ListField(StringField())
    # Связь с коллекцией authors. При удалении автора удалятся и его цитаты (CASCADE)
    author = ReferenceField(Author, reverse_delete_rule=CASCADE, required=True)
    quote = StringField(required=True)

# Додайте нові поля в імпорт зверху файлу, якщо їх там немає:
# from mongoengine import Document, StringField, BooleanField

class Contact(Document):
    meta = {'collection': 'contacts'}
    
    fullname = StringField(required=True)
    email = StringField()
    phone = StringField()
    # БЫЛО: is_sent = Column(BooleanField(default=False))
    # СТАЛО (убрали Column, теперь это чистый тип Mongoengine):
    is_sent = BooleanField(default=False)
    preferred_method = StringField(choices=['email', 'sms'], default='email')