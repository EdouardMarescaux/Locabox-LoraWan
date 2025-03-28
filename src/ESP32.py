from src.Config import *
import grpc
from chirpstack_api.as_pb.external import api

def sendCode():
    channel = grpc.insecure_channel(CHIRPSTACK_SERVER)

    # Device-queue API client.
    client = api.DeviceQueueServiceStub(channel)

    # Define the API key meta-data.
    auth_token = [("authorization", "Bearer %s" % API_TOKEN)]

    # Construct request.
    req = api.EnqueueDeviceQueueItemRequest()
    req.device_queue_item.confirmed = False
    req.device_queue_item.data = bytes([0x43,0x32, 0x31, 0x33,0x36, 0x35, 0x36,0x45])
    req.device_queue_item.dev_eui = dev_eui.hex()
    req.device_queue_item.f_port = 10
    resp = client.Enqueue(req, metadata=auth_token)
    print("Code envoyé : données enqueue", resp.f_cnt)