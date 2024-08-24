import json
from models import Author, Quote
from config import connect_to_db

def load_authors_from_json():
    with open('authors.json', 'r', encoding='utf-8') as f:
        authors_data = json.load(f)
        for author in authors_data:
            Author(**author).save()


#
def load_quotes_from_json():
    with open('/DZ1/quotes.json', 'r', encoding='utf-8') as f:
        quotes_data = json.load(f)
        for quote_data in quotes_data:
            author = Author.objects(fullname=quote_data['author']).first()
            if author:
                Quote(tags=quote_data['tags'], author=author, quote=quote_data['quote']).save()


if __name__ == "__main__":
    connect_to_db()
    load_authors_from_json()
    load_quotes_from_json()
