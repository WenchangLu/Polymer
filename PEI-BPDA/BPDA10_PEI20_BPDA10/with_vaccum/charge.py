#!/usr/bin/python3
import numpy as np
import sys

with open('dump.qxyz.txt','r') as f:
    all_lines = f.readlines()
num_atoms = int(all_lines[3])
print(num_atoms)
tot_lines = len(all_lines)
qxyz = []
for i in range(tot_lines - num_atoms, tot_lines):
    qxyz.append(all_lines[i].split())

groups =[]

num_atom_pei = 138
num_atom_bpda = 120
for i in range(10):
    groups.append([i * num_atom_pei, (i+1) * num_atom_pei])
for i in range(20):
    groups.append([1380 +  i * num_atom_bpda, 1380 + (i+1) * num_atom_bpda])
for i in range(10):
    groups.append([3780 + i * num_atom_pei, 3780 + (i+1) * num_atom_pei])
print(groups)

for i in range(len(groups)):
    q_tot = 0.0
    for j in range(groups[i][0], groups[i][1]):
        q_tot += float(qxyz[j][1])
    print(i, q_tot)
