//
// Created by WL on 2022/8/6.
//

#ifndef GENERATEOPLSFORCEFIELD_FORCEFIELD_H
#define GENERATEOPLSFORCEFIELD_FORCEFIELD_H
#include <iostream>
#include <string>
#include <vector>
#include <set>
#include <map>
using std::string;

// An atom in the OPLSAA forcefield. Not the same as a 'real' atom.
class Atom{
public:
    Atom() = default;
    Atom(const Atom &a) = default;
    ~Atom() = default;
    string element;
    string comment;
    // All are based on text search and replacement. therefore charge and mass are strings
    string charge;
    string mass;
    string epsilon;
    string sigma;
    friend std::ostream &operator<<(std::ostream &os, const Atom &atom);
    // In OPLS, each atom has two types:
    // the type of the atom itself, and the type when it participate in a bond (B),
    // angle (A), dihedral (D), or improper (I).
    string atom_type;
    string bond_type;
    };

template <int TYPE_COUNT,int PARA_COUNT>
class BADI{
    // Bond, Angle, Dihedral, or Improper
public:
    const int type_count = TYPE_COUNT;
    const int para_count = PARA_COUNT;
    string types[TYPE_COUNT];
    string parameters[PARA_COUNT];
    BADI() = default;
    bool involves(string bond_type);
    template <int TYPE_COUNTX,int PARA_COUNTX>
    friend std::ostream& operator<<(std::ostream &os,const BADI<TYPE_COUNTX,PARA_COUNTX> &badi);
};
typedef BADI<2,2> Bond;
typedef BADI<3,2> Angle;
typedef BADI<4,4> Dihedral;
typedef BADI<4,2> Improper;

class AtomicWeights{
    std::map<std::string,double> atomic_weights;
public:
    AtomicWeights(std::string atomic_weights_file);
    double getWeight(std::string element);
    std::string getElement(double weight);
};

class OPLSAAForcefield{
    std::map<string,Atom> atoms;
    std::vector<Bond> bonds;
    std::vector<Angle> angles;
    std::vector<Dihedral> dihedrals;
    std::vector<Improper> impropers;
    std::vector<string> atomtypesDefinedInRecognitionFile;
    std::set<std::string> already_included_atom_types;
    std::set<std::string> already_included_bonding_types;
    void ReadAtomTypesAndCharges(std::ifstream &file);
    void ReadAtomMasses(std::ifstream &file,AtomicWeights &aw);
    void ReadBondType(std::ifstream &file);
    void ReadPairCoeff(std::ifstream &file);
    void ReadBADICoeff(std::ifstream &file,string affect_what,string keyword, int types_count,int para_count);
    void WriteFunctional(std::ofstream &ofs, const string &functional_part_file) const;
    void WriteAtoms(std::ofstream &ofs);
    template <class T>
    void WriteBADI(std::ofstream &ofs,std::string title,std::string keyword,std::vector<T> &badi);
public:
    OPLSAAForcefield(string oplsfilename,AtomicWeights &aw);
    void ReadAtomTypesRecognitionFile(std::string atrfile_name);
    void WriteForcefieldDescriptionFile(std::string outputfile_name,std::string functional_part_file);

};


#endif //GENERATEOPLSFORCEFIELD_FORCEFIELD_H
