#%% System Level Modeling and Simulation of MVDC Microgrids featuring Solid State Transformers
#%% Tutorial given by Daniel Siemaszko on 5th August at IEEE ICDCM 2024, Columbia SC
#%% Hands on examples run with Powersys Aesim Simba
#%% Python Script for runing SST_DCMicroGrid_Models.jsimba
#%% Model 4 MultiCell IPOS SST
#%% https://github.com/PESC-CH/System-level-MVDC-with-SST/

#%%  Load required module
import matplotlib.pyplot as plt
from aesim.simba import Design, JsonProjectRepository
import os, pathlib
import numpy as np
import math

#%%  Open Design
filepath = os.path.join(pathlib.Path().absolute(), "SST_DCMicroGrid_Models.jsimba")
print("loading model: "+filepath)
project = JsonProjectRepository(filepath) # Open file
sst_model = project.GetDesignByName("4 MultiCell IPOS SST")
print("loading model: "+sst_model.Name)

#%%  List of all variables
variables = sst_model.Circuit.Variables
for variable in variables:
    print("Name:" + variable.Name + "\t Value:" + variable.Value)

#%%  Run Simulation
job = sst_model.TransientAnalysis.NewJob()
print("-> Job Started ")
status = job.Run()

#%% Get results
t = job.TimePoints
VMVDCp = np.array(job.GetSignalByName('Sc3:V_MVDCHI - Instantaneous Voltage').DataPoints)
VMVDCm = np.array(job.GetSignalByName('Sc3:V_MVDCLO - Instantaneous Voltage').DataPoints)
IMVDCp = np.array(job.GetSignalByName('Sc3:I_MVDCHI - Instantaneous Current').DataPoints)
IMVDCm = np.array(job.GetSignalByName('Sc3:I_MVDCLO - Instantaneous Current').DataPoints)

VPCC = np.array(job.GetSignalByName('Sc1:Sc1:V_PCC - Instantaneous Voltage').DataPoints)
VCELL1 = np.array(job.GetSignalByName('Sc1:Sc1:V_CELL1 - Instantaneous Voltage').DataPoints)
VCELL2 = np.array(job.GetSignalByName('Sc1:Sc1:V_CELL2 - Instantaneous Voltage').DataPoints)
VCELL3 = np.array(job.GetSignalByName('Sc1:Sc1:V_CELL3 - Instantaneous Voltage').DataPoints)
VCELL4 = np.array(job.GetSignalByName('Sc1:Sc1:V_CELL4 - Instantaneous Voltage').DataPoints)
VCELL5 = np.array(job.GetSignalByName('Sc1:Sc1:V_CELL5 - Instantaneous Voltage').DataPoints)
VCELL6 = np.array(job.GetSignalByName('Sc1:Sc1:V_CELL6 - Instantaneous Voltage').DataPoints)
VCELL7 = np.array(job.GetSignalByName('Sc1:Sc1:V_CELL7 - Instantaneous Voltage').DataPoints)
VCELL8 = np.array(job.GetSignalByName('Sc1:Sc1:V_CELL8 - Instantaneous Voltage').DataPoints)
VCELL9 = np.array(job.GetSignalByName('Sc1:Sc1:V_CELL9 - Instantaneous Voltage').DataPoints)
VCELL10 = np.array(job.GetSignalByName('Sc1:Sc1:V_CELL10 - Instantaneous Voltage').DataPoints)
IGRID = np.array(job.GetSignalByName('Sc1:Sc1:I_GRID - Instantaneous Current').DataPoints)
ICELL1 = np.array(job.GetSignalByName('Sc1:Sc1:I_CELL1 - Instantaneous Current').DataPoints)
ICELL2 = np.array(job.GetSignalByName('Sc1:Sc1:I_CELL2 - Instantaneous Current').DataPoints)
ICELL3 = np.array(job.GetSignalByName('Sc1:Sc1:I_CELL3 - Instantaneous Current').DataPoints)
ICELL4 = np.array(job.GetSignalByName('Sc1:Sc1:I_CELL4 - Instantaneous Current').DataPoints)
ICELL5 = np.array(job.GetSignalByName('Sc1:Sc1:I_CELL5 - Instantaneous Current').DataPoints)
ICELL6 = np.array(job.GetSignalByName('Sc1:Sc1:I_CELL6 - Instantaneous Current').DataPoints)
ICELL7 = np.array(job.GetSignalByName('Sc1:Sc1:I_CELL7 - Instantaneous Current').DataPoints)
ICELL8 = np.array(job.GetSignalByName('Sc1:Sc1:I_CELL8 - Instantaneous Current').DataPoints)
ICELL9 = np.array(job.GetSignalByName('Sc1:Sc1:I_CELL9 - Instantaneous Current').DataPoints)
ICELL10 = np.array(job.GetSignalByName('Sc1:Sc1:I_CELL10 - Instantaneous Current').DataPoints)

VSEC1 = np.array(job.GetSignalByName('Sc1:Sc2:Sc1:V_SEC - Instantaneous Voltage').DataPoints)
VSEC2 = np.array(job.GetSignalByName('Sc1:Sc3:Sc1:V_SEC - Instantaneous Voltage').DataPoints)
VSEC3 = np.array(job.GetSignalByName('Sc1:Sc4:Sc1:V_SEC - Instantaneous Voltage').DataPoints)
VSEC4 = np.array(job.GetSignalByName('Sc1:Sc5:Sc1:V_SEC - Instantaneous Voltage').DataPoints)
VSEC5 = np.array(job.GetSignalByName('Sc1:Sc6:Sc1:V_SEC - Instantaneous Voltage').DataPoints)
VSEC6 = np.array(job.GetSignalByName('Sc1:Sc7:Sc1:V_SEC - Instantaneous Voltage').DataPoints)
VSEC7 = np.array(job.GetSignalByName('Sc1:Sc8:Sc1:V_SEC - Instantaneous Voltage').DataPoints)
VSEC8 = np.array(job.GetSignalByName('Sc1:Sc9:Sc1:V_SEC - Instantaneous Voltage').DataPoints)
VSEC9 = np.array(job.GetSignalByName('Sc1:Sc10:Sc1:V_SEC - Instantaneous Voltage').DataPoints)
VSEC10 = np.array(job.GetSignalByName('Sc1:Sc11:Sc1:V_SEC - Instantaneous Voltage').DataPoints)
ISEC1 = np.array(job.GetSignalByName('Sc1:Sc2:Sc1:I_SEC - Instantaneous Current').DataPoints)
ISEC2 = np.array(job.GetSignalByName('Sc1:Sc3:Sc1:I_SEC - Instantaneous Current').DataPoints)
ISEC3 = np.array(job.GetSignalByName('Sc1:Sc4:Sc1:I_SEC - Instantaneous Current').DataPoints)
ISEC4 = np.array(job.GetSignalByName('Sc1:Sc5:Sc1:I_SEC - Instantaneous Current').DataPoints)
ISEC5 = np.array(job.GetSignalByName('Sc1:Sc6:Sc1:I_SEC - Instantaneous Current').DataPoints)
ISEC6 = np.array(job.GetSignalByName('Sc1:Sc7:Sc1:I_SEC - Instantaneous Current').DataPoints)
ISEC7 = np.array(job.GetSignalByName('Sc1:Sc8:Sc1:I_SEC - Instantaneous Current').DataPoints)
ISEC8 = np.array(job.GetSignalByName('Sc1:Sc9:Sc1:I_SEC - Instantaneous Current').DataPoints)
ISEC9 = np.array(job.GetSignalByName('Sc1:Sc10:Sc1:I_SEC - Instantaneous Current').DataPoints)
ISEC10 = np.array(job.GetSignalByName('Sc1:Sc11:Sc1:I_SEC - Instantaneous Current').DataPoints)

I_AFE = np.array(job.GetSignalByName('Sc2:I_AFE - Instantaneous Current').DataPoints)
V_AFE = np.array(job.GetSignalByName('Sc2:V_AFE - Instantaneous Voltage').DataPoints)

#%% Plot Curve

fig1, (ax1,ax2) = plt.subplots(2, 1, sharex=True)
ax1.set_title('MultiCell IPOS SST - MVDC Currents and Voltages')
ax1.plot(t, VMVDCp, label='V_MVDC+')
ax1.plot(t, VMVDCm, label='V_MVDC-')
ax1.set_ylim(8000, 12000)
ax1.set_ylabel('Voltages [V]')
ax1.grid(True)
ax1.legend(loc='lower left',fancybox=True, shadow=True, ncol=2)
ax2.plot(t, IMVDCp, label='I_MVDC+')
ax2.plot(t, IMVDCm, label='I_MVDC-')
ax2.set_ylim(-500, 500)
ax2.set_xlim(0, 0.2)
ax2.set_ylabel('Currents [V]')
ax2.set_xlabel('time [s]')
ax2.grid(True)
ax2.legend(loc='lower left',fancybox=True, shadow=True, ncol=2)

fig2, (ax1,ax2) = plt.subplots(2, 1, sharex=True)
ax1.set_title('MultiCell IPOS SST - Cell Secondary Currents and Voltages')
ax1.plot(t, VSEC1, label='V1')
ax1.plot(t, VSEC2, label='V2')
ax1.plot(t, VSEC3, label='V3')
ax1.plot(t, VSEC4, label='V4')
ax1.plot(t, VSEC5, label='V5')
ax1.plot(t, VSEC6, label='V6')
ax1.plot(t, VSEC7, label='V7')
ax1.plot(t, VSEC8, label='V8')
ax1.plot(t, VSEC9, label='V9')
ax1.plot(t, VSEC10, label='V10')
ax1.set_ylim(1600, 2400)
ax1.set_ylabel('Voltages [V]')
ax1.grid(True)
ax1.legend(loc='lower left',fancybox=True, shadow=True, ncol=6)
ax2.plot(t, ISEC1, label='I1')
ax2.plot(t, ISEC2, label='I2')
ax2.plot(t, ISEC3, label='I3')
ax2.plot(t, ISEC4, label='I4')
ax2.plot(t, ISEC5, label='I5')
ax2.plot(t, ISEC6, label='I6')
ax2.plot(t, ISEC7, label='I7')
ax2.plot(t, ISEC8, label='I8')
ax2.plot(t, ISEC9, label='I9')
ax2.plot(t, ISEC10, label='I10')
ax2.set_ylim(-1500, 1000)
ax2.set_xlim(0, 0.2)
ax2.set_ylabel('Currents [V]')
ax2.set_xlabel('time [s]')
ax2.grid(True)
ax2.legend(loc='lower left',fancybox=True, shadow=True, ncol=5)

fig3, (ax1,ax2) = plt.subplots(2, 1, sharex=True)
ax1.set_title('MultiCell IPOS SST - Cell Primary Currents and PCC Voltage')
##ax1.plot(t, VCELL1, label='V1')
##ax1.plot(t, VCELL2, label='V2')
##ax1.plot(t, VCELL3, label='V3')
##ax1.plot(t, VCELL4, label='V4')
##ax1.plot(t, VCELL5, label='V5')
##ax1.plot(t, VCELL6, label='V6')
##ax1.plot(t, VCELL7, label='V7')
##ax1.plot(t, VCELL8, label='V8')
##ax1.plot(t, VCELL9, label='V9')
##ax1.plot(t, VCELL10, label='V10')
ax1.plot(t, VPCC, label='VPCC')
ax1.set_ylim(0, 1500)
ax1.set_ylabel('Voltages [V]')
ax1.grid(True)
ax1.legend(loc='lower left',fancybox=True, shadow=True, ncol=5)
ax2.plot(t, ICELL1, label='I1')
ax2.plot(t, ICELL2, label='I2')
ax2.plot(t, ICELL3, label='I3')
ax2.plot(t, ICELL4, label='I4')
ax2.plot(t, ICELL5, label='I5')
ax2.plot(t, ICELL6, label='I6')
ax2.plot(t, ICELL7, label='I7')
ax2.plot(t, ICELL8, label='I8')
ax2.plot(t, ICELL9, label='I9')
ax2.plot(t, ICELL10, label='I10')
ax2.set_ylim(-3000, 1500)
ax2.set_xlim(0, 0.2)
ax2.set_ylabel('Currents [V]')
ax2.set_xlabel('time [s]')
ax2.grid(True)
ax2.legend(loc='lower left',fancybox=True, shadow=True, ncol=5)

fig4, (ax1,ax2) = plt.subplots(2, 1, sharex=True)
ax1.set_title('MultiCell IPOS SST - Active Front End')
ax1.plot(t, I_AFE, label='I_AFE')
ax1.set_ylim(-8000, 8000)
ax1.set_ylabel('Current [A]')
ax1.grid(True)
ax1.legend(loc='lower left',fancybox=True, shadow=True, ncol=2)
ax2.plot(t, V_AFE, label='V_AFE')
ax2.set_ylim(0, 1500)
ax2.set_xlim(0, 0.2)
ax2.set_ylabel('Voltage [V]')
ax2.set_xlabel('time [s]')
ax2.grid(True)
ax2.legend(loc='lower left',fancybox=True, shadow=True)

plt.show()
# %%
