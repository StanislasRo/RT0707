import paho.mqtt.client as mqtt

def on_publish(client, userdata, result):
   print("data published \n")
   pass

def on_message(client, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

def mqtt_change_warehouse(warehouse_name, tracking_number):
    client = mqtt.Client()
    client.username_pw_set("guest", "guest")
    client.on_publish = on_publish
    client.on_message = on_message
    client.connect("127.0.0.1", 1883)
    res = client.publish(warehouse_name, tracking_number, 0)
    client.disconnect()
    if res[0] == 0:
        return "Successfully sent"
    return "Failed"