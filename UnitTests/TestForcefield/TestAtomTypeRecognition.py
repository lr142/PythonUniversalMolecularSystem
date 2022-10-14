import sys
sys.path.append("../../")
from ForcefieldAtomTypeRecognition import *
from UniversalMolecularSystem import *
from XYZFile import XYZFile
from BondDetection import *
from MOL2File import MOL2File
from VMDInterface import VMDInterface
from Utility import *
import os

def SetupMolecule(filename):
    ms = MolecularSystem()
    if filename.endswith("mol2"):
        ms.Read(MOL2File(),filename)
    elif filename.endswith("xyz"):
        ms.Read(XYZFile(), filename)
    else:
        return

    ms.AutoDetectBonds(DefaultBondRules())
    for a in ms.molecules[0].atoms:
        a.type = None
    ms.Summary()
    with open("dump.mol2", "w") as dumpfile:
        output.setoutput(dumpfile)
        ms.Write(MOL2File())
        output.setoutput(sys.stdout)
    return ms

def AddLabels(molecularSystem):
    mol = molecularSystem.molecules[0]
    indexes = [_ for _ in range(len(mol.atoms))]
    labels = ["%i:{}".format(a.type) for a in mol.atoms]
    vmd = VMDInterface("dump.mol2", autobonds=False)
    vmd.AddLabels(indexes, labels, offset=[0.01, 0.01, 0.5])
    vmd.AddCommand("mol modstyle 0 0 CPK 0.6 0.2 12.0 12.0")
    return vmd

def Main():
    atr = AtomTypeRecognition(os.path.join(FORCEFIELDSPATH,"OPLSAtomTypes.txt"))
    filename = os.path.join(DATAFILESPATH,"Structures","naphalene.xyz")
    ms = SetupMolecule(filename)

    #atr.__RecognizeOneAtomToOneRule_ForDebugging__(ms.molecules[0],iRule=12,iAtom=1,debugging=True)
    atr.RecognizeAllAtoms(ms.molecules[0],debugging=False,maxIterations=5)

    #atr.__RecognizeOneAtomToOneRule_ForDebugging__(ms.molecules[0], iRule=7, iAtom=7, debugging=True)

    vmd = AddLabels(ms)
    vmd.AddCommand("label textthickness 3.6")
    vmd.AddCommand("label textsize 1.0")
    vmd.Run()

Main()




