//
// Created by WL on 2022/8/6.
//
#include <fstream>
#include <cmath>
#include <iomanip>
#include <algorithm>
#include <sstream>
#include "forcefield.h"
#include "utility.h"
using namespace std;

ostream &operator<<(ostream &os, const Atom &atom) {
    os << "element: " << atom.element << " comment: " << atom.comment << " charge: " << atom.charge << " mass: "
       << atom.mass << " epsilon: " << atom.epsilon << " sigma: " << atom.sigma << " atom_type: " << atom.atom_type
       << " bond_type: " << atom.bond_type;
    return os;
}

template <int TYPE_COUNT,int PARA_COUNT>
bool BADI<TYPE_COUNT,PARA_COUNT>::involves(string bond_type) {
    for(int i=0;i<TYPE_COUNT;i++){
        if(this->types[i] == bond_type)
            return true;
    }
    return false;
}
template <int TYPE_COUNT,int PARA_COUNT>
ostream& operator<<(ostream &os, BADI<TYPE_COUNT,PARA_COUNT> &badi) {
    os << "types: ";
    for(int i=0;i<TYPE_COUNT;i++){
        os<<badi.types[i]<<" ";
    }
    os<<" parameters: ";
    for(int j=0;j<PARA_COUNT;j++){
        os<<badi.parameters[j]<<" ";
    }
    return os;
}

AtomicWeights::AtomicWeights(string atomic_weights_file){
    ifstream ifs(atomic_weights_file);
    if(!ifs.is_open()){
        cerr<<"Can't open ["<<atomic_weights_file<<"]"<<endl;
    }
    string line;
    while(getline(ifs,line)){
        auto parts = split(line,',');
        auto element = parts[0];
        auto weight = stof(parts[1]);
        this->atomic_weights[element] = weight;
    }
}
double AtomicWeights::getWeight(std::string element){
    if(atomic_weights.find(element)!=atomic_weights.end()){
        return atomic_weights[element];
    }else{
        return 0.0;
    }
}
string AtomicWeights::getElement(double weight){
    double minDiff = 999999.9;
    string bestMatch;
    for(auto kv:this->atomic_weights){
        double diff = fabs(weight - kv.second);
        if(diff<minDiff){
            minDiff = diff;
            bestMatch = kv.first;
        }
    }
//    if(minDiff > 0.5){
//        cerr<<"Warning: In AtomicWeights::getElement(), can't find an element with weight = "<<weight
//        <<". And the best match is ["<<bestMatch<<"] = "<<this->atomic_weights[bestMatch]<<endl;
//    }
    return bestMatch;
}
OPLSAAForcefield::OPLSAAForcefield(string oplsfilename,AtomicWeights &aw) {
    ifstream file(oplsfilename);
    if(!file.is_open()){
        cerr << "Can't open " << oplsfilename << endl;
    }
    ReadAtomTypesAndCharges(file);
    ReadAtomMasses(file,aw);
    ReadBondType(file);
    ReadPairCoeff(file);
    ReadBADICoeff(file,"bond","bond_coeff",2,2);
    ReadBADICoeff(file,"angle","angle_coeff",3,2);
    ReadBADICoeff(file,"dihedral","dihedral_coeff",4,4);
    ReadBADICoeff(file,"improper","improper_coeff",4,2);

    // 对于IMPROPERS，还需要调整一下，把第3个原子换做第一个原子，并把参数角度换成 180-原角度。
    for(auto &im:this->impropers){
        string temp[] = { im.types[2],im.types[0],im.types[1],im.types[3] };
        copy(begin(temp),end(temp),begin(im.types));
        im.parameters[1] = to_string(180.0 - stof(im.parameters[1]));
    }

    //    for(auto a:this->atoms){
//        cout<<a.second<<endl;
//    }
//    for(auto b:this->bonds){
//        cout<<b<<endl;
//    }
//    for(auto a:this->angles){
//        cout<<a<<endl;
//    }
//    for(auto d:this->dihedrals){
//        cout<<d<<endl;
//    }
//    for(auto i:this->impropers){
//        cout<<i<<endl;
//    }
}
void OPLSAAForcefield::ReadAtomTypesAndCharges(ifstream &file) {// Read Atom types and charges
    string line;
    while(getline(file,line)) {
        if (strip(line) == "write_once(\"In Charges\") {")
            break;
    }
    while(getline(file,line)) {
        line = strip(line);
        if(line[0] == '#')
            continue;
        else if(line[0] == '}')
            break;
        else {}
        // set type @atom:902 charge 0.05  # "Allene/Ketene R2C=C=X"
        auto parts = split(line);
        if(parts.size() < 6)
            continue;
        Atom a;
        a.atom_type = split(parts[2],':')[1];
        a.charge = parts[4];
        auto comment_begin_pos = line.find('"');
        auto comment_end_pos = line.find_last_of('"');
        a.comment = line.substr(comment_begin_pos+1,comment_end_pos-comment_begin_pos-1);
        atoms[a.atom_type] = a;
    }
}
void OPLSAAForcefield::ReadAtomMasses(ifstream &file,AtomicWeights &aw) {
    string line;
    while(getline(file,line)) {
        if (strip(line) == "write_once(\"Data Masses\") {")
            break;
    }
    while(getline(file,line)) {
        line = strip(line);
        if(line[0] == '#')
            continue;
        else if(line[0] == '}')
            break;
        else {}
        // @atom:906 12.011  # 906
        auto parts = split(line);
        if(parts.size() < 3)
            continue;
        auto atom_type = split(parts[0],':')[1];
        auto mass = parts[1];
        atoms[atom_type].mass = mass;
        atoms[atom_type].element = aw.getElement(stof(mass));
    }
}
void OPLSAAForcefield::ReadBondType(ifstream &file) {
    string line;
    while(getline(file,line)) {
        auto parts = split(line);
        if(parts.size() != 4 || parts[0]!="replace{")
            continue;
        if(strip(line)=="write_once(\"In Settings\")")
            break;
        // replace{ @atom:892 @atom:892_b046_a046_d046_i046 }
        parts = split(parts[2],'_');
        // [0:"atom:892", 1:"b046", 2:"a046", 3:"d046", 4:"i046"]
        auto atom_type = split(parts[0],':')[1];
        auto bond_type = parts[1].substr(1,3);
        auto angle_type = parts[2].substr(1,3);
        auto dihedral_type = parts[3].substr(1,3);
        auto improper_type = parts[4].substr(1,3);
        if (bond_type!=angle_type){
            cerr << "bond_type!=angle_type";
        }
        if (bond_type!=dihedral_type){
            cerr << "bond_type!=dihedral_type";
        }
        if (bond_type!=improper_type){
            cerr << "bond_type!=improper_type";
        }
        atoms[atom_type].bond_type = bond_type;
    }
}
void OPLSAAForcefield::ReadPairCoeff(ifstream &file) {//Read Pair_Coeff
//pair_coeff @atom:1_b001_a001_d001_i001 @atom:1_b001_a001_d001_i001  0.061 2.94
    string line;
    file.clear();
    file.seekg(0);
    while(getline(file,line)){
        if(!startswith(strip(line),"pair_coeff"))
            continue;
        auto parts = split(line);
        if(parts[1]!=parts[2]){
            cerr<<"pair_coeff between unlike atoms!"<<endl;
            cerr<<line<<endl;
        }
        auto epsilon = parts[3];
        auto sigma = parts[4];
        auto atom_type = split(split(parts[1],'_')[0],':')[1];
        atoms[atom_type].epsilon = epsilon;
        atoms[atom_type].sigma = sigma;
    }
}
void OPLSAAForcefield::ReadBADICoeff(std::ifstream &file,string affect_what,string keyword, int types_count,int para_count) {
    file.clear();
    file.seekg(0);
    string line;
    while(getline(file,line)){
        //bond_coeff @bond:001_002  367.0 1.38
        //angle_coeff @angle:002_002_002  63.0 112.4
        //dihedral_coeff @dihedral:X_002_002_002  -2.5 1.25 3.1 0.0
        //improper_coeff @improper:X_X_003_004  10.5 180.0  # (moltemplate)
        if(!startswith(strip(line),keyword))
            continue;
        auto parts = split(line);
        auto types = split(split(parts[1],':')[1],'_');
        for(auto &t:types){
            if(t=="X")
                t = "*";
        }
        auto write_to = [types,parts](string *w_types,string *w_paras,int types_count,int para_count){
            for(int i=0;i<types_count;i++)
                w_types[i] = types[i];
            for(int j=0;j<para_count;j++)
                w_paras[j] = parts[j+2];
        };
        if(affect_what == "bond"){
            Bond b;
            write_to(b.types,b.parameters,types_count,para_count);
            this->bonds.push_back(b);
        }else if(affect_what == "angle"){
            Angle a;
            write_to(a.types,a.parameters,types_count,para_count);
            this->angles.push_back(a);
        }else if(affect_what == "dihedral"){
            Dihedral d;
            write_to(d.types,d.parameters,types_count,para_count);
            this->dihedrals.push_back(d);
        }else if(affect_what == "improper"){
            Improper i;
            write_to(i.types,i.parameters,types_count,para_count);
            this->impropers.push_back(i);
        }else{}
    }
}
void OPLSAAForcefield::ReadAtomTypesRecognitionFile(string atrfile_name){
    ifstream ifs(atrfile_name);
    if(!ifs.is_open()){
        cerr<<"Can't open ["<<atrfile_name<<"]."<<endl;
    }
    string line;
    int lineno = 0;
    while(getline(ifs,line)){
        ++lineno;
        line = strip(line);
        if(line.length()==0 || startswith(line,"#"))
            continue;
        string keyword = split(line)[0];
        auto parts = split(keyword,':');
        if(parts.size()<2){
            cerr<<"On line "<<lineno<<" of ["<<atrfile_name<<"]:"<<endl;
            cerr<<line<<endl;
            cerr<<"Format error"<<endl;
        }
        auto atom_type = parts[1];
        this->atomtypesDefinedInRecognitionFile.push_back(atom_type);
    }
}
void OPLSAAForcefield::WriteForcefieldDescriptionFile(std::string outputfile_name,string functional_part_file){
    ofstream ofs(outputfile_name,ofstream::out);
    if(!ofs.is_open()){
        cerr<<"Can't open ["<<outputfile_name<<"] to write."<<endl;
    }

    WriteFunctional(ofs, functional_part_file);
    WriteAtoms(ofs);
    WriteBADI(ofs,"BONDS", "bond_coeff",this->bonds);
    WriteBADI(ofs,"ANGLES", "angle_coeff",this->angles);
    WriteBADI(ofs,"DIHEDRALS","dihedral_coeff", this->dihedrals);
    WriteBADI(ofs,"IMPROPERS","improper_coeff",this->impropers);
    ofs.close();
}
void OPLSAAForcefield::WriteFunctional(ofstream &ofs, const string &functional_part_file) const {
    ifstream ifs(functional_part_file);
    if(!ifs.is_open()){
        cerr<<"Can't open ["<<functional_part_file<<"] to read."<<endl;
    }
    string line;
    while(getline(ifs,line)){
        ofs<<line<<endl;
    }
}
void OPLSAAForcefield::WriteAtoms(ofstream &ofs) {
    ostringstream buffer_for_PAIRWISE;
    ofs<<"ATOMS {"<<endl;
    ofs<<"#    Atom    Bond     Mass     Charge # Comment"<<endl;
    buffer_for_PAIRWISE << "PAIRWISE {"<<endl;
    for(string atom_type: atomtypesDefinedInRecognitionFile){
        if(already_included_atom_types.find(atom_type)!=already_included_atom_types.end())
            continue;
        // 考虑特殊情况：C:87(charge=-0.215)表示基于87号类型，但电荷要改成-0.215。正常情况下没有括号中部分
        string custom_charge = "";
        // 用于索引的原子类型。如果不含特殊情况，应该等于atom_type为一个普通的两位数字
        string atom_type_for_indexing = atom_type;
        if(atom_type.find("charge")!=atom_type.npos){ // 以上所说的特殊情况
            auto start = atom_type.find("=")+1;
            auto end = atom_type.find(")");
            custom_charge = atom_type.substr(start,end-start );
            atom_type_for_indexing = split(atom_type,'(')[0];
        }
        Atom &a = atoms[atom_type_for_indexing];
        already_included_atom_types.insert(atom_type);
        already_included_bonding_types.insert(a.bond_type);
        if(custom_charge == "")
            custom_charge = a.charge;
        ofs<<"    "<<setw(6)<<atom_type<<setw(6)<<a.bond_type
           <<setw(10)<<a.mass<<setw(10)<<custom_charge
           <<"  # "<<a.comment<<endl;
        buffer_for_PAIRWISE <<"    pair_coeff "
        <<setw(8)<<atom_type<<"  "<<setw(8)<<atom_type
        <<setw(10)<<a.epsilon<<setw(10)<<a.sigma<<endl;
    }
    ofs<<"}"<<endl<<endl;
    ofs<<buffer_for_PAIRWISE.str()<<"}"<<endl<<endl;
}
template <class T>
void OPLSAAForcefield::WriteBADI(ofstream &ofs,string title,string keyword,vector<T> &badi) {
    ofs << title<<" {" << endl;
    for(auto &b: badi){
        // 什么时候应该将该种B，A，D，I写入文件中？它涉及的几种原子类型均在原子类型识别文件中就需要。（或者是*）
        bool should_include = true;
        for(int i=0;i<b.type_count;i++){
            auto bondingType = b.types[i];
            if(bondingType == "*")
                continue;
            if(already_included_bonding_types.find(bondingType) == already_included_bonding_types.end()){
                should_include = false;
                break;
            }
        }

        if(should_include){
            ofs<<"   ";
            for(int i=0;i<b.type_count;i++){
                ofs<<" "<<setw(8)<<b.types[i];
            }
            ofs<<"    "<<keyword<<" -- ";
            for(int i=0;i<b.para_count;i++){
                ofs<<" "<<setw(10)<<b.parameters[i];
            }
            ofs<<endl;
        }
    }
    ofs<<"}"<<endl<<endl;
}
