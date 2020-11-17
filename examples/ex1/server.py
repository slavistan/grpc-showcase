#!/usr/bin/env python3
from concurrent import futures
import grpc
import time

import calc_pb2 # generated
import calc_pb2_grpc # generated

import calc


# Specify procedures to expose ("services")
class CalcServicer(calc_pb2_grpc.CalcServicer):
    def SquareRoot(self, request, context):
        response = calc_pb2.Number()
        response.value = calc.square_root(request.value)
        return response

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

calc_pb2_grpc.add_CalcServicer_to_server(CalcServicer(), server)

server.add_insecure_port('[::]:50051')
server.start()

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
