from ase.phonons import Phonons
from phonopy import Phonopy
from phonopy.structure.atoms import PhonopyAtoms

import os
import shutil

from phonopy.interface.calculator import read_crystal_structure, write_crystal_structure

unitcell, optional_structure_info = read_crystal_structure("geometry.in", interface_mode='aims')

phonon = Phonopy(unitcell,
                 supercell_matrix=[[2, 0, 0], [0, 2, 0], [0, 0, 2]])

phonon.generate_displacements(distance=0.01)
supercells = phonon.supercells_with_displacements

print(supercells[0])

for ind, sup in enumerate(supercells):
    write_crystal_structure(f"geomtry_{ind}.in", supercells[ind], interface_mode='aims')

    directory = f"disp_{ind}"
    parent_dir = "C:/Users/Merlin Warner-Huish/PycharmProjects/Merlin/"
    path = os.path.join(parent_dir, directory)
    try:
        os.mkdir(path)
        shutil.move(f'C:/Users/Merlin Warner-Huish/PycharmProjects/Merlin/geomtry_{ind}.in', path + "/geometry.in")
    except Exception as e:
        print('error', e)

