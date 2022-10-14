import sys
sys.path.append('/Users/me/_Nutbox/UniversalMolecularSystem')

from UniversalMolecularSystem import *
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from matplotlib.patches import *
from Utility import *

class AtomAppearance:
    def __init__(self,size,color):
        self.size = size
        self.color = color
# Singleton object in this module
atomAppearances = None

# atomAppearances are read from "AtomAppearances.csv"
def ReadAtomAppearances():
    import os
    default_route = os.path.join(DATAFILESPATH,"AtomAppearances.csv")
    with open(default_route,'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith('#'):
                continue
            segments = line.split(',')
            element = segments[0]
            size = float(segments[1])
            color = segments[2]
            atomAppearances[element.upper()] = AtomAppearance(size,color)

def DefaultAtomSize_VDW(molecule,atom):
    #DefaultAtomSize by Element, VDW radius
    if atom.element.upper() in atomAppearances:
        return atomAppearances[atom.element.upper()].size
    else:
        return atomAppearances['Default'].size

def DefaultAtomSize_BallnStick(molecule, atom):
    return DefaultAtomSize_VDW(molecule,atom) * 0.3

def DefaultAtomColor(molecule,atom):
    #DefaultAtomColor by Element
    if atom.element.upper() in atomAppearances:
        return atomAppearances[atom.element.upper()].color
    else:
        return atomAppearances['Default'].color

def DefaultBondSize(molecule,atom1,atom2,bond):
    return 0.1

def LabelAtomIndex(molecule,atom):
    return "{}{}".format(atom.element,atom.serial)

def DefaultLabel_ElementSerials(molecule,atom):
    return "{}{}".format(atom.element,atom.serial)

def DefaultLabelSize(molecule,atom,labeltext):
    return 12

def DefaultLabelColor(molecule,atom,labeltext):
    return 'tomato'

def DrawBond(mol,atom1,atom2,bond,atomcolor_func,bondsize_func,depth_of_view):

    midZ = (atom1.z + atom2.z)/2

    if abs(midZ) > depth_of_view:
        return (None,None)
    alpha = 1.0 - abs(midZ)/depth_of_view

    size = bondsize_func(mol,atom1,atom2,bond)
    color1 = atomcolor_func(mol,atom1)
    color2 = atomcolor_func(mol,atom2)
    atom1Center = np.array([atom1.x,atom1.y])
    atom2Center = np.array([atom2.x,atom2.y])
    midPoint = (atom1Center + atom2Center) * 0.5
    atom1ToAtom2Vector = atom2Center - atom1Center
    bondLength = VectorNorm(atom1ToAtom2Vector)
    if bondLength < 1E-4 or bondLength > 5:
        # A Protective measure to avoid drawing bonds between two atoms that are in fact clumped together
        # Also not show bonds that are too long (maybe those are across the periodic boundaries)
        return (None,None)
    atom1ToAtom2VectorNormalized = np.array(VectorNormalize(atom1ToAtom2Vector))

    perpendicularVectorNormalized = np.array([-atom1ToAtom2VectorNormalized[1],atom1ToAtom2VectorNormalized[0]])

    # draw the 1st half of the bond, stretching from atom1 to the midpoint
    points = np.array([ atom1Center + 0.5 * size * perpendicularVectorNormalized,
               midPoint    + 0.5 * size * perpendicularVectorNormalized,
               midPoint    - 0.5 * size * perpendicularVectorNormalized,
               atom1Center - 0.5 * size * perpendicularVectorNormalized])

    # print(points)
    # print(points.transpose())

    patch1 = Polygon( points, closed = True, facecolor=color1, edgecolor=None,zorder = 9,alpha=alpha)
    # about the zorder, atoms have zorder 10, which is in front of bonds.

    # draw the 2nd half
    points = np.array([ atom2Center + 0.5 * size * perpendicularVectorNormalized,
               midPoint    + 0.5 * size * perpendicularVectorNormalized,
               midPoint    - 0.5 * size * perpendicularVectorNormalized,
               atom2Center - 0.5 * size * perpendicularVectorNormalized])
    patch2 = Polygon( points, closed = True, facecolor=color2, edgecolor=None, zorder = 9,alpha=alpha)

    return (patch1,patch2)
    # Planned feature: Differentiate between distinct types of bond

def DrawLabel(axes,mol,atom,label_func,labelsize_func,labelcolor_func,depth_of_view):

    if abs(atom.z) > depth_of_view:
        return

    alpha = 1.0 - abs(atom.z)/depth_of_view    
    content = label_func(mol,atom)

    if content == "":
        return

    size = labelsize_func(mol,atom,content)
    color = labelcolor_func(mol,atom,content)

    axes.text(atom.x,atom.y,content,va='bottom',ha='left',weight='bold',color=color,
              fontsize = size, fontfamily='Helvetica',zorder = 12,alpha=alpha)



def Draw2D(molSys,filename=None,
           atomsize_func=DefaultAtomSize_BallnStick,atomcolor_func=DefaultAtomColor,
           bondsize_func=DefaultBondSize,
           label_func=None,labelsize_func=DefaultLabelSize,labelcolor_func=DefaultLabelColor,
           depth_of_view=10):
    # meaning of each parameter should be self-evident.
    # if 'filename' is given, the view is written to a file instead of bringing up a window.
    # Those end with '_func' are callback functions which allow the caller to finetune the behavior
    # of each individual atom/bond/label
    # depth_of_view controls the viewing of atoms before and behind the focus.
    # The default focus is Z = 0, those in front of and behind the focus will be faded away by
    # setting an alpha value.

    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])

    # plot atoms:
    def __draw_atoms__():
        xmin,xmax,ymin,ymax = (9999, -9999, 9999, -9999)
        for mol in molSys.molecules:
            for atom in mol.atoms:
                xmin = min(xmin,atom.x)
                xmax = max(xmax,atom.x)
                ymin = min(ymin,atom.y)
                ymax = max(ymax,atom.y)

                if abs(atom.z) > depth_of_view:
                    continue
                else:
                    alpha = 1.0 - abs(atom.z)/depth_of_view
                    a = Circle((atom.x,atom.y),radius=atomsize_func(mol,atom),\
                        facecolor=atomcolor_func(mol,atom),edgecolor=None,zorder=10,\
                        alpha = alpha)
                    ax.add_patch(a)

        xrange = xmax - xmin
        yrange = ymax - ymin
        pan_ratio = 0.1
        xmin -= xrange * pan_ratio
        xmax += xrange * pan_ratio
        ymin -= yrange * pan_ratio
        ymax += yrange * pan_ratio
        ax.axis([xmin,xmax,ymin,ymax])
        ax.set_aspect('equal')
        ax.set_axis_off()



    # draw bonds:
    def __draw_bonds__():
        for mol in molSys.molecules:
            serialToAtomMap = dict()
            for atom in mol.atoms:
                serialToAtomMap[atom.serial] = atom
            for bond in mol.bonds:
                atom1 = serialToAtomMap[bond.atom1]
                atom2 = serialToAtomMap[bond.atom2]
                p1,p2 = DrawBond(mol,atom1,atom2,bond,atomcolor_func,bondsize_func,depth_of_view)
                if p1 != None:
                    ax.add_patch(p1)
                if p2 != None:
                    ax.add_patch(p2)

    # draw labels:
    def __draw_labels__():
        for mol in molSys.molecules:
            for atom in mol.atoms:
                DrawLabel(ax,mol,atom,label_func,labelsize_func,labelcolor_func,depth_of_view)

    # Capture Move Scroll to Pan/Zoom
    def OnScroll(event):
        direction = event.button
        x = event.xdata
        y = event.ydata
        w = ax.get_xlim()[1] - ax.get_xlim()[0]
        h = ax.get_ylim()[1] - ax.get_ylim()[0]
        # Each scroll enlarge/shrink the view by 10% around the x,y center
        ratio = 0.90 if direction == 'up' else 1.1
        upper = (ax.get_ylim()[1] - y) * ratio + y
        lower = y - (y - ax.get_ylim()[0]) * ratio
        left  = x - (x - ax.get_xlim()[0]) * ratio
        right = (ax.get_xlim()[1] - x) * ratio + x
        ax.axis([left,right,lower,upper])
        plt.draw()


    def OnResize(event):
        new_aspect = 1.0 * event.height/event.width  # The larger the aspect, the taller
        old_width = ax.get_xlim()[1] - ax.get_xlim()[0]
        old_height = ax.get_ylim()[1] - ax.get_ylim()[0]
        old_aspect = 1.0 * old_height / old_width
        if new_aspect < old_aspect:
            # Make it flatter by showing more contents in the x-direction
            new_width = old_height/new_aspect
            mid_point = (ax.get_xlim()[1] + ax.get_xlim()[0])/2
            ax.set_xlim(mid_point - new_width/2, mid_point + new_width/2)
        else:
            # Make it taller by showing more contents in the y-direction
            new_height = old_width*new_aspect
            mid_point = (ax.get_ylim()[1] + ax.get_ylim()[0])/2
            ax.set_ylim(mid_point - new_height/2, mid_point + new_height/2)
        plt.draw()

    def OnPress(event):
        shifted = False
        if '+' in event.key:
            shifted = True
            key = event.key.split('+')[-1]
        else:
            key = event.key

        ratio = 0.01 if shifted else 0.1   # moving by 10%. If shift is pressed, move just 1%.
        height = ax.get_ylim()[1] - ax.get_ylim()[0]
        width = ax.get_xlim()[1] - ax.get_xlim()[0]

        need_to_redraw = True

        if key == 'up':
            ax.set_ylim(ax.get_ylim() + height * ratio)
        elif key == 'down':
            ax.set_ylim(ax.get_ylim() - height * ratio)
        elif key == 'left':
            ax.set_xlim(ax.get_xlim() - width * ratio)
        elif key == 'right':
            ax.set_xlim(ax.get_xlim() + width * ratio)
        else:
            need_to_redraw = False

        if need_to_redraw:
            plt.draw()



    __draw_atoms__()
    if bondsize_func != None:
        __draw_bonds__()
    if label_func != None:
        __draw_labels__()

    fig.canvas.mpl_connect('scroll_event', OnScroll)
    fig.canvas.mpl_connect('resize_event', OnResize)
    fig.canvas.mpl_connect('key_press_event',OnPress)

    if filename!=None:
        plt.savefig(filename,dpi = 1000)
    else:
        plt.show()

# This function will be executed while this module is loaded for the first time
if atomAppearances == None:
    atomAppearances = dict()
    ReadAtomAppearances()