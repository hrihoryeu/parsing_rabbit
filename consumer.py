import sqlite3
import pika
from functions import JSONSerialization

# database connection
connection_bd = sqlite3.connect('lamoda.db')
cursor = connection_bd.cursor()

# connection_bd.execute("CREATE TABLE nike_sneakers (individual_id VARCHAR, title VARCHAR, price INTEGER, available_sizes VARCHAR)")
# connection_bd.execute("ALTER TABLE nike_sneakers ADD COLUMN seller VARCHAR")


# rabbitmq connection
connection_mq = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection_mq.channel()

channel.queue_declare(queue='hello')


def callback(ch, method, properties, body):
    nike_dict = JSONSerialization.deserialize(body)
    print(' [x] Received %r' % body.decode())
    insert_with_param = "INSERT INTO nike_sneakers VALUES ('', ?, ?, '', '')"
    data_tuple = (nike_dict['name'], nike_dict['price'])
    connection_bd.execute(insert_with_param, data_tuple)
    connection_bd.commit()
    print(' [x] Done')


channel.basic_consume(queue='hello',
                      auto_ack=True,
                      on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
