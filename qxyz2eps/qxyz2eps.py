#!/usr/bin/python3

from dump2dipole import dump2dipole
import sys
import numpy as np

fName = sys.argv[1]
N_atom_group = sys.argv[2]
temperature = np.float(sys.argv[3])

box_volume,dipole_group_sum = dump2dipole(
        fName,flagDebug=True,N_atom_group=N_atom_group)

# dipole moment with time steps
np.savetxt('m.txt',np.column_stack((np.arange(len(dipole_group_sum)),dipole_group_sum)))

# camulative summation along the time steps
m_mean = dipole_group_sum.cumsum(axis=0)
mm_mean = (dipole_group_sum**2).cumsum(axis=0)

# divide by the cumulative length to get average
m_mean /= np.arange(1,1+len(m_mean)).reshape((len(m_mean),1))
mm_mean /= np.arange(1,1+len(mm_mean)).reshape((len(mm_mean),1))
np.savetxt('m_mean.txt',np.column_stack((np.arange(len(m_mean)),m_mean)))
m_var = mm_mean - m_mean**2

m_var[1:] *= (1+1./np.arange(1,len(m_var))).reshape((len(m_var)-1,1))
m_var[0,:] = 0
np.savetxt('m_var.txt',np.column_stack((np.arange(len(m_var)),m_var)))

# calculate vibrational K
unitConv_eps_au2gcs = 2099861.93766
eps = m_var/box_volume/temperature*unitConv_eps_au2gcs

print(eps)
np.savetxt('eps.txt',np.column_stack((np.arange(len(eps)),eps)))
