from pymongo import MongoClient
import json

# Підключення до MongoDB Atlas
client = MongoClient("mongodb://localhost:27017/")
db = client['quotes_db']

# Завантаження цитат
with open('quotes.json', 'r', encoding='utf-8') as f:
    quotes_data = json.load(f)
    db.quotes.insert_many(quotes_data)

# Завантаження авторів
with open('authors.json', 'r', encoding='utf-8') as f:
    authors_data = json.load(f)
    db.authors.insert_many(authors_data)

print("Data successfully imported into Atlas.")
