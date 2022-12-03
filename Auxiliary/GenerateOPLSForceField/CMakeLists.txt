cmake_minimum_required(VERSION 3.10)
project(GenerateOPLSForceField)

set(CMAKE_CXX_STANDARD 20)

add_executable(GenerateOPLSForceField main.cpp forcefield.cpp forcefield.h utility.cpp utility.h)
