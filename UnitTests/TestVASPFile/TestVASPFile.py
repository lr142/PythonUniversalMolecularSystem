import sys
sys.path.append("../")
from VASPFile import *
from Opener import *
import os

def TestVASPFileMain(filename):
    s = MolecularSystem()
    s.Read(VASPFile(),filename)
    s.Summary()
    QuickSaveFile(s,"CONTCAR.dump")


    # file = open("dump.xyz",'w')
    # output.setoutput(file)
    # s.Write(XYZFile())
    # file.close()
    #
    # vmd = VMDInterface("dump.xyz",autobonds=True)
    # vmd.Run()

if __name__ == "__main__":
    TestVASPFileMain("CONTCAR-")