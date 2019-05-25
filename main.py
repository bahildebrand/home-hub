import requests
import yaml
import asyncio
import os
import paho.mqtt.client as mqtt #import the client1
import time
import boto3

laundryTopic = 'house/laundry'
laundryLogTopic = 'house/laundry/log'

dbTable = 'LaundryAcellData'

async def sendLaundryStatus(machineType):
    requests.post('https://6vdfu36mrb.execute-api.us-east-1.amazonaws.com/dev/laundry', json={'machine':machineType}, headers={'x-api-key':'VomVKwY9A31eHyNUUX9qf9ep0F4KeOYe7zUFlDBy'})

def on_message(client, userdata, message):
    if(message.topic == laundryTopic):
        asyncio.run(sendLaundryStatus(message.payload.decode('ascii')))
    elif(message.topic == laundryLogTopic):
        print(message.payload)
        print(int.from_bytes(message.payload[:4], "little"))

def on_connect(client, userdata, flags, rc):
    print("connected")

def mqtt_client():
    broker_address="192.168.1.100"
    #broker_address="iot.eclipse.org"
    print("creating new instance")
    client = mqtt.Client("P1") #create new instance
    client.on_message=on_message #attach function to callback
    client.on_connect = on_connect
    print("connecting to broker")
    client.connect(broker_address)
    print("Subscribing to topic",laundryTopic)
    client.subscribe(laundryTopic)
    client.subscribe(laundryLogTopic)
    client.loop_forever() #start the loop

async def dynamoDB_log():
    db_res = boto3.resource('dynamodb')
    table = db_res.Table(dbTable)
    table.put_item(
        Item={
            'SessionID': 'blahtest',
            'TimeStamp': 'time',
            'x': 1,
            'y': 2,
            'z': 3,
        }
    )


if __name__ == '__main__':
    # dynamoDB_log()
    mqtt_client()


