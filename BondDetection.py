# 此模块实现以下功能：根据元素类型和距离自动检测化学键。
# 它应该以更高级的方式实现，例如通过机器学习...
# 我会考虑在以后的版本中实现这个功能...

# [bond_rule_file] 是一个 txt 文件（csv 格式），它定义了成键规则，它们可以包含多行，
# 每行如下：
# AtomType1 AtomType2 MinBondLength MaxBondLength BondType
# 例如下面几行
# C,O,1.2,1.6,1
# C,O,1.1,1.2,ar
# 上面两行要求程序判断任意两个距离在 1.1 埃（Å） 至 1.2 Å 的 C、O 原子形成芳香键，任何两个相距在 1.2Å至1.6Å 范围内的 C、O 原子形成单键。
# 在有多条（可能相冲突的）规则存在时，程序以后出现的规则为准，这意味着文件中稍后出现的规则会覆盖较早的规则。
# 其他一些说明如下：
# 1. 在每条规则中，两个原子的名字顺序无关紧要，意思是“C O 1.2 1.6 1”和“O C 1.2 1.6 1”是一模一样的。
# 2. 这个程序的第三个参数，[bond_rule_file]，是可选的。有一个默认的绑定规则文件，名为
# "DATA/ClayBondRules.csv"，程序每次读取它运行，以识别有机分子中一些常见的键。但是用户定义的 [bond_rule_file]
# 注意如果用户提供的成键规则与bondrules.csv中的规则有矛盾，以用户提供的规则为准（因为它们后出现）
# 3.bond_rule_file中每一行的第5段定义了bond类型，可以是任何符合 TRIPOS mol2文件格式规范的类型，如1、2、3、ar、am等。更多信息可以参考
# www.tripos.com。

import sys
import os
from Utility import *
from UniversalMolecularSystem import *
from XYZFile import *
from MOL2File import *
from MolecularManipulation import *
from PDBFile import *

class NeighborList:
    minx:float
    miny:float
    minz:float
    maxx:float
    maxy:float
    maxz:float
    gridSize:float
    Nx: int
    Ny: int
    Nz: int
    neighborList: [set]
    atomList: [Atom]
    #grid: a 3-dimensional array of sets, recording which atoms are in each grid
    def __init__(self, listOfAtoms, gridSize):

        if len(listOfAtoms) == 0:
            error("In NeighborList.__init__(), listOfAtoms must not be empty")
        if gridSize < 0:
            error("In NeighborList.__init__(), gridSize = {} must be positive".format(gridSize))

        self.minx = self.miny = self.minz = 1E10
        self.maxx = self.maxy = self.maxz = -1E10
        self.gridSize = float(gridSize)
        self.atomList = listOfAtoms
        for a in listOfAtoms:
            self.minx = min(a.x,self.minx)
            self.miny = min(a.y,self.miny)
            self.minz = min(a.z,self.minz)
            self.maxx = max(a.x,self.maxx)
            self.maxy = max(a.y,self.maxy)
            self.maxz = max(a.z,self.maxz)

        # The 'border' of the neighbors list
        self.minx -= 0.95*gridSize
        self.miny -= 0.95*gridSize
        self.minz -= 0.95*gridSize
        self.maxx += 0.95*gridSize
        self.maxy += 0.95*gridSize
        self.maxz += 0.95*gridSize

        from math import floor
        self.Nx = int(floor( (self.maxx - self.minx) / self.gridSize)) + 1
        self.Ny = int(floor( (self.maxy - self.miny) / self.gridSize)) + 1
        self.Nz = int(floor( (self.maxz - self.minz) / self.gridSize)) + 1
        self.grid = [[[ set() for k in range(self.Nz)] for j in range(self.Ny) ] for i in range(self.Nx) ]

        # 2nd pass, assign atoms to each grid:
        for a in listOfAtoms:
            ix,iy,iz = self._find_grid_(a.x,a.y,a.z)
            self.grid[ix][iy][iz].add(a)

        # 3rd pass, create the neighborList
        N = len(listOfAtoms)
        self.neighborList = [set() for i in range(N)]

        for i,a in enumerate(listOfAtoms):
            ix, iy, iz = self._find_grid_(a.x, a.y, a.z)
            self.neighborList[i] = self.allAtomsInNeighborsOfAGridBlock(ix,iy,iz)
            self.neighborList[i].remove(a)  # remove itself

        #self._checking_()

    def allAtomsInNeighborsOfAGridBlock(self, ix, iy, iz):
        # Find all atoms in the 9 blocks (including itself) around grid[ix, iy, iz]
        result = set()
        for i in range(max(ix - 1, 0), min(ix + 2, self.Nx)):
            for j in range(max(iy - 1, 0), min(iy + 2, self.Ny)):
                for k in range(max(iz - 1, 0), min(iz + 2, self.Nz)):
                    for a in self.grid[i][j][k]:
                        result.add(a)
        return result

    def GetNeighborList(self,index):
        # returns a copy of the neighborlist. Just a copy, don't modify it
        return self.neighborList[index]

    def _checking_(self):
        from math import sqrt
        for i,a in enumerate(self.atomList):
            neighlist = self.GetNeighborList(i)
            output("Neighbor List of atom {} contains {} atoms.".format(i,len(neighlist)))
            for b in neighlist:
                dist = Distance(a,b)
                if dist > sqrt(3)*2*self.gridSize:
                    error("Something is wrong in _check_(), distance = {}".format(dist))

    def _find_grid_(self,x,y,z):
        # return a list [ix,iy,iz] indicating the grid index of x, y, z
        # ix, iy, iz must be within [0, Nx], [0, Ny], [0, Nz]. Otherwise something is wrong.
        from math import floor
        ix = int(floor((x - self.minx) / self.gridSize))
        iy = int(floor((y - self.miny) / self.gridSize))
        iz = int(floor((z - self.minz) / self.gridSize))

        # Debugging, double-checking:
        # if ix < 0 or ix >= self.Nx or iy < 0 or iy >= self.Ny or iz < 0 or iz >= self.Nz:
        #     error("Something is wrong within _find_grid_()")

        return [ix,iy,iz]

    def DetectClashing(self,guestAtomList,minDist):
        # This function tests whether atoms in the guestAtomList clashes with any of the atoms that are used to
        # construct this neighbor list. minDist is the minimal distance that is considered to be a clash.
        # This function, if successful, returns a list of Bool with the same length as the guestAtomList, indicating
        # whether or not each atom in guestAtomList clashes with the host system. (True for clash, False for non-clash)
        # If a guestAtom is outside the box of the host system, ie, guestAtom.x not in [self.minx, self.maxx], etc, it's
        # considered to be a non-clash.
        result = [None for i in range(len(guestAtomList))]
        for index, guestAtom in enumerate(guestAtomList):
            result[index] = False
            ix,iy,iz = self._find_grid_(guestAtom.x,guestAtom.y,guestAtom.z)
            if ix<0 or ix>=self.Nx or iy<0 or iy>= self.Ny or iz<0 or iz>=self.Nz:
                # guest atom outside the box, it's a non-clash
                continue
            neighbors = self.allAtomsInNeighborsOfAGridBlock(ix,iy,iz)
            for hostAtom in neighbors:
                dist = Distance(hostAtom,guestAtom)
                if dist <= minDist:
                    result[index] = True
                    break

        return result


class Rule:
    ele1: str
    ele2: str
    low: float
    high: float
    type: str
    def __init__(self):
        pass

def _DetectBond_DealwithJustOneAtom_(atomList:[Atom],neighList:NeighborList,i:int,rules:[]):
    a1 = atomList[i]
    neighbors = neighList.GetNeighborList(i)
    tempBondList = []
    for a2 in neighbors:
        # To prevent the same bond from appearing twice, such as A-B and B-A, we require that the
        # systemwideSerial of a2 being greater than a1.
        # What are now comparing are two strings rather than integers. But it serves our purpose.
        if a1.systemwideSerial >= a2.systemwideSerial:
            continue

        distance = Distance(a1, a2)
        newBond = None
        for r in rules:
            if (a1.element != r.ele1 or a2.element != r.ele2) and (a1.element != r.ele2 or a2.element != r.ele1):
                continue
            if distance < r.low or distance > r.high:
                continue
            # Now we have a confirmed bond
            newBond = Bond()
            newBond.atom1 = a1.systemwideSerial
            newBond.atom2 = a2.systemwideSerial
            newBond.type = r.type
            newBond.length = distance
        # Note that through the search of bond rules, multiple rules may be satisfied, but only the last satisfied
        # rule will be recorded. In other words, bond rules that appear later will override previous ones.
        if newBond != None:
            tempBondList.append(newBond)
    return tempBondList

def _DetectBond_DealwithOneBatch_(atomList:[Atom],neighList:NeighborList,iAtomFrom,iAtomTo,rules:[]):
    bondList = []
    for iAtom in range(iAtomFrom,iAtomTo):
        bondList.extend(_DetectBond_DealwithJustOneAtom_(atomList,neighList,iAtom,rules))
    return bondList

class BondRules(BondDetector):
    def __init__(self,globalCutoff = 5.0):
        self.rules = []
        self.globalCutoff = globalCutoff
        # Optional parameter global cutoff is used to build neighbor list as the grid size. Set this parameter to
        # be slightly larger than the maximum bond length in your system. If this value is too large, bond detection
        # may be very slow for large systems. If this value is too small, you may miss some bonds.

    def ParseFile(self,file_name):
        lines = None
        try:
            with open (file_name,"r") as file:
                lines = file.readlines()
        except:
            error("Can't open bond rule file <{}>".format(file_name),False)
            return False

        for i,line in enumerate(lines, start=1):
            if line.startswith('#'):
                continue
            l = line.strip(',')
            if (len(l)==0):
                continue
            rule = Bond()
            try:
                parts = l.split(',')
                rule.ele1 = parts[0]
                rule.ele2 = parts[1]
                rule.low = float(parts[2])
                rule.high = float(parts[3])
                rule.type = parts[4]
            except:
                error("Unexpected format @ line {} of bond rule file <{}>:\n{}".format(i,file_name,l),False)
                return False
            self.rules.append(rule)

        return True

    def Detect(self,molecularSystem,flushCurrentBonds,periodicBoundary,max_workers=None,batch_size=5000):
        # It is required that the systemwideSerial of each atom must be unique.
        # periodicBoundary 是周期性边界。如果不为None，则要考虑跨周期性边办的键。
        # periodicBoundary 的格式是[[xlo,xhi],[ylo,yhi],[zlo,zhi]]
        systemwideSerialToAtomMap = {}
        systemwideSerialToMoleculeMap = {}
        atomList = []
        tempBondList = []

        if flushCurrentBonds:
            molecularSystem.interMolecularBonds = []

        for m in molecularSystem.molecules:
            if flushCurrentBonds:
                m.bonds = []
            for a in m.atoms:
                if a.systemwideSerial == None or a.systemwideSerial in systemwideSerialToAtomMap:
                    error("In BondRule:Detect(), each atom's systemwideSerial must be unique", True)
                    return False
                systemwideSerialToAtomMap[a.systemwideSerial] = a
                systemwideSerialToMoleculeMap[a.systemwideSerial] = m
                atomList.append(a)
        # 处理跨周期性边界的键。处理的方法是在+x,+y,+z方向添加一个厚度为self.globalCutoff的buffer层，复制得到部分
        # Ghost 原子。Ghost原子与原始原子的systemwideSerial相同，故不致产生混淆。
        ghostAtomList = []
        if periodicBoundary != None:
            [[xlo,xhi],[ylo,yhi],[zlo,zhi]] = periodicBoundary
            xlength,ylength,zlength = xhi-xlo, yhi-ylo, zhi-zlo
            for atom in atomList:
                def __dup__(atom,offx,offy,offz):
                    ghostAtom = atom.Copy()
                    ghostAtom.x, ghostAtom.y, ghostAtom.z = atom.x+offx, atom.y+offy, atom.z+offz
                    ghostAtomList.append(ghostAtom)
                # x,y,z为原子距离Cell原点的相对位置：
                x,y,z = atom.x-xlo, atom.y-ylo, atom.z-zlo
                if x < self.globalCutoff:
                    __dup__(atom,xlength,0,0)
                if y < self.globalCutoff:
                    __dup__(atom,0,ylength,0)
                if z < self.globalCutoff:
                    __dup__(atom,0,0,zlength)
                # 注意以下特殊情况，需要将原子多复制一份
                if x<self.globalCutoff and y<self.globalCutoff:
                    __dup__(atom,xlength,ylength,0)
                if x<self.globalCutoff and z<self.globalCutoff:
                    __dup__(atom,xlength,0,zlength)
                if y<self.globalCutoff and z<self.globalCutoff:
                    __dup__(atom,0,ylength,zlength)
                if x<self.globalCutoff and y<self.globalCutoff and z<self.globalCutoff:
                    __dup__(atom,xlength,ylength,zlength)
        atomList.extend(ghostAtomList)

        # Performs a 2-body scan.
        # For system contains more than 10^4 atoms, O(N^2) is not acceptable. A neighbor list is needed here.
        N = len(atomList)
        if N > 10000:
            sys.stdout.write("Building NeighborList for system {} with grid size {} Å...".format(molecularSystem.name,self.globalCutoff))
        neighList = NeighborList(atomList,self.globalCutoff)
        if N > 10000:
            sys.stdout.write("Done.\n")
            sys.stdout.write("Scanning for Bonds:\n")

        if max_workers == 1:
            for i in range(N):
                if N > 10000 and i%1000 == 0:
                    ProgressBar(float(i)/N)
                tempBondList.extend(_DetectBond_DealwithJustOneAtom_(atomList,neighList,i,self.rules))
            if N > 10000:
                ProgressBar(1.0)
                output('')
        else:  # 并行计算
            if max_workers != None and max_workers<1:
                max_workers = None
            from concurrent.futures import ProcessPoolExecutor, as_completed
            futures = []
            with ProcessPoolExecutor(max_workers=max_workers) as pool:
                for iAtom in range(0,N,batch_size):
                    start = iAtom
                    end = min(iAtom+batch_size,N)
                    f = pool.submit(_DetectBond_DealwithOneBatch_,atomList,neighList,start,end,self.rules)
                    futures.append(f)
                for f in as_completed(futures):
                    tempBondList.extend(f.result())

        # Now we add the bonds to the system.
        # If old bonds are not removed, extra work is need to make sure that there are no duplicate bonds.
        existingBonds = set()
        if not flushCurrentBonds:
            # Going to construct a set to record which bonds are already present.
            # The 'existingBonds' is a set that records pairs of atoms that are bonded previously.
            # If A and B are bonded, then both 'A.#-B.#' and 'B.#-A.#' are stored in it, where # means atom's systemwideSerial
            for m in molecularSystem.molecules:
                for b in m.bonds:
                    a1 = None
                    a2 = None
                    for a in m.atoms:
                        if a.serial == b.atom1:
                            a1 = a
                        elif a.serial == b.atom2:
                            a2 = a
                        else:
                            pass
                    key1 = '{}-{}'.format(a1.systemwideSerial,a2.systemwideSerial)
                    key2 = '{}-{}'.format(a2.systemwideSerial,a1.systemwideSerial)
                    existingBonds.add(key1)
                    existingBonds.add(key2)
            for b in molecularSystem.interMolecularBonds:
                key1 = '{}-{}'.format(b.atom1,b.atom2)
                key2 = '{}-{}'.format(b.atom2,b.atom1)
                existingBonds.add(key1)
                existingBonds.add(key2)



        totalBonds = len(tempBondList)
        actuallyAddedBonds = 0

        for bond in tempBondList:
            if not flushCurrentBonds:
                key = '{}-{}'.format(bond.atom1, bond.atom2)
                if key in existingBonds:
                    continue

            a1 = systemwideSerialToAtomMap[bond.atom1]
            a2 = systemwideSerialToAtomMap[bond.atom2]
            m1 = systemwideSerialToMoleculeMap[bond.atom1]
            m2 = systemwideSerialToMoleculeMap[bond.atom2]
            if m1 == m2: # Intermolecular bond
                bond.atom1 = a1.serial
                bond.atom2 = a2.serial
                m1.bonds.append(bond)
            else: # Intramolecular bonds
                molecularSystem.interMolecularBonds.append(bond)

            actuallyAddedBonds += 1

        # For debugging:
        #output('Totally {} bonds found, {} bonds are added.'.format(totalBonds,actuallyAddedBonds))

        return True

    def Extend(self,file_name_or_another_rules_set):
        if isinstance(file_name_or_another_rules_set,str):
            newRules = BondRules()
            newRules.ParseFile(file_name_or_another_rules_set)
            self.rules.extend(newRules.rules)
        elif isinstance(file_name_or_another_rules_set,BondRules):
            self.rule.extend(file_name_or_another_rules_set.rules)
        else:
            error("In BondRules::Extend(para), para must be either a filename or a BondRules object")

def DefaultBondRules(globalCutoff = 5.0):
    # This is a factory method that returns a BondRules object which reads the default bond rule file 'ClayBondRules.csv'
    rules = BondRules(globalCutoff)
    default_route = os.path.join(DATAFILESPATH,"bondrules.csv")
    # the first part of the path is needed if case the script is called from other directories
    result = rules.ParseFile(default_route)
    return rules
