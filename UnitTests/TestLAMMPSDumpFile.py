import sys
sys.path.append("../")
from LAMMPSDATAFile import *
from LAMMPSDUMPFile import *
from Utility import *
from UniversalMolecularSystem import *
from MolecularManipulation import *
import numpy as np
import time
def TestLAMMPSDUMPFile():

    #data_path = 'F:/seed2/0101_PolyAA_300K/system.data'
    #trj_path = 'F:/seed2/0101_PolyAA_300K/system.lammpstrj.2'
    data_path = "D:/0103_PolyAA_500K/system.data"
    trj_path = "D:/0103_PolyAA_500K/system.lammpstrj.2"

    ms = MolecularSystem()
    ms.Read(LAMMPSDATAFile(),data_path)
    ms.Summary()

    # start = time.time()
    # ms.ReadTrajectory(LAMMPSDUMPFile(),trj_path,timestep_in_fs=1.0,max_workers=1)
    # end = time.time()
    # print("Serial Reading Takes {} s".format(end-start))

    start = time.time()
    ms.ReadTrajectory(LAMMPSDUMPFile(),trj_path,timestep_in_fs=1.0)
    end = time.time()
    print("Parallel Reading Takes {} s".format(end-start))

    # output.setoutput(open('dump.xyz', 'w'))

    # for iFrame in range(ms.trajectory.NFrames):
    #     print(iFrame)
    #     subSys.UpdateCoordinatesByTrajectoryFrame(iFrame)
    #     toWrite = ReduceSystemToOneMolecule(subSys)
    #     toWrite.Write(XYZFile())

if __name__ == "__main__":
    TestLAMMPSDUMPFile()
    #cProfile.run("TestLAMMPSDUMPFile()")
