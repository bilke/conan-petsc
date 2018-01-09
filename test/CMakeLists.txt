cmake_minimum_required(VERSION 2.8.12)
project(MyPetsc)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)

conan_basic_setup()

find_package(MPI REQUIRED)

include_directories(${MPI_C_INCLUDE_DIRS})
add_executable(test main.cpp)
target_link_libraries(test ${CONAN_LIBS} ${CMAKE_DL_LIBS} ${MPI_C_LIBRARIES} MPI::MPI_C)
