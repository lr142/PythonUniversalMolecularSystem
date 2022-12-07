import sys
import os
sys.path.append("../../../")
from UniversalMolecularSystem import *
from Opener import *
from Utility import *
import Forcefield
import VMDInterface

def Main(what,pdbfile):
    chunk = QuickOpenFile(pdbfile)
    chunk.boundary = [[0,100],[0,100],[0,100]]
    chunk.Summary()

    opls_ff = Forcefield.Forcefield(what+"/system",
                                    os.path.join("../../","oplsaa_2022.10.14","AtomTypes_Input.txt"),
                                    os.path.join("../../","oplsaa_2022.10.14", "FFDescription_Output.txt") )
    tip4p_ff = Forcefield.Forcefield(None,
                                    os.path.join("../../","tip4p","TIP4PAtomTypes.txt"),
                                    os.path.join("../../","tip4p", "TIP4PDescription.txt") )
    opls_ff.Extend(tip4p_ff)

    for i,mol in enumerate(chunk.molecules):
        if i == 0:
            opls_ff.AddMolecule(mol)
        else:
            opls_ff.AddMolecule(mol,copyFromMol=opls_ff.molecules[-1])

        ProgressBar(1.0*i/len(chunk.molecules))
    opls_ff.Finalize()
    opls_ff.SetBoundary(chunk.boundary)
    ProgressBar(1.0)
    print("")

    opls_ff.WriteLAMMPSFiles()
    dumpfilename = what+"/dump.mol2"
    vmdfile = what+"/vmd.tcl"
    chunk = ReduceSystemToOneMolecule(chunk)
    QuickSaveFile(chunk,dumpfilename)
    vmd = VMDInterface.VMDInterface("dump.mol2",scriptFileName=vmdfile)
    vmd.AddPeriodicBoundaryBox(boundary=chunk.boundary)
    vmd.Run(dryrun=True)

if __name__ == "__main__":
    Main("CH4","7500methane.pdb")
    Main("H2O","33428water.pdb")