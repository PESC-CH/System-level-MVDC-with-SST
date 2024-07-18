#%% System Level Modeling and Simulation of MVDC Microgrids featuring Solid State Transformers
#%% Tutorial given by Daniel Siemaszko on 5th August at IEEE ICDCM 2024, Columbia SC
#%% Hands on examples run with Powersys Aesim Simba
#%% Python Script for runing SST_DCMicroGrid_Models.jsimba
#%% Model 3 Single SST with BESS and AFE
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
sst_model = project.GetDesignByName("3 Single SST with BESS and AFE")
print("loading model: "+sst_model.Name)

#%%  List of all variables
variables = sst_model.Circuit.Variables
print("loading variables: ")
for variable in variables:
    print("Name:" + variable.Name + "\t Value:" + variable.Value)

qbatt=10
Q_BATT = next(variable for variable in variables if variable.Name == "Q_BATT")
Q_BATT.Value=str(qbatt)
print("Name: Q_BATT" + "\t Value: " + str(qbatt))

#%%  Run Simulation
job = sst_model.TransientAnalysis.NewJob()
print("-> Job Started ")
status = job.Run()

#%% Get results
t = job.TimePoints
#AFE
I_AFE = np.array(job.GetSignalByName('Sc3:I_AFE - Instantaneous Current').DataPoints)
V_AFE = np.array(job.GetSignalByName('Sc3:V_AFE - Instantaneous Voltage').DataPoints)
#Batteries
I_BATT = np.array(job.GetSignalByName('Sc4:I_BATT - Instantaneous Current').DataPoints)
SOC_BATT = np.array(job.GetSignalByName('Sc4:Sc1:SOC - Out').DataPoints)
ISP_BATT = np.array(job.GetSignalByName('Sc2:I_SP - Out').DataPoints)
# SST
Vprim = np.array(job.GetSignalByName('Sc1:Sc1:V_PRIM - Instantaneous Voltage').DataPoints)
Isec = np.array(job.GetSignalByName('Sc1:Sc1:I_SEC - Instantaneous Current').DataPoints)
Vsec = np.array(job.GetSignalByName('Sc1:Sc1:V_SEC - Instantaneous Voltage').DataPoints)
Iprim = np.array(job.GetSignalByName('Sc1:Sc1:I_PRIM - Instantaneous Current').DataPoints)


#%% Plot Curve

fig1, (ax1,ax2) = plt.subplots(2, 1, sharex=True)
ax1.set_title('Single DAB SST with BESS and AFE - Active Front End')
ax1.plot(t, I_AFE, label='I_AFE')
ax1.plot(t, -Iprim, label='I_prim')
ax1.set_ylim(-2000, 2000)
ax1.set_ylabel('Current [A]')
ax1.grid(True)
ax1.legend(loc='lower left',fancybox=True, shadow=True, ncol=2)
ax2.plot(t, V_AFE, label='V_AFE')
ax2.plot(t, Vprim, label='V_prim')
ax2.set_ylim(0, 1500)
ax2.set_xlim(0, 0.1)
ax2.set_ylabel('Voltage [V]')
ax2.set_xlabel('time [s]')
ax2.grid(True)
ax2.legend(loc='lower left',fancybox=True, shadow=True)

fig2, (ax1,ax2) = plt.subplots(2, 1, sharex=True)
ax1.set_title('Single DAB SST with BESS and AFE - Battery')
ax1.plot(t, ISP_BATT, label='SPI_BATT')
ax1.plot(t, I_BATT, label='I_BATT')
ax1.plot(t, -Isec, label='I_sec')
ax1.set_ylim(-500, 500)
ax1.set_ylabel('Current [A]')
ax1.grid(True)
ax1.legend(loc='lower left',fancybox=True, shadow=True, ncol=2)
ax2.plot(t, 100*SOC_BATT, label='SOC_BATT')
ax2.set_ylim(0, 100)
ax2.set_xlim(0, 0.1)
ax2.set_ylabel('State of Charge [%]')
ax2.set_xlabel('time [s]')
ax2.grid(True)
ax2.legend(loc='lower left',fancybox=True, shadow=True)
print("-> Job Done")
plt.show()
# %%
