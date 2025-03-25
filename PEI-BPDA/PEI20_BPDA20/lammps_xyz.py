#!/usr/bin/python3

import sys
import os
import math

atom_symbol = [" ","C", "H", "O", "N", "S"]
if len(sys.argv) > 1:
    with open(sys.argv[1], "r") as f:
        all_lines = f.readlines()
else:
    with open("final.lammps", "r") as f:
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

xy = 0.0
xz = 0.0
yz = 0.0
line = all_lines[8].split()
if len(line) > 5:
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

lattice="%f 0.0  0.0  0.0 %f  0.0  0.0 0.0 %f"%(a,b,c)

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
    ix = 0
    iy = 0
    iz = 0
    if len(line) > 6:
        ix = int(line[6])
        iy = int(line[7])
        iz = int(line[8])
    x = float(line[3]) + ix * a + iy * xy + iz * xz
    y = float(line[4]) + iy * (yhi-ylo) + iz * yz
    z = float(line[5]) + iz * (zhi-zlo)

    atoms.append([int(line[0]), int(line[1]), x,y,z])

atoms.sort()

#first 10 chains have 138 atoms each
for i in range(10):
    x = atoms[i*138][2]
    y = atoms[i*138][3]
    z = atoms[i*138][4]
    xshift = round(x/a) * a
    yshift = round(y/b) * b
    zshift = round(z/c) * c
    for j in range(138):
        atoms[i*138+j][2] -= xshift
        atoms[i*138+j][3] -= yshift
        atoms[i*138+j][4] -= zshift
#second 20 chains have 120 atoms each
for i in range(20):
    x = atoms[1380+i*120][2]
    y = atoms[1380+i*120][3]
    z = atoms[1380+i*120][4]
    xshift = round(x/a) * a
    yshift = round(y/b) * b
    zshift = round(z/c) * c
    for j in range(120):
        atoms[1380+i*120+j][2] -= xshift
        atoms[1380+i*120+j][3] -= yshift
        atoms[1380+i*120+j][4] -= zshift
#last 10 chains have 138 atoms each
for i in range(10):
    x = atoms[1380 + 120 * 20 +i*138][2]
    y = atoms[1380 + 120 * 20 +i*138][3]
    z = atoms[1380 + 120 * 20 +i*138][4]
    xshift = round(x/a) * a
    yshift = round(y/b) * b
    zshift = round(z/c) * c
    for j in range(138):
        atoms[1380 + 120 * 20 +i*138+j][2] -= xshift
        atoms[1380 + 120 * 20 +i*138+j][3] -= yshift
        atoms[1380 + 120 * 20 +i*138+j][4] -= zshift

for atom in atoms:
   xyz_lines += "%s   %f   %f   %f\n"%(atom_symbol[atom[1]], atom[2],atom[3],atom[4])

with open("final.xyz", "w") as f:
    f.write(xyz_lines)
