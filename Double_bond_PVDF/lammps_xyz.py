#!/usr/bin/python

import sys
import os
import math

atom_symbol = [" ","C", "F", "H"]
if len(sys.argv) > 1:
    with open(sys.argv[1], "r") as f:
        all_lines = f.readlines()
else:
    with open("final.lmpdata", "r") as f:
        all_lines = f.readlines()
if len(all_lines) < 19:
    print("is it a lammps outputfile with atom and charge info?")

line = all_lines[2].split()
num_atoms = int(line[0])
line = all_lines[3].split()
num_types = int(line[0])

line = all_lines[5].split()
xlo = float(line[0])
xhi = float(line[1])
line = all_lines[6].split()
ylo = float(line[0])
yhi = float(line[1])
line = all_lines[7].split()
zlo = float(line[0])
zhi = float(line[1])

line = all_lines[8].split()
xy = float(line[0])
xz = float(line[1])
yz = float(line[2])

a = xhi - xlo
b = math.sqrt((yhi-ylo)*(yhi-ylo) + xy*xy)
c = math.sqrt((zhi-zlo)*(zhi-zlo) + xz*xz + yz * yz)
cosalpha = (xy*xz + (yhi-ylo) * yz)/b/c
cosbeta = xz/c
cosgamma = xy/b
singamma = math.sqrt(1.0 - cosgamma * cosgamma)

angfac1 = (cosalpha - cosbeta*cosgamma)/singamma
angfac2 = math.sqrt(singamma**2 - cosbeta**2 - cosalpha**2 + 2*cosalpha*cosbeta*cosgamma)/singamma

lattice="%f 0.0  0.0  %f %f  0.0  %f %f %f"%(a,b*cosgamma, b*singamma, c*cosbeta, c*angfac1, c* angfac2)

xyz_lines = str(num_atoms) + "\n"
xyz_lines +='Lattice="' + lattice +'"\n'
for i in range(len(all_lines)):
   if "Atoms # charge" in all_lines[i]:
      line_num = i
      break
del all_lines[0:line_num+2]
del all_lines[num_atoms:]

atoms = []  
for i in range(num_atoms):  
    line = all_lines[i].split()
    atoms.append([int(line[0]), int(line[1]), float(line[3]), float(line[4]), float(line[5])])

atoms.sort()

for atom in atoms:
   xyz_lines += "%s   %f   %f   %f\n"%(atom_symbol[atom[1]], atom[2],atom[3],atom[4])

with open("input.xyz", "w") as f:
    f.write(xyz_lines)
