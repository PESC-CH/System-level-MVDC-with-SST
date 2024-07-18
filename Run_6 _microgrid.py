#%% System Level Modeling and Simulation of MVDC Microgrids featuring Solid State Transformers
#%% Tutorial given by Daniel Siemaszko on 5th August at IEEE ICDCM 2024, Columbia SC
#%% Hands on examples run with Powersys Aesim Simba
#%% Python Script for runing SST_DCMicroGrid_Models.jsimba
#%% Model 6 DCMicrogrod
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
sst_model = project.GetDesignByName("6 DCMicrogrid")
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
t = np.array(job.TimePoints) + 5
VAFE = np.array(job.GetSignalByName('Sc6:V_AFE - Instantaneous Voltage').DataPoints)/1000
IAFE = np.array(job.GetSignalByName('Sc6:I_AFE - Instantaneous Current').DataPoints)

VPCC = np.array(job.GetSignalByName('Sc6:PCC - Out').DataPoints)
VPFE1 = np.array(job.GetSignalByName('Sc6:V_PFE1 - Instantaneous Voltage').DataPoints)
VPFE2 = np.array(job.GetSignalByName('Sc6:V_PFE2 - Instantaneous Voltage').DataPoints)
VPFE3 = np.array(job.GetSignalByName('Sc6:V_PFE3 - Instantaneous Voltage').DataPoints)
VPFE4 = np.array(job.GetSignalByName('Sc6:V_PFE4 - Instantaneous Voltage').DataPoints)
VPFE5 = np.array(job.GetSignalByName('Sc6:V_PFE5 - Instantaneous Voltage').DataPoints)
IPFE1 = np.array(job.GetSignalByName('Sc6:I_PFE1 - Instantaneous Current').DataPoints)
IPFE2 = np.array(job.GetSignalByName('Sc6:I_PFE2 - Instantaneous Current').DataPoints)
IPFE3 = np.array(job.GetSignalByName('Sc6:I_PFE3 - Instantaneous Current').DataPoints)
IPFE4 = np.array(job.GetSignalByName('Sc6:I_PFE4 - Instantaneous Current').DataPoints)
IPFE5 = np.array(job.GetSignalByName('Sc6:I_PFE5 - Instantaneous Current').DataPoints)

VL1PCC = np.array(job.GetSignalByName('Sc19:PCC - Out').DataPoints)
VL1PFE1 = np.array(job.GetSignalByName('Sc19:V_PFE1 - Instantaneous Voltage').DataPoints)
VL1PFE2 = np.array(job.GetSignalByName('Sc19:V_PFE2 - Instantaneous Voltage').DataPoints)
VL1PFE3 = np.array(job.GetSignalByName('Sc19:V_PFE3 - Instantaneous Voltage').DataPoints)
IL1AFE = np.array(job.GetSignalByName('Sc19:I_AFE - Instantaneous Current').DataPoints)
IL1PFE1 = np.array(job.GetSignalByName('Sc19:I_PFE1 - Instantaneous Current').DataPoints)
IL1PFE2 = np.array(job.GetSignalByName('Sc19:I_PFE2 - Instantaneous Current').DataPoints)*2
IL1PFE3 = np.array(job.GetSignalByName('Sc19:I_PFE3 - Instantaneous Current').DataPoints)

VL2PCC = np.array(job.GetSignalByName('Sc5:PCC - Out').DataPoints)
VL2PFE1 = np.array(job.GetSignalByName('Sc5:V_PFE1 - Instantaneous Voltage').DataPoints)
VL2PFE2 = np.array(job.GetSignalByName('Sc5:V_PFE2 - Instantaneous Voltage').DataPoints)
VL2PFE3 = np.array(job.GetSignalByName('Sc5:V_PFE3 - Instantaneous Voltage').DataPoints)
IL2AFE = np.array(job.GetSignalByName('Sc5:I_AFE - Instantaneous Current').DataPoints)
IL2PFE1 = np.array(job.GetSignalByName('Sc5:I_PFE1 - Instantaneous Current').DataPoints)
IL2PFE2 = np.array(job.GetSignalByName('Sc5:I_PFE2 - Instantaneous Current').DataPoints)
IL2PFE3 = np.array(job.GetSignalByName('Sc5:I_PFE3 - Instantaneous Current').DataPoints)

#%% Plot Curve

fig1, (ax1,ax2,ax3) = plt.subplots(3, 1, sharex=True)
ax1.set_title('MVDC Bus Currents and Voltages')
ax1.plot(t, VAFE, label='V_MVDC')
ax1.set_ylim(9, 11)
ax1.set_ylabel('Voltage [kV]')
ax1.grid(True)
ax1.legend(loc='lower left',fancybox=True, shadow=True, ncol=4)
ax2.plot(t, -IAFE, label='IAFE')
ax2.set_ylim(-300, 200)
ax2.set_ylabel('Current [A]')
ax2.grid(True)
ax2.legend(loc='lower left',fancybox=True, shadow=True, ncol=3)
ax3.plot(t, IPFE1, label='H2')
ax3.plot(t, IPFE4, label='LVDC res')
ax3.plot(t, IPFE2, label='PV')
ax3.plot(t, IPFE5, label='LVDC DtC')
ax3.plot(t, IPFE3, label='Train')
ax3.set_ylim(-400, 200)
ax3.set_xlim(5, 21)
ax3.set_ylabel('Current [A]')
ax3.set_xlabel('time [H]')
ax3.grid(True)
ax3.legend(loc='lower left',fancybox=True, shadow=True, ncol=3)
fig1.set_figheight(fig1.get_figheight()*1.5)

fig2, (ax1,ax2) = plt.subplots(2, 1, sharex=True)
ax1.set_title('LVDC car charging with PV and peak-shaving')
ax1.plot(t, VL1PCC, label='VPCC')
ax1.set_ylim(0, 1200)
ax1.set_ylabel('Voltages [V]')
ax1.grid(True)
ax1.legend(loc='lower left',fancybox=True, shadow=True, ncol=4)
ax2.plot(t, IL2AFE, label='IAFE')
ax2.plot(t, IL2PFE1, label='BESS')
ax2.plot(t, IL2PFE2, label='Car')
ax2.plot(t, IL2PFE3, label='PV')
ax2.set_ylim(-900, 600)
ax2.set_xlim(5, 21)
ax2.set_ylabel('Currents [A]')
ax2.set_xlabel('time [h]')
ax2.grid(True)
ax2.legend(loc='lower left',fancybox=True, shadow=True, ncol=4)

fig3, (ax1,ax2) = plt.subplots(2, 1, sharex=True)
ax1.set_title('High availability Data Centre with UPS')
ax1.plot(t, VL2PCC, label='VPCC')
ax1.set_ylim(0, 1200)
ax1.set_ylabel('Voltages [V]')
ax1.grid(True)
ax1.legend(loc='lower left',fancybox=True, shadow=True, ncol=4)
ax2.plot(t, IL1AFE, label='IAFE')
#ax2.plot(t, IL1PFE2, label='DtC1')
ax2.plot(t, IL1PFE2, label='DtC')
ax2.plot(t, IL1PFE3, label='UPS')
ax2.set_ylim(-900, 600)
ax2.set_xlim(5, 21)
ax2.set_ylabel('Currents [A]')
ax2.set_xlabel('time [h]')
ax2.grid(True)
ax2.legend(loc='lower left',fancybox=True, shadow=True, ncol=4)

plt.show()
# %%
