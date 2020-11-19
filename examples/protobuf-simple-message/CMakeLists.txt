cmake_minimum_required(VERSION 3.18)

set(CMAKE_EXPORT_COMPILE_COMMANDS on)
set(CMAKE_DISABLE_SOURCE_CHANGES on)
set(CMAKE_DISABLE_IN_SOURCE_BUILD on)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS ON)

project(simple-message CXX)

find_package(Protobuf REQUIRED)
find_package(Threads REQUIRED)

# Add target to compile protobuf
add_custom_target(compile-proto
    COMMAND protoc --cpp_out=${PROJECT_BINARY_DIR} ./simple-message.proto
    BYPRODUCTS ${PROJECT_BINARY_DIR}/simple-message.pb.cc
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
)

add_executable(simple-message simple-message.cc ${PROJECT_BINARY_DIR}/simple-message.pb.cc)
target_link_libraries(simple-message ${PROTOBUF_LIBRARY} ${CMAKE_THREAD_LIBS_INIT})
target_include_directories(simple-message
    PRIVATE ${PROJECT_BINARY_DIR})
add_dependencies(simple-message compile-proto)