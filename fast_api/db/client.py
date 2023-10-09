from pymongo import MongoClient
import os

# Local dataBase
#db_client = MongoClient().local #Por defecto se conecta a localhost

# Remote dataBase
name_DB = os.environ.get('DATABASE_NAME')
user_DB = os.environ.get('DATABASE_USER')
pass_DB = os.environ.get('DATABASE_PASS')
url_base = 'mongodb+srv://{}:{}@{}.mongodb.net/?retryWrites=true&w=majority'.format(user_DB, pass_DB, name_DB)

db_client = MongoClient(url_base).db
