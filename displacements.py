
from ase.phonons import Phonons
from phonopy import Phonopy
from phonopy.structure.atoms import PhonopyAtoms

import numpy as np
from phonopy import Phonopy
from phonopy.structure.atoms import PhonopyAtoms


from phonopy.interface.calculator import read_crystal_structure, write_crystal_structure



a = 5.404
unitcell = PhonopyAtoms(symbols=['Si'] * 8,
                        cell=(np.eye(3) * a),
                        scaled_positions=[[0, 0, 0],
                                          [0, 0.5, 0.5],
                                          [0.5, 0, 0.5],
                                          [0.5, 0.5, 0],
                                          [0.25, 0.25, 0.25],
                                          [0.25, 0.75, 0.75],
                                          [0.75, 0.25, 0.75],
                                          [0.75, 0.75, 0.25]])
phonon = Phonopy(unitcell,
                 supercell_matrix=[[2, 0, 0], [0, 2, 0], [0, 0, 2]])

phonon.generate_displacements(distance=0.01)
supercells = phonon.supercells_with_displacements

print(supercells[0])

for ind, sup in enumerate(supercells):
    write_crystal_structure(f"geomtry_{ind}.in", supercells[ind], interface_mode='aims')



