from MOL2File import *
from PDBFile import *
from XYZFile import *
from XSDFile import *
from LAMMPSDATAFile import *
from VASPFile import *

import MolecularManipulation
from UniversalMolecularSystem import *
from Utility import *
from BondDetection import *

def RecognizeFileType(filename):
    reader = None
    filename = filename.lower()
    if filename.endswith(".xyz"):
        reader = XYZFile()
    elif filename.endswith(".mol2"):
        reader = MOL2File()
    elif filename.endswith(".xsd"):
        reader = XSDFile()
    elif filename.endswith(".pdb"):
        reader = PDBFile()
    elif filename.endswith(".data"):
        reader = LAMMPSDATAFile()
    elif filename.find("poscar")!=-1 or filename.find("contcar")!=-1 or filename.find("vasp")!=-1: # This rule has lower priority
        reader = VASPFile()
    else:
        error("File <{}> with unknown extension. Can't open it. Sorry! ".format(filename))
    return reader

def QuickOpenFile(filename,withTiming=False,detectBond=True):
    reader = RecognizeFileType(filename)
    if reader == None:
        return
    ms = MolecularSystem()
    ms.Read(reader,filename)
    import time
    start = time.time()
    if detectBond:
        ms.AutoDetectBonds(DefaultBondRules(),flushCurrentBonds=True,periodicBoundary=None,max_workers=None,batch_size=5000)
    end = time.time()
    if withTiming:
        output("Bond Detection Takes {} s.".format(end-start))
    return ms

def QuickSaveFile(ms:MolecularSystem,filename:str):
    writer = RecognizeFileType(filename)
    if writer == None:
        return
    with open(filename,"w") as file:
        output.setoutput(file)
        ms.Write(writer)
        output.setoutput(sys.stdout)
