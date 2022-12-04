import sys
import os
sys.path.append("../../")
from UniversalMolecularSystem import *
from Opener import *
from Utility import *
import Forcefield
import VMDInterface

def Main():
    # molSys = QuickOpenFile("Cluster06_1.mol2")
    # molSys.Summary()
    # molSys = BreakupMoleculeByConnectivity(molSys.molecules[0])
    # molSys.Summary()
    cluster = MolecularSystem()
    cluster.Read(MOL2File(),"222Super.mol2")
    bound = cluster.boundary
    # cluster = ReduceSystemToOneMolecule(cluster)
    cluster = BreakupMoleculeByConnectivity(cluster.molecules[0])
    cluster.boundary = bound
    for mol in cluster.molecules:
        for atom in mol.atoms:
            atom.type = None

    # determine min distance
    NAtoms = 0
    for mol in cluster.molecules:
        NAtoms += len(mol.atoms)
    dists = np.zeros((NAtoms,NAtoms))

    # import math
    # i = 0
    # for mol1 in cluster.molecules:
    #     for atom1 in mol1.atoms:
    #         i+=1
    #         j = -1
    #         for mol2 in cluster.molecules:
    #             for atom2 in mol2.atoms:
    #                 j+=1
    #                 if i>j:
    #                     continue
    #                 elif i==j:
    #                     dists[i,j] = 999
    #                 else:
    #                     d = math.pow(atom1.x - atom2.x,2) + math.pow(atom1.y-atom2.y,2) + math.pow(atom1.z-atom2.z,2)
    #                     d = math.sqrt(d)
    #                     dists[i,j] = dists[j,i] = d
    # print(np.min(dists))



    ff_opls = Forcefield.Forcefield("system",
                                    os.path.join("../","oplsaa_2022.10.14", "AtomTypes_Input.txt"),
                                    os.path.join("../","oplsaa_2022.10.14", "FFDescription_Output.txt"))

    U = bound[0][0]
    V = bound[1][1]
    W = bound[2][2]
    ff_opls.SetBoundary([[0,U],[0,V],[0,W]])
    for i,mol in enumerate(cluster.molecules):
        if i > 0 and len(mol.atoms) == len(cluster.molecules[i-1].atoms):
            ff_opls.AddMolecule(mol,copyFromMol=ff_opls.molecules[-1])
        else:
            ff_opls.AddMolecule(mol,copyFromMol=None)

        ProgressBar(1.0*i/len(cluster.molecules))
    ProgressBar(1.0)
    print("")

    ff_opls.Finalize()
    ff_opls.WriteLAMMPSFiles()
    as_one = ReduceSystemToOneMolecule(cluster)
    as_one.boundary = bound
    QuickSaveFile(as_one,"dump.mol2")
    vmd = VMDInterface.VMDInterface("dump.mol2")
    vmd.Run(dryrun=True)

    totalCharge = 0.0
    for mol in ff_opls.molecules:
        for atom in mol.atoms:
            charge = atom.charge
            totalCharge += charge
    print("Total Charge = {}".format(totalCharge))


if __name__ == "__main__":
    Main()