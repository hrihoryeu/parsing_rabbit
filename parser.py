import pika
from functions import ParserRunner, JSONSerialization

# rabbit connection
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# sending to queue
parser = ParserRunner.choose_parser('https://by.wildberries.ru/catalog/obuv/muzhskaya/kedy-i-krossovki?sort=popular&page=1&xsubject=104%3B105&fbrand=671#c13150694')
#parser = ParserRunner.choose_parser('https://www.lamoda.by/c/2981/shoes-krossovk-kedy-muzhskie/?brands=2047&page=1')
for values in parser.parsing():
    channel.basic_publish(exchange='',
                          routing_key='hello',
                          body=JSONSerialization.serialize(values))
    print(' [x] Sent %r' % values[1])

connection.close()
