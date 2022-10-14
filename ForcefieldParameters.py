# 此函数部分定义了分子动力学的经典力场
# 一个完整的经典力场包含三个部分：
# 1. 关于原子类型的定义及识别规则
# 2. 力场参数，包括力场的函数形式，原子类型（含电荷、质量），pairwise参数，
# 键类型，键角类型，二面角类型，非正常二面角类型，多体作用类型等；
# 3. 分子体系中含有的所有原子，键，键角，二面角，多体作用等及它们对应的力场类型

# 此模块实现的是第2部分，定义类 ForcefieldParameters 来记录一个力场中的所有参数：
# 本模块要实现的功能包括：
# 1. 定义一种文件形式，存储力场参数。程序可以从文件中读取一个力场中包含的所有参数
# 2. (重点)现实一种根据原子间成键情况来自动判定原子所属力场类型的功能（力场推断）
# 3. 在判定了原子类型后，进一步根据成键情况判定体系中所有的键、键角、二面角等
# 4. 导出MD程序（如LAMMPS，CP2K等）计算所需的结构文件。

from Utility import *
from UniversalMolecularSystem import *
import os

class Parameter:
    # 一个virtual类，是AtomType，Pairwise，BondType，AngleType，DihedralType，ImproperType的基类
    # 提供virtual接口
    name:str    # name 是原子类型名称、pairwise的名称、bondtype的名称等
    number:str  # number 是为了符合LAMMPS规范，对所有AtomType，BondType，AngleType，DihedralType，ImproperType 重新编号后得到的号码
    types:[str] # types是此参数涉及的原子种类，例如Pairwise/Bond涉及的两种原子，Angle涉及的三种原子，DihedralType，ImproperType涉及的四种原子
    parameter:str  # parameter是以字符串形式存储的，可以写入LAMMPS的设置命令。例如"angle_coeff {}  58.35 112.7"。其中的类型名称用{}代替
    priority: int  # 规则中通配符*号的个数。个数越多，优先级越低。
    def __init__(self):
        self.name = ""
        self.number = None
        self.types = []
        self.parameter = ""
        pass
    def ParseLine(self,line):
        # 读入一行文件，并根据内容写入自身的相应字段。成功返回True,失败返回False
        pass
    def Matches(self,types):
        # 此命令主要适用于BondType，AngleType，DihedralType，ImproperType，用于检测以list给出的种类列表types是否适用于此规则
        pass
    def WriteParameter(self, numbered=False):
        # 打印参数内容。numbered的意思是输出符合LAMMPS格式规范的格式，
        # 即只输出原子类型、键类型等的编号。则为False则输出具体的信息（成键原子的具体类型）供调试
        pass

class AtomType(Parameter):
    def __init__(self):
        super().__init__()
        self.mass = self.charge = 0.0
        self.name_in_bonding = ""
        pass
    def ParseLine(self,line):
        try:
            words = line.split()
            self.name = words[0]
            self.name_in_bonding = words[1]
            if self.name_in_bonding == "--":
                self.name_in_bonding = self.name
            self.mass = float(words[2])
            self.charge = float(words[3])
        except:
            output("A line like this is expected:\n"
            "CH3-  Csingle  12.011  -0.18".format(line))
            return False
        return True
    def WriteParameter(self, numbered=False):
        name = "{}".format(self.number) if numbered else self.name
        output("mass {} {} # set type {} charge {}".format(name,self.mass,name,self.charge))
        pass
class Pairwise(Parameter):
    def __init__(self):
        super().__init__()
        pass
    def ParseLine(self,line):
        try:
            words = line.split()
            assert(words[0] == "pair_coeff")
            self.types = [words[1],words[2]]
            self.name = ""
            self.parameter = "pair_coeff {{}} {{}} {}".format(" ".join(words[3:]))
        except:
            output("A line like this is expected:\n"
            "pair_coeff SPC_O SPC_O  0.1554 3.16557".format(line))
            return False
        return True
    def WriteParameter(self, atomTypeToNumberMap=None, numbered=False):
        types = [ self.types[_] for _ in range(2)]
        if atomTypeToNumberMap != None and numbered:
            types = [ atomTypeToNumberMap[types[_]] for _ in range(2)]
        output(self.parameter.format(types[0],types[1]))
        pass
class BondType(Parameter):
    def __init__(self):
        super().__init__()
        pass
    def ParseLine(self,line):
        try:
            words = line.split()
            assert (words[2] == "bond_coeff")
            self.types = [words[0], words[1]]
            self.name = words[3] if words[3]!="--" else "_".join(words[:2])
            self.parameter = "bond_coeff {{}} {}".format(" ".join(words[4:]))
            self.priority = self.types.count("*")
        except:
            output("A line like this is expected:\n"
                   "SPC_O SPC_H bond_coeff --  554.1349 1.0".format(line))
            return False
        return True
    def WriteParameter(self, numbered=False):
        if numbered:
            output(self.parameter.format(self.number))
        else:
            output(self.parameter.format(" ".join(self.types)))
class AngleType(Parameter):
    def __init__(self):
        super().__init__()
        pass
    def ParseLine(self,line):
        try:
            words = line.split()
            assert (words[3] == "angle_coeff")
            self.types = [words[0], words[1], words[2]]
            self.name = words[4] if words[4]!="--" else "_".join(words[:3])
            self.parameter = "angle_coeff {{}} {}".format(" ".join(words[5:]))
            self.priority = self.types.count("*")
        except:
            output("A line like this is expected:\n"
                   "SPC_H SPC_O SPC_H       angle_coeff --  45.7696 109.47".format(line))
            return False
        return True
    def WriteParameter(self, numbered=False):
        if numbered:
            output(self.parameter.format(self.number))
        else:
            output(self.parameter.format(" ".join(self.types)))
class DihedralType(Parameter):
    def __init__(self):
        super().__init__()
        pass
    def ParseLine(self,line):
        try:
            words = line.split()
            assert (words[4] == "dihedral_coeff")
            self.types = [words[0], words[1], words[2], words[3]]
            self.name = words[5] if words[5]!="--" else "_".join(words[:4])
            self.parameter = "dihedral_coeff {{}} {}".format(" ".join(words[6:]))
            self.priority = self.types.count("*")
        except:
            output("A line like this is expected:\n"
                   "Hsingle Csingle Csingle C.ar    dihedral_coeff --  0.0 0.0 0.462 0.0".format(line))
            return False
        return True
    def WriteParameter(self, numbered=False):
        if numbered:
            output(self.parameter.format(self.number))
        else:
            output(self.parameter.format(" ".join(self.types)))
class ImproperType(Parameter):
    def __init__(self):
        super().__init__()
        pass
    def ParseLine(self,line):
        try:
            words = line.split()
            assert (words[4] == "improper_coeff")
            self.types = [words[0], words[1], words[2], words[3]]
            self.name = words[5] if words[5]!="--" else "_".join(words[:4])
            self.parameter = "improper_coeff {{}} {}".format(" ".join(words[6:]))
            self.priority = self.types.count("*")
        except:
            output("A line like this is expected:\n"
                   "Cdouble * * *       improper_coeff --  15.0 0.0".format(line))
            return False
        return True
    def WriteParameter(self, numbered=False):
        if numbered:
            output(self.parameter.format(self.number))
        else:
            output(self.parameter.format(" ".join(self.types)))
class ManyBodyType(Parameter):
    # 暂未实现
    def __init__(self):
        pass
class ForcefieldParameters:
    name:str # 力场名称
    functional:[str] # 字符串数组，直接记录它在LAMMPS程序中出现的对力场函数形式的描述
    atomTypes:[AtomType]
    pairwiseTypes:[Pairwise]
    bondTypes:[BondType]
    angleTypes:[AngleType]
    dihedralTypes:[DihedralType]
    improperTypes:[ImproperType]
    manyBodyTypes:[ManyBodyType]
    atomTypesToNumberMap: {} # 原子类型 --> 类型编号的 map
    atomTypesToChargeMap: {} # 原子类型 --> Charges的 map
    atomTypesToBondedTypeMap: {}  # 原子类型 --> 成键时所使用的类型的 map

    def __init__(self,name):
        self.name = name
        self.functional = []
        self.atomTypes = []
        self.pairwiseTypes = []
        self.bondTypes = []
        self.angleTypes = []
        self.dihedralTypes = []
        self.improperTypes = []
        self.manyBodyTypes = []
        self.atomTypesToNumberMap = None
        self.atomTypesToChargeMap = None
        self.atomTypesToBondedTypeMap = None

    def LookupTypeNumber(self,type):
        if self.atomTypesToNumberMap == None:
            return None
        else:
            return self.atomTypesToNumberMap[type]

    def LookupTypeCharge(self,type):
        if self.atomTypesToChargeMap == None:
            return None
        else:
            return self.atomTypesToChargeMap[type]

    def LookupTypeInBonding(self,type):
        if self.atomTypesToBondedTypeMap == None:
            return None
        else:
            return self.atomTypesToBondedTypeMap[type]

    def Finalize(self):
        # 对所有的原子，键，角、二面角类型（重新）进行编号。
        # 生成 self.atomTypesToNumberMap 数据结构
        # 生成 self.atomTypesToChargeMap 数据结构
        # 生成 self.atomTypesToBondedTypeMap 数据结构
        # 读入力场文件后，程序会自动对力场进行一次Finalize
        # 力场合并后，程序也会自动对力场进行一次Finalize
        # 如果用户用动往力场里加入/删除/改变了元素，则用户有责任手动调用Finalize()
        groups = [self.atomTypes, self.pairwiseTypes, self.bondTypes, self.angleTypes,
                 self.dihedralTypes, self.improperTypes, self.manyBodyTypes]
        for group in groups:
            for i,item in enumerate(group,start=1):
                item.number = i
        self.atomTypesToNumberMap = {}
        self.atomTypesToChargeMap = {}
        self.atomTypesToBondedTypeMap = {}
        for atom in self.atomTypes:
            # 先判断一下是否存在重复的原子类型
            if atom.name in self.atomTypesToNumberMap:
                error("AtomTypes '{}' appears at least twice in the Forcefield, please double check!".format(atom.name),fatal=False)
                return False
            else:
                self.atomTypesToNumberMap[atom.name] = atom.number
                self.atomTypesToChargeMap[atom.name] = atom.charge
                self.atomTypesToBondedTypeMap[atom.name] = atom.name_in_bonding
        return True

    def ReadForcefieldParametersFile(self,filename):
        # 读入一个力场参数文件。该文件的格式类似LAMMPS的输入文件，以一行行命令构成。但该文件中只包含对力场参数的
        # 的描述，不包含对具体每个原子的描述
        # 文件格式的详细说明及示例详见"./DATA/Forcefields/ExampleForcefieldDescription.txt"
        lines = None
        try:
            file = open(filename,"r",encoding='utf-8')
            lines = file.readlines()
            file.close()
        except:
            error("Cannot open {} to read".format(filename))

        sections = {"FUNCTIONAL":0, "ATOMS":1, "PAIRWISE":2, "BONDS":3,
                    "ANGLES":4, "DIHEDRALS":5, "IMPROPERS":6, "MANYBODIES":7}
        currentSection = ""
        for lineno in range(1,len(lines)+1):
            line = lines[lineno-1]
            line = RemoveComment(line).strip().rstrip()
            if len(line) == 0:
                continue
            successfulFlag = True
            if currentSection == "":
                sectionName = line[:line.find("{")].strip()
                if sectionName.upper() in sections:
                    currentSection = sectionName
                else:
                    successfulFlag = False
            elif line == "}":
                currentSection = ""
            elif currentSection == "FUNCTIONAL":
                self.functional.append(line)
            elif currentSection == "ATOMS":
                newType = AtomType()
                successfulFlag = newType.ParseLine(line)
                self.atomTypes.append(newType)
            elif currentSection == "PAIRWISE":
                newType = Pairwise()
                successfulFlag = newType.ParseLine(line)
                self.pairwiseTypes.append(newType)
            elif currentSection == "BONDS":
                newType = BondType()
                successfulFlag = newType.ParseLine(line)
                self.bondTypes.append(newType)
            elif currentSection == "ANGLES":
                newType = AngleType()
                successfulFlag = newType.ParseLine(line)
                self.angleTypes.append(newType)
            elif currentSection == "DIHEDRALS":
                newType = DihedralType()
                successfulFlag = newType.ParseLine(line)
                self.dihedralTypes.append(newType)
            elif currentSection == "IMPROPERS":
                newType = ImproperType()
                successfulFlag = newType.ParseLine(line)
                self.improperTypes.append(newType)
            elif currentSection == "MANYBODIES":
                print("MANYBODIES_NOT_HANDLED_YET")
            else:
                pass
            if not successfulFlag:
                error("While reading file <{}> at line {}:\n{}".format(filename,lineno,lines[lineno-1]))
        self.Finalize()

    def __matching_types_to_types__(self,srcTypes,destTypes):
        for s,d in zip(srcTypes,destTypes):
            if not MatchingWithWildcards(s,d):
                return False
        return True
    def LookupB_A_D_I_Types(self, atomTypes, B_A_D_I):# B_A_D_I=2,3,4,5
        # atomTypes是长度为2到4的list，检查是否存在这种类型的键/角/二面角。存在就返回键类型的序号，不存在就返回None
        # 注意，原子出现的顺序正反都要考虑。
        # B_A_D_I 是查找的对象，2，3，4，5 分别是键/角/二面角/非正常二面角

        seq_original = [self.LookupTypeInBonding(type) for type in atomTypes]
        # seq_original 是出现在路径生成器中，以原子升序排列得到的原子类型列表。它不一定能和BADI定义中的顺序对应得上
        # 因此要考虑原子间按照不同的顺序排列得到的可能结果。
        # 对于B,A,D比较简单，只需考虑正序与逆序，但对I比较复杂，要考虑后三个原子（除中心原子外）的6种全排列

        all_sequences = []
        if B_A_D_I < 5:
            seq_reverse = seq_original.copy()
            seq_reverse.reverse()
            all_sequences = [seq_original,seq_reverse]
        else:
            import itertools
            permutations = itertools.permutations(seq_original[1:])
            first_element = seq_original[:1]
            for perm in permutations:
                all_sequences.append(first_element+list(perm))

        # elements是待处理的对象集合
        elements = None
        if B_A_D_I == 2:
            elements = self.bondTypes
        elif B_A_D_I == 3:
            elements = self.angleTypes
        elif B_A_D_I == 4:
            elements = self.dihedralTypes
        elif B_A_D_I == 5:
            elements = self.improperTypes
        else:
            pass
        assert(elements!=None)
        matchingResult = None
        # 逐一规则进行判断
        for i,e in enumerate(elements):
            # 在按不同顺序排列的序列中，至少要找到一条匹配，才能继续查找下一条规则
            foundASeq = False
            for seq in all_sequences:
                if self.__matching_types_to_types__(e.types,seq):
                    foundASeq = True
                    break
            if not foundASeq:
                continue
            # 发现匹配，先查看是否有已有规则，若无，直接设置匹配结果
            if matchingResult == None:
                matchingResult = i
            # 若之前已有匹配，看规则优先级。priority为规则中*号数目，*越多优先级越低。
            # * 数相同时，后出现的规则优先。
            elif elements[i].priority <= elements[matchingResult].priority:
                matchingResult = i
            else:
                pass
        return matchingResult

    def Extend(self,anotherFF):
        # 力场整合。指把anotherFF中的 原子,B A D I种类 加入到此力场中
        # 整合的规则是，
        # 整合的规则是，。
        # 1. 尽量避免原子种类的冲突。如果有冲突，给出提示，以后出现的原子种类定义为准
        # 2. 对于Pairwise, B A D I类型，不做处理。按照本程序中对于B A D I的识别算法，后出现的规则总是优先。应此anotherFF会优先于原力场
        # 该方法比较适合用于对力场进行小规模扩充，比如在OPLS力场中加入TIP4P水模型或一个特定小分子的模型。
        # 如果只是想对原有的原子类型提供一些额外的力场参数(Pairwise或B A D I)，请不要在anotherFF中定义新的原子类型。
        atomTypesInAnotherFF = set()
        for atomType in anotherFF.atomTypes:
            atomTypesInAnotherFF.add(atomType.name)

        newAtomTypes = []
        for atomType in self.atomTypes:
            if atomType.name in atomTypesInAnotherFF:
                error("In ForcefieldParameters()::Extend(), atom type {} clashes with the original definition."
                      "The later definition will be used".format(atomType.name), fatal=False)
            else:
                newAtomTypes.append(atomType)
        newAtomTypes.extend(anotherFF.atomTypes)
        self.atomTypes = newAtomTypes

        oldComponents = [self.pairwiseTypes, self.bondTypes, self.angleTypes, self.dihedralTypes,
                         self.improperTypes, self.manyBodyTypes]
        newComponents = [anotherFF.pairwiseTypes, anotherFF.bondTypes, anotherFF.angleTypes, anotherFF.dihedralTypes,
                         anotherFF.improperTypes, anotherFF.manyBodyTypes]
        for oldC, newC in zip(oldComponents,newComponents):
            oldC.extend(newC)
        self.Finalize() # 非常重要！
        return True

    def Show(self):
        groups = [self.atomTypes, self.pairwiseTypes, self.bondTypes, self.angleTypes,
                 self.dihedralTypes, self.improperTypes, self.manyBodyTypes]
        groupNames = "ATOMS PAIRWISE BONDS ANGLES DIHEDRALS IMPROPERS MANYBODIES".split()
        for i,group in enumerate(groups):
            output("{} items in group {}:".format(len(group),groupNames[i]))
            for item in group:
                item.WriteParameter(numbered=False)
