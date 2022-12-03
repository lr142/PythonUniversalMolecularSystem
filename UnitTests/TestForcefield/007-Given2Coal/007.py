import os
import sys
sys.path.append("../")
from TestForcefield import *

ff_atoms = os.path.join("../oplsaa_2022.10.14", "AtomTypes_Input.txt")
ff_descript = os.path.join("../oplsaa_2022.10.14", "FFDescription_Output.txt")
if __name__ == '__main__':
    RunCase("Given2.mol2",ff_atoms,ff_descript)
