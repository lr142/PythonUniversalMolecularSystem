import sys

import Utility
from Utility import *
from UniversalMolecularSystem import *
from MOL2File import *
from XYZFile import *

def BreakupMolecule(originalMolecule, atomBelongToNewMoleculeSerialMap):
    # This function breaks up a molecule and return a MolecularSystem.
    # If successful, a NEWLY CREATED MolecularSystem, along with newly created constituent Molecules
    #    and Atoms shall be returned. Otherwise, it returns None.
    # The breakup scheme is 'atomBelongToNewMoleculeSerialMap', which maps each atom serial to a new molecule serial
    # Requirements:
    # 1. atom serials in the original molecule must be unique
    # 2. each atom must belong to one and only one molecule in the new system
    # Features:
    # 1. After the breakup, some bonds may become intermolecular, which are move in the 'interMolecularBonds' property
    #    in the new MolecularSystem. Those bond that are entirely within a single molecule in the new system becomes a
    #    part of the newly created molecule.
    # 2. While the serials of new molecules are specified by the user, all new molecules will duplicate the name of the original one
    # 3. Molecules in the new system are sorted according to the smallest index of its constituent atoms in the original molecule.
    #    For example, if atom [2 3 6],[1 4], and [5] are assigned to molecule x, y, and z in the new system, then molecule y (atom [1 4])
    #    shall come first, then molecule x ([2,3,6]) and molecule z ([5]).


    foundSerial = set()
    newMoleculeSerialToIndexMap = {}
    for atom in originalMolecule.atoms:
        # Check that atom serials are unique, and each atom is assigned to a new molecule
        if atom.serial in foundSerial:
            error("BreakupMolecule() fails because atom serials are not unique. Serial {} appears at least twice.".format(atom.serial),False)
            return None
        else:
            foundSerial.add(atom.serial)

        if not atom.serial in atomBelongToNewMoleculeSerialMap:
            error("BreakupMolecule() fails because the atom with serial {} are not assigned to a new molecule.".format(atom.serial),False)
            return None
        else:
            molSerial = atomBelongToNewMoleculeSerialMap[atom.serial]
            if not molSerial in newMoleculeSerialToIndexMap:
                molIndex = len(newMoleculeSerialToIndexMap)
                newMoleculeSerialToIndexMap[molSerial] = molIndex

    molCount = len(newMoleculeSerialToIndexMap)   # number of new molecules found in the first scan
    if molCount == 0 or len(originalMolecule.atoms) == 0:  # Do nothing upon empty molecule or empty splitting scheme
        return None

    newMS = MolecularSystem()                     # creates new Molecule objects and set their properties
    newMS.molecules = [Molecule() for i in range(molCount)]
    for molSerial in newMoleculeSerialToIndexMap:
        index = newMoleculeSerialToIndexMap[molSerial]
        mol = newMS.molecules[index]
        mol.serial = molSerial
        mol.name = originalMolecule.name
        mol.type = originalMolecule.type

    def FindMoleculeFromAtomSerial(atomSerial):
        molSerial = atomBelongToNewMoleculeSerialMap[atomSerial]
        molIndex = newMoleculeSerialToIndexMap[molSerial]
        return newMS.molecules[molIndex]

    # copy atoms into the new system
    serialGlobalToLocalMap = {}
    for atom in originalMolecule.atoms:
        newMol = FindMoleculeFromAtomSerial(atom.serial)
        newAtom = atom.Copy()
        newAtom.systemwideSerial = newAtom.serial   # Sets the systemwide serial.
        # Also need to renumber atoms within each molecule
        newAtom.serial = "{}".format(len(newMol.atoms)+1)
        serialGlobalToLocalMap[newAtom.systemwideSerial] = newAtom.serial

        newMol.atoms.append(newAtom)

    # copy bonds into the new system. Need to distinguish between inter- and intra-molecular bonds
    for bond in originalMolecule.bonds:
        mol1 = FindMoleculeFromAtomSerial(bond.atom1)
        mol2 = FindMoleculeFromAtomSerial(bond.atom2)
        if mol1 == mol2:    # comparing two references, shall be fine  # intra-molecular
            # In this case, must switch to the local (within a molecule) serial
            newBond = bond.Copy()
            newBond.atom1 = serialGlobalToLocalMap[bond.atom1]
            newBond.atom2 = serialGlobalToLocalMap[bond.atom2]
            mol1.bonds.append(newBond)
        else:  # intermolecular
            newMS.interMolecularBonds.append(bond.Copy())

    # for m in newMS.molecules:
    #     error.turn_on()
    #     m.CheckConsistency()
    # exit()
    return newMS

def BreakupMoleculeByConnectivity(molecule,requestTheBelongToMap=False):
    # returns a MolecularStructure
    
    atomCount = len(molecule.atoms)

    # Initially, every atom is associated with a parent (itself) and an empty set of children
    parent = [i for i in range(atomCount)]
    children = [set() for i in range(atomCount)]

    # Merge two 'flat' trees
    def TreeMerge(n1,n2):
        p1 = parent[n1]
        p2 = parent[n2]
        if p1 == p2:
            return
        for c in children[p2]:
            parent[c] = p1
            children[p1].add(c)

        children[p1].add(p2)
        parent[p2] = p1
        children[p2] = set()


    # Now we check the bonding map
    bondedTo = molecule.BondedMap()
    for index, connected in enumerate(bondedTo):
        # For each atom
        for toAtomIndex in connected:
            # Only need to check its connectivity with previous atoms
            if toAtomIndex < index:
                TreeMerge(toAtomIndex,index)

    #Debugging, Display the tree
    # ms = MolecularSystem()
    # for i in region(atomCount):
    #     if parent[i] == i:  # This is a root node
    #         ms.molecules.append(Molecule())
    #         output("Root : {}, with {} children: \n{}".format(i,len(children[i]),children[i]))
    #         ms.molecules[-1].atoms.append(molecule.atoms[i])
    #         for c in children[i]:
    #             ms.molecules[-1].atoms.append(molecule.atoms[c])
    # output.setoutput(open('dump.xyz','w'))
    # ms.Write(XYZFile())
    # exit()

    # Create the belongTo map
    belongTo = {}
    moleculeSerialCounter = 0
    # 1st round, scan for all root nodes and create molecules as the scan goes
    for i, atom in enumerate(molecule.atoms):
        if parent[i] == i: # Root node found, which suggests a new molecule should be created
            moleculeSerialCounter += 1
            belongTo[atom.serial] = '{}'.format(moleculeSerialCounter)
    # 2nd round, sets the belongTo map properly.
    for i, atom in enumerate(molecule.atoms):
        # Set its belongTo molecule to its parent's. For root nodes, this operation has no effect
        parentAtom = molecule.atoms[parent[i]]
        belongTo[atom.serial] = belongTo[parentAtom.serial]

    # All set, break it up!
    if requestTheBelongToMap:
        return BreakupMolecule(molecule, belongTo),belongTo
    else:
        return BreakupMolecule(molecule,belongTo)

def BreakupMoleculeRandomly(molecule,numberOfMolecules):
    belongTo = {}
    import random
    for a in molecule.atoms:
        belongTo[a.serial] = random.randint(1,numberOfMolecules)
    return BreakupMolecule(molecule,belongTo)

def ReduceSystemToOneMolecule(originalSystem):
    # This function combines all molecules in a system into a single molecule.
    # If successful, a NEWLY CREATED one-molecule system shall be returned. Otherwise it returns None
    # Requirement:
    # 1. If there are intermolecular bonds, each atom must have a unique system-wide serial number
    # Features:
    # 1. If each atom has a systemwide serial, this serial will replace its original, molecular-wide serial.
    #    If no systemwide serial is available, a consecutive number will be assigned to each atom.
    # 2. Name and type of the combined molecule is set to be the same as the first molecule.

    if len(originalSystem.molecules) == 0:    # Quit on emtpy systems:
        return None

    systemwideSerialsSet = set()
    systemwideSerialsOK = False
    if originalSystem.interMolecularBonds != None and len(originalSystem.interMolecularBonds) > 0:
        # Check that each atom has a unique systemwide serial
        for m in originalSystem.molecules:
            for a in m.atoms:
                if a.systemwideSerial == None or a.systemwideSerial in systemwideSerialsSet:
                    error("ReduceSystemToOneMolecule() fails because the some atom doesn't have unique systemwideSerial"
                          " when intermolecular bonds are present",False)
                    return None
                else:
                    systemwideSerialsSet.add(a.systemwideSerial)
        systemwideSerialsOK = True


    newMolecule = Molecule()
    newMolecule.name = originalSystem.molecules[0].name
    newMolecule.type = originalSystem.molecules[0].type

    for m in originalSystem.molecules:

        localSerialToGlobalSerialMap = {}
        for a in m.atoms:
            newAtom = a.Copy()
            if not systemwideSerialsOK: # If there is originally no systemwide serial, assign one to it
                newAtom.systemwideSerial = "{}".format(len(newMolecule.atoms)+1)
            localSerialToGlobalSerialMap[newAtom.serial] = newAtom.systemwideSerial
            newAtom.serial = newAtom.systemwideSerial
            newMolecule.atoms.append(newAtom)
        for b in m.bonds:
            newBond = b.Copy()
            try:
                newBond.atom1 = localSerialToGlobalSerialMap[newBond.atom1]
                newBond.atom2 = localSerialToGlobalSerialMap[newBond.atom2]
            except:
                error("Can't find atom {} or atom {}!".format(newBond.atom1,newBond.atom2))
            newMolecule.bonds.append(newBond)

    if originalSystem.interMolecularBonds != None:
        for b in originalSystem.interMolecularBonds:
            newBond = b.Copy()
            newMolecule.bonds.append(newBond)

    import copy
    newMS = copy.copy(originalSystem)   # 'Shallow' copy
    newMS.molecules = [newMolecule]     # The sole molecule
    newMS.interMolecularBonds = []      # No intermolecular bonds
    newMS.boundary = copy.deepcopy(originalSystem.boundary)  # Don't forget the periodicity

    return newMS

def ExtendSystem(destSystem, srcSystem):
    # Copy all atoms, molecules, and bonds in srcSystem into destSystem to extend destSystem
    # This function will modify the 'destSystem' but leave 'srcSystem' unchanged
    # by making a copy of the srcSystem:
    copyOfSrcSystem = srcSystem.Copy()
    atomsCountInDestSystem = 0
    for m in destSystem.molecules:
        atomsCountInDestSystem += len(m.atoms)
    # Need to renumber atoms in the srcSystem so that atom serials don't clash
    copyOfSrcSystem.RenumberAtomSerials(atomsCountInDestSystem + 1)
    destSystem.molecules.extend(copyOfSrcSystem.molecules)
    destSystem.interMolecularBonds.extend(copyOfSrcSystem.interMolecularBonds)
    # Assume that there is no bonds across systems. If there is, the caller shall need to add them manually or call
    # AutoDetectBonds on the extended system.
    return True

def DuplicateSystemPeriodically(moleculerSystem,images):
    # images is a list of 3-membered vectors, for example [[0,0,1],[1,0,-1],...]
    # [0,0,1] means that the caller wants to get a periodic image along the z-direction just above the original image
    # [1,0,-1] means the image is in the greater x-direction and lower z-direction. Other coordinates have similar meanings.
    # [0,0,0] means the original image, whether the original image appears in the list of images has no effect.
    # Requirement: the molecularSystem must have the 'boundary' property properly set.
    # Currently it ONLY supports ORTHOGONAL systems!
    # Also note that the 'boundary' of the system is unaltered! Duplicated atoms WILL BE OUTSIDE THE BOX!
    copyOfOriginalSystem = moleculerSystem.Copy()  # This copy saves the original state of the unduplicated system.
    A,B,C = [None,None,None]
    try:
        A = float(moleculerSystem.boundary[0][0])
        B = float(moleculerSystem.boundary[1][1])
        C = float(moleculerSystem.boundary[2][2])
    except:
        error("In DuplicateSystemPeriodically(), the system is required to have a periodic unit cell size.",False)
        return False

    showProgress = False
    if len(images) * moleculerSystem.NAtoms() > 10000:
        showProgress = True
    if showProgress:
        output("Duplicating system {} in {} periodic images...".format(moleculerSystem.name,len(images)))

    totalAtoms = moleculerSystem.NAtoms()

    for i,img in enumerate(images):

        # If there are many atoms, show a progress bar.
        if showProgress:
            ProgressBar(float(i)/len(images))

        for i in range(3):
            if type(img[i]) != int:
                error("In DuplicateSystemPeriodically() for system {}, the image indicators "
                "must be integers.".format(moleculerSystem.name), False)
                return False
        if img[0] == 0 and img[1] == 0 and img[2] == 0:
            continue

        dx = A* int(img[0])
        dy = B* int(img[1])
        dz = C* int(img[2])

        newMS = copyOfOriginalSystem.Copy()
        newMS.Translate(dx,dy,dz)

        # ExtendSystem(moleculerSystem, newMS) # it's slower to call ExtendSystem
        newMS.RenumberAtomSerials(totalAtoms+1)
        totalAtoms += newMS.NAtoms()
        moleculerSystem.molecules.extend(newMS.molecules)
        moleculerSystem.interMolecularBonds.extend(newMS.interMolecularBonds) # no further renumbering needed


    if showProgress:
        ProgressBar(1.0)
        output('')

    del copyOfOriginalSystem
    return True

def SubSystemByMask(molecularSystem,mask):
    # Generates a sub-system of the original one with some atoms and associated bonds removed (to ensure that there is
    # no dangling bonds). mask is a list of booleans having the length of the number of atoms indicating which atoms are
    # picked. If there is only a handful of atoms to pick, for example in the case that the user wants to focus on
    # a certain molecule in the system, the user can call the other function 'SubSystemBySystemwideSerials()'
    # by providing a list of serials.
    # Features: This function will return a new MolecularSystem that retains the molecules structures as much as it can.
    # Restrictions: The returned MolecularSystem shall have systemwideSerials identical to the original one, which is
    # intentional so that the sub-system can utilize the original system's Trajectory to update its coordinates.
    # It also means that systemwideSerials are not continuous in the returned sub-system and calling Write() function on
    # the sub-system will produce an unreadable format by some file writers, i.e. MOL2File(). The users must call
    # RenumberAtomSerials() on the sub-system before writing out the sub-structure in such formats.
    ms = molecularSystem.Copy()
    NAtoms = ms.NAtoms()
    if len(mask) != NAtoms:
        error("In SubSystemByMask(ms,mask), the length of mask ({}) must equal NAtoms ({})".format(len(mask),NAtoms))
        return None

    systemWideSerial_to_index_map = {}
    index = 0
    for mol in ms.molecules:
        for atom in mol.atoms:
            systemWideSerial_to_index_map[atom.systemwideSerial] = index
            index += 1

    for mol in ms.molecules:
        newAtomList = []
        newBondList = []
        remainingAtomsSerialSet = set()   # intra-molecular serial, not systemwideSerial
        for atom in mol.atoms:
            index = systemWideSerial_to_index_map[atom.systemwideSerial]
            if mask[index]:
                newAtomList.append(atom)
                remainingAtomsSerialSet.add(atom.serial)
        for bond in mol.bonds:
            if bond.atom1 in remainingAtomsSerialSet and bond.atom2 in remainingAtomsSerialSet:
                # Both ends must remain in order to survive, otherwise there shall be dangling bonds
                newBondList.append(bond)
        mol.atoms = newAtomList
        mol.bonds = newBondList

    newIntermolecularBondList = []
    for bond in ms.interMolecularBonds:
        if bond.atom1 in systemWideSerial_to_index_map and bond.atom2 in systemWideSerial_to_index_map:
            newIntermolecularBondList.append(bond)
    ms.interMolecularBonds = newIntermolecularBondList

    # Run a last check to remove all-empty molecules
    newMolList = []
    for mol in ms.molecules:
        if len(mol.atoms) > 0:
            newMolList.append(mol)
    ms.molecules = newMolList
    return ms

def SubSystemBySystemwideSerials(molecularSystem,surviving_atoms_by_systemwideSerials):
    # See the explanation in SubSystemByMask(). This function is similar except that a list of surviving atoms instead
    # of a list of masks are provided.
    # This function is implemented via SubSystemByMask()
    mask = [False] * molecularSystem.NAtoms()
    surviving_set = set(surviving_atoms_by_systemwideSerials)
    index = 0
    for m in molecularSystem.molecules:
        for a in m.atoms:
            if a.systemwideSerial in surviving_set:
                mask[index] = True
            index += 1
    return SubSystemByMask(molecularSystem,mask)

def SubSystemByLambdaFunction(ms,lamdafunc):
    # lamdafunc is a lambda function lambda: mol, atom which return either True or False
    mask = [False] * ms.NAtoms()
    index = 0
    for m in ms.molecules:
        for a in m.atoms:
            mask[index] = lamdafunc(m,a)
            index += 1
    return SubSystemByMask(ms,mask)

def TestBreakupMolecule():
    ms = MolecularSystem()

    ms.Read(MOL2File(),'testcase/Coal70A.mol2')
    ms.Summary()

    images = [[0,0,0],[1,0,0],[0,1,0]]
    DuplicateSystemPeriodically(ms,images)
    ms.Summary()

def SolvateSystem(ms, region, type, minDistance=3.0):
    # 为一个体系加上溶剂。region为3*2的数组，代表 [[xlo,xhi],[ylo,yhi],[zlo,zhi]], 需保证每个hi值>lo值
    # type 为所加溶剂分子的类型
    # 目前支持SPC与TIP4P。所需的溶剂分子模型坐标是预先平衡好的周期性纯水体系，盒子尺寸5nm。存储在 ./DATA/Structures/下面
    # minDistance 是水分子与目前体系中的原子的最小允许距离（H2O的位置以O原子为准）。
    # 成功的话会返回一个单独的MolecularSystem, 里面包含所添加的水分子。失败返回None
    import os
    import math
    from Utility import DATAFILESPATH
    from BondDetection import NeighborList
    chunk_file = None
    chunk_size = 50 # 目前提供的水分子模型中，均是平衡好的边长为5nm的周转
    if type.upper() == "SPC":
        chunk_file = os.path.join(DATAFILESPATH,"Structures","spc_water_5nm_chunk.mol2")
    elif type.upper() == "TIP4P":
        chunk_file = os.path.join(DATAFILESPATH, "Structures", "tip4p_water_5nm_chunk.mol2")
    else:
        error("In SolvateSystem(), water type \"{}\" is not supported".format(type))
    water_chunk = MolecularSystem("{}_Water_Chunk".format(type))
    water_chunk.Read(MOL2File(),chunk_file)
    # 先抹掉读到的结构中的原子类型信息。后面再识别
    for mol in water_chunk.molecules:
        for atom in mol.atoms:
            atom.type = None
    #water_chunk.Summary()
    try:
        solvate_origin = [region[i][0] for i in range(3)] # 填充区域的原点
        solvate_sizes = [region[i][1] - region[i][0] for i in range(3)] # 填充区域在x,y,z方向上的大小
        for i in range(3):
            assert(solvate_sizes[i] > 0)
    except:
        error("In SolvateSystem(), the filling region must be in the format [[xlo,xhi],[ylo,yhi],[zlo,zhi]] ")
    duplication_times = [math.ceil(solvate_sizes[i]/chunk_size) for i in range(3)]
    images = []
    for i in range(duplication_times[0]):
        for j in range(duplication_times[1]):
            for k in range(duplication_times[2]):
                images.append([i,j,k])
    DuplicateSystemPeriodically(water_chunk,images)
    water_chunk = ReduceSystemToOneMolecule(water_chunk)
    water_chunk = BreakupMoleculeByConnectivity(water_chunk.molecules[0])
    # 检查水分子是否在范围内
    water_chunk_in_region = MolecularSystem()
    for mol in water_chunk.molecules:
        # 假定O原子始终是第一个原子
        Oatom = mol.atoms[0]
        if Oatom.x > solvate_sizes[0] or Oatom.y > solvate_sizes[1] or Oatom.z > solvate_sizes[2]:
            continue
        water_chunk_in_region.molecules.append(mol.Copy())
    # water_chunk.Summary()
    # water_chunk_in_region.Summary()

    water_chunk_in_region.Translate(solvate_origin[0],solvate_origin[1],solvate_origin[2])
    # with open("dump.mol2","w") as file:
    #     output.setoutput(file)
    #     water_chunk_in_region = ReduceSystemToOneMolecule(water_chunk_in_region)
    #     water_chunk_in_region.Write(MOL2File())
    # exit(0)

    list_of_original_atoms = []
    for mol in ms.molecules:
        list_of_original_atoms.extend(mol.atoms)
    neighbor_list = NeighborList(list_of_original_atoms,5.0)
    list_of_solvate_atoms = [mol.atoms[0] for mol in water_chunk_in_region.molecules]
    ifClashed = neighbor_list.DetectClashing(list_of_solvate_atoms,minDistance)
    allSolvateMolecules = MolecularSystem()
    count = 0
    for i,flag in enumerate(ifClashed):
        if not flag:
            allSolvateMolecules.molecules.append(water_chunk_in_region.molecules[i])
            count += 1
    if count > 0:
        return allSolvateMolecules
    else:
        return None

def SystemCenter(ms,excluded_set=set()):
    # return the geometric center of the ms
    # if excluded_set is not empty set, atoms in the excluded_set are excluded (for example, light atoms)
    coords = np.zeros((ms.NAtoms(),3))
    counter = 0
    for iAtom, atom in enumerate(ms.Atoms()):
        if not iAtom in excluded_set:
            coords[counter,:] = atom.x,atom.y,atom.z
            counter += 1
    coords = coords[:counter,:]
    center = np.sum(coords,axis=0)
    center /= counter
    return center

def SystemFitPlane(ms,excluded_set=set()):
    # Fit the ms into a plane, return the normal direction (Z) in a unit vector
    NAtoms = ms.NAtoms()
    A = np.ones((NAtoms,3))
    B = np.zeros((NAtoms,1))
    counter = 0
    for i, atom in enumerate(ms.Atoms()):
        if i in excluded_set:
            continue
        A[counter, 0] = atom.x
        A[counter, 1] = atom.y
        B[counter, 0] = atom.z
        counter += 1
    # Special Cases:
    # 1. Only one atom, just return Z-direction
    # 2. Two atoms, return the direction (1->2) x [0,0,1], if (1->2) happens to be along z-direction, return [1,0,0]
    # 3. 3+ noncollinear atoms, just do the math
    if counter == 1:
        return np.array([0,0,1])
    elif counter == 2:
        X = SystemFitLine(ms,excluded_set)
        Z = VectorCrossProduct(X,[0,0,1])
        if VectorNorm(Z) < 1e-8: # means X is along [0,0,1]
            return np.array([1,0,0])
        else:
            return np.array(Z)
    else:
        A = np.matrix(A[:counter,:])
        B = np.matrix(B[:counter,:])
        X = (A.T * A).I * A.T * B  # ax+by+c = z, normal direction in [-a,-b,1]
        normalDirection = np.array([-X[0, 0], -X[1, 0], 1])
        normalDirection /= np.sqrt(np.dot(normalDirection, normalDirection))
        return normalDirection


def SystemFitLine(ms,excluded_set=set()):
    # Fit the system with a line: L = A + N t; where L is the points, A is the interception, N is normal direction,
    # t is the parameter
    # A is simply the average coordinates of (xi, yi, zi)
    # N is the eigenvector of the covariance matrix corresponding to the largest eigenvector:
    # cov(x,y,z) = [ [<x^2>-<x>^2, <xy>-<x><y>, <xz>-<x><z>],
    #                [<xy>-<x><y>, <y^2>-<y>^2, <yz>-<y><z>],
    #                [<xz>-<x><z>, <yz>-<y><z>, <z^2>-<z>^2] ]
    NAtoms = ms.NAtoms()
    X = np.zeros(NAtoms)
    Y = np.zeros(NAtoms)
    Z = np.zeros(NAtoms)
    counter = 0
    for iAtom, atom in enumerate(ms.Atoms()):
        if iAtom in excluded_set:
            continue
        X[counter], Y[counter], Z[counter] = atom.x, atom.y, atom.z
        counter += 1
    cov = np.zeros((3,3))
    X,Y,Z = X[:counter], Y[:counter], Z[:counter]
    xmean = np.average(X)
    ymean = np.average(Y)
    zmean = np.average(Z)

    cov[0,0] = np.average(X*X) - xmean*xmean
    cov[0,1] = cov[1,0] = np.average(X*Y) - xmean*ymean
    cov[0,2] = cov[2,0] = np.average(X*Z) - xmean*zmean
    cov[1,1] = np.average(Y*Y) - ymean*ymean
    cov[1,2] = cov[2,1] = np.average(Y*Z) - ymean*zmean
    cov[2,2] = np.average(Z*Z) - zmean*zmean
    eigenvalues,eigenvectors = np.linalg.eig(cov)
    eigenvalues = np.fabs(eigenvalues)
    maxEigenvalue = -9999
    maxEigIndex = -1
    # print(eigenvalues)
    # print(eigenvectors)
    # exit()
    for i, e in enumerate(eigenvalues):
        if e > maxEigenvalue:
            maxEigIndex = i
            maxEigenvalue = e
    N = eigenvectors[:,maxEigIndex]
    N /= np.sqrt(np.dot(N,N))
    # There are two choices (left/right) for the X-direction.
    # Make this choice definite by make the atom with smaller indicies on the left, atoms with larger indices on the
    # right
    sum = 0.0
    for i in range(counter):
        weight = i - counter/2.0
        dir = np.array([X[i],Y[i],Z[i]]) - np.array([xmean,ymean,zmean])
        sum += np.dot(dir,N) * weight
    if sum < 0.0:
        N = -N

    return N
