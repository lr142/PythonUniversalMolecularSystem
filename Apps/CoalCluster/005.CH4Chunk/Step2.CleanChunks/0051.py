import sys
import os

import TopologyMatching

sys.path.append("../../../")
from UniversalMolecularSystem import *
from Opener import *
from Utility import *
import Forcefield
import VMDInterface


def Process(what:str,datafile:str,P_in_MPa:int):
    if not os.path.isfile(datafile):
        print("File <{}> not read.".format(datafile))
        return
    molSys = MolecularSystem()
    molSys.Read(LAMMPSDATAFile(),datafile)
    molSys.Summary()
    NAtomsEachMol = len(molSys.molecules[0].atoms)
    UVW = [0,0,0]
    for i in range(3):
        UVW[i] = molSys.boundary[i][i]
    for iMol, mol in enumerate(molSys.molecules):
        result = TopologyMatching.TopologyMatching([molSys.molecules[0], mol], [0, 0])
        # check atoms order not altered
        for i in range(NAtomsEachMol):
            if result == None or result[i] != i:
                print("Not Match!")
                print(result)
                exit(-1)
        # Wrap atoms within the original cell
        center = np.zeros(3)
        for atom in mol.atoms:
            center += atom.XYZ()
        center /= len(mol.atoms)
        offset = [0,0,0]
        for i in range(3):
            offset[i] = - int(math.floor(center[i]/UVW[i])) * UVW[i]
        for atom in mol.atoms:
            atom.Translate(offset[0],offset[1],offset[2])
    # Dump
    molSys = ReduceSystemToOneMolecule(molSys)
    outputname = "./{}/{}MPa.mol2".format(what,P_in_MPa)
    QuickSaveFile(molSys,outputname)

def Main(what,pressures_atm):
    for p_atm in pressures_atm:
        datapath = os.path.join("..","Step1.PrepareChunks",what,"{}.data".format(p_atm) )
        Process(what,datapath,int(p_atm/10))

if __name__ == "__main__":
    pressures_atm_CH4 = [(i + 1) * 10 for i in range(25)]
    pressures_atm_H2O = [100]
    Main("CH4",pressures_atm_CH4)
    Main("H2O",pressures_atm_H2O)