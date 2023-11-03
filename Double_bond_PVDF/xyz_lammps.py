#!/usr/bin/python

import sys
import os
import math

mass_dict = {
        "C":12.0107,
        "H":1.00794,
        "F":18.998404
        }
type_dict = {
        "C":1,
        "H":3,
        "F":2
        }

if len(sys.argv) > 1:
    with open(sys.argv[1], "r") as f:
        all_lines = f.readlines()
else:
    with open("init.xyz", "r") as f:
        all_lines = f.readlines()
if len(all_lines) < 3:
    print(" not a xyz file")

num_atoms = int(all_lines[0])
species = set()
atom_types = {}
line = all_lines[1].split('"')
lattice_vec = []
if len(line) > 1: 
    lat_str = line[1].split()
    for a in lat_str:
       lattice_vec.append(float(a))
atoms = []
for i in range(num_atoms):
    line = all_lines[i+2].split()
    atoms.append([line[0], float(line[1]),float(line[2]),float(line[3])])
    species.add(line[0])

xlo = 0.0
ylo = 0.0
zlo = 0.0
xy = 0.0
xz = 0.0
yz = 0.0
if len(lattice_vec) == 9:
    xhi =lattice_vec[0] * lattice_vec[0] 
    xhi +=lattice_vec[1] * lattice_vec[1] 
    xhi +=lattice_vec[2] * lattice_vec[2] 
    xhi = math.sqrt(xhi)
    yhi =lattice_vec[3] * lattice_vec[3] 
    yhi +=lattice_vec[4] * lattice_vec[4] 
    yhi +=lattice_vec[5] * lattice_vec[5] 
    yhi = math.sqrt(yhi)
    zhi =lattice_vec[6] * lattice_vec[6] 
    zhi +=lattice_vec[7] * lattice_vec[7] 
    zhi +=lattice_vec[8] * lattice_vec[8] 
    zhi = math.sqrt(zhi)

else:
   print("lattice info missing")

lammps_data = " LAMMPS data file, charge style generated xyz_lammps.py by Wenchang Lu \n\n"
lammps_data += "%d atoms\n"%num_atoms
lammps_data += "%d atom types\n"%len(species)
lammps_data += "\n"
lammps_data += "%f   %f   xlo xhi \n"%(xlo, xhi)
lammps_data += "%f   %f   ylo yhi \n"%(ylo, yhi)
lammps_data += "%f   %f   zlo zhi \n"%(zlo, zhi)
lammps_data += "%f   %f   %f  xy xz yz \n"%(xy, xz, yz)
lammps_data += "\n"
lammps_data += "Masses\n"
lammps_data += "\n"

for s in species:
    lammps_data += "%d  %f\n"%(type_dict[s], mass_dict[s])

lammps_data += "\n"
lammps_data += "Atoms # charge\n"
lammps_data += "\n"

for i in range(num_atoms):
    atom_sym = atoms[i][0]
    lammps_data += "%d %d 0.0 %f %f %f \n"%(i+1, type_dict[atom_sym], atoms[i][1],  atoms[i][2],  atoms[i][3])  

with open("lmp.data", "w") as f:
    f.write(lammps_data)
