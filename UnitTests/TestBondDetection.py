import sys

import MolecularDrawer

sys.path.append("../")
from BondDetection import *
from VMDInterface import *
from Utility import *
import os
source = os.path.join(DATAFILESPATH,'Structures','FuchsSandoff.xyz')

def TestBondDetection():
    r = DefaultBondRules()
    ms = MolecularSystem()
    # 第一个系统，正确的单分子体系
    ms.name = "System 1"
    ms.Read(XYZFile(),source)
    ms.AutoDetectBonds(r)
    ms.Summary()

    from MolecularDrawer import Draw2D
    MolecularDrawer.Draw2D(ms)

    # 第二个体系，将System 1 随机拆分成10个小系统
    ms2 = MolecularSystem()
    ms2 = BreakupMoleculeRandomly(ms.molecules[0],10)
    ms2.name = "System 2"
    ms2.interMolecularBonds = []

    # 对第二个体系的随机测试。随机删掉一些分子间和分子内键。重复若干次测试
    def RandDelBonds():
        for m in ms2.molecules:
            import random
            random.shuffle(m.bonds)
            for i in range(random.randint(0,len(m.bonds))):
                del(m.bonds[-1])
        random.shuffle(ms2.interMolecularBonds)
        for i in range(random.randint(0,len(ms2.interMolecularBonds))):
            del(ms2.interMolecularBonds[-1])
    for i in range(20):
        RandDelBonds()
        ms2.AutoDetectBonds(r)
        ms2.Summary()
    ms2.Summary()

    # 第三个体系，将第二个体系再合并成单一分子
    ms3 = ReduceSystemToOneMolecule(ms2)
    ms3.name = "System 3"
    ms3.Summary()
    ms3.RenumberAtomSerials()
    output.setoutput(open('dump.mol2','w'))
    ms3.Write(MOL2File())

    # 最后输出第三个体系并作图
    vmd = VMDInterface("dump.mol2",autobonds=False)
    vmd.Run()


if __name__ == '__main__':
    TestBondDetection()
