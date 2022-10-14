//
// Created by WL on 2022/8/6.
//

#ifndef GENERATEOPLSFORCEFIELD_UTILITY_H
#define GENERATEOPLSFORCEFIELD_UTILITY_H
#include <vector>
#include <iostream>

std::vector<std::string> split(std::string str,char delimitator=' ');
std::string strip(std::string);
bool startswith(std::string line,std::string start);
#endif //GENERATEOPLSFORCEFIELD_UTILITY_H
