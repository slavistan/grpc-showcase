# Inspect the binary structure of Protobuf messages

Inspect the binary structure of simple Protobuf messages containing a single
data field. Depending on the type and field ID specification a Protobuf
definition is generated from which Python boilerplate is compiled. A Protobuf
message is generated and its data field is intialized according to the value
read from the command-line. The message's byte listing and JSON-equivalent are
printed to stdout.

Exemplary output:

`python3 ./simple-message.py --type=uint32 --val=150`
```
JSON equivalent (12 bytes)
--------------------------
{"data":150}

Serialized data (3 bytes)
-------------------------
DEC    HEX     BIN         ASCII
  8    0x08    00001000
150    0x96    10010110
  1    0x01    00000001
```

---
`python3 ./simple-message.py --type=string --val=test`
```
JSON equivalent (15 bytes)
--------------------------
{"data":"test"}

Serialized data (6 bytes)
-------------------------
DEC    HEX     BIN         ASCII
 10    0x0a    00001010
  4    0x04    00000100
116    0x74    01110100    t
101    0x65    01100101    e
115    0x73    01110011    s
116    0x74    01110100    t
```

---

`python3 ./simple-message.py --type="repeated bytes" --val=0xdeadbeef1337affe,0x44,0xac`
```
JSON equivalent (39 bytes)
--------------------------
{"data":["3q2+7xM3r/4=","RA==","rA=="]}

Serialized data (16 bytes)
--------------------------
DEC    HEX     BIN         ASCII
 10    0x0a    00001010
  8    0x08    00001000
222    0xde    11011110
173    0xad    10101101
190    0xbe    10111110
239    0xef    11101111
 19    0x13    00010011
 55    0x37    00110111    7
175    0xaf    10101111
254    0xfe    11111110
 10    0x0a    00001010
  1    0x01    00000001
 68    0x44    01000100    D
 10    0x0a    00001010
  1    0x01    00000001
172    0xac    10101100
```

## Usage

See `python3 simple-message.py --help`.

**Dependencies**

- `python3` ≥ v3.7.5
- Python protobuf package ≥ v3.14.0
- `protoc` ≥ v3.14.0