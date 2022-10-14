import os
import sys
sys.path.append("../../")
from Forcefield import *
from Utility import *
from UniversalMolecularSystem import *
from XYZFile import *
from MOL2File import *
from BondDetection import *
from VMDInterface import *

def SetupMolecule(filename):
    ms = MolecularSystem("'{}'".format(filename))
    if filename.endswith("mol2"):
        ms.Read(MOL2File(),filename)
    elif filename.endswith("xyz"):
        ms.Read(XYZFile(), filename)
    else:
        return
    ms.AutoDetectBonds(DefaultBondRules())
    for a in ms.molecules[0].atoms:
        a.type = None
    return ms

def AddLabels(molecularSystem,ABADI):
    mol = ReduceSystemToOneMolecule(molecularSystem).molecules[0]
    vmd = VMDInterface("dump.mol2", autobonds=False)
    vmd.AddCommand("label textthickness 1.5")
    vmd.AddCommand("label textsize 1.0")

    if 1 in ABADI:
        indexes = [_ for _ in range(len(mol.atoms))]
        labels = ["%i:{}".format(a.type) for a in mol.atoms]
        vmd.AddLabels(indexes, labels, offset=[0.01, 0.01, 0.5])
        vmd.AddCommand("mol modstyle 0 0 CPK 0.6 0.2 12.0 12.0")
    for BADI in range(2,5):
        if BADI not in ABADI:
            continue
        categories = ["-","-","Bonds","Angles","Dihedrals"]
        pg = PathGenerator(mol.BondedMap())
        paths = pg.AllBondsAnglesDihedrals(BADI)
        for p in paths:
            placeholder = "0/{} "*BADI
            primitive = "label add {} {}".format(categories[BADI],placeholder)
            cmd = None
            if BADI == 2:
                cmd = primitive.format(p[0],p[1])
            elif BADI == 3:
                cmd = primitive.format(p[0],p[1],p[2])
            else:
                cmd = primitive.format(p[0],p[1],p[2],p[3])
            #print(primitive,cmd)
            vmd.AddCommand(cmd)
    return vmd

def Main():

    #filename = os.path.join(DATAFILESPATH,"Structures","tip4p_water_chunk.xyz")
    #filename = os.path.join(DATAFILESPATH, "Structures", "naphalene.xyz")
    filename = os.path.join("SPC_Cu.xyz")

    ms = SetupMolecule(filename)
    #ms = BreakupMoleculeByConnectivity(ms.molecules[0])
    ms.Summary()

    solvates = SolvateSystem(ms,[[0,30],[0,30],[0,20]],"spc",3.0)
    ms.molecules.extend(solvates.molecules)
    ms.Summary()

    with open("dump.mol2", "w") as dumpfile:
        output.setoutput(dumpfile)
        ms.Write(MOL2File())
        output.setoutput(sys.stdout)
    with open("dump.xyz", "w") as dumpfile:
        output.setoutput(dumpfile)
        ms.Write(XYZFile())
        output.setoutput(sys.stdout)

    ff = Forcefield("system","FFAtomTypes.txt","FFDescription.txt")
    #anotherFF = Forcefield("system",
                           #os.path.join(FORCEFIELDSPATH, "AtomTypes.txt"),
                           #os.path.join(FORCEFIELDSPATH, "TIP4PDescription.txt"))
    #ff.Extend(anotherFF)

    ff.SetBoundary([[-10, 40], [-10, 40], [-10, 40]])

    output("Building Forcefield Parameters...")
    for i,mol in enumerate(ms.molecules):
        ff.AddMolecule(mol)
        if len(ms.molecules)>1000:
            ProgressBar(i/len(ms.molecules))
    ff.Finalize()
    ff.WriteLAMMPSFiles()

    vmd = AddLabels(ms,[])

    vmd.Run(dryrun=True)

Main()


