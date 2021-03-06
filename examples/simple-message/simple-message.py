#!/usr/bin/env python3

import argparse
import google.protobuf.json_format
import json
from pathlib import Path
import subprocess
import sys

###
### Parse user input
###

# TODO: Extend 'proto_types' to dict to use for all type associations.
#       The current solution uses implementation details (internal type enums),
#       which may or may not be stable.
proto_types = ["double", "float", "int32", "int64", "uint32", "uint64", "sint32", "sint64",
    "fixed32", "fixed64", "sfixed32", "sfixed64", "bool", "string", "bytes"]

parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
    description="""\
Inspect the binary structure of simple Protobuf messages containing a single
data field. Depending on the type and field ID specification a Protobuf
definition is generated from which Python boilerplate is compiled. A Protobuf
message is generated and its data field is intialized according to the value
read from the command-line. The message's byte listing and JSON-equivalent are
printed to stdout.

Note: For some integer types the generated JSON-equivalent of a message
erroneously wraps the values in quotation marks. This is an error in the Python
Protobuf library. The Protobuf message is unaffected by this.

""",
    epilog="""Examples:
    python3 %(prog)s --type=uint32 --val=150
    python3 %(prog)s --type=sint64 --val=-5512
    python3 %(prog)s --type="repeated uint32" --val=1,2,3,4,5,6,7,8
    python3 %(prog)s --type="repeated bytes" --val=0xBEEFAFFE,0xdead1337
    python3 %(prog)s --type=string --val=Paris
    python3 %(prog)s --type="repeated string" --val=UTF-8,2≠3
""")
parser.add_argument("--type",
    choices=proto_types + [ "repeated "+t for t in proto_types ],
    metavar="TYPE", # don't print all choices
    help="Field type. May use the 'repeated' prefix.", required=True)
parser.add_argument("--val", required=True,
    help="Comma-separated field value(s). See examples for type-dependent representation.")
parser.add_argument("--id", type=int, help="Field ID. Default: %(default)d.", default=1)
parser.add_argument("--proto_out", default=".",
    help="Output directory to contain generated Protobuf definition files. "
        "Will be created if necessary. "
        "Relative paths are based on the current working directory. "
        "Default: '%(default)s'.")
parser.add_argument("--python_out", default=".",
    help="Output directory to contain generated Python boilerplate. "
        "Will be created if necessary."
        "Relative paths are based on the current working directory. "
        "Default: '%(default)s'.")
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
Path(args.proto_out).mkdir(mode=0o755, parents=True, exist_ok=True)
open(f"{args.proto_out}/simple-message.proto", "w").write(protodecl)

###
### Compile Protobuf and generate Python boilerplate
###

Path(args.python_out).mkdir(mode=0o755, parents=True, exist_ok=True)
cmd = subprocess.run(["protoc", f"--python_out={str(Path(args.python_out))}",
    f"{str(Path(args.proto_out) / Path('simple-message.proto'))}"])
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
# BUG: Somtimes integer values generate strings in Python. Same for MessageToJson().
#      Serialized protobuf is correct, however.
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