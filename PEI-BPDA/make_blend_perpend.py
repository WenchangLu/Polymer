#!/usr/bin/python3

import sys
import os
import math
from random import random

file1 = "PEI.xyz"
file2 = "BPDA.xyz"
#blend = [1,1,1,1,1,1]  #pure PES
c_average = (44.70 +47.28)/2.0
a0 = c_average /3.0
b0 = 20.0
num_units = 12
a_shift = [0.0, a0, 2.0*a0, 0.5 * a0, 1.5*a0, 2.5*a0]
b_shift = [0.0, 0.0, 0.0]

a_shift += a_shift + a_shift 
b_shift += [x + b0 for x in b_shift] 
b_shift += [x + 2*b0 for x in b_shift] 
print(a_shift)
print(b_shift)

c_average = (44.70 +47.28)/2.0
#print(a_shift)
#print(b_shift)

with open(file1, "r") as f:
    all_lines = f.readlines()
if len(all_lines) < 3:
    print(" not a xyz file")

num_atoms_1 = int(all_lines[0])
line = all_lines[1].split('"')
lattice_vec = []
if len(line) > 1: 
    lat_str = line[1].split()
    for a in lat_str:
       lattice_vec.append(float(a))
c1 = lattice_vec[8]
atoms_1 = []
for i in range(num_atoms_1):
    line = all_lines[i+2].split()
    atoms_1.append([line[0], float(line[1]),float(line[2]),float(line[3]) * c_average/c1])

x_max = max(atoms_1, key=lambda x:x[1])[1]
x_min = min(atoms_1, key=lambda x:x[1])[1]
x_center = (x_max + x_min)/2.0
y_max = max(atoms_1, key=lambda x:x[2])[2]
y_min = min(atoms_1, key=lambda x:x[2])[2]
y_center = (y_max + y_min)/2.0

atoms_1_center = [[atom[0], atom[1]-x_center, atom[2]-y_center, atom[3]] for atom in atoms_1]

with open(file2, "r") as f:
    all_lines = f.readlines()
if len(all_lines) < 3:
    print(" not a xyz file")

num_atoms_2 = int(all_lines[0])
line = all_lines[1].split('"')
lattice_vec = []
if len(line) > 1: 
    lat_str = line[1].split()
    for a in lat_str:
       lattice_vec.append(float(a))
c2 = lattice_vec[8]

atoms_2 = []
for i in range(num_atoms_2):
    line = all_lines[i+2].split()
    atoms_2.append([line[0], float(line[1]),float(line[2]),float(line[3]) * c_average/c2])

x_max = max(atoms_2, key=lambda x:x[1])[1]
x_min = min(atoms_2, key=lambda x:x[1])[1]
x_center = (x_max + x_min)/2.0
y_max = max(atoms_2, key=lambda x:x[2])[2]
y_min = min(atoms_2, key=lambda x:x[2])[2]
y_center = (y_max + y_min)/2.0

atoms_2_center = [[atom[0], atom[1]-x_center, atom[2]-y_center, atom[3]] for atom in atoms_2]


atoms_blend = []
for i in range(num_units):
    alpha = random() * 3.14* 2.0
    z_rand = random() * c_average * 0.5 
    for atom in atoms_1_center:
        x = atom[1] * math.cos(alpha) + atom[2] * math.sin(alpha) + a_shift[i]
        y = -atom[1] * math.sin(alpha) + atom[2] * math.cos(alpha) + b_shift[i]
        z = atom[3] +z_rand
        atoms_blend.append([atom[0], x,y,z])

for i in range(num_units):
    alpha = random() * 3.14* 2.0
    z_rand = random() * c_average * 0.5 
    for atom in atoms_2_center:
        x = atom[1] * math.cos(alpha) + atom[2] * math.sin(alpha) + a_shift[i]
        y = -atom[1] * math.sin(alpha) + atom[2] * math.cos(alpha) + b_shift[i]
        z = atom[3] +z_rand
        atoms_blend.append([atom[0], z,y + 4.0* b0,x ])


xyz_lines = "%d\n"%len(atoms_blend)

lattice_vec[0] = 3.0 * a0
lattice_vec[1] = 0.0
lattice_vec[2] = 0.0
lattice_vec[3] = 0.0
lattice_vec[4] = 8.0 * b0
lattice_vec[5] = 0.0
lattice_vec[6] = 0.0
lattice_vec[7] = 0.0
lattice_vec[8] =  c_average
lattice = ""
for a in lattice_vec:
    lattice += "%f "%a
xyz_lines +='Lattice="' + lattice +'"\n'

for atom in atoms_blend:
    xyz_lines += "%s   %f   %f   %f\n"%(atom[0], atom[1] , atom[2] ,atom[3] )

filename = "blend_perpend"
filename += ".xyz"    
with open(filename, "w") as f:
    f.write(xyz_lines)