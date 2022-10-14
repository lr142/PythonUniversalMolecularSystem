import os
import sys
sys.path.append("../")
from TestForcefield import *

def Main():
    filename = os.path.join(".", "spc_water.xyz")

    ms = SetupMolecule(filename)
    ms = BreakupMoleculeByConnectivity(ms.molecules[0])

    ff = Forcefield("system",
                    os.path.join("../OPLS", "AtomTypes_Input.txt"),
                    os.path.join("../OPLS", "FFDescription_Output.txt"))
    # 如果需要组合力场，请在这里加入
    # anotherFF = Forcefield("system",
    #     os.path.join(FORCEFIELDSPATH, "TIP4PAtomTypes.txt"),
    #     os.path.join(FORCEFIELDSPATH, "TIP4PDescription.txt"))
    # ff.Extend(anotherFF)

    ff.SetBoundary([[-50, 50], [-50, 50], [-50, 50]])
    for mol in ms.molecules:
        ff.AddMolecule(mol)
    ff.Finalize()
    ff.WriteLAMMPSFiles()

    vmd = AddLabels(ms,[1])

    vmd.Run(dryrun=True)

if __name__ == '__main__':
    Main()


