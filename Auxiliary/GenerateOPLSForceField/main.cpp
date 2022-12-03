#include <iostream>
#include "forcefield.h"
#include "utility.h"
using namespace std;

int main(int argc, char *argv[]) {
    string PATH;
    if (argc==1)
        PATH = "../";
    else
        PATH = string(argv[1]);

    string OPLSAA_LT = PATH+"oplsaa.lt";
    string atomic_weights_file = PATH+"atomicweights.csv";
    string atom_type_recognition_file = PATH+"AtomTypes_Input.txt";
    string output_file_name = PATH+"FFDescription_Output.txt";
    string functional_file = PATH+"functional.txt";

    AtomicWeights aw(atomic_weights_file);
    OPLSAAForcefield opls(OPLSAA_LT,aw);
    opls.ReadAtomTypesRecognitionFile(atom_type_recognition_file);
    opls.WriteForcefieldDescriptionFile(output_file_name,functional_file);
}
