import sys
sys.path.append("../")
from MOL2File import *
from VMDInterface import *
from BondDetection import *


def TestMOL2File():

    import SpecialStructure
    import MolecularManipulation

    s = SpecialStructure.GrapheneSheet(5,3)
    s2 = SpecialStructure.GrapheneSheet(5,3)
    s2.Translate(1.42,0,s.boundary[2][2])
    MolecularManipulation.ExtendSystem(s,s2)
    s.boundary[2][2] *= 2

    result = s.molecules[0].CheckConsistency()
    output('Check {}'.format("passed" if result else "NOT PASSED!"))
    s.Summary()

    images = []
    for i in range(3):
        for j in range(3):
            for k in range(1):
                images.append([i,j,k])
    MolecularManipulation.DuplicateSystemPeriodically(s,images)

    file = open("dump.mol2",'w')
    output.setoutput(file)
    newSys = MolecularManipulation.ReduceSystemToOneMolecule(s)
    newSys.AutoDetectBonds(DefaultBondRules(),True)
    newSys.Write(MOL2File())

    vmd = VMDInterface("dump.mol2",autobonds=False)
    vmd.Run()

TestMOL2File()