"""
    Файл с описанием документов в базе данных
"""
import mongoengine

# Класс, описываюший пользователя
class User_stud(mongoengine.Document):
    user_id = mongoengine.IntField(required=True)
    user_name = mongoengine.StringField(required=True, max_length=50)
    user_status = mongoengine.StringField(max_length=20)
    user_count_que = mongoengine.IntField(required=True)
    user_number_que = mongoengine.IntField(required=True)
    user_wrong_answer = mongoengine.StringField()

# Класс, описывающий данные вопроса
class Question(mongoengine.Document):
    number = mongoengine.IntField(required=True)
    text = mongoengine.StringField(required=True, max_length=50)
    answers = mongoengine.ListField(mongoengine.StringField(required=True, max_lenght=50))
    correct_answer = mongoengine.StringField(required=True, max_length=1)
