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
nu_1 = 20
nu_2 = 40
nu_3 = 20

n_1 = num_atom_pei * nu_1
n_2 = num_atom_pei * nu_1 + num_atom_bpda * nu_2
for i in range(nu_1):
    groups.append([i * num_atom_pei, (i+1) * num_atom_pei])
for i in range(nu_2):
    groups.append([n_1 +  i * num_atom_bpda, n_1 + (i+1) * num_atom_bpda])
for i in range(nu_3):
    groups.append([n_2 + i * num_atom_pei, n_2 + (i+1) * num_atom_pei])
#print(groups)

for i in range(len(groups)):
    q_tot = 0.0
    for j in range(groups[i][0], groups[i][1]):
        q_tot += float(qxyz[j][1])
    print(i, q_tot)
