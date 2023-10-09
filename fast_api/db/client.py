from pymongo import MongoClient

# Local dataBase
#db_client = MongoClient().local #Por defecto se conecta a localhost

# Remote dataBase

url = 'mongodb+srv://<username>:<password>@cluster0.dmidmld.mongodb.net/?retryWrites=true&w=majority'

db_client = MongoClient(url).db
