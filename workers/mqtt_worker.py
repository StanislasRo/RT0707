import paho.mqtt.client as mqtt

# callback function for when a message is received
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

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

# subscribe to a topic
client.subscribe("WAREFIRST")

# start the loop to process incoming messages
client.loop_forever()