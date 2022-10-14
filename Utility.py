# 公共实用程序函数和类。 实现常用常量、数学函数等。
# 此模块应当不依赖程序中的任何其他模块，可以被任何其他的模块import
import math
import sys
import numpy as np
import os

# 定义一些程序中需要的数据文件的路径。此路径依赖于程序所在的目录。
import os
DATAFILESPATH = os.path.join(os.path.dirname(__file__),"Data")
FORCEFIELDSPATH = os.path.join(DATAFILESPATH,"Forcefields")


class PeriodicTable:
    def __init__(self):
        # M is the dummy atom
        self.elements = "M H He "\
        "Li Be B C N O F Ne "\
        "Na Mg Al Si P S Cl Ar "\
        "K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr "\
        "Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe "\
        "Cs Ba La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu Hf Ta W Re Os Ir Pt Au Hg Tl Pb Bi Po At Rn "\
        "Fr Ra Ac Th Pa U Np Pu Am Cm Bk Cf Es Fm Md No Lr Rf Db Sg Bh Hs Mt Ds Rg Uub Uut Uuq Uup Uuh Uus Uuo";
        self.elements = self.elements.split()
        self.atomicweights = {}
        with open(os.path.join(DATAFILESPATH,"atomicweights.csv"),"r") as awfile:
            lines = awfile.readlines()
            for l in lines:
                words = l.strip().split(",")
                ele = words[0].upper()
                weight = float(words[1])
                self.atomicweights[ele] = weight
    
    def AtomicNumberToElement(self,i):
        if i >= len(self.elements):
            i = 0
        return self.elements[i]
    def ElementToAtomicNumber(self,element):
        for i in range(len(self.elements)):
            if element == self.elements[i]:
                return i
        return -1
    def AtomicWeight(self,element:str):
        if element.upper() in self.atomicweights:
            return self.atomicweights[element.upper()]
        else:
            return 0

class ErrorHandler():
    # ErrorHandling 类控制如何输出和处理错误信息
    # 只存在一个名为'error'的ErrorHandling对象。 这里我们使用了“单例(Singleton)”的设计模式
    # 'error' 对象必须被构造一次，且仅被构造一次（这是它被称为Singleton的原因），详情请参考设计模式相关书箱。
    def __init__(self):
        self.outputfile = None
        self.OnOffState = True

    def setoutput(self,outputfile):
        self.outputfile = outputfile

    def __call__(self,message,fatal = True):

        # Warning 可以被关闭。 但致命错误Fatal errors无法被忽略。
        if (not self.OnOffState) and (not fatal):
            return

        message = "Fatal Error: "+message if fatal else "Warning: "+message
        print(message) # output to stdout
        if self.outputfile != None: # and to the outputfile. If no output file is set up, to stdout only
            print(message, file = self.outputfile)
        if fatal:
            quit()

    def turn_on(self):
        self.OnOffState = True

    def turn_off(self):
        self.OnOffState = False

error = ErrorHandler()
# 一个全局错误处理对象（该类的唯一对象）。
# 在 main.py 中，可以调用 error.setoutput() 将错误消息引导到命令行屏幕或某处
# 例如在 GUI 版本中，将错误消息定向到消息框

class OutputHandler():
    def __init__(self):
        self.outputfile = None
        self.OnOffState = True

    def setoutput(self, outputfile):
        self.outputfile = outputfile

    def __call__(self,message):

        if self.OnOffState == False: # Output is turned off
            return

        if self.outputfile != None:
            print(message,file = self.outputfile)
        else:
            print(message)


    def turn_on(self):
        self.OnOffState = True

    def turn_off(self):
        self.OnOffState = False

output = OutputHandler() # A unique and global object, similar as the ErrorHandler()

# Mathematical Functions
def Distance(atom1, atom2):
    return math.sqrt(
        math.pow(atom1.x - atom2.x,2) +
        math.pow(atom1.y - atom2.y,2) +
        math.pow(atom1.z - atom2.z,2)
    )
def VectorAdd(v1,v2):
    result = [v1[i]+v2[i] for i in range(len(v1))]
    return result

def VectorMinus(v1,v2):
    result = [v1[i]-v2[i] for i in range(len(v1))]
    return result

def VectorNorm(v):
    import math
    sum = 0.0
    for x in v:
        sum += math.pow(x,2)
    return math.sqrt(sum)

def VectorNormalize(v):
    return VectorScalarProduct(v, 1.0/VectorNorm(v))

def VectorScalarProduct(v,scale):
    result = [x*scale for x in v]
    return result

def VectorDotProduct(v1,v2):
    sum = 0.0
    for i in range(len(v1)):
        sum += v1[i] * v2[i]
    return sum

def VectorCrossProduct(v1,v2):
    result = [0,0,0]
    result[0] =   v1[1]*v2[2] - v1[2]*v2[1]
    result[1] = - v1[0]*v2[2] + v1[2]*v2[0]
    result[2] =   v1[0]*v2[1] - v1[1]*v2[0]
    return result

def Rotate(coordinates, degree_clockwise, axis):
    rx,ry,rz = VectorNormalize(axis)
    # The rotational matrix was copied from a previous code. I forgot its reference...
    phi = degree_clockwise * math.pi / 180.0
    c = math.cos(phi)
    s = math.sin(phi)
    RMatrix = np.mat(np.zeros((3,3)))
    RMatrix[0,0] = c + (1-c)*rx*rx
    RMatrix[0,1] = (1-c)*rx*ry - rz*s
    RMatrix[0,2] = (1-c)*rx*rz + ry*s
    RMatrix[1,0] = (1-c)*rx*ry + rz*s
    RMatrix[1,1] = c + (1-c)*ry*ry
    RMatrix[1,2] = (1-c)*ry*rz - rx*s
    RMatrix[2,0] = (1-c)*rx*rz - ry*s
    RMatrix[2,1] = (1-c)*ry*rz + rx*s
    RMatrix[2,2] = c+(1-c)*rz*rz
    return coordinates * RMatrix


# String Manipulations
# Note: Due to my lack of knowledge in this field, there may be better ways to implement the following functions,
# for example through regular expressions. Please bear with the clumsiness of these functions. At least they work.

def StringTok(string, token):
    # Finds the first occurrence of the token in the string and split the string into a tuple (first,second) without
    # the given token. For example StringTok("xyz = 543",'=') returns ("xyz" and "543"). (Both parts are with
    # beginning and ending blank spaces striped away. If no such token is found, it returns None.
    pos = string.find(token)
    if pos == -1:
        return None
    else:
        return (string[0:pos].strip(), string[pos + len(token):].strip())

def ProgressBar(percent,length = 50):
    filled = round(length * percent)
    bar = '['+''.join(['#' for i in range(filled)]) + ''.join([' ' for i in range(length-filled)])+']'
    sys.stdout.write('\r{} {:.2f}%'.format(bar,percent*100.0))

def RemoveComment(line):
    # 移除行中注释
    pos = line.find('#')
    if pos != -1:
       line = line[:pos]
    return line

def MatchingWithWildcards(pattern, objString, case_sensitive=False):
    # 带通配符的字符串模式匹配。pattern是模式，objString是待匹配的字段串。
    # 要求pattern与objString的前后均无空格。但模式为[A|B|C]中，中间可以有空格，如[A | B|C ]。
    # 默认大小写无关。也可以要求case sensitive

    # if "461" in pattern:
    #     print(pattern,objString)

    if not case_sensitive:
        pattern = pattern.upper()
        objString = objString.upper()
    # 情况1. 直接可以匹配或模式本身是通配符*
    if pattern == "*" or pattern == objString:
        return True
    # 情况2. 模式是or模式，[A|B|C]，则把字符串分开匹配。由于每个或选项本身又有可能含有通配符，故使用了递归
    elif pattern.startswith("[") and pattern.endswith("]"):
        options = pattern[1:-1].split("|")
        for option in options:
            if __matching__(option.strip().rstrip(), objString):
                return True
        return False
    # 情况3. 模式是A*，那么拿出*之前的部分进行匹配。不支持*A这种模式的匹配
    elif pattern[-1] == "*":
        patternStart = pattern[:-1]
        if objString.startswith(patternStart):
            return True
        else:
            return False
    else:
        return False