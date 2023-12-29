#!/usr/bin/python

import sys
import os
import math

num_cell_x = 1
num_cell_y = 1
num_cell_z = 5
first_id = 7
second_id = 16

if len(sys.argv) > 1:
    with open(sys.argv[1], "r") as f:
        all_lines = f.readlines()
else:
    with open("input.xyz", "r") as f:
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

if len(lattice_vec) != 9:
   print("lattice info missing")

atoms_replica = []
for ix in range(num_cell_x):
    for iy in range(num_cell_y):
        for iz in range(num_cell_z):
            x = lattice_vec[0] * ix + lattice_vec[3] * iy + lattice_vec[6] * iz
            y = lattice_vec[1] * ix + lattice_vec[4] * iy + lattice_vec[7] * iz
            z = lattice_vec[2] * ix + lattice_vec[5] * iy + lattice_vec[8] * iz
            for atom in atoms:
                atoms_replica.append([atom[0], atom[1] + x, atom[2]+y, atom[3]+z])


## add twi H at the end of monomers

x = atoms[first_id][1] + (atoms[second_id][1] - atoms[first_id][1]) * 0.7
y = atoms[first_id][2] + (atoms[second_id][2] - atoms[first_id][2]) * 0.7
z = atoms[first_id][2] + (atoms[second_id][2] - atoms[first_id][2] - lattice_vec[8]) * 0.7
atoms_replica.append(["H",  x, y, z])
x = atoms[second_id][1] + (atoms[first_id][1] - atoms[second_id][1]) * 0.7
y = atoms[second_id][2] + (atoms[first_id][2] - atoms[second_id][2]) * 0.7
z = atoms[second_id][2] + (atoms[first_id][2] - atoms[second_id][2] + lattice_vec[8]) * 0.7
atoms_replica.append(["H",  x, y, z + num_cell_z * lattice_vec[8]])

xyz_lines = "%d\n"%len(atoms_replica)

lattice_vec[0] = num_cell_x * lattice_vec[0]
lattice_vec[1] = num_cell_x * lattice_vec[1]
lattice_vec[2] = num_cell_x * lattice_vec[2]
lattice_vec[3] = num_cell_y * lattice_vec[3]
lattice_vec[4] = num_cell_y * lattice_vec[4]
lattice_vec[5] = num_cell_y * lattice_vec[5]
lattice_vec[6] = num_cell_z * lattice_vec[6]
lattice_vec[7] = num_cell_z * lattice_vec[7]
lattice_vec[8] = num_cell_z * lattice_vec[8]
lattice = ""
for a in lattice_vec:
    lattice += "%f "%a
xyz_lines +='Lattice="' + lattice +'"\n'

for atom in atoms_replica:
    xyz_lines += "%s   %f   %f   %f\n"%(atom[0], atom[1] , atom[2] ,atom[3] )

filename = "replica.xyz"
with open(filename, "w") as f:
    f.write(xyz_lines)
