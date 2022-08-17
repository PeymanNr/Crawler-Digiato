from models import Article, Category, database


def create_tables():
    database.create_tables([Article, Category])