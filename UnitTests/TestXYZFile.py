import sys
sys.path.append("../")
from XYZFile import *
from VMDInterface import *
from Utility import *
import os
source = os.path.join(DATAFILESPATH,'Structures','FuchsSandoff.xyz')

def TestXYZFileMain(filename):

    s = MolecularSystem()

    s.Read(XYZFile(),filename)
    result = s.molecules[0].CheckConsistency()
    output('Check {}'.format("passed" if result else "NOT PASSED!"))
    s.Summary()

    file = open("dump.xyz",'w')
    output.setoutput(file)
    s.Write(XYZFile())
    file.close()

    vmd = VMDInterface("dump.xyz",autobonds=True)
    vmd.Run()

TestXYZFileMain(source)