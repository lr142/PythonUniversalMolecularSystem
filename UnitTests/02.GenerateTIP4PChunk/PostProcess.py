import sys
sys.path.append("../../")
from UniversalMolecularSystem import *
from LAMMPSDATAFile import *
from XYZFile import *
from MOL2File import *
from MolecularManipulation import *
from VMDInterface import *

def Wrap(molSys,A,B,C):
    def __TranslateMol(mol,offX,offY,offZ):
        for a in mol.atoms:
            a.Translate(offX,offY,offZ)
    def __WrapOneMol(mol,A,B,C):
        while mol.atoms[0].x < 0:
            __TranslateMol(mol,A, 0, 0)
        while mol.atoms[0].x > A:
            __TranslateMol(mol,-A, 0, 0)
        while mol.atoms[0].y < 0:
            __TranslateMol(mol, 0, B, 0)
        while mol.atoms[0].y > B:
            __TranslateMol(mol, 0, -B, 0)
        while mol.atoms[0].z < 0:
            __TranslateMol(mol, 0, 0, C)
        while mol.atoms[0].z > C:
            __TranslateMol(mol, 0, 0, -C)
    for i,mol in enumerate(molSys.molecules):
        __WrapOneMol(mol,A,B,C)
        ProgressBar(i/len(molSys.molecules))

def Main():
    ms = MolecularSystem()
    ms.Read(LAMMPSDATAFile(),"relax.data")
    ms.Summary()
    Wrap(ms,50,50,50)
    ms = ReduceSystemToOneMolecule(ms)
    ms.Summary()



    with open("tip4p_water_5nm_chunk.mol2","w") as file:
        output.setoutput(file)
        ms.Write(MOL2File())

    vmd = VMDInterface("tip4p_water_5nm_chunk.mol2")
    vmd.Run()



Main()