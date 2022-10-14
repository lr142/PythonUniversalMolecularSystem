import sys
sys.path.append("../")
sys.path.append("D:/_Nutbox/UniversalMolecularSystem")
sys.path.append("/mnt/d/_Nutbox/UniversalMolecularSystem")
from UniversalMolecularSystem import *
from Utility import *
from LAMMPSDATAFile import *
from LAMMPSDUMPFile import *

PATH="E:/seed1/0101_PolyAA_300K"

def AnalyzePolymerPosition(ms):
    ClaySurfZ = -9999
    for atom in ms.molecules[0].atoms:
        if atom.z > ClaySurfZ:
            ClaySurfZ = atom.z
    #print("Clay Surf Z = {}".format(ClaySurfZ))
    x = []
    y1 = []
    y2 = []


    for iFrame in range(ms.trajectory.NFrames):
        ms.UpdateCoordinatesByTrajectoryFrame(iFrame)
        polymerMinZ = 99999
        polymerCenterZ = 0.0
        for atom in ms.molecules[4].atoms:
            if atom.z < polymerMinZ:
                polymerMinZ = atom.z
            polymerCenterZ += atom.z
        polymerCenterZ /= len(ms.molecules[4].atoms)
        #print("Polymer Center = {}, Min = {}".format(polymerCenterZ,polymerMinZ))
        x.append(ms.trajectory.timesteps_of_each_frame[iFrame]/1e6)
        y1.append(polymerCenterZ - ClaySurfZ)
        y2.append(polymerMinZ - ClaySurfZ)


    outputfile = open("PolymerPosition.csv","w")
    for i,val in enumerate(x):
        outputfile.write("{},{},{},,\n".format(x[i],y1[i],y2[i]))
    outputfile.close()
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    plt.rcParams['font.family'] = 'Helvetica'
    plt.rcParams['xtick.labelsize'] = 14
    plt.rcParams['ytick.labelsize'] = 14
    plt.rcParams['axes.labelsize'] = 14

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(x,y1,label='center',color='black',linewidth=1)
    ax.plot(x,y2,label='min',color='red', linewidth=1)
    ax.legend()
    ax.set_xlabel("Time (ns)")
    ax.set_ylabel("Distance (Å)")
    plt.savefig('PolymerPosition.jpg')

def Main():
    ms = MolecularSystem()
    ms.Read(LAMMPSDATAFile(),os.path.join(PATH,"system.data"))
    ms.Summary()
    ms.ReadTrajectory(LAMMPSDUMPFile(),os.path.join(PATH,"system.lammpstrj"),maxFrames=99999,flushSameTimestep=True,
                      timestep_in_fs=1.0,every=1)
    ms.ReadTrajectory(LAMMPSDUMPFile(), os.path.join(PATH, "system.lammpstrj.2"), maxFrames=999999, flushSameTimestep=True,
                      timestep_in_fs=1.0,every=1)

    AnalyzePolymerPosition(ms)

Main()
