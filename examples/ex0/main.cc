#include <iostream>
#include <iomanip>
#include <cstdio>
#include <string>
#include <sstream>
#include <vector>

#include <google/protobuf/stubs/common.h>
#include <google/protobuf/util/json_util.h>

#include "simple.pb.h"

std::string to_hex_listing(const std::vector<uint8_t>&);
std::string to_bitstring(uint8_t x, const std::string& nibble_sep = " ");
std::vector<uint8_t> msg_serialize(const google::protobuf::Message& msg);
std::string msg_jsonify(const google::protobuf::Message& msg);

using namespace google::protobuf;

int
main(int argc, char **argv)
{
    GOOGLE_PROTOBUF_VERIFY_VERSION;

    auto msg = foo::SimpleMessage {};
    msg.set_a(16384);
    std::cout << msg.DebugString();

    std::cout << "ByteSizeLong(): " << msg.ByteSizeLong() << std::endl;

    std::cout << to_hex_listing(msg_serialize(msg));

    auto json = msg_jsonify(msg);
    std::cout << "Compact JSON:\n" << json << std::endl;

    std::cout << "Size JSON = " << json.size() << ", Protobuf = " << msg.ByteSizeLong() << std::endl;

    ShutdownProtobufLibrary();
}

std::string
to_hex_listing(const std::vector<uint8_t>& bytes)
{
    auto ss = std::stringstream {};
    for (auto e: bytes) {
        ss << "0x" << std::hex << std::right << std::setfill('0') << std::setw(2) << (unsigned)e << "\t" << to_bitstring(e) << std::endl;
    }
    return ss.str();
}

std::string
to_bitstring(uint8_t x, const std::string& nibble_sep)
{
    auto ss = std::stringstream {};
    for (auto ii = 7; ii >= 4; ii--) {
        ss << ((x & (1 << ii)) ? 1 : 0);
    }
    ss << nibble_sep;
    for (auto ii = 3; ii >= 0; ii--) {
        ss << ((x & (1 << ii)) ? 1 : 0);
    }
    return ss.str();
}

std::vector<uint8_t>
msg_serialize(const google::protobuf::Message& msg)
{
    auto bytes = std::vector<uint8_t>(msg.ByteSizeLong());
    msg.SerializeToArray(bytes.data(), bytes.size());
    return bytes;
}

/*
 * Return a message's compact JSON representation.
 */
std::string
msg_jsonify(const google::protobuf::Message& msg)
{
    auto json = std::string {};
    util::MessageToJsonString(msg, &json);

    return json;
}