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

def SetupMolecule(filename, customBondRulesFilename,boundary):
    ms = MolecularSystem("'{}'".format(filename))
    if filename.endswith("mol2"):
        ms.Read(MOL2File(),filename)
    elif filename.endswith("xyz"):
        ms.Read(XYZFile(), filename)
    else:
        return
    if ms.boundary != None:  # 如果文件中有Cell信息，用文件中的，否则用参数boundary中的
        [xhi,yhi,zhi] = [ms.boundary[i][i] for i in range(3)]  # 把boundary信息从3x3矩阵转成3x2格式
        ms.boundary = [[0,xhi],[0,yhi],[0,zhi]]
    else:
        ms.boundary = boundary
    bondRules = DefaultBondRules()
    bondRules.Extend(customBondRulesFilename)
    ms.AutoDetectBonds(bondRules,flushCurrentBonds=True,periodicBoundary=ms.boundary)
    for a in ms.molecules[0].atoms:
        a.type = None
    return ms,bondRules

def AddLabels(molecularSystem,ABADI):
    mol = ReduceSystemToOneMolecule(molecularSystem).molecules[0]
    vmd = VMDInterface("dump.mol2", autobonds=False)
    vmd.AddCommand("label textthickness 1.5")
    vmd.AddCommand("label textsize 1.0")

    if 1 in ABADI:
        indexes = [_ for _ in range(len(mol.atoms))]
        labels = ["{}:{}".format(i+1,a.type) for i,a in enumerate(mol.atoms)]
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

    #filename = os.path.join(os.getcwd(),"2nm.cell.mol2")
    #filename = os.path.join(os.getcwd(),"4.Na3(Si31Al)(Al14Mg2)O80(OH)16.mol2")
    #filename = os.path.join(os.getcwd(), "2.Neutral_Perfect.mol2")

    #filename = os.path.join("/users/me","SCPDest","Montmorillonite","04.ScanAM","small.xyz")
    filename = os.path.join("TestMol","1.AM.xyz")
    #filename = os.path.join("TestMol", "4.C6H5CONH2.xyz")
    #filename = os.path.join("TestMol", "5.C6H5COOH.xyz")
    #filename = os.path.join("TestMol","6.C6H5COO.xyz")
    #filename = os.path.join("TestMol","7.AA.xyz")
    #filename = os.path.join("TestMol", "8.C2H5COOH.xyz")
    #filename = os.path.join("TestMol", "12.AANa.xyz")
    #filename = os.path.join("TestMol", "13.DADMAC.xyz")
    #filename = os.path.join("TestMol", "14.AADADMAC.xyz")

    customBondRules = os.path.join(os.getcwd(),"ClayBondRules.csv")
    boundary = None # 对MOL2文件无须提供boundary。对xyz文件，需在这里提供盒子大小
    boundary = [[-25,25],[-25,25],[-25,25]]
    ms,bondRules = SetupMolecule(filename,customBondRules,boundary)
    ms.Summary()

    # 填充溶剂的范围是盒子的范围减2.0
    # solvent_boundary = [[0,ms.boundary[i][1]-2] for i in range(3)]
    # solvates = SolvateSystem(ms,solvent_boundary,"spc",3.0)
    # ms.molecules.extend(solvates.molecules)
    # ms.RenumberAtomSerials()
    # ms.Summary()

    ff = Forcefield("system","ClayFFAtomTypes.txt","ClayFFDescription.txt")
    anotherFF = Forcefield("system",
                           os.path.join(FORCEFIELDSPATH, "OPLSAtomTypes.txt"),
                           os.path.join(FORCEFIELDSPATH, "OPLSDescription.txt"))
    ff.Extend(anotherFF)

    ########################DEBUGGING###################
    # ff.atomTypeRecognition.Show()
    # ff.forcefieldParameters.Show()
    # ff.atomTypeRecognition.__RecognizeOneAtomToOneRule_ForDebugging__(ms.molecules[0],-1,2)
    # exit(0)
    # bonded = ms.molecules[0].BondedMap()
    # ms.molecules[0].atoms[168].ShowAllFields()
    # print(bonded[168])
    # exit(0)
    ff.atomTypeRecognition.RecognizeAllAtoms(ms.molecules[0], maxDepth=3, maxIterations=5)
    for atom in ms.molecules[0].atoms:
        if atom.type == None:
            atom.ShowAllFields()
    #########################

    ff.SetBoundary(ms.boundary)
    output("Building Forcefield Parameters...")
    for i,mol in enumerate(ms.molecules):
        ff.AddMolecule(mol)
        if len(ms.molecules)>1000:
            ProgressBar(i/len(ms.molecules))
    output("")
    ff.Finalize()
    #ff.Show()
    ff.WriteLAMMPSFiles()


    totalCharge = 0.0
    for mol in ff.molecules:
        for atom in mol.atoms:
            totalCharge += atom.charge
    output("Total Charge = {}".format(totalCharge))

    vmd = AddLabels(ms,[1])
    # 最后输出整个体系。输出之前再重新找下键，把跨周期边界的键删了。
    ms.AutoDetectBonds(bondRules,flushCurrentBonds=True,periodicBoundary=None)
    with open("dump.mol2", "w") as dumpfile:
        output.setoutput(dumpfile)
        ReduceSystemToOneMolecule(ms).Write(MOL2File())
        output.setoutput(sys.stdout)
    vmd.Run(dryrun=True)

Main()


