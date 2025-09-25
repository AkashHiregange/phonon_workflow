import fontTools.ttx
from ase.io import read, write
import os
from ase import Atoms
from ase.calculators.aims import Aims
from ase.optimize import BFGS
from ase.build import bulk
from ase.phonons import Phonons
from ase.io.trajectory import Trajectory
from ase.dft.kpoints import bandpath

# atoms = read('geometry.in')

def get_band_conf(atoms):

    lat1 = atoms.cell.bandpath()
    band_label = []
    band = []
    for sp in lat1.path:
        if sp == 'G':
            band_label.append('$\\Gamma$')
        elif sp.isnumeric():
            band_label[-1] = band_label[-1] + sp
        else:
            band_label.append(sp)
    for sp in band_label:
        if sp != ',':
            if sp == '$\\Gamma$':
                band.append('0 0 0')
            else:
                cor1 = lat1.special_points[sp][0]
                cor2 = lat1.special_points[sp][1]
                cor3 = lat1.special_points[sp][2]
                band.append(f'{cor1} {cor2} {cor3}')
        elif sp == ',':
            band[-1] = band[-1] + ','

    for i in band_label:
        if i == ',':
            band_label.pop(band_label.index(i))

    band_label_final = ' '.join(band_label)
    print(band_label_final)
    band_final = '    '.join(band)
    print(band_final)

    try:
        f = open('band.conf', 'x')
        f.close()
    except:
        print()

    f = open('band.conf', 'w')
    f.write(f'BAND = {band_final}\n'
            f'BAND_LABELS = {band_label_final}\n'
            f'BAND_POINTS = 101\n')
    f.close()
    # f.write(f'TPROP =.TRUE.\n'
    #         f'MESH = 16 16 16\n')

def get_thermal_conf(atoms):
    f = open('thermal.conf', 'w')
    f.write(f'TPROP =.TRUE.\n'
            f'MESH = 16 16 16\n')
    f.close()

def os_commands():
    os.system("phonopy -f disp_*/aims.out")
    os.system("phonopy -p -s band.conf")
    os.system("phonopy -p -s thermal.conf")


# get_band(atoms)
# os_commands()