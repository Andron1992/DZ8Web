import pika
from faker import Faker
from models import Contact


def generate_contacts(num_contacts):
    fake = Faker()
    for _ in range(num_contacts):
        contact = Contact(
            full_name=fake.name(),
            email=fake.email(),
            additional_info=fake.text()
        )
        contact.save()
        send_to_queue(str(contact.id))


def send_to_queue(contact_id):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='email_queue', durable=True)

    channel.basic_publish(
        exchange='',
        routing_key='email_queue',
        body=contact_id,
        properties=pika.BasicProperties(
            delivery_mode=2,
        ))
    print(f'[x] Sent contact ID {contact_id}')
    connection.close()


if __name__ == '__main__':
    generate_contacts(10)