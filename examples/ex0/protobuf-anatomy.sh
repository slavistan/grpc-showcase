#!/usr/bin/env zsh

cd ${0:A:h}

case "$1" in
--help|-h)
    cat <<EOF
Usage:
  $0 [--wiretype TYPE] [--value VALUE] [--fieldid ID]
  $0 clean
  $0 --help | -h
EOF
    exit 0
    ;;
clean)
    rm -r build main.cc simple.proto
    exit 0
    ;;
esac
set -e

# Parse args
wiretype=${wiretype:-int32}
fieldid=${fieldid:-1}
value=${value:-100}

ii=0
for var in "$@"; do
    ii=$((ii + 1))
    if [ "$var" = "--fieldid" ]; then
        fieldid=$argv[$((ii + 1))]
    elif [ "$var" = "--wiretype" ]; then
        wiretype=$argv[$((ii + 1))]
    elif [ "$var" = "--value" ]; then
        value=$argv[$((ii + 1))]
    fi
done

sed 's/<<__WIRETYPE__>>/'"$wiretype"'/g' ./simple.proto.template |
    sed 's/<<__FIELDID__>>/'"$fieldid"'/g' > simple.proto

if [ "$wiretype" = "string" ]; then
    # add outer quotation marks and quote inner quotation marks
    value="$(echo "$value" | sed 's:":\\\\":g')"
    sed 's/<<__VALUE__>>/"'"${value}"'"/g' ./main.cc.template > main.cc
else
    sed 's/<<__VALUE__>>/'"${value}"'/g' ./main.cc.template > main.cc
fi

if [ ! -d build ]; then
    mkdir -p build
    cd build
    cmake ..
    cd ..
fi

make -C build >/dev/null
./build/protobuf-anatomy