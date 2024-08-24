import pika
from models import Contact
from bson import ObjectId
import logging


logging.basicConfig(level=logging.INFO)


def send_email(contact):
    print(f"Sending email to {contact.full_name} at {contact.email}")


def callback(ch, method, properties, body):
    try:
        contact_id = body.decode()
        logging.info(f"Received contact ID: {contact_id}")

        # Перевірка, чи є contact_id дійсним ObjectId
        if not ObjectId.is_valid(contact_id):
            logging.error(f"Invalid ObjectId: {contact_id}")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        contact = Contact.objects(id=ObjectId(contact_id)).first()

        if contact:
            send_email(contact)
            contact.email_sent = True
            contact.save()
            logging.info(f'[x] Email sent to {contact.full_name}')

        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        logging.error(f"Error processing message: {e}")


def start_consumer():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='email_queue', durable=True)
        channel.basic_consume(queue='email_queue', on_message_callback=callback)

        print('[*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()

    except Exception as e:
        logging.error(f"Failed to start consumer: {e}")


if __name__ == '__main__':
    start_consumer()