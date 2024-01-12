#!/usr/bin/python

import sys
import os
import math
import copy

with open("input.xyz", "r") as f:
        all_lines = f.readlines()

num_atoms = int(all_lines[0])
atoms = []
for i in range(num_atoms):
    line = all_lines[i+2].split()
    atoms.append([line[0], float(line[1]),float(line[2]),float(line[3])])
x0 = (atoms[67][1] + atoms[69][1])/2.0
y0 = (atoms[67][2] + atoms[69][2])/2.0
z0 = (atoms[67][3] + atoms[69][3])/2.0

for i in range(num_atoms):
    atoms[i][1] -= x0
    atoms[i][2] -= y0
    atoms[i][3] -= z0
x = atoms[67][1]
y = atoms[67][2]
cosa = x/math.sqrt(x*x+y*y)
sina = y/math.sqrt(x*x+y*y)
for i in range(num_atoms):
    x = atoms[i][1]
    y = atoms[i][2]
    atoms[i][1] = x * cosa + y * sina
    atoms[i][2] = x * sina - y * cosa

x = atoms[67][1]
z = atoms[67][3]
cosa = z/math.sqrt(x*x+z*z)
sina = x/math.sqrt(x*x+z*z)
for i in range(num_atoms):
    x = atoms[i][1]
    z = atoms[i][3]
    atoms[i][1] = x * cosa - z * sina
    atoms[i][3] = x * sina + z * cosa

rotate_degree = 15.0/180.0 * 3.1415926

input_lines_common = """
description="rotate"  
#******** REAL SPACE GRID ********   
wavefunction_grid="168 96 296"  
potential_grid_refinement="2"  
  
#******* CONTROL OPTIONS *******  
start_mode          ="LCAO Start"  
calculation_mode    ="Relax Structure  "  
kohn_sham_solver    ="davidson"  
subdiag_driver      ="auto"  
#auto: if cuda available, use cusolver, otherwise use lapack for n<128 and scaplack for large system  
cube_rho = "True"  
relax_method="LBFGS"
charge_density_mixing = "0.10000000"

  
#********* K POINT SETUP *********  
kpoint_mesh = "1 1 1"  
kpoint_is_shift = "0 0 0"  
  
#******* Pseudopotentials *******   
internal_pseudo_type = "sg15"  
#use Optimized Norm-Conserving Vanderbilt (ONCV) pseudopotenitals  
#those pseudopotentials are built in with RMG  
write_pseudopotential_plots ="False"  
  
#*****Exchange Correlation ******  
exchange_correlation_type="AUTO_XC"  
#AUTO_XC: XC will be determined from pseudopotential  
  
#****  LATTICE and ATOMS  ****   
bravais_lattice_type="Orthorhombic Primitive"  
crds_units = "Angstrom"  
lattice_units = "Angstrom"  
a_length="      32.00000000"  
b_length="      18.00000000"  
c_length="     58.000"
atomic_coordinate_type = "Absolute"  
atoms="  
"""

a_len = 0.0
b_len = 0.0
c_len = 0.0
atoms_keep = copy.deepcopy(atoms)

for ro in range(0, 380, 15):
    rotate_degree = float(ro) /180.0 * 3.1415926
    cosa = math.cos(rotate_degree)
    sina = math.sin(rotate_degree)

    atoms = []

    atoms = copy.deepcopy(atoms_keep)
       
    for i in range(70,num_atoms):
        x = atoms[i][1]
        y = atoms[i][2]

        atoms[i][1] = x * cosa + y * sina
        atoms[i][2] = x * sina - y * cosa

    x_min = min(atoms, key=lambda x:x[1])[1]
    y_min = min(atoms, key=lambda x:x[2])[2]
    z_min = min(atoms, key=lambda x:x[3])[3]
    x_max = max(atoms, key=lambda x:x[1])[1]
    y_max = max(atoms, key=lambda x:x[2])[2]
    z_max = max(atoms, key=lambda x:x[3])[3]

    #print(ro, x_min, x_max)
    a_len = max(a_len, x_max-x_min)
    b_len = max(b_len, y_max-y_min)
    c_len = max(c_len, z_max-z_min)
 
    input_lines = input_lines_common
    xyz_lines = "%d\n\n"%num_atoms
    for atom in atoms:
        xyz_lines += "%s   %f   %f   %f\n"%(atom[0], atom[1]-x_min + 1.0, atom[2]-y_min + 1.0,atom[3]-z_min + 1.0)
        input_lines += "%s   %f   %f   %f\n"%(atom[0], atom[1]-x_min + 1.0, atom[2]-y_min + 1.0,atom[3]-z_min + 1.0)

    input_lines += "\"\n"
    dir_name = "rotate_"+str(ro)
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)
        
    filename = dir_name+"/init.xyz"
    with open(filename, "w") as f:
        f.write(xyz_lines)
    filename = dir_name+"/input"
    with open(filename, "w") as f:
        f.write(input_lines)
# 67 69

    x0 = (atoms[67][1] + atoms[69][1]) * 0.5
    y0 = (atoms[67][2] + atoms[69][2]) * 0.5
    z0 = (atoms[67][3] + atoms[69][3]) * 0.5
    x1 = atoms[1][1] - x0
    y1 = atoms[1][2] - y0
    z1 = atoms[1][3] - z0
    x2 = atoms[134][1] - x0
    y2 = atoms[134][2] - y0
    z2 = atoms[134][3] - z0
    tem = x1*x2 + y1 *y2 + z1 * z2
    tem = tem/ math.sqrt(x1*x1+y1*y1+z1*z1)
    tem = tem/ math.sqrt(x2*x2+y2*y2+z2*z2)
    tem = 180 - math.acos(tem) /3.1415926 * 180
    print("angle", ro, tem)
print(a_len, b_len, c_len)
