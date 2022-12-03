import os
import sys
sys.path.append("../")
from TestForcefield import *

if __name__ == '__main__':
    ff_atoms = os.path.join("../oplsaa_2022.10.14", "AtomTypes_Input.txt")
    ff_descript = os.path.join("../oplsaa_2022.10.14", "FFDescription_Output.txt")

    #RunCase("PolyDADMAC.xsd")
    RunCase("Given1.mol2",ff_atoms,ff_descript)
