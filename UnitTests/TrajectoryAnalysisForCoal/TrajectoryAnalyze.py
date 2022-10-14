import sys
import os
sys.path.append('../../')
#sys.path.append('{}/../'.format(os.path.dirname(__file__)))
from UniversalMolecularSystem import *
from LAMMPSDUMPFile import LAMMPSDUMPFile
from MOL2File import MOL2File
from XYZFile import XYZFile
from Utility import *
import MolecularManipulation
import BondDetection
from LAMMPSDATAFile import LAMMPSDATAFile


def PengRobinsonForCH4(rho,T):   # rho in mol count / nm^3
    import math
    Na = 6.022E23 # /mol
    V = Na/(1E27*rho)  # m^3/mol,  1E27*rho is the mol count per m^3, its inverse is the molar volume.
    Tc = 190.564 # K
    Pc = 45.99E5 # Pa
    w  = 0.011
    R = 8.3145 # J / mol / K
    Tr = T / Tc
    k = 0.37464 + 1.54226 * w - 0.26992 * w * w
    alpha = math.pow((1 + k * (1 - math.sqrt(Tr))),2)
    b = 0.077880 * R * Tc / Pc
    a = 0.45724 * R*R * Tc*Tc * alpha / Pc
    P = R * T / (V - b) - a / (V * (V + b) + b * (V - b))
    return P/1E6   # Pressure as MPa

def Read(master_path,maxFrames=99999999):


    if not master_path.endswith('/'):
        master_path += '/'

    ms = MolecularSystem()
    ms.Read(LAMMPSDATAFile(),master_path+'equil.data')
    ms.Summary()

    counter = 1
    while True:   # Automatically read all dump files found in the folder
        import os
        dump_file_name = master_path+'dump{}.lammpstrj'.format(counter)
        if os.path.isfile(dump_file_name):
            if counter == 1:
                ms.ReadTrajectory(LAMMPSDUMPFile(), dump_file_name, timestep_in_fs= 2.0,maxFrames=maxFrames)
            else:
                ms.trajectory.DropFrame(-1)
                ms.ReadTrajectory(LAMMPSDUMPFile(), dump_file_name,maxFrames=maxFrames)
            counter += 1
        else:
            break

    return ms

def RadialDistribution(ms_with_trj, length, centerY, centerZ, radius, binSize, frames, \
                       tail_beg, tail_end, path, fig, plot_range_in_Angstrom,temperature):
    Nbins = int(math.floor(radius/binSize))
    bins = [0.0 for _ in range(Nbins)]
    volumes = [0 for _ in range(Nbins)]   # the volume of shells
    for ibin in range(Nbins):
        rout = radius - ibin * binSize
        rin = rout - binSize if ibin < Nbins-1 else 0.0
        volumes[ibin] = math.pi * length * ( rout * rout - rin * rin ) / 1000.0 # in unit of nm^3

    for iFrame in frames:
        ms_with_trj.UpdateCoordinatesByTrajectoryFrame(iFrame)
        for mol in ms_with_trj.molecules:
            for a in mol.atoms:
                dist_to_axis = math.sqrt(math.pow(a.y-centerY,2) + math.pow(a.z-centerZ,2))
                dist_to_edge = radius - dist_to_axis
                which_bin = int(math.floor(dist_to_edge/binSize))
                if which_bin >= Nbins:
                    which_bin = -1
                bins[which_bin] += 1.0

    # number in each bin are averaged by NFrames
    for ibin in range(Nbins):
        bins[ibin] /= len(frames)

    totalNumber = int(round(sum(bins)))
    totalVolume = sum(volumes)
    boundNumber = sum(bins[0:int(round(10/binSize))])  # Count of CH4 bound on the surface (< 1.0nm)

    # And further converted to NAtoms/nm^3
    for ibin in range(Nbins):
        bins[ibin] = bins[ibin]/volumes[ibin]

    file = open('{}/{}.csv'.format(path,fig),'w')
    output.setoutput(file)
    for ibin in range(Nbins):
        output('{},{},{},'.format(ibin,ibin*binSize,bins[ibin]))

    tail_range = range(tail_beg,tail_end)
    tail_average = sum(bins[tail_beg:tail_end])/len(tail_range)

    pressure = PengRobinsonForCH4(tail_average,temperature)

    import matplotlib.pyplot as plt
    Npoints = int(math.ceil(plot_range_in_Angstrom/binSize))
    distances = [ i*binSize/10.0 for i in range(Npoints)]   # distance in unit of nm

    plt.figure()
    plt.rcParams['font.family'] = 'Helvetica'
    plt.rcParams['xtick.labelsize'] = 14
    plt.rcParams['ytick.labelsize'] = 14
    plt.plot(distances,bins[0:Npoints],color='black',marker='s',markersize=5,linestyle='solid',linewidth=1)
    #plt.plot([0,Nbins],[ref,ref],color='black',linestyle='dashed',linewidth=2)
    #plt.plot([0,distances[-1]], [tail_average, tail_average], color='black', linestyle='solid', linewidth=2)
    plt.savefig('{}/{}.png'.format(path,fig))
    plt.show()
    plt.close()

    output('total count,volume,density,tail_density,pressure')
    output('{},{},{},{},{}'.format(totalNumber,totalVolume,totalNumber/totalVolume,tail_average,pressure))

    output('bound_mol,percentage')
    output('{},{:.2f}%'.format(boundNumber,100.0*boundNumber/totalNumber))

    file.close()

def MSD(ms_with_trj:MolecularSystem, path, fig):

    NFrames = ms_with_trj.trajectory.NFrames
    timestep = ms_with_trj.trajectory.timestep
    NAtoms = ms_with_trj.trajectory.NAtoms
    times = [ms_with_trj.trajectory.timesteps_of_each_frame[i] * timestep / 1000.0 for i in range(NFrames)] # in unit of ps
    MSD = [0 for _ in range(NFrames)]

    for iFrame in range(NFrames):
        distances = [0 for _ in range(NAtoms)]
        for iAtom in range(NAtoms):
            diff = VectorMinus(ms_with_trj.trajectory.positions[iFrame][iAtom],\
                               ms_with_trj.trajectory.positions[0][iAtom])
            distances[iAtom] = VectorDotProduct(diff,diff)
        MSD[iFrame] = sum(distances[:])/NAtoms  # The unit is  Å^2

    import matplotlib.pyplot as plt

    plt.figure()
    plt.rcParams['font.family'] = 'Helvetica'
    plt.rcParams['xtick.labelsize'] = 14
    plt.rcParams['ytick.labelsize'] = 14
    plt.rcParams['axes.labelsize'] = 14
    plt.xlabel = 'time (ps)'
    plt.ylabel = 'MSD (Å^2)'
    plt.plot(times, MSD, color='black', marker='s', markersize=5, linestyle='solid', linewidth=1)
    plt.savefig('{}/{}.png'.format(path, fig))
    plt.show()
    plt.close()

    file = open('{}/{}.csv'.format(path, fig), 'w')
    output.setoutput(file)
    for i in range(NFrames):
        output("{},{},".format(times[i],MSD[i]))
    file.close()

def AxialDistributionAnalysis(ms_with_trj:MolecularSystem,\
                              selector_methane_C,selector_water_O,\
                              path,figname,binSize,to_plot_this_many_bins_beyond_interface,iFrame):
    Length = ms_with_trj.boundary[0][0]
    Nbins = int(math.floor(Length/binSize))
    import numpy as np
    bins = np.zeros((2,Nbins))

    ms_methane_C = MolecularManipulation.SubSystemByLambdaFunction(ms_with_trj,selector_methane_C)
    ms_water_O = MolecularManipulation.SubSystemByLambdaFunction(ms_with_trj, selector_water_O)

    if iFrame != -1:   # If iFrame == -1, don't update the coordinates, just use the original
        ms_methane_C.UpdateCoordinatesByTrajectoryFrame(iFrame)
        ms_water_O.UpdateCoordinatesByTrajectoryFrame(iFrame)

    def __x_to_ibin__(x):
        ibin = int(math.floor(x/binSize))
        # For out of bounds atoms. Collect them within the box.
        ibin = min(ibin,Nbins-1)
        ibin = max(ibin,0)
        return ibin

    for mol in ms_methane_C.molecules:
        ibin = __x_to_ibin__(mol.atoms[0].x)
        bins[0][ibin] += 1

    for mol in ms_water_O.molecules:
        ibin = __x_to_ibin__(mol.atoms[0].x)
        bins[1][ibin] += 1

    for ibin in range(Nbins):
        total = bins[0][ibin] + bins[1][ibin]
        bins[0][ibin]/=total
        bins[1][ibin]/=total

    # Assuming bins[0] is decreasing and bins[1] is increasing, the point at which these series cross with each other
    # is the phase interface
    pivot = None
    for ibin in range(1,Nbins):
        if bins[0][ibin-1] > bins[1][ibin-1] and bins[0][ibin] < bins[1][ibin]:
            pivot = ibin
            break
    if pivot == None:
        output("Error in AxialDistributionAnalysis(), can't find the phase interface.",False)
        return False

    NPoints = to_plot_this_many_bins_beyond_interface*2+1
    x = np.zeros(NPoints)
    y1 = np.zeros(NPoints)
    y2 = np.zeros(NPoints)
    for i in range(NPoints):
        offset = -to_plot_this_many_bins_beyond_interface+i
        x[i] = offset * binSize * 0.1
        y1[i] = bins[0][pivot+offset]
        y2[i] = bins[1][pivot+offset]
        # Use the log scale
        y1[i] = math.log10(y1[i]) if y1[i] > 1e-10 else -10
        y2[i] = math.log10(y2[i]) if y2[i] > 1e-10 else -10

    import matplotlib.pyplot as plt
    plt.rcParams['font.family'] = 'Helvetica'
    plt.rcParams['xtick.labelsize'] = 14
    plt.rcParams['ytick.labelsize'] = 14
    plt.rcParams['axes.labelsize'] = 14
    fig, ax = plt.subplots()
    ax.plot(x, y1, color='k', marker='s', markersize=5,  markerFaceColor='w', linewidth=0)
    ax.plot(x, y2, color='k', marker='v', markersize=6, markerFaceColor='w', linewidth=0)
 #   ax.set_ylim([-0.05,1.05])
    ax.set_ylim([-2.5, 0.10])
    ax.set_xlim([-5.1, 5.1])


    #plt.show()
    filename = '{}/{}.png'.format(path,figname)
    plt.savefig(filename)
    plt.close()



def CaseAsAxialDistributionAnalysis(ms_whole,selection_funs:[],path,interval=1):
    Nframes = ms_whole.trajectory.NFrames

    for iFrame in range(0,Nframes,interval):
        AxialDistributionAnalysis(ms_whole,selector_methane_C=selection_funs[0],\
                                  selector_water_O=selection_funs[1],\
                                  path=path,figname='axial{}'.format(iFrame),\
                                  binSize=2,to_plot_this_many_bins_beyond_interface=25,\
                                  iFrame=iFrame)


def CaseAsWriteTrajectory(ms_whole,selection_func,path,filename,interval=1):

    ms_copy = ms_whole.Copy()

    for iFrame in range(0, ms_whole.trajectory.NFrames, interval):
        ProgressBar(iFrame * 1.0 / ms_whole.trajectory.NFrames)
        file = open('{}/{}_{}.xyz'.format(path,filename,iFrame), 'w')
        output.setoutput(file)
        ms_copy.UpdateCoordinatesByTrajectoryFrame(iFrame)
        to_write = MolecularManipulation.SubSystemByLambdaFunction(ms_copy,selection_func)
        MolecularManipulation.ReduceSystemToOneMolecule(to_write).Write(XYZFile())
        output.setoutput(None)
        file.close()

    ProgressBar(1.00);
    output('')

def CaseAsRadialDistribution(ms_whole,selection_func,path,CenterYZ,Radius,Plot_range_in_Angstrom=25,Tempareture=313):

    ms_selected = MolecularManipulation.SubSystemByLambdaFunction(ms_whole, selection_func)
    import math
    binSize = 0.5
    NBins = int(math.floor(Radius/binSize))

    # tail_beg and tail_end are used to sample densities far from the tube wall and to estimate core pressure
    # The below values are used because existing analysis used these settings. They mean that for R = 5.3 nm,
    # rho values in [2.8 nm, 4.5 nm] are averaged, while for R = 2.8 nm tube, values in [1.5 nm, 2.25 nm] are used
    if Radius > 45:
        tail_beg = 48
        tail_end = 90
    elif Radius > 23:
        tail_beg = 30
        tail_end = 45
    else:
        error("The Tube is too thin, core density is not accurate! ")
        tail_beg = int(NBins*0.6)
        tail_end = int(NBins*0.95)

    beg_frame = int(math.floor(ms_selected.trajectory.NFrames * 0.75))   # Analyze only the last quarter of all frames
    end_frame = ms_selected.trajectory.NFrames
    RadialDistribution(ms_selected, length=ms_selected.boundary[0][0], centerY=CenterYZ, centerZ=CenterYZ, \
        radius=Radius, binSize=binSize, frames=range(beg_frame,end_frame),\
        tail_beg=tail_beg, tail_end=tail_end, path=path, fig='density',\
                       plot_range_in_Angstrom=Plot_range_in_Angstrom,temperature=Tempareture)

def CaseAsMSDAnalysis(ms_whole,selection_function,path):
    ms_Selected = MolecularManipulation.SubSystemByLambdaFunction(ms_whole, selection_function)
    MSD(ms_Selected, path=path, fig='MSD')




def Main():
    import sys
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = '/'

    # This Parameter Needs To Be Adjusted In Some Cases.
    InnerDiameter = 100
    CenterYZ = (InnerDiameter+50)/2
    # Also check if the Radius is Correct
    Radius = InnerDiameter/2 + 3

    # Select further half of the system. For H2O or CH4, judged by positions of C or O.
    half_tube_small_mol_func = lambda m, a: True if len(m.atoms) <= 5 and m.atoms[0].y >= CenterYZ else False
    half_tube_only_coal_func = lambda m, a: True if len(m.atoms) > 5 and a.y >= CenterYZ else False
    dummy_atom = Atom()
    dummy_atom.x, dummy_atom.y, dummy_atom.z = [18.2727, 81.2727, 111.024]
    region_func = lambda m,a: True if Distance(a,dummy_atom) < 10.0 else False
    water_onlyO_func = lambda m,a: True if len(m.atoms) == 4 and a.element == 'O' else False
    water_func = lambda m, a: True if len(m.atoms) == 4 else False
    methane_onlyC_func = lambda m, a: True if len(m.atoms) == 5 and a.element == 'C' else False
    methane_func = lambda m,a: True if len(m.atoms) == 5 else False


    ms_whole = Read(path)
    CaseAsWriteTrajectory(ms_whole, half_tube_only_coal_func,path,  'coal',  interval=999)   # Just the coal
    CaseAsWriteTrajectory(ms_whole, half_tube_small_mol_func, path, 'small', interval=10)  # Then the small mol


    # Choose the appropriate function, such as water_onlyO_func or methane_onlyC_func
    #CaseAsRadialDistribution(ms_whole,water_onlyO_func,path,CenterYZ,Radius,Plot_range_in_Angstrom=50)
    #CaseAsMSDAnalysis(ms_whole,water_onlyO_func,path)
    CaseAsAxialDistributionAnalysis(ms_whole,[methane_onlyC_func,water_onlyO_func],path,interval=10)

if __name__ == '__main__':
    Main()


