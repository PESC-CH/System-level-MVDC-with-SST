#%%  Load required module
import matplotlib.pyplot as plt
from aesim.simba import Design, JsonProjectRepository
import os, pathlib
import numpy as np
import math

#%%  Open Design
filepath = os.path.join(pathlib.Path().absolute(), "SST_Switched_Model.jsimba")
print("loading model: "+filepath)
project = JsonProjectRepository(filepath) # Open file
sst_model_1 = project.GetDesignByName("Semiconductor level Blocks - Voltage Control")
sst_model_2 = project.GetDesignByName("System level SST Block")

#%%  List of all variables
variables_1 = sst_model_1.Circuit.Variables
for variable_1 in variables_1:
    print("Name:" + variable_1.Name + "\t Value:" + variable_1.Value)
variables_2 = sst_model_2.Circuit.Variables
for variable_2 in variables_2:
    print("Name:" + variable_2.Name + "\t Value:" + variable_2.Value)

#%% Find a device in a subcircuit
#Sc2 = design.Circuit.GetDeviceByName("Sc2").Definition
#Sc2_Sc1 =  Sc2.GetDeviceByName("Sc1").Definition
#Sc2_Sc1_Sc2 =  Sc2_Sc1.GetDeviceByName("Sc2").Definition
#PID1 = Sc2_Sc1_Sc2.GetDeviceByName("PID1")
#PID1.Ki = "333"

#%%  Run Simulation
job_1 = sst_model_1.TransientAnalysis.NewJob()
status = job_1.Run()

job_2 = sst_model_2.TransientAnalysis.NewJob()
status = job_2.Run()

#%% Get results
t = job_1.TimePoints
V_C1 = np.array(job_1.GetSignalByName('C1 - Instantaneous Voltage').DataPoints)
I_C1 = np.array(job_1.GetSignalByName('CP3 - Instantaneous Current').DataPoints)
I_C1_RMS = np.array(job_1.GetSignalByName('RMS1 - Out').DataPoints)
I_L1 = np.array(job_1.GetSignalByName('CCS1 - Instantaneous Current').DataPoints)
V_C2 = np.array(job_2.GetSignalByName('Sc4:Sc1:V_SEC - Instantaneous Voltage').DataPoints)
I_C2 = np.array(job_2.GetSignalByName('Sc4:Sc1:I_SEC - Instantaneous Current').DataPoints)
I_L2 = np.array(job_2.GetSignalByName('Sc4:Sc1:I_LOAD - Instantaneous Current').DataPoints)

#%% Plot Curve

fig1, (ax1,ax2) = plt.subplots(2, 1, sharex=True)
ax1.set_title('Load Current Step Response and Perturbations')
ax1.plot(t, V_C1, label='Switching Model')
ax1.plot(t, V_C2, label='Average Model')
ax1.set_ylim(1800, 2200)
ax1.set_ylabel('Secondary side Capacitor Voltage [V]')
ax1.grid(True)
ax1.legend(loc='lower left',fancybox=True, shadow=True, ncol=2)
ax2.plot(t, I_C1, label='Switching Model')
ax2.plot(t, I_L1, label='Load step')
ax2.plot(t, I_C1_RMS, label='Switching Model - RMS')
ax2.plot(t, -I_C2, label='Average Model')
ax2.set_ylim(-1200, 700)
ax2.set_xlim(0, 0.06)
ax2.set_ylabel('Load Current [A]')
ax2.set_xlabel('time [s]')
ax2.grid(True)
ax2.legend(loc='lower left',fancybox=True, shadow=True, ncol=2)

plt.show()
# %%
