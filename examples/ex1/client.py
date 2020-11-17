#!/usr/bin/env python3
import grpc
import sys

import calc_pb2 # generated
import calc_pb2_grpc # generated

ipport = sys.argv[2] if len(sys.argv) > 2 and len(sys.argv[2]) > 0 else 'localhost:50051'
val = float(sys.argv[1]) if len(sys.argv) > 1 and len(sys.argv[1]) > 0 else 4

channel = grpc.insecure_channel(ipport)

# set up the 'stub'
stub = calc_pb2_grpc.CalcStub(channel)

# request message
response = stub.SquareRoot(calc_pb2.Number(value=val))

print(response.value)
