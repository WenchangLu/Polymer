#!/usr/bin/python

import sys
import os
import math

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


for ro in range(0, 360, 15):
    rotate_degree = float(ro) /180.0 * 3.1415926
    for i in range(70,num_atoms):
        x = atoms[i][1]
        y = atoms[i][2]
        cosa = math.cos(rotate_degree)
        sina = math.sin(rotate_degree)

        atoms[i][1] = x * cosa + y * sina
        atoms[i][2] = x * sina - y * cosa

    x_min = min(atoms, key=lambda x:x[1])[1]
    y_min = min(atoms, key=lambda x:x[2])[2]
    z_min = min(atoms, key=lambda x:x[3])[3]
 
    xyz_lines = "%d\n\n"%num_atoms
    for atom in atoms:
        xyz_lines += "%s   %f   %f   %f\n"%(atom[0], atom[1]-x_min + 1.0, atom[2]-y_min + 1.0,atom[3]-z_min + 1.0)

    filename = "rotate_"+str(ro)+".xyz"
    with open(filename, "w") as f:
        f.write(xyz_lines)
