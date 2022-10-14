# 此函数部分定义了分子动力学的经典力场
# 一个完整的经典力场包含三个部分：
# 1. 关于原子类型的定义及识别规则
# 2. 力场参数，包括力场的函数形式，原子类型（含电荷、质量），pairwise参数，
# 键类型，键角类型，二面角类型，非正常二面角类型，多体作用类型等；
# 3. 分子体系中含有的所有原子，键，键角，二面角，多体作用等及它们对应的力场类型

# 此模块实现的是第1部分，定义类 AtomTypeRecognition 来实现原子力场类型的自动识别
# 识别的方法完全基于原子间的成键情况。需要一个原子类型描述文件，文件的格式见
# ./DATA/Forcefields/ExampleAtomTypes.txt

from Utility import *
import itertools

def __TestStringMatchingWithWildcards__():
    # 以上函数的单元测试函数。内部使用。
    patterns = ["*","Cl","C*","[ SPE& | SPC*| SPE]","ar*"]
    objStrings = ["Cl","C","ab","SPC.5","S","SPE5","SPE","SPE&","spE","archive","&*"]
    for p in patterns:
        for o in objStrings:
            print("{} - {} : {}".format(p, o, __matching__(p, o)))

class PatternTreeNode:
    element: str # 元素。可以用通配符，[A|B|C] 表示A或B或C。也可使用A*表示字符串的部分匹配（不支持*A的表达式),见上面的函数
    type: str # 力场。规则同上
    children: [] # 子节点
    def __init__(self,element,type):
        self.element = element
        self.type = type
        self.children = None
        # self.children == None时，表示规则没有指定它的下级节点情况，可以匹配。如果children不为None，那么在匹配时，待匹配对象的children
        # 个数必须和规则中的children个数一样（包括0个时）

    def NodeMatch(self,objectNode,debugging=False,level=0):
        # 节点匹配。以自身节点作为模式，查看objectNode是否符合自身所定义的模式。注：objectNode可能含有更深的子节点层数，
        # 如果self.children == None, 只要self本身能和objectNode的同一层级节点匹配上，就算成功
        # 如果self.children != None，则节点本身和所有子节点必须都要能匹配上。
        leading = "   |   " * level + "—" if level > 0 else "+"
        if not MatchingWithWildcards(self.element, objectNode.element) or \
           not MatchingWithWildcards(self.type, objectNode.type):
            if debugging:
                output("{}{} != {}".format(leading,self,objectNode))
            return False
        if debugging:
            output("{}{} == {}".format(leading, self, objectNode))

        # 情况1: self本身的children==None，则不执行更深层次的检查
        if self.children == None:   #
            return True
        NChildren = len(self.children)
        # 情况2：self本身的NChildren==0，即要求是端点原子，那么目标原子也必须是端点原子：
        if NChildren == 0:
            if objectNode.children == None or len(objectNode.children)==0:
                return True
            else:
                return False
        # 情况3： self本身的NChildren!=0，即要求目标原子的Nchildren与之相等
        else:
            if objectNode.children == None or len(objectNode.children) != NChildren:
                return False
        # 情况4：经过以上判断，规则原子与目标原子均有非零（且相等）个数的子节点。因此需按所有可能的组合逐一判断
        permutations = itertools.permutations(objectNode.children)
        import math
        NPerm = math.factorial(len(objectNode.children))
        for iPerm,perm in enumerate(permutations):
            found_a_match = True
            if debugging:
                output("{}Testing {} out of {} permutations...".format(leading,iPerm+1,NPerm))
            for i in range(NChildren):
                flag = self.children[i].NodeMatch(perm[i],debugging,level+1)
                if not flag:
                    found_a_match = False
                    break
            if found_a_match:
                if debugging:
                    output("{}Found at least one matching permutation.".format(leading))
                return True

    def Show(self,level=0,collapsed=True):
        if collapsed:
            str = "{}".format(self)
            if self.children != None:
                str += " {"
                for c in self.children:
                    str += c.Show(level+1,collapsed) + " "
                str += "}"
            return str
        else:
            leading = " | "*level + "—" if level>0 else "+"
            output("{}{}".format(leading,self))
            if self.children == None:
                return
            for c in self.children:
                c.Show(level+1,collapsed)
    def __str__(self):
        return "{}:{}".format(self.element,self.type)

class PatternTree:
    root : PatternTreeNode # 根节点
    def __init__(self):
        self.root = None

    def Show(self,collapsed):
        return self.root.Show(0,collapsed)

    def ConstructFromString(self,line):
        # 从一行字符串描述中构建节点.这行字符串的格式见./UnitTests/TestForcefield/ForcefieldAtomType.txt中的说明。例如：
        # C:R2-C= {C{* *} C{* * *} C{* * *}}
        # 这里使用了栈(利用deque来实现)来实现树形结构的构建。随时维护一个栈顶节点。当读到普通节点时，把它加入到栈顶节点的子节点中；
        # 当读到{时，将最后一个读到的节点入栈。当读到}时，栈顶节点出栈；读到其它符号则继续跳过。
        line = RemoveComment(line).strip().rstrip()

        if len(line) == 0:
            return False

        from collections import deque
        nodeStack = deque()
        start = 0
        stackEmpty = False  # 用于额外的检测，防止}多于{，导致对空栈进行pop()操作
        lastReadNode = None  # 最后一个构建的节点
        def SetupNewNode(line,start,end):
            # 内嵌辅助函数，通过字符串的 line[start:end] 部分来构建一个不含子节点的树节点。只使用了一次。目的是防止嵌套过深。
            field = line[start:end]
            if field.upper() == "*TERMINAL*":
                return None
            if field.find(":") != -1:
                [name, type] = field.split(":")
            else:
                name = field
                type = '*'
            newNode = PatternTreeNode(name, type)
            return newNode
        for end in range(len(line)):
            if line[end] in [' ','{','}'] and end-start > 0:
                lastReadNode = SetupNewNode(line,start,end)
                if lastReadNode == None:
                    x = 3+2
                # 如果此时栈是空的，说明读入的是root节点，它不是任何节点的子节点。否则不是root节点，它应该加入到栈顶节点的子节点list中
                if self.root == None:
                    assert(len(nodeStack)==0)
                    self.root = lastReadNode
                else:
                    if nodeStack[-1].children == None:
                        nodeStack[-1].children = []
                    if lastReadNode != None:
                        nodeStack[-1].children.append(lastReadNode)
                    # nodeStack[-1] 就是栈顶元素
                # 这里的 start=end 跳过了所读到的（用于构建节点的）一串字符。不是start=end+1的原因是line[end]已经不是这串字符的一部分，
                # 而是它后面的' ','{',或'}'字符。
                start = end
            if line[end] == '{':
                # 入栈操作。这里的 start = end+1 是为了字符串处理时，"跳过"这个{字符。下面几处也相同。
                start = end+1
                nodeStack.append(lastReadNode)
            elif line[end] == '}':
                start = end+1
                # 出栈操作。这里为了防止对空栈进行pop()操作，进行了额外判断。发现错误则设置错误代码。
                if len(nodeStack) > 0:
                    nodeStack.pop()
                else:
                    stackEmpty = True
                    break
            elif line[end] == ' ':
                start = end+1
            else:
                pass
        # 最后读完字符串，栈应该正好为空。这里做一下检测。如果不是正好为空（或者之前出现了空栈pop），说明输入的字符串中{}不匹配。提示错误
        if stackEmpty or len(nodeStack) > 0:
            error("In PatternNodeTree::ConstructFromString(): "
            "Unmatched brackets in line:\n\"{}\"".format(line))
        else:
            return True

    def ConstructFromMolecule(self,molecule,iAtom,bondedMap,maxDepth=3):
        # 该函数针对一个Molecule，对其中的第iAtom个原子构建一个PatternTree。
        # 需要提供这个分子的bondedMap（可通过Molecule::BondedMap）获取。为效率原因，本函数不主动调用此函数，否则可能会重复调用。
        # maxDepth是搜索的最大深度，必要性取决于依据成键情况判断原子类型时，需要看相距多远的间接相连原子。maxDepth=0为原子本身，
        # =1为直接相连的，=2间接相连，=3次间接相连，以此类推。一般maxDepth=3已足够。
        # 本算法不执行循环检测，因此对于含有环（特别是小环）的分子中，某个原子可能会出现在生成的树的同一层中的多个位置。但这正是期望的结果。
        # 本算法利用一个队列（First in first out）,实现广度优先搜索 (BFS)。
        from collections import deque
        queue = deque()
        #visited = [False for _ in range(len(molecule.atoms))]
        # 在当前BFS搜索过程，每个节点的直接上级（随搜索的进行，这个状态可能会改变，因为该算法不执行循环检测，一个节点可能出现在树的多个位置）
        parentID = [-1 for _ in range(len(molecule.atoms))]
        def SetupNodeFromAtom(atom):
            type = atom.type if atom.type!=None else ""
            return PatternTreeNode(atom.element,type)
        # 每次将一个新的节点，这个节点对应的原子序号，搜索深度加入到队列中。首先加入的是目标原子本身。
        self.root = SetupNodeFromAtom(molecule.atoms[iAtom])
        queue.append((self.root,iAtom,0))
        #visited[] = True
        parentID[iAtom] = iAtom  # parentID == self的节点是root
        # 执行BFS
        while len(queue) > 0:
            topNode, atomIndex, depth = queue.popleft()
            for childIndex in bondedMap[atomIndex]:
                # if visited[childIndex]:
                #     continue
                if childIndex == parentID[atomIndex]:
                    continue
                childNode = SetupNodeFromAtom(molecule.atoms[childIndex])
                if topNode.children == None:
                    topNode.children = []
                topNode.children.append(childNode)
                #visited[childIndex] = True
                parentID[childIndex] = atomIndex
                if depth < maxDepth:
                    queue.append((childNode,childIndex,depth+1))

    def Match(self,objectTree,debugging=False):
        return self.root.NodeMatch(objectTree.root,debugging)

    def __TestConstructFromString__(self):
        line = "C:fancy{C{* *}C{X:M * {X:M Y:Z} *}C{* * *{A:B C:D E:F{1{2{3{5 {6{7 8 9{10}}}} 4}}}}}}"
        self.ConstructFromString(line)
        self.root.Show()
    def __TestConstructFromMolecule__(self,moleculeFileInXYZ,index):
        from UniversalMolecularSystem import MolecularSystem
        from MOL2File import MOL2File
        from XYZFile import XYZFile
        from BondDetection import DefaultBondRules
        import sys
        ms = MolecularSystem()
        reader = XYZFile()
        writer = MOL2File()
        ms.Read(reader,moleculeFileInXYZ)
        ms.AutoDetectBonds(DefaultBondRules())
        ms.Summary()
        mol = ms.molecules[0]
        bondedTo = mol.BondedMap()
        self.ConstructFromMolecule(ms.molecules[0],index,bondedTo,maxDepth=10)
        self.Show()
        dumpfile = open("dump.mol2","w")
        output.setoutput(dumpfile)
        ms.Write(writer)
        output.setoutput(sys.stdout)
        dumpfile.close()

        from VMDInterface import VMDInterface
        vmd = VMDInterface("dump.mol2",autobonds=False)
        for i in range(len(mol.atoms)):
            vmd.AddCommand("label add Atoms 0/{}".format(i))
            vmd.AddCommand("label textformat Atoms {} {{%i}}".format(i))
            vmd.AddCommand("label textoffset Atoms {} {{ 0.03 0.03 0.03 }}".format(i))
        #vmd.Run()

class AtomTypeRecognition:
    rules: [PatternTree]
    def __init__(self,rulefile):
        self.rules = []
        lines = None
        with open(rulefile,"r",encoding='utf-8') as rules:
            lines = rules.readlines()
        for line in lines:
            newRule = PatternTree()
            result = newRule.ConstructFromString(line)
            if result:
                self.rules.append(newRule)

    def __Match_One_Rule_To_One_Atom__(self,rule, pattern, debugging):
        # 用一条规则与一个原子相匹配。如果成功，返回原子的类型。如果失败，返回None
        # 不会写入原子信息（因为参数没有给Atom对象）
        # 匹配之前，要先把rule中的type名称改为*，判断完后再改回来。因为原子本身的类型开始是不知道的(None或"")，不改的话就一定匹配不上。
        if debugging:
            output("Matching Rule:")
            output(rule.Show(collapsed=True))
            output("Pattern in Atom:")
            output(pattern.Show(collapsed=True))
        type = rule.root.type
        rule.root.type = "*"
        flag = rule.Match(pattern, debugging)
        rule.root.type = type
        if flag == True:
            return type
        else:
            return None

    def __Match_All_Rules_To_One_Atom__(self, patternInAtom, debugging=False):
        # 用所有规则与一个原子相匹配。如果成功，返回原子的类型。如果失败，返回None
        # 不会写入原子信息（因为参数没有给Atom对象）
        # 成功的话，返回匹配到的原子类型。失败返回None
        # 本函数依次查找所有可用的规则，如果给的规则中有多条可以和原子匹配，以后出现的为准。
        # 因此，请把高优先级的规则放在后面。
        result = None
        for rule in self.rules:
            newResult = self.__Match_One_Rule_To_One_Atom__(rule, patternInAtom, debugging)
            if newResult != None:
                result = newResult
        return result

    def __RecognizeOneAtomToOneRule_ForDebugging__(self,molecule,iRule,iAtom,maxDepth=3,debugging=True):
        bondedMap = molecule.BondedMap()
        patternOfAtom = PatternTree()
        patternOfAtom.ConstructFromMolecule(molecule,iAtom,bondedMap,maxDepth)
        result = self.__Match_One_Rule_To_One_Atom__(self.rules[iRule],patternOfAtom,debugging=debugging)
        if debugging:
            output("The final type is \"{}\"".format(result))
        return result

    def RecognizeAllAtoms(self,molecule,maxDepth=3,maxIterations=5,debugging=False):
        bondedMap = molecule.BondedMap()
        NAtoms = len(molecule.atoms)
        if debugging:
            output("Matching {} atoms to {} possible atom types".format(NAtoms,len(self.rules)))

        # May need multiple iterations
        for iter in range(maxIterations):
            if debugging:
                output("Iteration {}:".format(iter))
            # 构建原子的类型及成键情况列表。这个工作在每轮迭代时均需重复一次。
            NAtomsWithTypes = 0
            patternOfEachAtom = []
            for iAtom in range(NAtoms):
                pattern = PatternTree()
                pattern.ConstructFromMolecule(molecule, iAtom, bondedMap, maxDepth)
                patternOfEachAtom.append(pattern)
                if molecule.atoms[iAtom].type != None and molecule.atoms[iAtom].type != "":
                    NAtomsWithTypes += 1

            NFoundNewTypesInThisRound = 0
            for iAtom in range(NAtoms):
                if molecule.atoms[iAtom].type!=None and molecule.atoms[iAtom].type!="":
                    continue
                result = self.__Match_All_Rules_To_One_Atom__(patternOfEachAtom[iAtom], debugging=debugging)
                if result != None:
                    molecule.atoms[iAtom].type = result
                    NFoundNewTypesInThisRound += 1
                else:
                    pass

            NAtomsWithTypes += NFoundNewTypesInThisRound
            if NAtomsWithTypes == NAtoms:
                if debugging:
                    output("In AtomTypeRecognition::Recognize(), All {} atoms are assigned atom types.".format(NAtoms))
                return True
            elif NFoundNewTypesInThisRound == 0:
                if debugging:
                    output("In AtomTypeRecognition::Recognize(), "
                        "Only {} out of {} atoms can be assigned atom types.".format(NAtomsWithTypes,NAtoms))
                return False
            else:
                if debugging:
                    output("In AtomTypeRecognition::Recognize(), iteration {} found "
                           "{}/{} types".format(iter,NAtomsWithTypes,NAtoms))
                else:
                    pass

    def Extend(self, anotherATR):
        # 力场整合。指把anotherATR中的 原子种类 加入到此力场中
        # 整合的规则是，
        # 尽量避免原子种类的冲突。如果有冲突，给出提示，以后出现的原子种类定义为准.
        typesInOtherATR = set()
        for rule in anotherATR.rules:
            typesInOtherATR.add(rule.root.type)
        newRules = []
        for rule in self.rules:
            if rule.root.type in typesInOtherATR:
                error("In AtomTypeRecognition()::Extend(), atom type {} clashes with the original definition."
                "The later definition will be used".format(rule.root.type),fatal=False)
            else:
                newRules.append(rule)
        newRules.extend(anotherATR.rules)
        self.rules = newRules
        return True

    def Show(self,collapsed=True):
        for iRule,rule in enumerate(self.rules):
            if collapsed:
                sys.stdout.write("{} : ".format(iRule))
                output(rule.Show(collapsed))
            else:
                sys.stdout.write("{} : ".format(iRule))
                rule.Show(collapsed)
