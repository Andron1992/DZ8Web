from mongoengine import Document, StringField, BooleanField, connect


connect(db='DZ8n2', host='mongodb+srv://Andronweb8:20242024@cluster0.6hgsz.mongodb.net/')

class Contact(Document):
    full_name = StringField(required=True)
    email = StringField(required=True)
    email_sent = BooleanField(default=False)
    additional_info = StringField()

    def __str__(self):
        return f'{self.full_name} ({self.email}) - Email Sent: {self.email_sent}'
