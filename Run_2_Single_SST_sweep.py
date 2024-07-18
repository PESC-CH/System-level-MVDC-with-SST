#%% System Level Modeling and Simulation of MVDC Microgrids featuring Solid State Transformers
#%% Tutorial given by Daniel Siemaszko on 5th August at IEEE ICDCM 2024, Columbia SC
#%% Hands on examples run with Powersys Aesim Simba
#%% Python Script for runing SST_DCMicroGrid_Models.jsimba
#%% Model 2 Single SST
#%% https://github.com/PESC-CH/System-level-MVDC-with-SST/

#%%  Load required module
import matplotlib.pyplot as plt
from aesim.simba import Design, JsonProjectRepository
import os, pathlib
import numpy as np
import math

#%%  Open Design
filepath = os.path.join(pathlib.Path().absolute(), "SST_DCMicroGrid_Models.jsimba")
print("loading file: "+filepath)
project = JsonProjectRepository(filepath) # Open file
sst_model = project.GetDesignByName("2 Single SST")
print("loading model: "+sst_model.Name)

#%%  List of all variables
variables = sst_model.Circuit.Variables
print("loading variables: ")
for variable in variables:
    print("Name: " + variable.Name + "\t Value: " + variable.Value)

#%%  Run Simulation
job = sst_model.TransientAnalysis.NewJob()
print("-> Job Started ")
status = job.Run()

#%% Get results
t = job.TimePoints
Vprim = np.array(job.GetSignalByName('Sc1:Sc1:V_PRIM - Instantaneous Voltage').DataPoints)
Isec = np.array(job.GetSignalByName('Sc1:Sc1:I_SEC - Instantaneous Current').DataPoints)
Vsec = np.array(job.GetSignalByName('Sc1:Sc1:V_SEC - Instantaneous Voltage').DataPoints)
Iprim = np.array(job.GetSignalByName('Sc1:Sc1:I_PRIM - Instantaneous Current').DataPoints)
Isrc = np.array(job.GetSignalByName('Sc1:Sc1:I_SRC - Instantaneous Current').DataPoints)
Iload = np.array(job.GetSignalByName('Sc1:Sc1:I_LOAD - Instantaneous Current').DataPoints)

#%% Plot Curve
fig1, (ax1,ax2) = plt.subplots(2, 1, sharex=True)
ax1.set_title('Single DAB SST voltage controlled - Load Step Response')
ax1.plot(t, Vprim, label='V_prim')
ax1.plot(t, Vsec, label='V_sec')
ax1.set_ylim(0, 2500)
ax1.set_ylabel('Voltages [V]')
ax1.grid(True)
ax1.legend(loc='lower left',fancybox=True, shadow=True, ncol=2)
ax2.plot(t, -Iload, label='I_load')
ax2.plot(t, -Iprim, label='I_prim')
ax2.plot(t, -Isec, label='I_sec')
ax2.set_ylim(-1000, 1000)
ax2.set_xlim(0, 0.1)
ax2.set_ylabel('Currents [V]')
ax2.set_xlabel('time [s]')
ax2.grid(True)
ax2.legend(loc='lower left',fancybox=True, shadow=True, ncol=4)

#%% Sweep Ki values KI_V = 500 -> 5000
print("-> Job Done")
print("-> Sweep PI parameter KI_V : 500 -> 5000")
i_limit=400
I_SST_LIMIT = next(variable for variable in variables if variable.Name == "I_SST_LIMIT")
I_SST_LIMIT.Value=str(i_limit)
print("Name: I_SST_LIMI" + "\t Value: " + str(i_limit))

ki_values = np.array([5000,2000,1000,500])

t_arr    = []
Vprim_arr = []
Vsec_arr = []
Iprim_arr = []
Isec_arr = []

#%% Iterate
for ki in ki_values:
    KI_V = next(variable for variable in variables if variable.Name == "KI_V")
    KI_V.Value=str(ki)
    print("Name: KI_V" + "\t Value: " + str(ki))
    
    # Run calculation
    job = sst_model.TransientAnalysis.NewJob()
    print("-> Job Started ")
    status = job.Run()

    #%% Get results
    t_arr.append(np.asarray(job.TimePoints))
    Vprim_arr.append(np.asarray(job.GetSignalByName('Sc1:Sc1:V_PRIM - Instantaneous Voltage').DataPoints))
    Isec_arr.append(np.asarray(job.GetSignalByName('Sc1:Sc1:I_SEC - Instantaneous Current').DataPoints))
    Vsec_arr.append(np.asarray(job.GetSignalByName('Sc1:Sc1:V_SEC - Instantaneous Voltage').DataPoints))
    Iprim_arr.append(np.asarray(job.GetSignalByName('Sc1:Sc1:I_PRIM - Instantaneous Current').DataPoints))

#%% Plot Curve
fig2, (ax1,ax2) = plt.subplots(2, 1, sharex=True)
ax1.set_title('Single DAB SST voltage controlled - Ki parameter sweep')
for i in range(len(Vsec_arr)):
    ax1.plot(np.asarray(t_arr[i]), np.asarray(Vsec_arr[i]), label='Vsec, ki = '+str(ki_values[i]))
ax1.set_ylim(0, 2500)
ax1.set_ylabel('Voltages [V]')
ax1.grid(True)
ax1.legend(loc='lower left')
for i in range(len(Iprim_arr)):
    ax2.plot(np.asarray(t_arr[i]), -np.asarray(Isec_arr[i]), label='I_sec, ki = '+str(ki_values[i]))
ax2.set_ylim(-500, 500)
ax2.set_xlim(0.025, 0.075)
ax2.set_ylabel('Currents [V]')
ax2.set_xlabel('time [s]')
ax2.grid(True)
ax2.legend(loc='lower left')

print("-> Job Done ")
plt.show()
# %%
