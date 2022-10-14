from MOL2File import *
from PDBFile import *
from XYZFile import *
from XSDFile import *
from LAMMPSDATAFile import *

import MolecularManipulation
from UniversalMolecularSystem import *
from Utility import *
from BondDetection import *

def RecognizeFileType(filename):
    reader = None
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
    else:
        error("File <> with unknown extension. Can't open it. Sorry! ".format(filename))
    return reader

def QuickOpenFile(filename):
    reader = RecognizeFileType(filename)
    if reader == None:
        return
    ms = MolecularSystem()
    ms.Read(reader,filename)
    import time
    start = time.time()
    ms.AutoDetectBonds(DefaultBondRules(),flushCurrentBonds=True,periodicBoundary=None,max_workers=None,batch_size=5000)
    end = time.time()
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
