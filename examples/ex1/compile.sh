#!/usr/bin/env zsh

cd "${0:A:h}"

python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./calc.proto
