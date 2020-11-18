#!/usr/bin/env zsh

cd "${0:A:h}"

protoc --python_out=./proto ./calc.proto
protoc --grpc_python_out=./proto ./calc.proto
