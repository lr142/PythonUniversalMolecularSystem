//
// Created by WL on 2022/8/6.
//

#include "utility.h"
#include <functional>
#include <algorithm>
using namespace std;
vector<string> split(string str,char delimitator) {
    string::size_type pos = 0;
    string::size_type new_pos = 0;
    vector<string> result;
    while(pos<str.size()){
        new_pos = str.find_first_of(delimitator,pos);
        if(new_pos == string::npos){
            // If the string not ends with delimitator, parse the last word
            new_pos = str.size();
        }
        if(new_pos>pos){
            // not true if two delimitator appears consecutively.
            result.push_back(str.substr(pos,new_pos-pos));
        }
        pos = new_pos + 1;
    }
    return result;
}
string strip(string str){
    auto not_a_space = [](char &c) {return !isspace(c);};
    auto pos = find_if(str.begin(),str.end(), not_a_space) - str.begin();
    if(pos==str.size())
        return "";
    auto rpos = str.rend() - find_if(str.rbegin(),str.rend(), not_a_space) ;
    return string(str.substr(pos,rpos-pos));
}
bool startswith(string line,string start){
    if(line.length() < start.length())
        return false;
    for(int i=0;i<start.length();i++){
        if(line[i] != start[i])
            return false;
    }
    return true;
}