import math
with open("wrapped_1unit.xyz", "r") as f:
    all_lines = f.readlines()
num_atoms = int(all_lines[0])
atoms = []
x0 = 0.0
y0 = 0.0
for i in range(num_atoms):
    line = all_lines[i+2].split()
    x = float(line[1]) 
    y = float(line[2])
    z = float(line[3])
    x0 += x
    y0 += y
    atoms.append([line[0], x,y,z ] )

x0 = x0/float(num_atoms)
y0 = y0/float(num_atoms)

lammps_input = "LAMMPS data file\n"
lammps_input += "%d atoms \n"%(num_atoms *4)
lammps_input += "3 atom types \n"
lammps_input += "0.0  48.0  xlo  xhi\n"
lammps_input += "0.0  6.0   ylo  yhi\n"
lammps_input += "17.398031476913488 229.293570523084 zlo zhi\n"
lammps_input += "0.0 0.00 0.0 xy xz yz\n"

lammps_input += """
Masses

1 12.0107
2 18.998404
3 1.00794

Atoms # charge

"""

dict_atoms = { "C" :1, "F" :2, "H" :3}

id_atom = 0
for ix in range(4):
    alpha = 3.1415926/4.0 * ix
    for atom in atoms:
        x = (atom[1] - x0) * math.cos(alpha) + (atom[2] - y0) * math.sin(alpha)
        y = (atom[1] - x0) * math.sin(alpha) - (atom[2] - y0) * math.cos(alpha)

        x = x + x0 + ix * 7.0
        y = y + y0
        z = atom[3]
        itype = dict_atoms[atom[0]]

        id_atom += 1
        lammps_input += "%d  %s  0.0  %f %f %f \n"%(id_atom, itype, x, y, z)

print(lammps_input)
