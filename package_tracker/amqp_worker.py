import pika, json
import requests


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='main')


def callback(ch, method, properties, body):
    print('Received in main')
    test = body.decode("utf-8")
    print(test)
    print(type(body))
    print(type(test))
    res = requests.post('http://127.0.0.1:5000/api/v1/update_geoloc', params=json.loads(test))
    print(res)



channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()