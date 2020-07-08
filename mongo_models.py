import mongoengine

class User_stud(mongoengine.Document):
    user_id = mongoengine.IntField(required=True)
    login = mongoengine.StringField(required=True, max_length=100, default="None")

class Question(mongoengine.Document):
    day = mongoengine.IntField(required=True)
    text = mongoengine.StringField(required=True, max_length=50)
    answers = mongoengine.ListField(mongoengine.StringField(required=True, max_lenght=50))
    correct_answer = mongoengine.StringField(required=True,max_length=1)

