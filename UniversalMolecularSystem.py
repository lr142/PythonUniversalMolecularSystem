import sys
import math
import numpy as np
from Utility import *

class Bond:
    atom1: str
    atom2: str
    type: str
    length: float
    def __init__(self):
        self.atom1 = None
        self.atom2 = None
        self.type = None
        self.length = 0.0

    def Copy(self):
        import copy
        return copy.copy(self)

class Atom:
    element: str
    x:float
    y:float
    z:float
    type:str
    charge:float
    flexible:bool
    serial:str
    systemwideSerial: str
    layerInfo: str
    parent: str

    # 注意：如果将来在 Atom 中包含复杂的数据结构，如列表或对其他对象的引用
    # 记住 Atom.Copy() 用于复制原子，它在内部使用 copy.copy()来'浅' 复制原子。 请确保此类操作是安全和合理的
    # 例如，如果一个原子包含指向第三个对象的链接，请记住外部对象不会被复制。 本注释也适用于 Bond。
    # 由于 Atom 和 Bond 都被认为是“基本”类，尽量不要在其中包含引用或复杂的东西。

    def __init__(self):
        self.element = None   # 元素类型。必须使用标准的化学符号，如"C"，"H"，"Fe"。而"C1", "c", "rh" 是不行的.
        self.x = self.y = self.z = 0.0  # 坐标。可以是笛卡尔坐标或分数坐标，视情况而定。
        self.name = None   # 内部名字，例如出现在mol2文件中的名字，可以是"H13" or "C2"或类型的名字。原子名字可以不是惟一的。
        self.type = None   # 原子类型。mol2文件中即涉及这一变量。这个字段可用于表示原子的力场类型，视所使用的力场而定。例如"C.3" or "P.2"
        self.charge = 0.0  # 电荷。主要用于MD
        self.flexible = None # 几何位置是否可以被弛豫
        self.serial = None     # 原子在分子内的序列号，通常从1开始，但也可以是任意字符串。注意一个分子内部的序列号必须惟一，不能重复。
        self.systemwideSerial = None  # 原子在整个MolecularSystem内的序列号，通常从1开始，但也可以是任意字符串。整个分子体系内不能重复
        self.layerInfo = None  # 用于 QM/MM 模型，如ONIOM 方法中的high/mid/low层
        self.parent = None     # 在某些情况下用于记录原子的Parent，例如在读取LAMMPS Data文件时，用它记录原子所属的分子。

        # 关于serial与systemwideSerial的额外说明：
        # 按惯例，serial与systemwideSerial是从1开始编号的数字（例如在VMD中），而index是从0开始编号的数字。例如
        # 在代码中，用mol.atoms[0]，指的是index=0,但serial=1的那个原子。
        # 尽管本程序允许serial与systemwideSerial可以不是从1开始编号的连续数字，但是在很多应用中，如果serial不满足
        # 这一要求，可能会导致各种错误。建议在不确定的情况下，尽量使用MolecularSystem::RenumberAtomSerials函数，强制对整个体系的所有
        # 原子重新编号，以满足序列号连续且惟一的要求！

        # 并非所有属性在所有情况下都可用或相关。 如有必要，文件Reader/Writer和用户可以利用Python的灵活语法，当额外的属性写入到Atom中。

    def XYZ(self):
        # 返回一个np.array
        return np.array([self.x,self.y,self.z])

    def Copy(self):
        # 返回当前 Atom 的拷贝。 它使用“浅”拷贝。 见本类开始时的注释
        import copy
        return copy.copy(self)

    def Translate(self,dx,dy,dz):  # Self-evident
        self.x += dx
        self.y += dy
        self.z += dz

    def ShowAsXYZ(self):
        print(str(self.element) + " " +
              str(self.x) + " " +
              str(self.y) + " " +
              str(self.z))
    def ShowAllFields(self):
        print(str(self.serial) + " " +
              str(self.element) + " " +
              str(self.x) + " " +
              str(self.y) + " " +
              str(self.z) + " " +
              str(self.name) + " " +
              str(self.type) + " " +
              str(self.flexible) + " " +
              str(self.charge)
              )

class Molecule:
    atoms: [Atom]
    bonds: [Bond]
    name: str
    bondedTo: [map]
    serial: str
    type: str
    chainID: str
    resName: str
    resSeq: str

    def __init__(self,name=None):
        self.atoms = []
        self.bonds = []
        self.name = name  # name 用户定义的标识符，不需要唯一
        self.serial = None # 序列号通常从 1 开始，在 MolecularSystem 中必须是唯一的。
        self.type = None #
        self.chainID = self.resName = self.resSeq = None #此三个属性只对蛋白质有效，它们可以在读取PBD文件时被写入

    def NAtoms(self):
        return len(self.atoms)

    # 一个旧版本的，检测分子内成键情况的函数。低效 O(n^2),已移除，被MolecularSystem::AutoDetectBonds取代
    # def FindBonds(self,rules):
    #     for i in region(0,len(self.atoms)):
    #         for j in region(i+1,len(self.atoms)):
    #             a1 = self.atoms[i]
    #             a2 = self.atoms[j]
    #             length = math.sqrt (  (a1.x-a2.x)**2 +
    #                              (a1.y-a2.y)**2 +
    #                              (a1.z-a2.z)**2)
    #             order = rules.CheckRules(a1.name,a2.name,length)
    #             if ( order != None ):
    #                 bond = Bond()
    #                 bond.atom1 = int(i)
    #                 bond.atom2 = int(j)
    #                 bond.length = length
    #                 bond.type = order
    #                 self.bonds.append(bond)

    def BondedMap(self):
        # 一个辅助函数，返回一个集合列表(a list of sets)（称为bondedTo），例如
        # bondedTo[0] 记录与index（非serial）=0 的原子连接的原子的indexes
        # 如果有悬空键（即有的键只有一端，没有另一端）,则出错返回 None。
        # 此数据结构较为耗费内存，故不会每次自动生成，而只在需要时，由用户或其它函数（例如MolecularSystem::AutoDetectBonds）即时生成。
        # 生成后，调用者可以将结果暂时存储下来（例如写入一个Molecule对象的bondedTo字段），以节约计算时间。
        bondedMap = [set() for i in range(len(self.atoms))]
        serialToIndexMap = {}
        for i,atom in enumerate(self.atoms):
            serialToIndexMap[atom.serial] = i
        for b in self.bonds:
            fromSerial = b.atom1
            toSerial = b.atom2
            if fromSerial in serialToIndexMap and toSerial in serialToIndexMap:
                fromIndex = serialToIndexMap[fromSerial]
                toIndex = serialToIndexMap[toSerial]
                bondedMap[fromIndex].add(toIndex)
                bondedMap[toIndex].add(fromIndex)
            else:
                return None
        return bondedMap

    def CheckConsistency(self):
        # 分子内部结构合理性（一致性）检测。如果所有检查都通过，则返回 True，否则返回 False
        # 检查的内容包含以下几项：
        # 1. Atom序列号必须唯一
        serialToIndexMap = {}
        for i,atom in enumerate(self.atoms):
            serial = atom.serial
            if serial in serialToIndexMap:  # serial are not unique
                error("Atom serials in the molecule are not unique, found that serial {} appears again".format(serial),False)
                return False

            serialToIndexMap[serial] = i
        # 2. 没有悬空键。通过使用辅助函数BondedMap来实现
        result = self.BondedMap()
        if result == None:
            error("Dangling bond found in molecule: {} - {} with type {}".format(b.atom1,b.atom2,b.type),False)
            return False
        return True

    def Copy(self):
        import copy
        newMol = copy.copy(self)   # 返回该分子（包括内部的所有原子、键）的一份拷贝。注意这个与Atom::Copy一样，也是浅拷贝。
                                   # 如果分子中包含除int，string之外的其它数据类型（例如由BondedMap生成的成键结构列表），是不会被拷贝的。
        newMol.atoms = []
        newMol.bonds = []
        for a in self.atoms:
            newMol.atoms.append(a.Copy())
        for b in self.bonds:
            newMol.bonds.append(b.Copy())
        return newMol

    def Summary(self):
        output("Molecule Serial: {}, Name: {}, Type: {}, with {} atoms, and {} bonds".format(
            self.serial,self.name,self.type,len(self.atoms),len(self.bonds)
        ))

class MolecularFile:
    # 文件读入器/文件写入器
    # 这是一个抽象类，实现读/写一个分子系统描述文件的方法。 对于每种支持的文件类型，例如.xyz、.mol2、.pdb等
    # 应写一个单独的具体类来继承这个抽象类，例如XYZFile，MOL2File等，来实现Read()与Write()这两个virtual函数（请参考面向对象编程的书箱）
    def __init__(self):  # Virtual function
        pass
    def Read(self,molecularSystem,filename):   # Virtual function，需要在具体类中根据文件类型来具体实现
        # 请记住，任何“读取”操作都会重置分子系统。即原MolecularSystem中的所有信息均会被清空（即使读取不成功）。
        # 如果需要从多个文件中读取一个系统，将它们分别读入多个MolecularSystems， 并合并它们。
        # （LAMMPSDUMPFile这种轨迹文件读入器例外）
        pass
    def Write(self,molecularSystem):   # Virtual function，需要在具体类中根据文件类型来具体实现
        pass

class BondDetector:
    # 这是一个抽象类，代表分子内共价键的识别器。
    # 在'BondDetection.py'中，我们定义了一个简单的，基于元素类型和原子间距离的成键判定器，
    # 在将来的版本中，可以使用更高级的方法，例如机器学习，来判断原子间成键情况。
    def Detect(self,molecularSystem,flushCurrentBonds):
        # Virtual function，需要在具体类中根据文件类型来具体实现
        # molecularSystem指操作内象，针对哪个分子体系进行判断。flushCurrentBonds为Bool变量，是否要清空体系中原有的Bonds。
        pass

class Trajectory:
    # 轨迹。通常指能量弛豫或MD过程中，分子体系的演化轨迹。它可以是一个MolecularSystem的（非必需）属性。
    # Trajectory 利用了Numpy中的'narray'来存储每帧中，每个原子的坐标，速度，力等信息
    timestep: float # timestep length 时间步长，单位fs, (与LAMMPS中的 'units real' 相适应)
    NFrames: int     # 总帧数
    timesteps_of_each_frame: []  # 每帧对应的时间步长。此为一个list，长度正好是NFrames.
    NAtoms: int     # 轨迹中每个frame里的原子数（可能小于体系中的原子数）。原则上，每帧里的原子数都应该等于此数（GCMC的轨迹不符合此规则，因此目前不支持读入GCMC的轨迹）
    serial_to_index_map: map   # 一个map，记录MolecularSystem中，每个原子的 atom.systemwideSerial对应到以下几个array中的原子index。条目数正好等于NAtoms
    index_to_serial: []        # 与上面相反，此list记录轨迹中每个原子对应到MolecularSystem中的systemwideSerial。长度等于NAtoms
                               # 需要以上两个数组的原因是因为轨迹中的原子个数可能小于体系中的原子数（有些在MD中固定的原子没有在轨迹中输出）
    # 下面是几个二维narrays 的list，记录了每一帧中每个原子的坐标、速度和力。
    # 并非所有字段都可能存在于转储文件中，例如速度和力可能不存在（设置为None）
    # 这些list of narrays 实际上是3维的，最高（第0维）维是帧的索引，
    # 第1维是原子索引，最后一维（第2维）是 x、y 或 z。 因此，位置[100][25][2]
    # 指第 101 帧中第 26 个原子的 z 坐标。
    # 注意：我尝试过将它们真接实现为 3 维 narray（而不是二维narray的list）。 但是由于我们在读取轨迹文件前，通常事先不知道帧数，无法预先分配空间
    # 并且动态扩展 narray 是很耗时的，故采取了折中的方案，把每帧的数据记录到二维narray中，而不同的帧用一个list来记录。
    positions: []
    velocities: []
    forces: []
    dtype: str  # 以上三个大数组中所采用的浮点数类型，默认'float32' (double). 可在初始化时设为'float16'以节约存储空间。
    #parentMolecularSystem: MolecularSystem  # 指向它所对应的 MolecularSystem. 不需要时可以设为None.

    # 假设所有帧都有相同数量的原子。
    # 目前不能处理原子数随帧数而变多（GCMC），但可以处理有些帧中原子丢失，在这种情况下，丢失的原子将被分配全零的 xyz/velocity/force。

    def __init__(self, parentMolecularSystem = None, timestep_in_fs = 1.0, dtype = 'float32'):
        # 调用者有责任告诉程序每个时间步长有多长，因为LAMMPS dump文件中一般读不到timestep。
        # 但在某些情况下（如 QM 中的几何驰豫），timestep无关紧要，此时可以用默认值 (1.0 fs)
        self.timestep = timestep_in_fs
        self.timesteps_of_each_frame = []
        self.NFrames = 0
        self.NAtoms = 0
        self.dtype = dtype
        self.positions = self.velocities = self.forces = 0
        self.parentMolecularSystem = parentMolecularSystem
        self.serial_to_index_map = {}
        self.index_to_serial = []
        self.positions = []
        self.velocities = []
        self.forces = []

    def Read(self,trajectoryFile,filename,max_workers,maxFrames,every,
             flushSameTimestep, certainFrames): # Needs a trajectory file reader
        return trajectoryFile.Read(self, filename,max_workers,maxFrames,every,flushSameTimestep,certainFrames)

    def Copy(self):
        import copy
        newTrj = copy.copy(self)
        newTrj.positions = []
        newTrj.velocities = []
        newTrj.forces = []
        for pos in self.positions:
            newTrj.positions.append(pos.copy())
        for vel in self.velocities:
            newTrj.velocities.append(vel.copy())
        for force in self.forces:
            newTrj.forces.append(force.copy())
        return newTrj

    def DropFrame(self,index):
        # Drop a frame by index. Useful when frames are duplicate
        try:
            del self.timesteps_of_each_frame[index]
            del self.positions[index]
            if len(self.velocities) > 0:
                del self.velocities[index]
            if len(self.forces) > 0:
                del self.forces[index]
            self.NFrames -= 1
        except:
            error("In Trajectory.DropFrame(), index {} is invalid.".format(index))
        return True

class MolecularSystem:
    # MolecularSystem是Molecule的集合，在某些情况下，还包括边界信息，体系性质及其它一些用以加速程序的辅助数据结构。
    molecules: [Molecule] # 体系中包含的所有Molecule
    boundary: [] # PBC边界条件。非周期性体系可设为None。对周期性系，设为3x3的矩阵，代表u,v,w三个lattice向量。
    origin: [] # 体系原点。默认是在[0,0,0]

    interMolecularBonds: [Bond] # Bond的list，记录分子间的Bond（这些Bond不属于任何一个Molecule）
    name: str # 体系名字
    trajectory: Trajectory # 体系的演化轨迹（如有）
    systemWideSerialToMoleculeAndAtomMap: map
    # 一个辅助的数据结构，记录体系中每个原子序号标记的原子所在的Molecule与Atom。这是一个长度为N（N等于体系中所有原子总数）的map，每个
    # 条目的key为该原子的systemwideSerial，value为一个(m,a)元组，m为原子所在Molecule对象的引用，a为原子对象本身的引用。
    # 注意该数据结构不会自动被生成，但可以通过调用RenumberAtomSerials()来要求生成。

    def __init__(self,name=None):
        self.molecules = []
        self.boundary = None
        self.origin = [0.0, 0.0, 0.0]
        self.interMolecularBonds = []
        self.name = name
        self.trajectory = None
        self.systemWideSerialToMoleculeAndAtomMap = None

    def Atoms(self):  # 一个简单的迭代器。需要遍历体系中所有原子时，直接写 for atom in ms.Atoms()，不必再写两重循环[先对mol，再对atom]
        for mol in self.molecules:
            for atom in mol.atoms:
                yield atom

    def Read(self,molecularFile,filename):
        # 通过一个文件读入器（molecularFile）来读入文件filename，并执行一次一致性检测。至于是何种文件读入器，调用者需根据文件
        # 的类型来自动构造合适的读入器，例如要读入Mol2文件，则通过mol2file = MOL2File()来构造一个mol2文件读入器。
        # 再次注意，读入操作（不管成功与或）会清空MolecularSystem中的所有原有数据。
        molecularFile.Read(self,filename)
        for m in self.molecules:
            if not m.CheckConsistency():
                return False

    def ReadTrajectory(self,TrajectoryFile, filename, timestep_in_fs=1.0,dtype='float32',max_workers=-1,
                       maxFrames = 999999,every=1,flushSameTimestep=True,certainFrames=None):
        # 读入轨迹。通过一个轨迹文件读入器（TrajectoryFile）来读入文件filename。轨迹文件读入器是一类特殊的文件读入器，它也继承自
        # MolecularFile这一抽象类，但它与其他类型的MolecularFile不同的是它不会清空 MolecularSystem中的Molecule及Bond信息。
        # 例如可以用 traj = LAMMPSDUMPFile()来创建一个Lammps轨迹读入器。
        # 且该函数可以被调用多次，每次读到的轨迹会追加到原轨迹的后面。
        # timestep_in_fs 只在第一次调用时才会设置轨迹的time_step字段，以后均不会更改。
        # dtype 为记录坐标与速度时使用的浮点数类型。可改为'float16'以节约空间。
        # maxFrames是最多读取的帧数，设为一个极大的数字意味着读入所有帧。
        # certainFrames为读入指定帧。须为int的list或set。若不为None，every将被忽略。
        # max_workers为并行计算的进程数。如果<0，则由系统分配，=1为串行，>1为执行用户指定的进程数。
        if self.trajectory == None:
            self.trajectory = Trajectory(self,timestep_in_fs,dtype)
        self.trajectory.Read(TrajectoryFile,filename,max_workers=max_workers,
                             maxFrames=maxFrames,every=every,flushSameTimestep=flushSameTimestep,certainFrames=certainFrames)

    # 仅对正交体系：此函数返回体系在x,y,z方向上的界限，为3x2数组。例如用在LAMMPS的边界条件中
    def LoHi(self):
        if self.boundary == None or self.origin == None:
            return None
        else:
            return [   [self.origin[i], self.origin[i]+self.boundary[i][i]] for i in range(3) ]
    # 仅对正交体系：返回体系在x，y，z方向上的尺寸。
    def Size(self):
        if self.boundary == None or self.origin == None:
            return None
        return [self.boundary[i][i] for i in range(3)]

    def Write(self,molecularFile):
        molecularFile.Write(self)

    def Copy(self):
        # 返回该分子体系（包括内部的所有分子、原子、键）的一份拷贝。该拷贝是'深'拷贝，会拷贝除Trajectory之外的一切信息
        # （Trajectory只拷贝了一个引用）。如果想连Trajectory一并复制，请使用CopyWithTrajectory()
        import copy
        newMS = copy.copy(self)
        newMS.molecules = []
        newMS.interMolecularBonds = []
        for m in self.molecules:
            newMS.molecules.append(m.Copy())
        for b in self.interMolecularBonds:
            newMS.interMolecularBonds.append(b.Copy())
        newMS.boundary = copy.deepcopy(self.boundary)
        newMS.trajectory = self.trajectory   # copies only a reference
        return newMS

    def CopyWithTrajectory(self):
        newMS = self.Copy()
        newMS.trajectory = self.trajectory.Copy()
        return newMS

    def NAtoms(self):
        atomCount = 0
        for m in self.molecules:
            atomCount += len(m.atoms)
        return atomCount

    def RenumberAtomSerials(self, startingSystemwideSerial = 1):
        # 重新编号 MolecularSystem中每个原子的serials 和 systemwideSerials。
        # 此函数还会（重新）构造“systemWideSerialToMoleculeAndAtomMap”
        # 这是一个非常重要的函数，因为很多情况下，原子编号的唯一性与连续性是开展MD和QM计算的必要条件。
        # 原则上，几乎所有的MolecularFile(文件读写器)在读取一个MolecularSystem结束时，都会自发调用此函数来对原子统一编号，只有少数例外，
        # 例如LAMMPSDATAFile，因为此时文件中已经有原子统一编号,可能需要保留，不再重新编号。
        # 在对MolecularSystem作其它操作，例如分解、合并、添加成份等后，一般也需要调用此函数。

        oldToNewSerialMap = [ {} for i in range(len(self.molecules)) ]
        oldToNewSystemwideSerialMap = {}

        counterInSystem = startingSystemwideSerial

        self.systemWideSerialToMoleculeAndAtomMap = {}
        for i,m in enumerate(self.molecules):
            counterInMolecule = 1
            for a in m.atoms:
                newSerial = '{}'.format(counterInMolecule)
                newSystemwideSerial = '{}'.format(counterInSystem)
                oldToNewSerialMap[i][a.serial] = newSerial
                if a.systemwideSerial != None:
                    oldToNewSystemwideSerialMap[a.systemwideSerial] = newSystemwideSerial
                a.serial = newSerial
                a.systemwideSerial = newSystemwideSerial
                counterInMolecule += 1
                counterInSystem += 1
                self.systemWideSerialToMoleculeAndAtomMap[a.systemwideSerial] = (m,a)

        for i,m in enumerate(self.molecules):
            for b in m.bonds:
                b.atom1 = oldToNewSerialMap[i][b.atom1]
                b.atom2 = oldToNewSerialMap[i][b.atom2]

        for b in self.interMolecularBonds:
            b.atom1 = oldToNewSystemwideSerialMap[b.atom1]
            b.atom2 = oldToNewSystemwideSerialMap[b.atom2]

    def AutoDetectBonds(self, autoBondDetector, flushCurrentBonds=False, periodicBoundary=None, max_workers=None, batch_size=5000):
        autoBondDetector.Detect(self, flushCurrentBonds,periodicBoundary,max_workers=max_workers, batch_size=batch_size)

    def Translate(self,dx,dy,dz):
        # Molecule.Translate is not defined. Seems unnecessary.
        for m in self.molecules:
            for a in m.atoms:
                a.Translate(dx,dy,dz)

    def Rotate(self, clockwise_degree, axis): # rotate around a axis. For rotation around x, give axis as [1,0,0])
        original = np.mat(np.zeros((self.NAtoms(), 3)))
        index = 0
        for mol in self.molecules:
            for atom in mol.atoms:
                original[index,0], original[index,1], original[index,2] = [atom.x, atom.y, atom.z]
                index += 1
        import Utility
        rotated = Utility.Rotate(original, clockwise_degree, axis)
        index = 0
        for mol in self.molecules:
            for atom in mol.atoms:
                atom.x, atom.y, atom.z = rotated[index,0], rotated[index,1], rotated[index,2]
                index += 1

    def FractionalToCartesianCoordinates(self):
        # Now support only orthogonal systems.
        A = self.boundary[0][0]
        B = self.boundary[1][1]
        C = self.boundary[2][2]
        for m in self.molecules:
            for a in m.atoms:
                a.x *= A
                a.y *= B
                a.z *= C

    def UpdateCoordinatesByTrajectoryFrame(self,iFrame):
        # 如果记录了轨迹，将体系中的所有原子的坐标更新为轨迹的第iFrame帧标记的位置。此函数一般用于生成轨迹图像，以利于分析。
        if self.trajectory == None or iFrame >= self.trajectory.NFrames:
            return False
        for mol in self.molecules:
            for atom in mol.atoms:
                if atom.systemwideSerial in self.trajectory.serial_to_index_map:
                    pos = self.trajectory.serial_to_index_map[atom.systemwideSerial]
                    atom.x = self.trajectory.positions[iFrame][pos][0]
                    atom.y = self.trajectory.positions[iFrame][pos][1]
                    atom.z = self.trajectory.positions[iFrame][pos][2]
                else:
                    pass # Don't update, do nothing

    def Summary(self):
        molCount = len(self.molecules)
        bondCount = 0
        for m in self.molecules:
            bondCount += len(m.bonds)
            #m.Summary()
        output("MolecularSystem [{}] has {} molecules, {} atoms, {} intra-molecular bonds, and {} inter-molecular bonds".format(
            self.name,molCount,self.NAtoms(),bondCount,len(self.interMolecularBonds)))
