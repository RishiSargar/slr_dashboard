from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import random,time
import json
import random
import datetime
import pytz

import time

deviceNames = ['D_InFlow01', 'D_OutFlow01', 'D_Turbidity01', 'D_Oxygen01']
tz=pytz.timezone('America/Phoenix')
HOST_NAME="a3hsv8ijyp2awt-ats.iot.us-west-2.amazonaws.com"

ROOT_CA="<file path to AmazonRootCA1.pem>"

INFLOW_PRIVATE_KEY="<file path to private.pem.key file of inflow device>"
INFLOW_CERT_FILE="<file path to certificate.pem.cert file of inflow device>"
INFLOW_SHADOW_HANDLER="inflow"

OUTFLOW_PRIVATE_KEY="<file path to private.pem.key file of outflow device>"
OUTFLOW_CERT_FILE="<file path to certificate.pem.cert file of outflow device>"
OUTFLOW_SHADOW_HANDLER="outflow"

TURBIDITY_PRIVATE_KEY="<file path to private.pem.key file of turbidity device>"
TURBIDITY_CERT_FILE="<file path to certificate.pem.cert file of turbidity device>"
TURBIDITY_SHADOW_HANDLER="turbidity"

OXYGEN_PRIVATE_KEY="<file path to private.pem.key file of dissolvedoxygen device>"
OXYGEN_CERT_FILE="<file path to certificate.pem.cert file of dissolvedoxygen device>"
OXYGEN_SHADOW_HANDLER="dissolvedoxygen"

def getInFlowValues():
    data = {}

    data['deviceValue'] = random.randint(60, 100)
    data['deviceParameter'] = 'InFlow'
    data['deviceId'] = deviceNames[0]
    data['timestamp'] = datetime.datetime.now(tz=tz).strftime("%Y-%m-%d %H:%M:%S")
    now = datetime.datetime.now(tz=tz)
    data['year'] = now.year
    if now.month < 10:
        data['month'] = int(str(data['year']) + "0" + str(now.month))
    else:
        data['month'] = int(str(data['year']) + str(now.month))
    if now.day < 10:
        data['day'] = int(str(data['month']) + "0" + str(now.day))
    else:
        data['day'] = int(str(data['month']) + str(now.day))
    if now.hour < 10:
        data['hour'] = int(str(data['day']) + "0" + str(now.hour))
    else:
        data['hour'] = int(str(data['day']) + str(now.hour))

    if datetime.date.today().isocalendar()[1] < 10:
        data['week'] = int(str(data['year']) + "0" + str(datetime.date.today().isocalendar()[1]))
    else:
        data['week'] = int(str(data['year']) + str(datetime.date.today().isocalendar()[1]))

    return data

def getOutFlowValues():
    data = {}
    data['deviceValue'] = random.randint(60, 100    )
    data['deviceParameter'] = 'OutFlow'
    data['deviceId'] = deviceNames[1]
    data['timestamp'] = datetime.datetime.now(tz=tz).strftime("%Y-%m-%d %H:%M:%S")
    now = datetime.datetime.now(tz=tz)
    data['year'] = now.year
    if now.month < 10:
        data['month'] = int(str(data['year']) + "0" + str(now.month))
    else:
        data['month'] = int(str(data['year']) + str(now.month))
    if now.day < 10:
        data['day'] = int(str(data['month']) + "0" + str(now.day))
    else:
        data['day'] = int(str(data['month']) + str(now.day))
    if now.hour < 10:
        data['hour'] = int(str(data['day']) + "0" + str(now.hour))
    else:
        data['hour'] = int(str(data['day']) + str(now.hour))

    if datetime.date.today().isocalendar()[1] < 10:
        data['week'] = int(str(data['year']) + "0" + str(datetime.date.today().isocalendar()[1]))
    else:
        data['week'] = int(str(data['year']) + str(datetime.date.today().isocalendar()[1]))
    #payload = {"message": data, "timestamp": data['dateTime']}
    return data


def getTurbidity():
    data = {}
    data['deviceValue'] = random.randint(50, 90)
    data['deviceParameter'] = 'Turbidity'
    data['deviceId'] = deviceNames[2]
    data['timestamp'] = datetime.datetime.now(tz=tz).strftime("%Y-%m-%d %H:%M:%S")
    now = datetime.datetime.now(tz=tz)
    data['year'] = now.year
    if now.month < 10:
        data['month'] = int(str(data['year']) + "0" + str(now.month))
    else:
        data['month'] = int(str(data['year']) + str(now.month))
    if now.day < 10:
        data['day'] = int(str(data['month']) + "0" + str(now.day))
    else:
        data['day'] = int(str(data['month']) + str(now.day))
    if now.hour < 10:
        data['hour'] = int(str(data['day']) + "0" + str(now.hour))
    else:
        data['hour'] = int(str(data['day']) + str(now.hour))

    if datetime.date.today().isocalendar()[1] < 10:
        data['week'] = int(str(data['year']) + "0" + str(datetime.date.today().isocalendar()[1]))
    else:
        data['week'] = int(str(data['year']) + str(datetime.date.today().isocalendar()[1]))
    #payload = {"message": data, "timestamp": data['dateTime']}
    return data


def getDissolvedOxygen():
    data = {}

    data['deviceValue'] = random.randint(100, 140)
    data['deviceParameter'] = 'DissolvedOxygen'
    data['deviceId'] = deviceNames[3]
    data['timestamp'] = datetime.datetime.now(tz=tz).strftime("%Y-%m-%d %H:%M:%S")
    now = datetime.datetime.now(tz=tz)
    data['year'] = now.year
    if now.month < 10:
        data['month'] = int(str(data['year']) + "0" + str(now.month))
    else:
        data['month'] = int(str(data['year']) + str(now.month))
    if now.day < 10:
        data['day'] = int(str(data['month']) + "0" + str(now.day))
    else:
        data['day'] = int(str(data['month']) + str(now.day))
    if now.hour < 10:
        data['hour'] = int(str(data['day']) + "0" + str(now.hour))
    else:
        data['hour'] = int(str(data['day']) + str(now.hour))

    if datetime.date.today().isocalendar()[1] < 10:
        data['week'] = int(str(data['year']) + "0" + str(datetime.date.today().isocalendar()[1]))
    else:
        data['week'] = int(str(data['year']) + str(datetime.date.today().isocalendar()[1]))

    #payload = {"message": data, "timestamp":data['dateTime']}
    return data


inFlowShadowClient = AWSIoTMQTTClient(INFLOW_SHADOW_HANDLER)
inFlowShadowClient.configureEndpoint(HOST_NAME,8883)
inFlowShadowClient.configureCredentials(ROOT_CA,INFLOW_PRIVATE_KEY,INFLOW_CERT_FILE)
inFlowShadowClient.configureConnectDisconnectTimeout(10)
inFlowShadowClient.configureMQTTOperationTimeout(5)
inFlowShadowClient.connect()

outFlowShadowClient = AWSIoTMQTTClient(OUTFLOW_SHADOW_HANDLER)
outFlowShadowClient.configureEndpoint(HOST_NAME, 8883)
outFlowShadowClient.configureCredentials(ROOT_CA, OUTFLOW_PRIVATE_KEY, OUTFLOW_CERT_FILE)
outFlowShadowClient.configureConnectDisconnectTimeout(10)
outFlowShadowClient.configureMQTTOperationTimeout(5)
outFlowShadowClient.connect()

turbidityShadowClient = AWSIoTMQTTClient(TURBIDITY_SHADOW_HANDLER)
turbidityShadowClient.configureEndpoint(HOST_NAME, 8883)
turbidityShadowClient.configureCredentials(ROOT_CA, TURBIDITY_PRIVATE_KEY, TURBIDITY_CERT_FILE)
turbidityShadowClient.configureConnectDisconnectTimeout(10)
turbidityShadowClient.configureMQTTOperationTimeout(5)
turbidityShadowClient.connect()

oxygenShadowClient = AWSIoTMQTTClient(OXYGEN_SHADOW_HANDLER)
oxygenShadowClient.configureEndpoint(HOST_NAME, 8883)
oxygenShadowClient.configureCredentials(ROOT_CA, OXYGEN_PRIVATE_KEY, OXYGEN_CERT_FILE)
oxygenShadowClient.configureConnectDisconnectTimeout(10)
oxygenShadowClient.configureMQTTOperationTimeout(5)
oxygenShadowClient.connect()

while True:
    time.sleep(5)
    data = json.dumps(getInFlowValues())
    print(data)
    topic = '/sensors/devicedata/inflow'
    inFlowShadowClient.publish(topic, data, 1)

    data = json.dumps(getOutFlowValues())
    print(data)
    topic = '/sensors/devicedata/outflow'
    outFlowShadowClient.publish(topic, data, 1)

    data = json.dumps(getTurbidity())
    print(data)
    topic = '/sensors/devicedata/turbidity'
    turbidityShadowClient.publish(topic, data, 1)

    data = json.dumps(getDissolvedOxygen())
    print(data)
    topic = '/sensors/devicedata/dissolvedoxygen'
    oxygenShadowClient.publish(topic, data, 1)



