from  UniversalMolecularSystem import *
import Utility
import math
from LAMMPSDATAFile import *
from MolecularManipulation import *


def __ReadAFrame__(contents:[str], NAtomsShouldBeThere:int,  serialToIndexMap:{},boundary):
    # 建立一个临时的Trajectory数据结构，用来记录此Frame的信息。
    trajectory = Trajectory()
    ts = int(contents[1].strip()) # 第一行记录的是timestep。核对用。
    trajectory.timesteps_of_each_frame = [ts]
    def _skip_to(flag:str, line_no:int):
        while line_no < len(contents):
            line = contents[line_no]
            if line.startswith(flag):
                return line_no
            else:
                line_no += 1

    line_no = _skip_to('ITEM: NUMBER OF ATOMS', 0) + 1

    NAtomsInThisFrame = int(contents[line_no].strip())

    if NAtomsInThisFrame != NAtomsShouldBeThere:
        error("NAtoms in frame {} with timestep {} is different from the rest!".format(trajectory.Nframes, timestep),False)
        error("{} atoms in this framehere, while others have {} atoms".format(NAtomsInThisFrame, trajectory.NAtoms),False)

    line_no = _skip_to('ITEM: ATOMS', line_no)
    line = contents[line_no]
    parts = line[12:].strip().split()

    # column number of the following properties, starting from 1
    def _index_of_keyword(key):
        return parts.index(key) if key in parts else -1

    idcol = _index_of_keyword('id')
    xcol = _index_of_keyword('x')
    ycol = _index_of_keyword('y')
    zcol = _index_of_keyword('z')
    vxcol = _index_of_keyword('vx')
    vycol = _index_of_keyword('vy')
    vzcol = _index_of_keyword('vz')
    fxcol = _index_of_keyword('fx')
    fycol = _index_of_keyword('fy')
    fzcol = _index_of_keyword('fz')
    ixcol = _index_of_keyword('ix')
    iycol = _index_of_keyword('iy')
    izcol = _index_of_keyword('iz')

    ifVelocity = False if (vxcol == -1 or vycol == -1 or vzcol == -1) else True
    ifForce = False if (fxcol == -1 or fycol == -1 or fzcol == -1) else True

    # The dump file must at least include id and x,y,z
    if idcol == -1 or xcol == -1 or ycol == -1 or zcol == -1:
        error("The DUMP file must at least include atom id and x,y,z", False)
        return False

    list_ids = ["" for _ in range(NAtomsInThisFrame)]
    list_xyzs = np.zeros((NAtomsInThisFrame, 3))
    list_velocities = np.zeros((NAtomsInThisFrame, 3))
    list_forces = np.zeros((NAtomsInThisFrame, 3))

    for i in range(NAtomsInThisFrame):
        line_no += 1

        parts = contents[line_no].strip().split()
        id = parts[idcol]
        list_ids[i] = id

        list_xyzs[i][0], list_xyzs[i][1], list_xyzs[i][2] = \
            [float(parts[xcol]), float(parts[ycol]), float(parts[zcol])]

        if ixcol != -1:
            list_xyzs[i][0] += int(parts[ixcol]) * boundary[0][0]
        if iycol != -1:
            list_xyzs[i][1] += int(parts[iycol]) * boundary[1][1]
        if izcol != -1:
            list_xyzs[i][2] += int(parts[izcol]) * boundary[2][2]

        if ifVelocity:
            list_velocities[i][0], list_velocities[i][1], list_velocities[i][2] = \
                [float(parts[vxcol]), float(parts[vycol]), float(parts[vzcol])]

        if ifForce:
            list_forces[i][0], list_forces[i][1], list_forces[i][2] = \
                [float(parts[fxcol]), float(parts[fycol]), float(parts[fzcol])]

    # Now we create the DATA Structure
    array_xyzs = np.zeros((NAtomsInThisFrame, 3))
    array_velocities = np.zeros((NAtomsInThisFrame, 3)) if ifVelocity else None
    array_forces = np.zeros((NAtomsInThisFrame, 3)) if ifForce else None

    for indexInFile, serial in enumerate(list_ids):
        position = serialToIndexMap[serial]
        array_xyzs[position, :] = list_xyzs[indexInFile]
        if ifVelocity:
            array_velocities[position, :] = list_velocities[indexInFile]
        if ifForce:
            array_forces[position, :] = list_forces[indexInFile]

    trajectory.positions = [array_xyzs]
    trajectory.velocities = [array_velocities]
    trajectory.forces = [array_forces]
    trajectory.NFrames += 1
    return trajectory

class LAMMPSDUMPFile(MolecularFile):
    def __init__(self):
        pass

    def __BeforeReadingFirstFrame__(self, trajectory: Trajectory, contents):
        # 读入第一个Frame前要执行的操作。主要是为了对trajectory对象进行初始化。并设置其中的若干数据结构
        # 如果trajectory中已经有frame信息，此函数直接退出
        if trajectory.NFrames > 0:
            return
        NAtomsInThisFrame = int(contents[3].strip())  # 第3行记录原子数
        trajectory.NAtoms = NAtomsInThisFrame

        lineno = 4
        while lineno < len(contents):
            if contents[lineno].startswith("ITEM: ATOMS"):
                break
            else:
                lineno += 1
        parts = contents[lineno][12:].strip().split()  # 此行的格式例如为：ITEM: ATOMS id mol type x y z vx vy vz，给出了以后每个字段的意义。

        def _index_of_keyword(key):
            return parts.index(key) if key in parts else -1

        idcol = _index_of_keyword('id')  # id关键字出现在第几列。例如在上面的例子中，id就是第一列，序号0
        # 以下需要顺序读一遍，详细记录哪些原子出现了。由于体系中不是所有原子都会在Trajectory中出现（有些原子是固定位置的，没有dump）
        # 因此以下记录哪些原子在Trajectory文件中出现了。Traj文件中的id字段记录的就是原子在体系中的systemwideSerial。
        list_of_ids = [-1 for _ in range(NAtomsInThisFrame)]
        for i in range(NAtomsInThisFrame):
            lineno += 1
            parts = contents[lineno].strip().split()
            id = parts[idcol]
            list_of_ids[i] = int(id)
        list_of_ids.sort()  # 按照原子的serial排序。
        # trajectory.index_to_serial 这个数组记录的是，Traj中出现的每个原子在原来的system中的序列号（从1开始的）
        # 而trajectory.serial_to_index_map这个map记录的是system中任意序列号的原子，是否在Traj中出现，以及如果出现的话，出现的顺序。
        # 比如，原system中有5个原子，serial分别为1，2，3，4，5.现在只有2，5号原子出现在Trajectory中，那么
        # trajectory.index_to_serial == ["2", "5"], 而
        # trajectory.serial_to_index_map == { “2”：0， “5”：1 }。而没有在Trajectory中出现的原子，序号就不在trajectory.serial_to_index_map的键值中。
        trajectory.index_to_serial = [""] * NAtomsInThisFrame
        for index, serial in enumerate(list_of_ids):
            trajectory.serial_to_index_map[str(serial)] = index  # 这里的index指的是它在frame中出现的原子里的顺序
            trajectory.index_to_serial[index] = str(serial)

    def Read(self, trajectory: Trajectory, filename: str, max_workers = -1,
             maxFrames=999999999, every=1, flushSameTimestep=True,certainFrames=None):
        # max_workers为并行计算的进程数。如果<0，则由系统分配，=1为串行，>1为执行用户指定的进程数。
        # every: if every > 1, skip frames between every N steps.
        # flushSameTimestep: if TRUE, old frame will be discarded if the same timestep appears.
        # certainFrames 指的是只读timestep等于这些指定值的帧。此参数具有比every更高的优先级。如果不为None，则只读指定的帧。certainFrames 必须是一个int的list或set！

        if trajectory.parentMolecularSystem == None or len(trajectory.parentMolecularSystem.molecules) == 0:
            error("We don't allow a LAMMPSDUMPFile to be read alone. The caller should construct a ", False)
            error("MolecularStructure at first by reading a LAMMPS DATA file first, then call ", False)
            error("molSys.ReadTrajectory() from that MolecularStructure object instead.", False)
            return False

        FileContentsOfEachFrame = []  # contents 用于记录文件的内容。它是一个字符串数组的数组，每一个元素对应文件中一个Frame的内容。在
        # 读取文件时，通过关键字“ITEM: TIMESTEP”来确定这是一个新的frame。通过它下面的那一行字来确定此frame对应的timestep。
        TimesStepOfEachFrame = []  # TimesStepOfEachFrame 用于记录每Frame后面显示的timestep。
        file = None
        try:
            file = open(filename, 'r')
        except:
            error("Can't open LAMMPS DUMP file [{}]".format(filename), False)
            return False
        import time
        start = time.time()
        sys.stdout.write("Reading LAMMPSDUMP file [{}] into memory...".format(filename))
        for line in file:
            if line.startswith("ITEM: TIMESTEP"):  # 新加入一个frame。
                FileContentsOfEachFrame.append([line])
            else:  # 必然是属于某一个frame的，contents必然至少包括一个元素，即上次读到"ITEM: TIMESTEP"时，新建的那一个frame。
                FileContentsOfEachFrame[-1].append(line)
        end = time.time()
        sys.stdout.write(
            " Done in {:.2}s. This file contains {} frames.\n".format(end - start, len(FileContentsOfEachFrame)))
        file.close()
        NFramesInThisFile = len(FileContentsOfEachFrame)
        # 看一下文件中每个Frame后面的timestep是多少
        for i in range(NFramesInThisFile):
            timestep = int(FileContentsOfEachFrame[i][1].strip())
            TimesStepOfEachFrame.append(timestep)

        # 执行在读入第一个Frame之前的必要操作。如果Trajectory已经有Frame了，此函数会自动返回，什么也不做。
        self.__BeforeReadingFirstFrame__(trajectory, FileContentsOfEachFrame[0])

        # 以下决定要读入哪些Frames
        # 判断的规则按优先级高低为：
        # 1.如果certainFrames不为空，则只读timestep等于这些指定值时候的Frames
        # 2.如果certainFrames为空且every > 1, 则每隔every步读一个frame，但是读入的总Frame数不超过maxFrames
        # 3.如果certainFrames为空且every == 1，则读入所有Frames，但是读入的总Frame数不超过maxFrames
        IndexesOfFramesToRead = []
        if certainFrames != None:
            for iFrame in range(NFramesInThisFile):
                if TimesStepOfEachFrame[iFrame] in certainFrames:
                    IndexesOfFramesToRead.append(iFrame)
        else:
            for iFrame in range(0, NFramesInThisFile, every):
                IndexesOfFramesToRead.append(iFrame)
                if len(IndexesOfFramesToRead) == maxFrames:
                    break
        # for i in IndexesOfFramesToRead:
        #     print(TimesStepOfEachFrame[i])

        # 再过一遍马上要读的Frames。如果之前的Trajectory中包含了这次将要读到的Frame，且有要求的话，将之前读到的Frames，重复的部分删掉：
        for i, t in enumerate(trajectory.timesteps_of_each_frame):
            for timestep_to_read in [TimesStepOfEachFrame[iFrame] for iFrame in IndexesOfFramesToRead]:
                if t == timestep_to_read and flushSameTimestep:
                    print("Duplicate Frame Found @ {} timestep {}".format(i, t))
                    # 如果发现重复出现的timestep,则丢弃(之前读到的)该timestep之后所有的frames。
                    for iFrame in range(len(trajectory.timesteps_of_each_frame)-1, i-1, -1):
                        # print(iFrame)
                        trajectory.DropFrame(iFrame)

        # 以下执行真正的读入操作，该操作可以实现并行。
        AllFramesReadFromFile = []
        if max_workers == 1: # 串行
            for i,iFrame in enumerate(IndexesOfFramesToRead):
                readFrame = __ReadAFrame__(FileContentsOfEachFrame[iFrame], trajectory.NAtoms, trajectory.serial_to_index_map, trajectory.parentMolecularSystem.boundary)
                ProgressBar((i+1)/len(IndexesOfFramesToRead))
                AllFramesReadFromFile.append(readFrame)
        else:
            from multiprocessing import Process
            from concurrent.futures import ProcessPoolExecutor
            with ProcessPoolExecutor(max_workers=None if max_workers<0 else max_workers) as pool:
                futures = []
                for iFrame in IndexesOfFramesToRead:
                    f = pool.submit(__ReadAFrame__,FileContentsOfEachFrame[iFrame],trajectory.NAtoms,trajectory.serial_to_index_map, trajectory.parentMolecularSystem.boundary)
                    futures.append(f)
                for f in futures:
                    AllFramesReadFromFile.append(f.result())

        # 结束后检查一下读到的frames与指定的frames是否一致
        for iIndex, iFrame in enumerate(IndexesOfFramesToRead):
            # 核对一下读到的frame的timestep信息与指定的timestep信息是否一致
            readTimestep = AllFramesReadFromFile[iIndex].timesteps_of_each_frame[0]
            specifiedTimestep = TimesStepOfEachFrame[iFrame]

            if readTimestep != specifiedTimestep:
                error("Timestep in read frame [{}] different from specified timestep [{}].".format(readTimestep,specifiedTimestep))

        # 以下将读到的Frames信息写到Trajectory中
        import time
        start = time.time()
        for frame in AllFramesReadFromFile:
            trajectory.timesteps_of_each_frame.append(frame.timesteps_of_each_frame[0])
            trajectory.positions.append(frame.positions[0])
            trajectory.velocities.append(frame.velocities[0])
            trajectory.forces.append(frame.forces[0])
            trajectory.NFrames += 1
        end = time.time()
        # print("Writing Info into Array takes {}s".format(end-start))
        # print(trajectory.timesteps_of_each_frame)

        return True

