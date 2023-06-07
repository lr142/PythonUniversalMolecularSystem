from Utility import *
from UniversalMolecularSystem import *
from MOL2File import *

# This is the class to read/write a VASP file in POSCAR or CONTCAR format
class VASPFile(MolecularFile):
    def __init__(self):
        pass

    def Read(self,molecularSystem,filename):
        # IN this format:
        # C H C H
        #    1.46300000000000
        #      3.4641016150000001    0.0000000000000000    0.0000000000000000
        #      0.0000000000000000    3.0000000000000000    0.0000000000000000
        #      0.0000000000000000    0.0000000000000000    6.2999999999999998
        #    C    H    C    H
        #      8     8     8     8
        # Selective dynamics
        # Direct
        #   0.9948698502372831  0.9956632048706661  0.0235556675433471   T   T   T
        #   0.4948607946906687  0.9956724762543142  0.0235334106627378   T   T   T
        #   0.9948674607348924  0.3289845074532531  0.9738136111020667   T   T   T
        #   0.4948764741761131  0.3289938569666656  0.9737911585156549   T   T   T
        #  ......
        # The 6th line may not be present
        file = None
        try:
            file = open(filename, "r")
        except IOError:
            error("Can't open VASP file <{}>".format(filename))
            return False
        contents = file.readlines()
        file.close()
        first_line = contents[0]
        # 1st line usually contains the list of elements, but not take it for granted. It not, the 6th line contains the
        # elements
        element_types = first_line.strip().split()
        scale = float(contents[1].strip())
        molecularSystem.scale = scale # write the scale factor to a special variable "scale", unique to VASP files
        molecularSystem.boundary = [[0,0,0],[0,0,0],[0,0,0]]
        for i in range(3):
            line = contents[i+2]
            words = line.strip().split()
            for j in range(3):
                molecularSystem.boundary[i][j] = float(words[j])*scale
        if len(contents) < 5: # if the file contains no other contents (just the header), ok to exit now.
            return True

        # The 6th line is either a declaration of elements, or that line is missing, followed by the count of each element
        lineno = 5
        words = contents[5].strip().split()
        try:
            number = int(words[0]) # this is the line of number of atoms
        except:
            # this should be saying the type of elements. Overriding what's in the first line
            element_types = words
            lineno = 6
        element_counts = [int(w) for w in contents[lineno].strip().split()]
        # construct the list of atoms in coordinates
        elements = []
        for i,c in enumerate(element_counts):
            temp_list = [element_types[i] for _ in range(c)]
            elements.extend(temp_list)
        NAtoms = len(elements)
        TF = [True for _ in range(NAtoms)] # Not support partial TF, just Fix or Flexible
        coords = np.zeros((NAtoms,3))
        fractional_line = contents[lineno+2].strip().upper()
        fractional = True if fractional_line.startswith("D") or fractional_line.startswith("F") else False
        # Assume all atoms are in fractional coordinates, start reading in atoms
        lineno+=3
        for i in range(NAtoms):
            words = contents[i+lineno].strip().split()
            for j in range(3):
                coords[i,j] = float(words[j])
            if len(words) > 3 and words[3]=="F":
                TF[i] = False
        # Convert coords into cartesian
        if fractional:
            uvw = np.array(molecularSystem.boundary)
            for i in range(NAtoms):
                coords[i,:] = uvw[0]*coords[i,0] + uvw[1]*coords[i,1] + uvw[2]*coords[i,2]
        # Record the atoms
        molecularSystem.molecules = [Molecule()]
        molecularSystem.molecules[0].atoms = []
        for i in range(NAtoms):
            newAtom = Atom()
            newAtom.element = elements[i]
            newAtom.x, newAtom.y, newAtom.z = coords[i,0], coords[i,1], coords[i,2]
            newAtom.flexible = TF[i]
            molecularSystem.molecules[0].atoms.append(newAtom)
        molecularSystem.RenumberAtomSerials()
        return True

    def Write(self,molecularSystem):
        # Writing out an POSCAR/CONTCAR file is straightforward
        # Write in default fractional coordinates
        scale = 1.0
        if hasattr(molecularSystem,'scale'): # if has this special property 'scale'
            scale = molecularSystem.scale
        uvw = np.array(molecularSystem.boundary)
        scaled_uvw = uvw / scale
        # Count the elements
        elements = []
        element_counts = []
        for atom in molecularSystem.Atoms():
            if len(elements)==0 or atom.element!=elements[-1]:
                elements.append(atom.element)
                element_counts.append(1)
            else:
                element_counts[-1] += 1
        first_line = ""
        atomcounts_line = "  "
        for iEle,e in enumerate(elements):
            first_line += e
            atomcounts_line += "{}".format(element_counts[iEle])
            if iEle < len(elements)-1:
                first_line += " "
                atomcounts_line += " "
        output(first_line)
        output("  {}".format(scale))
        for i in range(3):
            output("    {} {} {}".format(scaled_uvw[i,0],scaled_uvw[i,1],scaled_uvw[i,2]))
        # output("  {}".format(first_line)) # if you want, you can print this line, like in CONTCAR
        output(atomcounts_line)
        output("Selective dynamics")
        output("Direct")
        for atom in molecularSystem.Atoms():
            xyz = atom.XYZ()
            coords = [0,0,0]
            for i in range(3):
                # The fractional coordinates are projections to U,V,W vectors
                coords[i] = np.dot(xyz,uvw[i])/np.dot(uvw[i],uvw[i])
            TF = "T T T" if atom.flexible else "F F F"
            output("  {:.16f}  {:.16f}  {:.16f}  {}".format(coords[0],coords[1],coords[2],TF))
