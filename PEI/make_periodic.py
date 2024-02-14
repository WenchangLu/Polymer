#!/usr/bin/python

import sys
import os
import math
import copy

first_id = 45
last_id =108
remove_ids = [132 ,70 ]
with open("init.xyz", "r") as f:
        all_lines = f.readlines()

num_atoms = int(all_lines[0])
atoms = []
for i in range(num_atoms):
    line = all_lines[i+2].split()
    atoms.append([line[0], float(line[1]),float(line[2]),float(line[3])])
x0 = atoms[first_id][1]
y0 = atoms[first_id][2]
z0 = atoms[first_id][3]

for i in range(num_atoms):
    atoms[i][1] -= x0
    atoms[i][2] -= y0
    atoms[i][3] -= z0

x = atoms[last_id][1]
y = atoms[last_id][2]
cosa = x/math.sqrt(x*x+y*y)
sina = y/math.sqrt(x*x+y*y)
for i in range(num_atoms):
    x = atoms[i][1]
    y = atoms[i][2]
    atoms[i][1] = x * cosa + y * sina
    atoms[i][2] = x * sina - y * cosa

x = atoms[last_id][1]
z = atoms[last_id][3]
cosa = z/math.sqrt(x*x+z*z)
sina = x/math.sqrt(x*x+z*z)
for i in range(num_atoms):
    x = atoms[i][1]
    z = atoms[i][3]
    atoms[i][1] = x * cosa - z * sina
    atoms[i][3] = x * sina + z * cosa

c = atoms[last_id][3] + 1.5
for i in remove_ids:
    del atoms[i]


x_min = min(atoms, key=lambda x:x[1])[1]
y_min = min(atoms, key=lambda x:x[2])[2]
z_min = min(atoms, key=lambda x:x[3])[3]
x_max = max(atoms, key=lambda x:x[1])[1]
y_max = max(atoms, key=lambda x:x[2])[2]
z_max = max(atoms, key=lambda x:x[3])[3]

atoms.sort(key=lambda x:x[3])
print(x_min, y_min, z_min)
a = x_max - x_min + 5.0
b = y_max - y_min + 5.0
xyz_lines = "%d\n"%len(atoms)
xyz_lines +='Lattice="'
xyz_lines += "%f 0.0 0.0  0.0 %f 0.0  0.0 0.0 %f"%(a,b,c)
xyz_lines += '"\n'
for atom in atoms:
    xyz_lines += "%s   %f   %f   %f\n"%(atom[0], atom[1]-x_min , atom[2]-y_min ,atom[3]-z_min )

filename = "init_pb.xyz"
with open(filename, "w") as f:
    f.write(xyz_lines)
