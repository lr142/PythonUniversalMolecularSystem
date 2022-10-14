import sys
sys.path.append("../../")
from ForcefieldParameters import *

ffp = ForcefieldParameters("SPC")
at = Pairwise()
ffp.ReadForcefieldParametersFile(os.path.join(FORCEFIELDSPATH,"OPLSDescription.txt"))
ffp.ShowForcefieldParameters()

