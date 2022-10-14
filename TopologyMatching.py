import sys
sys.path.append('/Users/me/_Nutbox/UniversalMolecularSystem')

# The main function of this module, TopologyMatching, seeks to solve the problem of matching atoms between two
# identical molecules with different atom ordering.
from UniversalMolecularSystem import *
from collections import deque



class SolvingStatus:
    nAtoms: []   # number of atoms in each molecule, an array of length 2
    visited_order: [[]]   # 2 lists recording visited atoms and their order in each mole
                    # for example, visited = [ [0,3],[1,2] ] means that atoms 0,3 and 1,2 are visited in each molecule
                    # Here the word 'visited' also means that the atoms in two molecules are matched with each other
                    # In the above example, it means 0-3, 1-2 matching in these two molecules.
    to_visit: [deque] # 2 deques recording the to-be visited atoms in both atoms. Used for the BFS in each mole
    visited_or_in_queue: [[]]  # 2*NAtoms bool matrix indicating whether each atom is found ( either visited or in queue)

    def __init__(self,nAtoms1, nAtoms2=None):
        self.nAtoms = [nAtoms1, nAtoms2] if nAtoms2!=None else [nAtoms1,nAtoms1]
        self.visited_order = [[],[]]
        self.visited_or_in_queue = [None,None]
        for i in range(2):
            self.visited_or_in_queue[i] = [False for _ in range(self.nAtoms[i])]
        self.to_visit = [deque(),deque()]

    def Copy(self):
        ns = SolvingStatus(self.nAtoms[0],self.nAtoms[1])
        import copy
        ns.visited_order = copy.deepcopy(self.visited_order)
        ns.to_visit = [self.to_visit[_].copy() for _ in range(2)]
        ns.visited_or_in_queue = copy.deepcopy(self.visited_or_in_queue)
        return ns

    def Show(self):
        import sys
        sys.stdout.write("Matching Order: ")
        for i in range(len(self.visited_order[0])):
            sys.stdout.write("{}-{} ".format(self.visited_order[0][i],self.visited_order[1][i]))
        print("")
        sys.stdout.write("Deque of each molecule: (A) ")
        for i in range(len(self.to_visit[0])):
            sys.stdout.write("{} ".format(self.to_visit[0][i]))
        sys.stdout.write("(B) ")
        for i in range(len(self.to_visit[1])):
            sys.stdout.write("{} ".format(self.to_visit[1][i]))
        print("")

global_iter_counter = 0

def __Recursive__(mols,bondedMaps,status,level=0,__exit_on_first_match__ = True, __debugging__ = False):

    total_results = []

    if __debugging__:
        print("Level = {}".format(level))
        status.Show()
        global global_iter_counter
        global_iter_counter += 1
        print("Global Iter = {}".format(global_iter_counter))


    # Do a DFS on both molecules. In cases there are multiple choices, perform and branch-and-cut algorithm
    while len(status.to_visit[0]) > 0:  # Until the queue is empty
        candidates = [[], []]
        head = [None, None]
        for iMol in range(2):
            # Get the first node from the queue. popleft() is BFS by using a queue, while pop() is DFS by using a stack,
            # Testing shows DFS is faster
#            head[iMol] = status.to_visit[iMol].popleft()
            head[iMol] = status.to_visit[iMol].pop()

            status.visited_order[iMol].append(head[iMol])  # visit the node
            for next_node in bondedMaps[iMol][head[iMol]]:  # among its neighbors, add those un-visited and un-queued node to the queue
                if status.visited_or_in_queue[iMol][next_node] == False:
                    candidates[iMol].append(next_node)
                    status.visited_or_in_queue[iMol][next_node] = True  # Just flag those atoms, don't really add them into the queue,yet.

        if __debugging__:
            for iMol in range(2):
                print("Head For Mol{}: {}, Candidates = {}".format(iMol,head[iMol],candidates[iMol]))

        # Based on the visited node and the number of candidates, we should either branch, or cut:
        if mols[0].atoms[head[0]].element != mols[1].atoms[head[1]].element:
            # Cut because element type mismatch
            return []
        elif status.nAtoms[0] == status.nAtoms[1] and len(candidates[0]) != len(candidates[1]):
            # Cut because bonded atoms count mismatch in equivalent molecules
            return []
        elif status.nAtoms[0] < status.nAtoms[1] and len(candidates[0]) > len(candidates[1]):
            # Cut because bonded atoms count mismatch in fragmental match
            return []
        elif len(candidates[0]) == 0:
            # If there is no bonded atoms in mol1, the visit is finished
            pass
        # elif len(candidates[0]) == 1:
        #     for iMol in region(2):
        #         status.to_visit[iMol].append(candidates[iMol][0])
        else:
            # Branch!  Do a full permutation of mol[1]'s candidates
            # Keep in mind that since A may be a fragment of B, the candidates of A and B may be of different length
            import itertools
            candidates_permutated = list(itertools.permutations(candidates[1]))
            # For each possible permutation, there is a branch:
            candidates_of_mol0 = candidates[0]
            for candidates_of_mol1 in candidates_permutated:
                newStatus = status.Copy()
                pre_test_flag = True
                for iPerm in range(min(len(candidates_of_mol0),len(candidates_of_mol1))):

                    a0 = candidates_of_mol0[iPerm]
                    a1 = candidates_of_mol1[iPerm]

                    # Some simple tests to exclude impossible matches
                    if mols[0].atoms[a0].element != mols[1].atoms[a1].element:
                        pre_test_flag = False
                        break

                    # if two mols have identical # of atoms, we require the # of bonds to be equal
                    if status.nAtoms[0] == status.nAtoms[1] and len(bondedMaps[0][a0]) != len(bondedMaps[1][a1]):
                        pre_test_flag = False
                        break
                    # if mol1 is a possibly a fragment of mol2, we require differently
                    if status.nAtoms[0] < status.nAtoms[1] and len(bondedMaps[0][a0]) > len(bondedMaps[1][a1]):
                        pre_test_flag = False
                        break


                    newStatus.to_visit[0].append(a0)
                    newStatus.to_visit[1].append(a1)

                if not pre_test_flag:
                    continue

                results = __Recursive__(mols,bondedMaps,newStatus,level=level+1,\
                                        __exit_on_first_match__ = __exit_on_first_match__,__debugging__ = __debugging__)
                if len(results) > 0:
                    total_results.extend(results)
                    if __exit_on_first_match__:
                        break

            return total_results   # The return point for recursive levels other than the last

    # After the while, all matched. End of recursion
    return [status]

def TopologyMatching(mols:[Molecule], first_node):
    # mols[0] and mols[1] are two molecules. They should be identical but the order of atoms may be totally different in these
    # two molecules. This algorithm works by identifying bondings between atoms, so bonds must be properly set in both
    # molecules
    # Modified Feb 2021: mols[0] can be a fragment of mols[1]. This function works for this senario
    # without any modification.
    
    # If successful, returns a list of lists, each of which represents a matching.
    # For example, the return value of [  [1,3,2,0], [1,2,0,3] ] means that atoms 0,1,2,3 in the first molecule
    # can be either be matched to atoms 1,3,2,0 or atoms 1,2,0,3 in the second molecule.
    # All indexes for atoms in this module starts from 0! Atom's serials are not used here!
    # There may be multiple ways (or no way) to match atoms in the first molecule to those in the second molecule,
    # therefore the length of the list is not known beforehand. An empty list [] as the return value means that it is
    # impossible to find a match.

    # The 'first_node' parameter is a hint given by the caller, suggesting which two atoms in these two molecules are
    # equivalent. The subsequent search shall begin on these two atoms. If not given, the program will try all combinations
    # and the function may run NAtoms times longer.. To mandate the user to give an initial hint, this function will
    # refuse to work without it! If really necessary, the caller can write a loop to try all intial matching point.

    if len(mols[0].atoms) > len(mols[1].atoms):
        error("In TopologyMatching(), either the two molecules are identical, or mols[0] is a fragment of mols[1]")
        return []

    initial_status = SolvingStatus(len(mols[0].atoms),len(mols[1].atoms))

    bondedMaps = [ mols[_].BondedMap() for _ in range(2) ]

    if first_node == None:
        error("The caller must give a 'first_node' parameter such as [0,3] to suggest that\n"
        "atom index 0 in mol1 is matched to atom index 3 in mol2")
        

    for iMol in range(2):
        initial_status.to_visit[iMol].append(first_node[iMol])          # Put first node in queue
        initial_status.visited_or_in_queue[iMol][first_node[iMol]] = True     # Set the proper flag

    results = __Recursive__(mols,bondedMaps,initial_status,level=0,__exit_on_first_match__ = True,__debugging__= False)

    if len(results) == 0:
        return None

    result = results[0]
    matching_map = [-1 for _ in range(result.nAtoms[0])]
    for iAtom in range(result.nAtoms[0]):
        matching_map[result.visited_order[0][iAtom]] = result.visited_order[1][iAtom]

    def __verify__(bondedMaps,matching_map):
        passed = True
        for iAtomInMol0 in range(len(matching_map)):
            iAtomInMol1 = matching_map[iAtomInMol0]
            for iBondedToInMol0 in bondedMaps[0][iAtomInMol0]:
                iBondedToInMol1 = matching_map[iBondedToInMol0]
                # verify that iBondedToInMol1 is in bondedMaps[1][iAtomInMol1]
                if iBondedToInMol1 not in bondedMaps[1][iAtomInMol1]:
                    print("Verify Failed: atom {} in (A) is matched to atom {} in (B), which should be bonded to "
                          "atom {} in (A). According to matching, this is {} in (B), but this is not.".format(iAtomInMol0,iAtomInMol1,iBondedToInMol0,iBondedToInMol1))
                    passed = False
            if not passed:
                break
        return passed

    if not __verify__(bondedMaps,matching_map):
        error("Internal error in TopologyMatching(): Verification Not Passed !",False)

    # for i in region(result.nAtoms[0]):
    #     print("{},{}".format(i,matching_map[i]))

    return matching_map

def TestCase(mol):
    # This is a testing case by randomly permutating atoms within a molecule, and match them
    # with the original molecule
    from UniversalMolecularSystem import MolecularSystem
    from BondDetection import DefaultBondRules
    from random import shuffle

    originalSystem = MolecularSystem()
    originalSystem.molecules = [mol]
    originalSystem.AutoDetectBonds(DefaultBondRules(),flushCurrentBonds = True)

    permSystem = originalSystem.Copy()
    shuffle(permSystem.molecules[0].atoms)  # Shuffle all but the first atom
    permSystem.RenumberAtomSerials()
    permSystem.AutoDetectBonds(DefaultBondRules(),flushCurrentBonds = True)

    originalSystem.Summary()
    permSystem.Summary()

    for i in range(len(originalSystem.molecules[0].atoms)):
        result = TopologyMatching([originalSystem.molecules[0],permSystem.molecules[0]],[0,i])
        if result != None:
            print(i)
            print(result)
        else:
            print("{}: No Match".format(i))




if __name__ == '__main__':

    TestCase()