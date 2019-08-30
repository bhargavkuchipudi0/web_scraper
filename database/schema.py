from mongoengine import *
import datetime

class Users(Document):
    first_name = StringField(required=True, min_length=1, max_length=30)
    last_name = StringField(required=True, min_length=1, max_length=30)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    created_on = DateTimeField(default=datetime.datetime.now)

class Tasks(Document):
    user_id = StringField(required=True)
    url = StringField(required=True)
    product_image = StringField(default='not_available')
    product_name = StringField(required=True)
    actual_price = IntField(required=True, default='not_available')
    current_price = IntField(required=True, default='not_available')
    discount = IntField(required=True, default=0)
    updated_on = DateTimeField(default=datetime.datetime.now)
    
