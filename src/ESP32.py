import os
import sys
import time
import grpc
from chirpstack_api.as_pb.external import api

# Configuration.

# This must point to the API interface.
server = "172.16.0.49:8080"

# The DevEUI for which you want to enqueue the downlink.
dev_eui = bytes([0xff,0xfe,0x38,0x84,0xab,0x08,0xb7,0x64])

# The API token (retrieved using the web-interface).
api_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcGlfa2V5X2lkIjoiMjU1ZTFlMTktZjQ2Mi00MDBlLWIyYTUtYWYwNjJmMjgyYzQ1IiwiYXVkIjoiYXMiLCJpc3MiOiJhcyIsIm5iZiI6MTc0MTg3Mzk5MSwic3ViIjoiYXBpX2tleSJ9.iUvxw_hVlA9M5lG8oppcH97jlidi061wDJWSPRGzxCo"

def sendCode(dev_eui, ):
    channel = grpc.insecure_channel(server)

    # Device-queue API client.
    client = api.DeviceQueueServiceStub(channel)

    # Define the API key meta-data.
    auth_token = [("authorization", "Bearer %s" % api_token)]

    # Construct request.
    req = api.EnqueueDeviceQueueItemRequest()
    req.device_queue_item.confirmed = False
    req.device_queue_item.data = bytes([0x43,0x32, 0x31, 0x33,0x36, 0x35, 0x36,0x45])
    req.device_queue_item.dev_eui = dev_eui.hex()
    req.device_queue_item.f_port = 10
    resp = client.Enqueue(req, metadata=auth_token)
    print("Code envoyé : données enqueue", resp.f_cnt)

#def generate_and_send_code():
#  if __name__ == "__main__":
#    channel = grpc.insecure_channel(server)

    # Device-queue API client.
#    client = api.DeviceQueueServiceStub(channel)

    # Define the API key meta-data.
#    auth_token = [("authorization", "Bearer %s" % api_token)]

    # Construct request.
#    req = api.EnqueueDeviceQueueItemRequest()
#    req.device_queue_item.confirmed = False
#    req.device_queue_item.data = bytes([0x43,0x32, 0x31, 0x33,0x36, 0x35, 0x36,0x45])
#    req.device_queue_item.dev_eui = dev_eui.hex()
#    req.device_queue_item.f_port = 10
#    resp = client.Enqueue(req, metadata=auth_token)
#    generate_and_send_code()
#    print("Code envoyé : données enqueue", resp.f_cnt)

#while True:
#    generate_and_send_code()
#    time.sleep(120)  # Envoie toutes les 10 secondes (modifiable)