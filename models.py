from peewee import  CharField, DateTimeField, BooleanField, Model, \
    ForeignKeyField, TextField
from datetime import datetime
from pymongo import MongoClient


client = MongoClient

database = client.Digiato_Crawler


class BaseModel(Model):
    created_time = DateTimeField(default=datetime.now())

    class Meta:
         database = database


class Category(BaseModel):
    name = CharField()


class Article(BaseModel):
    title = CharField(null=True)
    date_shared = DateTimeField()
    winter = CharField()
    url = CharField()
    category = ForeignKeyField(Category, backref='articles')
    body = TextField(null=True)
    is_compeleted = BooleanField(default=False)

