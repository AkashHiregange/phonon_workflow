#IMPORTS
import numpy as np
from ase.build import bulk
from ase.phonons import Phonons
from phonopy import Phonopy
from phonopy.structure.atoms import PhonopyAtoms
from ase import Atoms
from ase.io import read, write
import numpy
import os
import shutil
from phonopy.interface.calculator import read_crystal_structure, write_crystal_structure

def make_displaced_supercells(atoms_object, supercell_size:[1,1,1], displacement: 0.01):

    '''

    :param atoms_object:
    :return:
    '''
    import numpy as np
    from phonopy import Phonopy
    from phonopy.structure.atoms import PhonopyAtoms
    import os
    import shutil
    from phonopy.interface.calculator import read_crystal_structure, write_crystal_structure
    import yaml
    from yaml import load
    from yaml import CLoader as Loader

    num1 = 1
    sup_matrix = np.diag(supercell_size)
    # print(sup_matrix.shape)
    # sup_matrix = np.array([[num1, 0, 0], [0, num1, 0], [0, 0, num1]])
    # print(sup_matrix.shape)
    atoms_object.write('geometry_eq.in')
    unitcell, optional_structure_info = read_crystal_structure("geometry_eq.in", interface_mode='aims')
    det = np.round(np.linalg.det(sup_matrix))
    phonon = Phonopy(unitcell, supercell_matrix=sup_matrix)

    phonon.generate_displacements(distance=displacement)
    supercells = phonon.supercells_with_displacements
    phonon.save('phonopy_disp.yaml')
    stream = open("phonopy_disp.yaml", 'r')
    dictionary = yaml.load(stream, Loader)
    stream.close()
    dictionary['phonopy'].update([('calculator', 'aims'), ('configuration', {'create_displacements': '".true."', 'dim':
        f'"{supercell_size[0]} {supercell_size[1]} {supercell_size[2]}"', 'calculator': '"aims"'})])
    # dictionary['physical_unit'].update([('length', '"angstrom"'), ('force_constants', '"eV/angstrom^2"')])
    with open('phonopy_disp.yaml', 'w') as f:
        data = yaml.dump(dictionary, f, sort_keys=False)

    return det, supercells

def make_matrix(atoms_object):
    '''

    :param atoms_object:
    :return:
    '''
    num1 = 1
    num2 = 0.01

    atoms_object.write('geometry.in')
    unitcell, optional_structure_info = read_crystal_structure("geometry.in", interface_mode='aims')
    os.remove('geometry.in')

    sup_matrix = np.array([[num1, 0, 0], [0, num1, 0], [0, 0, num1]])
    det = np.round(np.linalg.det(sup_matrix))
    phonon = Phonopy(unitcell, supercell_matrix=sup_matrix)

    phonon.generate_displacements(distance=num2)
    supercells = phonon.supercells_with_displacements
    phonon.save('phonopy_disp.yaml')
    '''
    IT IS IMPORTANT TO CREATE A phonopy_disp.yaml file to create force sets later.
    Furthermore, the disp yaml file should include details of the calculator used, the displacement, and the supercell 
    dimension. This is done below by reading the .yaml file and dumping the relevant info
    '''
    import yaml
    from yaml import load
    from yaml import CLoader as Loader
    stream = open("phonopy_disp.yaml", 'r')
    dictionary = yaml.load(stream, Loader)
    stream.close()
    print(dictionary)
    dictionary['phonopy'].update([('calculator', 'aims'), ('configuration', {'create_displacements': '".true."', 'dim': f'"{num1} {num1} {num1}"', 'calculator': '"aims"'})])
    # dictionary['physical_unit'].update([('length', '"angstrom"'), ('force_constants', '"eV/angstrom^2"')])
    print(dictionary)
    with open('phonopy_disp.yaml', 'w') as f:
        data = yaml.dump(dictionary, f, sort_keys=False)

    return det, supercells


def get_charges_and_moments(determinant, atoms_object):
    charges2 = []
    moments2 = []

    charges = atoms_object.get_initial_charges()
    moments = atoms_object.get_initial_magnetic_moments()

    for i in range(len(atoms_object)):
        for j in range(int(determinant)):
            charges2.append(charges[i])
            moments2.append(moments[i])

    return moments2, charges2


def creating_files_and_directories(atoms_object, charges, moments):
    '''

    :param atoms_object:
    :param charges:
    :param moments:
    :return:
    '''

    chem_sym = atoms_object.get_chemical_symbols()
    for ind, sup in enumerate(supercells):
        write_crystal_structure(f"geometry_{ind+1:03}.in", supercells[ind], interface_mode='aims')
        atoms = read(f"geometry_{ind+1:03}.in")
        atoms.set_initial_charges(charges)
        atoms.set_initial_magnetic_moments(moments)
        directory = f"disp_{ind+1:03}"
        parent_dir = os.getcwd()
        path_final = os.path.join(parent_dir, directory)
        if os.path.exists(path_final):
            shutil.rmtree(path_final) # this leads to access error on windows. Find an elegant workaround
        os.mkdir(path_final)
        atoms.write(path_final + '/geometry.in')
        #shutil.copy(parent_dir + '/input.py', path_final + '/input.py')
        #shutil.copy(parent_dir + '/submission.script', path_final + '/submission.script')
        os.chdir(parent_dir)
        os.remove(f"geometry_{ind+1:03}.in")


crys = bulk('Al', 'fcc', a=4.121, cubic=True)

det, supercells = make_displaced_supercells(crys, [1,1,1], 0.01)
moments, charges = get_charges_and_moments(det,crys)
print(moments)

creating_files_and_directories(crys, charges, moments)

