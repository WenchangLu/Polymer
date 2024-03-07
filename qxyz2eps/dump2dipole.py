#!$(which python3)
import numpy as np
import sys

def dump2dipole(fName,groups,flagDebug=False, hardCoded=False):

    N_group = len(groups)
    with open(fName,'r') as f:
        for _ in range(3):
            next(f)

        # total number of atoms
        Natom = int(next(f).strip().split()[0])

        next(f)

        # compute the volume
        xtem=np.array(next(f).strip().split(),dtype=np.float)
        ytem=np.array(next(f).strip().split(),dtype=np.float)
        ztem=np.array(next(f).strip().split(),dtype=np.float)
        if len(xtem) == 3:
            xlo,xhi, xy=xtem
            ylo,yhi, yz=ytem
            zlo,zhi, xz=ztem
        else:
            xlo,xhi=xtem
            ylo,yhi=ytem
            zlo,zhi=ztem
            xy = 0.0
            yz = 0.0
            xz = 0.0
            
        Lx,Ly,Lz = xhi-xlo,yhi-ylo,zhi-zlo
        Volume = Lx*Ly*Lz

        column_names = next(f).strip().split()[2:]

        N_column = len(column_names)
        column_index = {column_names[t]:t for t in range(N_column)}
        atomid_index = column_index['id']
        qxyz_index = [column_index[t] for t in ['q','xu','yu','zu']]

        N_lines = int(9)
        for _ in f:
            N_lines +=1
        N_lines_block = Natom+9
        N_blocks = int(np.floor(N_lines/N_lines_block))

        if flagDebug: print(N_lines,Natom,xlo,zhi,Volume,column_names,N_column,N_blocks,N_group)

        dipole_group = np.zeros([N_blocks,N_group,3])
        qxyz = np.zeros([Natom,4])
        f.seek(0)

        for i_line in range(N_lines):
            line = next(f)

            # number of time step
            i_block = i_line//N_lines_block

            # relative line in one time step
            j_line = i_line%N_lines_block

            if j_line<9:
                continue

            words = line.strip().split()

            atom_id = int(words[column_index['id']])

            qxyz[atom_id-1,:]=np.array([words[t] for t in qxyz_index],dtype=np.float)
            
            if j_line==N_lines_block-1:
                for iGroup in range(N_group):

                    # i0_atom and i1_atom are the start and end atom id
                    i0_atom = groups[iGroup][0]-1
                    i1_atom = groups[iGroup][1]

                    # neutralize the charge within the group
                    qxyz[i0_atom:i1_atom,0] -= qxyz[i0_atom:i1_atom,0].mean()
                    dipole_group[i_block,iGroup,:] = np.dot(
                            qxyz[i0_atom:i1_atom,:1].T,
                            qxyz[i0_atom:i1_atom,1:])
    if flagDebug:
        for iGroup in range(N_group):
            fName = 'dipole_group'+str(iGroup)+'.txt'
            np.savetxt(fName,dipole_group[:,iGroup,:])
    return Volume,dipole_group.sum(axis=1)[0:,:]
