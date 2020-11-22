#!/usr/bin/env python3

import argparse
import google.protobuf.json_format
import json
import os
import subprocess
import sys

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--type", help="Field type; may use 'repeated'")
parser.add_argument("-i", "--id", help="Field ID", default=1)
parser.add_argument("-v", "--val", help="Field value(s)")
parser.add_argument("--proto_out", help="Generated Protobuf output directory.", default=".")
parser.add_argument("--python_out", help="Generated Python output directory", default=".")
args = parser.parse_args()

###
### Generate .proto message declaration
###

protodecl = (
    f"syntax = \"proto3\";\n"
    f"package prototest;\n"
    f"\n"
    f"message SimpleMessage {{\n"
    f"    {args.type} data = {args.id};\n"
    f"}}\n"
)
os.system(f"mkdir -p {args.python_out}")
open(f"{args.proto_out}/simple-message.proto", "w").write(protodecl)

###
### Compile Protobuf and generate Python boilerplate
###

os.system(f"mkdir -p {args.python_out}")
cmd = subprocess.run(["protoc", f"--python_out={args.python_out}", f"{args.proto_out}/simple-message.proto"])
if cmd.returncode:
    sys.exit(f"protoc failed (return code {cmd.returncode}).")

###
### Create message from cli args
###

exec(open(f"{args.python_out}/simple_message_pb2.py").read())

# Type associations between Protobuf and Python. Type keys found here
#   https://googleapis.dev/python/protobuf/latest/google/protobuf/descriptor.html
# Corresp. Python types found here
#   https://developers.google.com/protocol-buffers/docs/proto3#scalar
# Bytes (key 12) differ from the above definitions to ease parsing.
typedict = {1: float, 2: float, 3: int, 4: int, 5: int,
            6: int, 7: int, 8: bool, 9: str, 10: None,
            11: None, 12: bytes, 13: int, 14: None, 15: int,
            16: int, 17: int, 18: int}

pytype = typedict[SimpleMessage.data.DESCRIPTOR.type]
if not pytype:
    sys.exit(f"Type {args.type} is not supported.")

def valfromstr(valstr):
    if pytype == bytes:
        if valstr.startswith("0x"):
            valstr = valstr[2:]
        if len(valstr) % 2:
            valstr = "0" + valstr
        val = bytes.fromhex(valstr)
    else:
        val = pytype(valstr)
    return val

if args.type.find("repeated") != -1:
    msg = SimpleMessage()
    for valstr in args.val.split(","):
        msg.data.append(valfromstr(valstr))
else:
    msg = SimpleMessage(data=valfromstr(args.val))

###
### Inspect message
###

## Print JSON equivalent
# BUG: JSON 64bit integer values get quoted. Same for MessageToDict()
as_dict = google.protobuf.json_format.MessageToDict(msg)
as_json = json.dumps(as_dict, separators=(',', ':'))
numbytes_json = len(as_json)
bitlisting_header = f"JSON equivalent ({numbytes_json} {'byte' if numbytes_json == 1 else 'bytes'})"
print("\033[1m" + bitlisting_header + "\033[0m\n" + ("-" * len(bitlisting_header)))
print(as_json + "\n")

## Print byte listing
numbytes_serial = msg.ByteSize()
bitlisting_header = f"Serialized data ({numbytes_serial} {'byte' if numbytes_serial == 1 else 'bytes'})"
print("\033[1m" + bitlisting_header + "\033[0m\n" + ("-" * len(bitlisting_header)))
print("DEC    HEX     BIN         ASCII")
for byte in msg.SerializeToString():
    val = int(byte)
    char = chr(val) if chr(val).isprintable() and val <= 127 else ""
    print(f"{val:3}    0x{val:02x}    {val:08b}    {char}")

# TODO: Usage help
# TODO: Remove linux dependencies (mkdir etc)
# TODO: Use python's protoc to reduce dependencies
# TODO: Assert dependencies:
#        - protobuf (+ protoc)
#        - json, sys, python version