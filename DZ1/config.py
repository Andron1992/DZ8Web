from mongoengine import connect


def connect_to_db():
    connect(db="DZ8", host="mongodb+srv://Andronweb8:20242024@cluster0.6hgsz.mongodb.net/")
