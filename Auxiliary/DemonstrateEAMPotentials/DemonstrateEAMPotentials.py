import matplotlib.pyplot as plt
import matplotlib as mpl

def ReadEAM(EAMFile):
    lines = None
    with open(EAMFile,"r") as file:
        lines = file.readlines()
    # EAM势能函数文件具有所谓的 DYNAMO funcfl文件格式
    # 第一行为Comment， 例如
    # DATE: 2007-06-11 UNITS: metal CONTRIBUTOR: Unknown CITATION: Adams et al, J Mater Res, 4, 102 (1989)
    # COMMENT: Cu functions (universal 4) - JB Adams et al J. Mater. Res., 4(1), 102 (1989)
    # 第二行为 原子序号 原子量 LatticeConstant LatticeType，例如：
    # 29     63.550         3.6150    FCC
    # 第三行为 Nrho, drho, Nr, dr, cutoff; rho指电子密度（arbitrary unit）, r指距离，单位为Angstrom；Cutoff针对的是r
    AtomicNumber, Mass, LA, LT = lines[1].strip().split()
    print("Atomic Number: {}; Mass = {}; Lattice Constant = {}, Lattice Type = {}".format(AtomicNumber,Mass,LA,LT))
    words = lines[2].strip().split()
    Nrho, drho, Nr, dr, cutoff = [int(words[0]),float(words[1]),int(words[2]),float(words[3]),float(words[4])]
    # 第一个大块是 F_alpha(rho)的函数形式，即embedding function，共有 Nrho 个数据，分布在多行
    # 第二个大块是 phi_alpha_beta(r)的函数形式，即effective charge，共有 Nr 个数据，分布在多行
    # 第三个大块是 rho_beta(r)的函数形式，即density function，共有 Nr 个数据，分布在多行
    F_alpha = []
    phi_alpha_beta = []
    rho_beta = []
    # 分三个stage，依次读入三个大块
    write_desinations = [F_alpha, phi_alpha_beta, rho_beta]
    lineno = 3
    for stage in range(3):
        destination = write_desinations[stage]
        while lineno < len(lines):
            numbers = [float(n) for n in lines[lineno].strip().split()]
            lineno += 1
            destination.extend(numbers)
            if len(destination) >= Nrho:
                break
    # for i in range(3):
    #     print(len(write_desinations[i]))

    # 画图
    fig = plt.figure(figsize=(18,6))
    ax = fig.add_subplot(131)
    x = [i*drho for i in range(Nrho)]
    ax.plot(x,F_alpha,label=r"$F_{\alpha}(\rho)$",color='k')
    ax.grid(zorder=100)
    ax.legend()
    ax.set_xlim(0, None)

    ax2 = fig.add_subplot(132)
    x2 = [i*dr for i in range(Nrho)]
    ax2.plot(x2,phi_alpha_beta,label=r"$\phi_{\alpha\beta}(r)$",color='k')
    ax2.plot(x2,rho_beta, label=r"$\rho_{\beta}(r)$", color='r')
    ax2.grid(zorder=100)
    ax2.legend()
    ax2.set_xlim(0,None)

    ax3 = fig.add_subplot(133)
    ax3.plot(x2,phi_alpha_beta,label=r"$\phi_{\alpha\beta}(r)$",color='k')
    ax3.plot(x2,rho_beta, label=r"$\rho_{\beta}(r)$", color='r')
    ax3.grid(zorder=100)
    ax3.legend()
    ax3.set_xlim(0,None)
    ax3.set_ylim(0,Nrho*drho)

    plt.show()

def ReadEAMAlloy(EAMFile):
    lines = None
    with open(EAMFile,"r") as file:
        lines = file.readlines()
    lineno = 0
    # EAM/alloy 势能函数文件具有所谓的 DYNAMO setfl文件格式
    # 前三行均为Comment？
    # 第四行为元素个数，及每种元素的符号，如：
    # 3   Ni  Al  H
    elements = []
    for lineno in range(10):
        words = lines[lineno].strip().split()
        try:
            Nelement = int(words[0])
            assert(Nelement == len(words)-1)
            elements = words[1:]
            lineno += 1
            break
        except:
            continue
    print(elements)
    # 第五行为 Nrho, drho, Nr, dr, cutoff; 意义同EAM。所有元素均相同
    words = lines[lineno].strip().split()
    Nrho, drho, Nr, dr, cutoff = [int(words[0]), float(words[1]), int(words[2]), float(words[3]), float(words[4])]
    # 第六行开始，分别给出每种元素的参数。对于每种元素，第一行为 原子序号 原子量 LatticeConstant LatticeType，例如：
    # 29     63.550         3.6150    FCC
    # 随后是  F_alpha(rho)，rho_beta(r)这两个大块
    fig = plt.figure()
    lineno += 1
    for iElement,element in enumerate(elements):
        AtomicNumber, Mass, LA, LT = lines[lineno].strip().split()
        print("Atomic Number: {}; Mass = {}; Lattice Constant = {}, Lattice Type = {}".format(AtomicNumber, Mass, LA, LT))
        lineno += 1
        F_alpha = []
        phi_alpha_beta = []
        rho_beta = []

        # 分两个stage，依次读入两个大块
        write_desinations = [F_alpha, rho_beta]
        for stage in range(2):
            destination = write_desinations[stage]
            while lineno < len(lines):
                numbers = [float(n) for n in lines[lineno].strip().split()]
                lineno += 1
                destination.extend(numbers)
                if len(destination) >= Nrho:
                    break

        # 画图
        ax = fig.add_subplot(len(elements),2,(iElement)*2+1)
        x = [i * drho for i in range(Nrho)]

        ax.plot(x, F_alpha, label=r"$F_{\alpha}(\rho)$", color='k')
        ax.grid(zorder=100)
        ax.legend()
        ax.set_xlim(0, None)
        ax.set_title("{}".format(element))

        ax2 = fig.add_subplot(len(elements),2,(iElement)*2+2)
        x2 = [i * dr for i in range(Nrho)]
        ax2.plot(x2, rho_beta, label=r"$\rho_{\beta}(r)$", color='r')
        ax2.grid(zorder=100)
        ax2.legend()
        ax2.set_xlim(0, None)

    plt.subplots_adjust(hspace=0.4)
    plt.show()

    # 然后是每两种元素之间的phi_alpha_beta。顺序是1-1，2-2，2-2，3-1，3-2，。。。即逐行扫描一个下三角矩阵的顺序
    NElements = len(elements)
    fig = plt.figure()
    x = [i * drho for i in range(Nrho)]
    for I in range(NElements):
        for J in range(I+1):
            phi_alpha_beta = []
            while lineno < len(lines):
                numbers = [float(n) for n in lines[lineno].strip().split()]
                lineno += 1
                phi_alpha_beta.extend(numbers)
                if len(phi_alpha_beta) >= Nrho:
                    break
            ax = fig.add_subplot(NElements, NElements, I*NElements + J + 1)
            ax.plot(x, phi_alpha_beta, label=r"$\phi_{\alpha_\beta}(r)$", color='k')
            ax.grid(zorder=100)
            ax.legend()
            ax.set_xlim(0, None)
            ax.set_title("{}-{}".format(elements[I],elements[J]))
    plt.show()

if __name__ == "__main__":
    #ReadEAM("Cu_u6.eam")
    ReadEAMAlloy("NiAlH_jea.eam.alloy")