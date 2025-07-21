#!/usr/bin/python3

from dump2dipole import dump2dipole
import sys
import numpy as np
from atom_group import *
# atom_group.py define the block of atoms and temperature, and dt
if len(sys.argv) == 2: 
    fName = sys.argv[1]
else:
    fName = "dump.qxyz.txt"


box_volume,dipole_group_sum = dump2dipole(
        fName,flagDebug=True,groups = groups)

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

eps_t = eps.sum(axis=1)/3.0
eps_f = np.fft.rfft(eps_t)

total_time = dt *float(len(eps_t))
print( len(eps_t), len(eps_f), total_time, dt)

freq = np.arange(len(eps_f))
np.savetxt('eps_f.txt',np.vstack((freq/total_time, eps_f.imag * freq, eps_f.real * freq)).T)
np.savetxt('eps_t.txt',eps_t)

