from mongoengine import connect, Document, IntField, StringField

connect('droider-bot')


class User(Document):
    chat_id = IntField()
    first_name = StringField()
    last_name = StringField()
    username = StringField()

    @staticmethod
    def get_by_chat_id(chat_id):
        try:
            return User.objects.get(chat_id=chat_id)
        except User.DoesNotExist:
            return None


class YouTube(Document):
    title = StringField()
    link = StringField(unique=True)
    published = StringField()


class Droider(Document):
    title = StringField()
    link = StringField(unique=True)
    published = StringField()
