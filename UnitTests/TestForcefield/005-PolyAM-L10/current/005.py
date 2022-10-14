import os
import sys
sys.path.append("../")
from TestForcefield import *
from Utility import *

if __name__ == '__main__':
    RunCase("PolyAM-L10.xsd",
            ff_atoms = os.path.join(FORCEFIELDSPATH,"OPLSAtomTypes.txt"),
            ff_descript = os.path.join(FORCEFIELDSPATH,"OPLSDescription.txt"))
