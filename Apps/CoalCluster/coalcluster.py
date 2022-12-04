import sys
import os
sys.path.append("../../")
from UniversalMolecularSystem import *
from Opener import *
from Utility import *
import Forcefield
import VMDInterface

def Main():
    names = ["Given1.mol2","FuchsSandoff.mol2","CartzHirsch.mol2"]
    molSys = MolecularSystem()
    for i,name in enumerate(names):
        newSys = QuickOpenFile(name)
        molSys.molecules.append(newSys.molecules[0])
        for atom in newSys.molecules[0].atoms:
            atom.type = None
            atom.z += 10*i
        ff_opls = Forcefield.Forcefield("system",
                                        os.path.join("oplsaa_2022.10.14", "AtomTypes_Input.txt"),
                                        os.path.join("oplsaa_2022.10.14", "FFDescription_Output.txt"))
        ff_opls.AddMolecule(newSys.molecules[0], fixed=False, rigid=False, withBonds=True,
                            useCurrentCharges=False, copyFromMol=None)
        ff_opls.Finalize()
        ff_opls.WriteMoleculeTemplateFile(name.split(".")[0]+".txt")


    ff_opls = Forcefield.Forcefield("system",
                                    os.path.join("oplsaa_2022.10.14", "AtomTypes_Input.txt"),
                                    os.path.join("oplsaa_2022.10.14", "FFDescription_Output.txt"))
    ff_opls.SetBoundary([[0, 100], [0, 100], [0, 100]])
    for mol in molSys.molecules:
        ff_opls.AddMolecule(molSys.molecules[0],fixed=False,rigid=False,withBonds=True,
                            useCurrentCharges=False,copyFromMol=None)
    ff_opls.Finalize()
    ff_opls.WriteLAMMPSFiles()
    molSys = ReduceSystemToOneMolecule(molSys)
    QuickSaveFile(molSys,"dump.mol2")
    vmd = VMDInterface.VMDInterface("dump.mol2","vmd.tcl",False)
    vmd.Run(None,True)

if __name__ == "__main__":
    Main()