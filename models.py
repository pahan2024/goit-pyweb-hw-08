from mongoengine import Document, StringField, ListField, ReferenceField, CASCADE

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
