import paho.mqtt.client as mqtt
from mariadb.models import Warehouse
import requests
import json


# callback function for when a message is received
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    target_warehouse = msg.topic
    target_package = msg.payload.decode("utf-8")
    payload = {
        "tracking_number": target_package,
        "warehouse": target_warehouse
    }
    res = requests.post('http://127.0.0.1:5000/api/v1/change_warehouse', params=payload)
    print(res)
    

def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# create a new MQTT client
client = mqtt.Client()

# set the callback function for when a message is received
client.on_message = on_message
client.on_subscribe = on_subscribe

# connect to the RabbitMQ broker
client.username_pw_set("guest", "guest")
client.connect("127.0.0.1", 1883, 60)


res = requests.get('http://127.0.0.1:5000/api/v1/warehouses')
warehouses_list = res.json()
queues_to_subscribe = [(warehouse, 0) for warehouse in warehouses_list]

# subscribe to a topic
client.subscribe(queues_to_subscribe)

# start the loop to process incoming messages
client.loop_forever()