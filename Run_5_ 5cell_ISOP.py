#%% System Level Modeling and Simulation of MVDC Microgrids featuring Solid State Transformers
#%% Tutorial given by Daniel Siemaszko on 5th August at IEEE ICDCM 2024, Columbia SC
#%% Hands on examples run with Powersys Aesim Simba
#%% Python Script for runing SST_DCMicroGrid_Models.jsimba
#%% Model 5 MultiCell ISOP SST
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
sst_model = project.GetDesignByName("5 MultiCell ISOP SST")
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
VLVDC = np.array(job.GetSignalByName('Sc2:V_LOAD - Instantaneous Voltage').DataPoints)
ILVDC = np.array(job.GetSignalByName('Sc2:I_LOAD - Instantaneous Current').DataPoints)

VPCC = np.array(job.GetSignalByName('Sc1:Sc1:V_PCC - Instantaneous Voltage').DataPoints)
VCELL1 = np.array(job.GetSignalByName('Sc1:Sc1:V_CELL1 - Instantaneous Voltage').DataPoints)
VCELL2 = np.array(job.GetSignalByName('Sc1:Sc1:V_CELL2 - Instantaneous Voltage').DataPoints)
VCELL3 = np.array(job.GetSignalByName('Sc1:Sc1:V_CELL3 - Instantaneous Voltage').DataPoints)
VCELL4 = np.array(job.GetSignalByName('Sc1:Sc1:V_CELL4 - Instantaneous Voltage').DataPoints)
VCELL5 = np.array(job.GetSignalByName('Sc1:Sc1:V_CELL5 - Instantaneous Voltage').DataPoints)
IGRID = np.array(job.GetSignalByName('Sc1:Sc1:I_GRID - Instantaneous Current').DataPoints)
ICELL1 = np.array(job.GetSignalByName('Sc1:Sc1:I_CELL1 - Instantaneous Current').DataPoints)
ICELL2 = np.array(job.GetSignalByName('Sc1:Sc1:I_CELL2 - Instantaneous Current').DataPoints)
ICELL3 = np.array(job.GetSignalByName('Sc1:Sc1:I_CELL3 - Instantaneous Current').DataPoints)
ICELL4 = np.array(job.GetSignalByName('Sc1:Sc1:I_CELL4 - Instantaneous Current').DataPoints)
ICELL5 = np.array(job.GetSignalByName('Sc1:Sc1:I_CELL5 - Instantaneous Current').DataPoints)

VSEC1 = np.array(job.GetSignalByName('Sc1:Sc2:Sc1:V_SEC - Instantaneous Voltage').DataPoints)
VSEC2 = np.array(job.GetSignalByName('Sc1:Sc3:Sc1:V_SEC - Instantaneous Voltage').DataPoints)
VSEC3 = np.array(job.GetSignalByName('Sc1:Sc4:Sc1:V_SEC - Instantaneous Voltage').DataPoints)
VSEC4 = np.array(job.GetSignalByName('Sc1:Sc5:Sc1:V_SEC - Instantaneous Voltage').DataPoints)
VSEC5 = np.array(job.GetSignalByName('Sc1:Sc6:Sc1:V_SEC - Instantaneous Voltage').DataPoints)
ISEC1 = np.array(job.GetSignalByName('Sc1:Sc2:Sc1:I_SEC - Instantaneous Current').DataPoints)
ISEC2 = np.array(job.GetSignalByName('Sc1:Sc3:Sc1:I_SEC - Instantaneous Current').DataPoints)
ISEC3 = np.array(job.GetSignalByName('Sc1:Sc4:Sc1:I_SEC - Instantaneous Current').DataPoints)
ISEC4 = np.array(job.GetSignalByName('Sc1:Sc5:Sc1:I_SEC - Instantaneous Current').DataPoints)
ISEC5 = np.array(job.GetSignalByName('Sc1:Sc6:Sc1:I_SEC - Instantaneous Current').DataPoints)

I_AFE = np.array(job.GetSignalByName('Sc4:I_AFE - Instantaneous Current').DataPoints)
V_AFE = np.array(job.GetSignalByName('Sc4:V_AFE - Instantaneous Voltage').DataPoints)

#%% Plot Curve

fig1, (ax1,ax2) = plt.subplots(2, 1, sharex=True)
ax1.set_title('MultiCell ISOP SST - LVDC Currents and Voltages')
ax1.plot(t, VLVDC, label='V_LVDC')
ax1.set_ylim(0, 1500)
ax1.set_ylabel('Voltages [V]')
ax1.grid(True)
ax1.legend(loc='lower left',fancybox=True, shadow=True, ncol=2)
ax2.plot(t, ILVDC, label='I_LVDC')
ax2.set_ylim(-5000, 5000)
ax2.set_xlim(0, 0.1)
ax2.set_ylabel('Currents [V]')
ax2.set_xlabel('time [s]')
ax2.grid(True)
ax2.legend(loc='lower left',fancybox=True, shadow=True, ncol=2)

fig2, (ax1,ax2) = plt.subplots(2, 1, sharex=True)
ax1.set_title('MultiCell ISOP SST - Cell Secondary Currents and Voltages')
ax1.plot(t, VSEC1, label='V1')
ax1.plot(t, VSEC2, label='V2')
ax1.plot(t, VSEC3, label='V3')
ax1.plot(t, VSEC4, label='V4')
ax1.plot(t, VSEC5, label='V5')
ax1.set_ylim(1600, 2400)
ax1.set_ylabel('Voltages [V]')
ax1.grid(True)
ax1.legend(loc='lower left',fancybox=True, shadow=True, ncol=6)
ax2.plot(t, ISEC1, label='I1')
ax2.plot(t, ISEC2, label='I2')
ax2.plot(t, ISEC3, label='I3')
ax2.plot(t, ISEC4, label='I4')
ax2.plot(t, ISEC5, label='I5')
ax2.set_ylim(-1500, 1000)
ax2.set_xlim(0, 0.1)
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
ax2.set_ylim(-3000, 1500)
ax2.set_xlim(0, 0.1)
ax2.set_ylabel('Currents [V]')
ax2.set_xlabel('time [s]')
ax2.grid(True)
ax2.legend(loc='lower left',fancybox=True, shadow=True, ncol=5)

fig4, (ax1,ax2) = plt.subplots(2, 1, sharex=True)
ax1.set_title('MultiCell IPOS SST - MVDC Active Front End')
ax1.plot(t, I_AFE, label='I_AFE')
ax1.set_ylim(-1000, 1000)
ax1.set_ylabel('Current [A]')
ax1.grid(True)
ax1.legend(loc='lower left',fancybox=True, shadow=True, ncol=2)
ax2.plot(t, V_AFE, label='V_AFE')
ax2.set_ylim(0, 15000)
ax2.set_xlim(0, 0.1)
ax2.set_ylabel('Voltage [V]')
ax2.set_xlabel('time [s]')
ax2.grid(True)
ax2.legend(loc='lower left',fancybox=True, shadow=True)

plt.show()
# %%
