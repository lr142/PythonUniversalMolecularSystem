# 此函数部分定义了分子动力学的经典力场
# 一个完整的经典力场包含三个部分：
# 1. 关于原子类型的定义及识别规则
# 2. 力场参数，包括力场的函数形式，原子类型（含电荷、质量），pairwise参数，
# 键类型，键角类型，二面角类型，非正常二面角类型，多体作用类型等；
# 3. 分子体系中含有的所有原子，键，键角，二面角，多体作用等及它们对应的力场类型

# 此模块实现的是第3部分。定义了类Forcefield。
# 一个Forcefield包含了一个AtomTypeRecognition对象和一个ForcefieldParameters对象。
# 同时，它还记录了体系的所有分子、原子、键、键角、二面角等信息。因此，一个Forcefield应当是
# 与一个MolecularSystem处于同一层级的结构。从一个Forcefield对象应当可以自洽地(self-contained)
# 导出得到一个LAMMPS data文件。

from ForcefieldParameters import ForcefieldParameters
from ForcefieldAtomTypeRecognition import AtomTypeRecognition
from Utility import *


class ForcefieldAtom:
    # 该类对应于类Atom。一个Molecule中的一个Atom应该正好对应于一个ForcefieldAtom。某些情况下，Molecule中的有些原子可能不对于
    # 出现在力场中的原子，例如使用United Atom或粗粒化模型时的情况。在那种情况下，我们要求先对Molecule进行处理，使其中仅含有会出现
    # 在力场计算中的原子
    type:str # 类型
    number:int # 序号。指输出成LAMMPS Data文件时，在那里面的序号，不是它在Molecule中的序号
    x:float # 坐标。在构建时，从MolecularSystem中拷贝得到。
    y:float
    z:float
    charge:float # 电荷。通常情况下以力场中设置为准，但保留此字段以允许用户调整个别原子的charge
    def __init__(self):
        super().__init__()
    def Show(self):
        output("Atom #{}({}), {} {} {} {}".format(self.number,self.type,self.charge,
                                                  self.x,self.y,self.z))
class ForcefieldComponent:
    # 虚基类，是ForcefieldBond，ForcefieldAngle，ForcefieldDihedral，ForcefieldImproper的父类
    type:int # 类型。内部存储的是这种类型的序号(0开始)
    type_number: int # 这种类型在全局的编号
    number:int # 序号。指输出成LAMMPS Data文件时，在那里面的序号，不是它在Molecule中的序号
    atoms:[int] # 涉及的原子。以原子在本Molecule中的index来表示，不是原子的number。
    atoms_numbers: [int] # 涉及的原子在整个体系中的 number。
    def __init__(self):
        self.atoms = None
        self.atoms_numbers = None
        self.number = self.type = None
    def Show(self):
        category = [None,None,"Bond","Angle","Dihedral","Improper"][len(self.atoms)]
        output("{} #{}({}), {}".format(category,self.number,self.type,self.atoms_numbers))
# 在目前的实现中，发现只用ForcefieldElement就可以实现功能了，以下单独实现每个具体类并不必要。
# 因此我把以下的代码注释掉了
# class ForcefieldBond(ForcefieldComponent):
#     def __init__(self):
#         super().__init__()
# class ForcefieldAngle(ForcefieldComponent):
#     def __init__(self):
#         super().__init__()
# class ForcefieldDihedral(ForcefieldComponent):
#     def __init__(self):
#         super().__init__()
# class ForcefieldImproper(ForcefieldComponent):
#     def __init__(self):
#         super().__init__()

class ForcefieldMolecule:
    # 力场中的分子
    type:str # 类型
    number:int # 序号。指输出成LAMMPS Data文件时，在那里面的序号，不是它在Molecule中的序号
    fixed:bool # 是否固定。fixed的分子在力场中不在任何一个thermostat考虑之内。
    rigid:bool # 是否为刚体。刚体分子结构固定，但它仍然在某一个thermostat考虑之内
    atoms:[ForcefieldAtom] # 以下是力场分子的成份，包括所有的原子、键、二面角等
    bonds:[ForcefieldComponent]
    angles:[ForcefieldComponent]
    dihedrals:[ForcefieldComponent]
    impropers:[ForcefieldComponent]
    def __init__(self):
        self.type = None
        self.number = None
        self.fixed = self.rigid = None
        self.atoms = []
        self.bonds = []
        self.angles = []
        self.dihedrals = []
        self.impropers = []
    def Summary(self):
        output("FFMolecule Number={}, FIX:{}, RIGID:{}. ATOMS,B,A,D,I = {} {} {} {} {}".format(
            self.number,"T" if self.fixed else "F", "T" if self.rigid else "F",
            len(self.atoms),len(self.bonds),len(self.angles),len(self.dihedrals),len(self.impropers)))

class PathGenerator():
    # 这是一个辅助函数类，用以枚举分子中所有的键、键角、二面角、非正常二面角。
    # 把分子内原子间成键情况想象成一个图，该类实现的功能即是枚举从图中每个点出发，具有指定长度（=2,3,4）的路径。
    bondedMap: [set] # 原子间成键情况图
    NAtoms: int # 原子数
    def __init__(self,bondedMap):
        self.bondedMap = bondedMap
        self.NAtoms = len(self.bondedMap)
    def __AllPathsFromGivenAtom__(self,iAtom,length,visited=None):
        # 从一个原子出发，找到所有长度为length的路径
        # 使用递归算法来实现
        pathsList = []  # 用来记录生成的路径，每条记录本身也是一个长度等于length的list
        if visited == None:
            visited = [False for _ in range(self.NAtoms)] # 是否已经在当前的路径上
        if length > 1:
            # 先把自己标记为"在路径上"，然后对自己的每个子节点，递归要求查找所有路径为 length-1 的子路径
            visited[iAtom] = True
            subpaths = []
            for child in self.bondedMap[iAtom]:
                if not visited[child]:
                    subpaths.extend(self.__AllPathsFromGivenAtom__(child,length-1,visited))
            # 在所有找到的子路径中，将自身的序号作为路径的第一个点，将路径变长
            for subpath in subpaths:
                subpath.insert(0,iAtom)
            # 退出时需要标记为假，允许其它路径通过该点来生长。
            visited[iAtom] = False
            return subpaths
        else:
            # 递归结束点。发现期望长度的路径，那么直接返回它自己（作为一个列表的列表）
            return [[iAtom]]
    # 返回所有的键/角/二面角。注意此函数和后面几个函数一样，会返回同一个键/键角/二面角两次（正，反向各一次）
    def AllBondsAnglesDihedrals(self, B_A_D):
        # B_A_D == 2，3，4分别为Bonds, Angles, Dihedrals
        paths = []
        for i in range(self.NAtoms):
            paths.extend(self.__AllPathsFromGivenAtom__(i, B_A_D))
        # 由于路径搜索算法会将正向与反向的路径都输出一次，因此这里要求规定一个顺序(原子序号升序)，将重复的路径去掉。
        uniquePaths = []
        for p in paths:
            if p[0] < p[-1]:
                uniquePaths.append(p)
        return uniquePaths
    def AllImpropers(self):
        lists = []
        for i in range(self.NAtoms):
            if len(self.bondedMap[i]) == 3:
                path = [x for x in self.bondedMap[i]]
                path.sort()
                path.insert(0,i)
                lists.append(path)
        return lists

class Forcefield:
    name : str  # 该力场的名称
    atomTypeRecognition:AtomTypeRecognition # 原子类型自动识别器，从规则文件中构建
    forcefieldParameters: ForcefieldParameters # 所有的力场参数
    molecules: [ForcefieldMolecule] #力场中的所有分子
    boundary : []  # 晶胞尺寸。与MolecularSystem中的boundary参数意义相同，可以是3*2，或3*3的形式。3*2指[[xlo,xhi],[ylo,yhi],[zlo,zhi]]
    groupsInfo: [] # LAMMPS中的分组信息，目前仅存储字符串数组，直接写入LAMMPS中
    def __init__(self,name,atomtypesFilename,parametersFilename):
        # 从两个描述文件中构建力场。第1个是原子类型自动识别的规则文件，第2是力场参数描述文件
        self.name = name
        self.atomTypeRecognition = AtomTypeRecognition(atomtypesFilename)
        self.forcefieldParameters = ForcefieldParameters(name)
        self.forcefieldParameters.ReadForcefieldParametersFile(parametersFilename)
        self.molecules = []
        self.boundary = []
        self.groupsInfo = []
        # 一致性检验。确保两个文件中定义的原子种类是一样的
        types1 = set()
        types2 = set()
        for rule in self.atomTypeRecognition.rules:
            types1.add(rule.root.type)
        for atomType in self.forcefieldParameters.atomTypes:
            types2.add(atomType.name)
        for type in types1:
            if type not in types2:
                error("Type \"{}\" defined in \"{}\" but not in \"{}\"".format(
                    type,atomtypesFilename,parametersFilename),fatal=False)
        for type in types2:
            if type not in types1:
                error("Type \"{}\" defined in \"{}\" but not in \"{}\"".format(
                    type,parametersFilename,atomtypesFilename),fatal=False)

    def SetBoundary(self,newBoundary):
        import copy
        self.boundary = copy.deepcopy(newBoundary)

    def SetGroupsInfo(self,groupsInfo):
        # 分组信息，即LAMMPS中的groups信息。此函数要求groupsInfo为字符串list，函数不做任何处理，仅拷贝此数组
        self.groupsInfo = [s for s in groupsInfo]

    def Extend(self,anotherFF):
        # 力场扩展。指把anotherFF中的力场参数（原子种类，B A D I种类）加入到此力场中
        # 整合的规则是，
        # 1. 对于力场的函数形式，以第一个力场的为准。anotherForcefield的functional部分会被直接忽略。
        # 2. 尽量避免原子种类的冲突。如果有冲突，给出提示，以后出现的原子种类定义为准
        # 3. 对于B A D I类型，不做处理。按照本程序中对于B A D I的识别算法，后出现的规则总是优先。应此anotherForcefield会优先于原力场
        # 该方法比较适合用于对力场进行小规模扩充，比如在OPLS力场中加入TIP4P水模型或一个特定小分子的模型。
        # 如果只是想对原有的原子类型提供一些额外的力场参数(Pairwise或B A D I)，请不要在anotherFF中定义新的原子类型。
        # 请注意：
        # 1. 合并后，请不要手动销毁anotherFF数据结构，也不要更改它的内容！因为anotherFF的数据是被浅拷贝进self的。
        # 2. 力场合并操作只针对力场参数，不针对力场中具体的原子,B,A,D,I。力场合并操作应该在添加任何分子之前完成。如果已经添加了分子
        # 再执行力场合并操作，原有的数据就没有意义了。程序如果检测到这种情况，也会给出错误提示。
        if len(self.molecules) > 0:
            error("Forcefield \"{}\" contains {} molecules, and Forcefield::Extend() operation is not allowed unless it "
                  "contains no molecule.".format(self.name,len(self.molecules)))
            return False
        self.atomTypeRecognition.Extend(anotherFF.atomTypeRecognition)
        self.forcefieldParameters.Extend(anotherFF.forcefieldParameters)

    def __AddMoleculeByCopyingFrom(self,molecule,refMol):
        # refMol：从一个已经构建好的分子中拷贝力场参数。如果一个体系中包含大量相同的分子，那么为了效率，当应对第个分子从头构键力场
        #         参数，而后面的所有相同分子都应当从之前的分子中复制得到。此函数中，程序仅从molecule
        #         读取原子坐标，而其它所有信息均从refMol这个参考分子中拷贝
        # 添加后，会将molecule的type字段设置为力场类型（唯一改动molecule的地方）。
        import copy
        newFFMol = copy.deepcopy(refMol)
        for ffAtom,realAtom in zip(newFFMol.atoms,molecule.atoms):
            ffAtom.x, ffAtom.y, ffAtom.z = realAtom.x, realAtom.y, realAtom.z
            realAtom.type = ffAtom.type
        self.molecules.append(newFFMol)
        pass

    def __AddMoleculeNew(self, molecule, fixed, rigid, withBonds, useCurrentAtomTypes, useCurrentCharges):
        # 往力场中添加一个分子。
        # 各参数的意义为：molecule 分子结构。其中应该具有完整的坐标信息与成键信息。每个原子的原子类型可以有;也可以没有，让程序自动识别
        # fixed: 是否fixed
        # rigid: 是否rigid
        # withoutBonds: 不考虑成键情况（常见于fixed或rigid分子，及不需要用共价键来描述的体系）
        # useCurrentAtomTypes: 是否要使用molecule中原有的Atom::type。如果为False，则原来Molecule中所有原子的type会被清空。否则原来的type会被
        #                      读取并在识别原子类型时加以利用。如果用户已经设置了部分或全部原子的type，则应该使用True
        # useCurrentCharges:   是否要使用molecule中原有的Atom::charge。如果为False，则原来Molecule中所有原子的charge会被忽略。
        #                      否则原来的charge会根据以下两种情况加以利用：1. 如果原来的charge是None，那么程序会在后面重新根据原子的力场类型
        #                      来设置charge。2. 如果原来的charge不是None，那么程序就会用原来的charge,不会再更改。
        ffmol = ForcefieldMolecule()
        ffmol.fixed = fixed
        ffmol.rigid = rigid
        # 第一步，分配原子类型
        if useCurrentAtomTypes:
            for atom in molecule.atoms:
                atom.type = None
        result = self.atomTypeRecognition.RecognizeAllAtoms(molecule,maxDepth=3,maxIterations=5,debugging=False)
        if not result:
            output("Error: For following atoms, forcefield types cannot be assigned")
            for atom in molecule.atoms:
                if atom.type == None or atom.type == "":
                    output("{} {} {}".format(atom.serial,atom.element,[atom.x,atom.y,atom.z]))
            error("Not all atoms in molecule {} are assigned forcefield types".format(molecule.name))

        # 第二步，构建atoms:[ForcefieldAtom]列表：
        # 注意在这一步，原子的number还没有设置
        # 原子的charge是要根据useCurrentCharges来判断。要么用molecule里的，要么用力场指定。
        for atom in molecule.atoms:
            newAtom = ForcefieldAtom()
            newAtom.type = atom.type
            if useCurrentCharges and atom.charge != None:
                newAtom.charge = atom.charge
            else:
                newAtom.charge = self.forcefieldParameters.LookupTypeCharge(atom.type)
            assert(newAtom.charge != None)

            newAtom.number = None
            newAtom.x, newAtom.y, newAtom.z = (atom.x, atom.y, atom.z)
            ffmol.atoms.append(newAtom)

        # 第三步，构建 bonds, angles, dihedrals, impropers
        # 如果withBonds==False,这里就可以提前终止了。
        if not withBonds:
            return True
        pg = PathGenerator(molecule.BondedMap()) # 路径生成器。

        # 这里使用统一的代码来实现键B、角A、二面角D、非正常二面角I的识别工作。
        # 变量BorAorD代表现在处理是的什么。2,3,4,5 对应B，A，D, I
        destinations = [None,None, ffmol.bonds, ffmol.angles, ffmol.dihedrals,ffmol.impropers]
        for BADI in [2,3,4,5]:
            if BADI < 5:
                atom_sequencies = pg.AllBondsAnglesDihedrals(BADI)
            else:
                atom_sequencies = pg.AllImpropers()
            for atom_sequence in atom_sequencies:
                atom_types = [ffmol.atoms[iAtom].type for iAtom in atom_sequence]
                bond_angle_dihedral_type = self.forcefieldParameters.LookupB_A_D_I_Types(atom_types, BADI)
                if bond_angle_dihedral_type != None:
                    newElement = ForcefieldComponent()
                    newElement.type = bond_angle_dihedral_type
                    newElement.atoms = atom_sequence
                    destinations[BADI].append(newElement)
            # print("Total Count of This Category: {}".format(len(destinations[BADI])))
            # for element in destinations[BADI]:
            #     ffPar = self.forcefieldParameters
            #     refs = [None,None,ffPar.bondTypes,ffPar.angleTypes,ffPar.dihedralTypes,ffPar.improperTypes]
            #     typename = refs[BADI][element.type].name
            #     print("{}  : {} {}".format(element.atoms,element.type,typename))

        # 第四步
        self.molecules.append(ffmol)
        return True

    def AddMolecule(self, molecule, fixed=False, rigid=False, withBonds=True,
                    useCurrentAtomTypes=False, useCurrentCharges=False, copyFromMol=None):
        # 最重要的一个函数，也是用户调用接口。往力场中添加一个分子。此函数是以上两个函数：
        # __AddMoleculeByCopyingFrom()与__AddMoleculeNew()的封装。如果copyFromMol不为None则调用第一个，
        # 否则调用第二个函数。
        # 添加后，会将molecule的type字段设置为力场类型（这是唯一对molecule的改动）。
        if copyFromMol != None:
            return self.__AddMoleculeByCopyingFrom(molecule,copyFromMol)
        else:
            return self.__AddMoleculeNew(molecule, fixed, rigid, withBonds, useCurrentAtomTypes, useCurrentCharges)

    def Finalize(self):
        # 本函数需要在力场已设置好，并且往里面添加完成了所有原子之后才可以调用。如果调用之后又添加了分子，则需要再次调用。
        # 本函数会对结构中的所有力场元素(Atom, B, A, D, I,)进行统一编号，并找出 B,A,D,I中涉及的原子
        # 在体系全局中的编号，写入atoms_numbers

        # 第一步，给每个原子和分子编号。在LAMMPS里，从1开始和从0开始都可以。这里从0开始编号
        global_atom_number = 1
        global_mol_number = 1
        for mol in self.molecules:
            mol.number = global_mol_number
            global_mol_number += 1
            for atom in mol.atoms:
                atom.number = global_atom_number
                global_atom_number += 1

        # 第二步，找到B，A，D，I中涉及的原子在全局的编号
        def find_gloable_number(mol,iAtom):
            return mol.atoms[iAtom].number

        for BADI in range(2,6):
            global_number = 1
            for mol in self.molecules:
                components = [None,None,mol.bonds, mol.angles, mol.dihedrals, mol.impropers]
                component = components[BADI] # 一个component代表分子中的所有B，所有A，等等
                for item in component:    # 一个item代表分子的一个B,A,D,I
                    item.atoms_numbers = [ find_gloable_number(mol,iAtom) for iAtom in item.atoms ]
                    item.number = global_number
                    global_number += 1

    def Show(self):
        for mol in self.molecules:
            for atom in mol.atoms:
                atom.Show()

        for BADI in range(2,6):
            for mol in self.molecules:
                components = [None,None,mol.bonds, mol.angles, mol.dihedrals, mol.impropers]
                component = components[BADI] # 一个component代表分子中的所有B，所有A，等等
                for item in component:    # 一个item代表分子的一个B,A,D,I
                    item.Show()

    def __WriteInitFile__(self,initFileName):
        with open(initFileName,"w") as initFile:
            for line in self.forcefieldParameters.functional:
                initFile.write(line+'\n')

    def __WriteSettingsFile__(self,settingsFileName):
        def __atom_type_to_number__(type):
            return self.forcefieldParameters.atomTypesToNumberMap[type]

        with open(settingsFileName,"w") as settingsFile:
            # Pairwise
            for item in self.forcefieldParameters.pairwiseTypes:
                numbers = [__atom_type_to_number__(type) for type in item.types]
                settingsFile.write(item.parameter.format(numbers[0],numbers[1])+'\n')
            # B,A,D,I
            for item in self.forcefieldParameters.bondTypes:
                settingsFile.write(item.parameter.format(item.number)+'\n')
            for item in self.forcefieldParameters.angleTypes:
                settingsFile.write(item.parameter.format(item.number)+'\n')
            for item in self.forcefieldParameters.dihedralTypes:
                settingsFile.write(item.parameter.format(item.number)+'\n')
            for item in self.forcefieldParameters.improperTypes:
                settingsFile.write(item.parameter.format(item.number)+'\n')
            #groups Infor
            for group in self.groupsInfo:
                settingsFile.write("{}\n".format(group))

    def __WriteDataFile__(self,dataFileName):
        datafile = None
        try:
            datafile = open(dataFileName,"w")
        except:
            error("Cannot open <{}> to write".format(dataFileName))

        totalCounts = [0,0,0,0,0,0]# counts for Atoms, B,A,D,I
        for mol in self.molecules:
            totalCounts[1] += len(mol.atoms)
            totalCounts[2] += len(mol.bonds)
            totalCounts[3] += len(mol.angles)
            totalCounts[4] += len(mol.dihedrals)
            totalCounts[5] += len(mol.impropers)

        datafile.write("LAMMPS Description\n\n")
        datafile.write("     {}  atoms\n".format(totalCounts[1]))
        datafile.write("     {}  bonds\n".format(totalCounts[2]))
        datafile.write("     {}  angles\n".format(totalCounts[3]))
        datafile.write("     {}  dihedrals\n".format(totalCounts[4]))
        datafile.write("     {}  impropers\n\n".format(totalCounts[5]))

        datafile.write("     {}  atom types\n".format(len(self.forcefieldParameters.atomTypes)))
        datafile.write("     {}  bond types\n".format(len(self.forcefieldParameters.bondTypes)))
        datafile.write("     {}  angle types\n".format(len(self.forcefieldParameters.angleTypes)))
        datafile.write("     {}  dihedral types\n".format(len(self.forcefieldParameters.dihedralTypes)))
        datafile.write("     {}  improper types\n\n".format(len(self.forcefieldParameters.improperTypes)))

        datafile.write("  {:.2f} {:.2f} xlo xhi\n".format(self.boundary[0][0],self.boundary[0][1]))
        datafile.write("  {:.2f} {:.2f} ylo yhi\n".format(self.boundary[1][0],self.boundary[1][1]))
        datafile.write("  {:.2f} {:.2f} zlo zhi\n\n".format(self.boundary[2][0], self.boundary[2][1]))

        datafile.write("Masses\n\n")
        for type in self.forcefieldParameters.atomTypes:
            datafile.write("{} {}\n".format(type.number,type.mass))

        datafile.write("\nAtoms\n\n")
        for mol in self.molecules:
            for atom in mol.atoms:
                atom_type_number = self.forcefieldParameters.atomTypesToNumberMap[atom.type]
                datafile.write("{} {} {} {} {} {} {}\n".format(
                    atom.number,mol.number,atom_type_number,atom.charge,atom.x,atom.y,atom.z))

        for BADI in range(2,6):
            if totalCounts[BADI] == 0:
                continue
            keyword = [None,None,"Bonds","Angles","Dihedrals","Impropers"][BADI]
            datafile.write("\n"+keyword+"\n\n")
            for mol in self.molecules:
                components = [None,None,mol.bonds,mol.angles,mol.dihedrals,mol.impropers][BADI]
                for item in components:
                    # item.type + 1 是因为BADI的类型是从1开始往后排的。
                    datafile.write("{} {} ".format(item.number,item.type+1))
                    for atom_number in item.atoms_numbers:
                        datafile.write("{} ".format(atom_number))
                    datafile.write("\n")

        datafile.write("\n")
        datafile.close()

    def WriteMoleculeTemplateFile(self,templateFileName):
        # Molecule template file is very similar to data file except that:
        # 1. no Atom Types, Bond Types, etc. no Boundary
        # 2. no Masses
        # 3. The Atoms section has been divided into 3 separate sections: Coords, Types, Charges
        molTemplateFile = None
        try:
            molTemplateFile = open(templateFileName,"w")
        except:
            error("Cannot open <{}> to write".format(templateFileName))

        totalCounts = [0,0,0,0,0,0]# counts for Atoms, B,A,D,I
        for mol in self.molecules:
            totalCounts[1] += len(mol.atoms)
            totalCounts[2] += len(mol.bonds)
            totalCounts[3] += len(mol.angles)
            totalCounts[4] += len(mol.dihedrals)
            totalCounts[5] += len(mol.impropers)

        molTemplateFile.write("LAMMPS Description\n\n")
        molTemplateFile.write("     {}  atoms\n".format(totalCounts[1]))
        molTemplateFile.write("     {}  bonds\n".format(totalCounts[2]))
        molTemplateFile.write("     {}  angles\n".format(totalCounts[3]))
        molTemplateFile.write("     {}  dihedrals\n".format(totalCounts[4]))
        molTemplateFile.write("     {}  impropers\n".format(totalCounts[5]))

        molTemplateFile.write("\nCoords\n\n")
        for mol in self.molecules:
            for atom in mol.atoms:
                atom_type_number = self.forcefieldParameters.atomTypesToNumberMap[atom.type]
                molTemplateFile.write("{} {} {} {}\n".format(
                    atom.number,atom.x,atom.y,atom.z))

        molTemplateFile.write("\nTypes\n\n")
        for mol in self.molecules:
            for atom in mol.atoms:
                atom_type_number = self.forcefieldParameters.atomTypesToNumberMap[atom.type]
                molTemplateFile.write("{} {} \n".format(
                    atom.number,atom_type_number))

        molTemplateFile.write("\nCharges\n\n")
        for mol in self.molecules:
            for atom in mol.atoms:
                atom_type_number = self.forcefieldParameters.atomTypesToNumberMap[atom.type]
                molTemplateFile.write("{} {}\n".format(
                    atom.number,atom.charge))

        for BADI in range(2,6):
            if totalCounts[BADI] == 0:
                continue
            keyword = [None,None,"Bonds","Angles","Dihedrals","Impropers"][BADI]
            molTemplateFile.write("\n"+keyword+"\n\n")
            for mol in self.molecules:
                components = [None,None,mol.bonds,mol.angles,mol.dihedrals,mol.impropers][BADI]
                for item in components:
                    # item.type + 1 是因为BADI的类型是从1开始往后排的。
                    molTemplateFile.write("{} {} ".format(item.number,item.type+1))
                    for atom_number in item.atoms_numbers:
                        molTemplateFile.write("{} ".format(atom_number))
                    molTemplateFile.write("\n")

        molTemplateFile.write("\n")
        molTemplateFile.close()

    def WriteLAMMPSFiles(self,writeInFile=False):
        dataFileName = "{}.data".format(self.name)
        initFileName = "{}.in.init".format(self.name)
        settingFileName = "{}.in.settings".format(self.name)
        inFileName = "{}.in".format(self.name)

        self.__WriteInitFile__(initFileName)
        self.__WriteSettingsFile__(settingFileName)
        self.__WriteDataFile__(dataFileName)

        if writeInFile == False:
            return

        with open(inFileName,"w") as infile:
            infile.write("include \"{}\"\n".format(initFileName))
            infile.write("read_data \"{}\"\n".format(dataFileName))
            infile.write("include \"{}\"\n".format(settingFileName))
            infile.write("minimize 1.0e-5 1.0e-7 1000 10000\n")
            infile.write("timestep 1\n")
            infile.write("thermo_style custom step temp pe etotal press time\n")
            infile.write("thermo 1000\n")
            infile.write("fix  fxnvt all nvt temp 300.0 300.0 100\n")
            infile.write("dump d1 all custom 10 system.lammpstrj id mol type x y z vx vy vz\n")
            infile.write("run  50000\n")

