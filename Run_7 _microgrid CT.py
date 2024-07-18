#%% System Level Modeling and Simulation of MVDC Microgrids featuring Solid State Transformers
#%% Tutorial given by Daniel Siemaszko on 5th August at IEEE ICDCM 2024, Columbia SC
#%% Hands on examples run with Powersys Aesim Simba
#%% Python Script for runing SST_DCMicroGrid_Models.jsimba
#%% Model 7 DCMicrogrid CT
#%% https://github.com/PESC-CH/System-level-MVDC-with-SST/

#%% Continuous Time simulation

#%%  Load required module
from aesim.simba import Design, JsonProjectRepository
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *   # requires the installation tk package
import sys              # requires the installation os-sys package
import os, pathlib
import numpy as np
import math

#%%  DECLARE VARIABLES

array_t = []
array_VAFE = []
array_IAFE = []

array_IPFE1 = []
array_IPFE2 = []
array_IPFE3 = []
array_IPFE4 = []
array_IPFE5 = []

array_VL1PCC = []
array_IL1AFE = []
array_IL1PFE1 = []
array_IL1PFE2 = []
array_IL1PFE3 = []

array_VL2PCC = []
array_IL2AFE = []
array_IL2PFE1 = []
array_IL2PFE2 = []
array_IL2PFE3 = []

VAL_H2 = 0;
VAL_UPS = 0;
VAL_Batt = 0;

Nb_sim_points = 1000
Nb_display_points = 45000

#%%  DECLARE FUNCTIONS

def circuit_init():
    # Open Project Design
    filepath = os.path.join(pathlib.Path().absolute(), "SST_DCMicroGrid_Models.jsimba")
    print("loading model: " + filepath)
    # Open file
    project = JsonProjectRepository(filepath)
    sst_model = project.GetDesignByName("7 DCMicrogrid - CT")
    print("loading model: "+sst_model.Name)
    # Definitation of simulation
    sst_model.TransientAnalysis.NumberOfPointsToSimulate = Nb_sim_points
    job = sst_model.TransientAnalysis.NewJob()
    # Definition of changeable variables
    variables = sst_model.Circuit.Variables
    for variable in variables:
        print("Name: " + variable.Name + "\t Value: " + variable.Value)
    SP_H2 = next(variable for variable in variables if variable.Name == "SP_H2")
    SP_UPS = next(variable for variable in variables if variable.Name == "SP_dtc_UPS")
    SP_BESS = next(variable for variable in variables if variable.Name == "SP_res_Batt")
    return [job,SP_H2,SP_UPS,SP_BESS]

def graph_init():
    # Init Graph figure
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1)
    fig.set_figheight(fig.get_figheight()*1.5)
    # Attribution des lignes au graphiques
    ln_VAFE, = ax1.plot([], [])
    ln_VL1PCC, = ax1.plot([], [])
    ln_VL2PCC, = ax1.plot([], [])

    ln_IAFE, = ax2.plot([], [])
    ln_IPFE1, = ax2.plot([], [])
    ln_IPFE2, = ax2.plot([], [])
    ln_IPFE3, = ax2.plot([], [])
    ln_IPFE4, = ax2.plot([], [])
    ln_IPFE5, = ax2.plot([], [])

    ln_IL1AFE, = ax3.plot([], [])
    ln_IL1PFE1, = ax3.plot([], [])
    ln_IL1PFE2, = ax3.plot([], [])
    ln_IL1PFE3, = ax3.plot([], [])

    ln_IL2AFE, = ax4.plot([], [])
    ln_IL2PFE1, = ax4.plot([], [])
    ln_IL2PFE2, = ax4.plot([], [])
    ln_IL2PFE3, = ax4.plot([], [])

    # axis parameters
    ax1.set_title('Continuous Time Run Simulation')
    ax1.set_ylabel('Voltages [V]')
    ax1.set_ylim(0, 12000)
    ax1.legend([ln_VAFE,ln_VL1PCC,ln_VL2PCC],['V_MVDC','V_LVDC 1','V_LVDC 2'])
    ax1.grid(True)

    ax2.set_ylabel('Currents [A]')
    ax2.set_ylim(-300, 300)
    ax2.legend([ln_IAFE,ln_IPFE1,ln_IPFE2,ln_IPFE3,ln_IPFE4,ln_IPFE5], \
               ['I_AFE','I_H2','I_PV','I_Train','I_LVDC 1','I_LVDC 2'])
    ax2.grid(True)

    ax3.set_ylabel('Currents [A]')
    ax3.set_ylim(-600, 600)
    ax3.legend([ln_IL1AFE,ln_IL1PFE1,ln_IL1PFE2,ln_IL1PFE3],['I_L2AFE','I_DtC 1','I_DtC 2','I_UPS'])
    ax3.grid(True)

    ax4.set_ylabel('Currents [A]')
    ax4.set_ylim(-600, 600)
    ax4.legend([ln_IL2AFE,ln_IL2PFE1,ln_IL2PFE2,ln_IL2PFE3],['I_L1AFE','I_Batt','I_Car','I_PV'])
    ax4.grid(True)
    ax4.set_xlabel('Time (s)')

    return ax1,ax2,ax3,ax4,fig,ln_VAFE,ln_VL1PCC,ln_VL2PCC,ln_IAFE,ln_IPFE1,ln_IPFE2,ln_IPFE3,ln_IPFE4,ln_IPFE5, \
           ln_IL1AFE,ln_IL1PFE1,ln_IL1PFE2,ln_IL1PFE3,ln_IL2AFE,ln_IL2PFE1,ln_IL2PFE2,ln_IL2PFE3

def get_results():
    # get data points
    status = job.Run()
    t = np.array(job.TimePoints)
    VAFE = np.array(job.GetSignalByName('Sc6:V_AFE - Instantaneous Voltage').DataPoints)
    IAFE = np.array(job.GetSignalByName('Sc6:I_AFE - Instantaneous Current').DataPoints)

    IPFE1 = np.array(job.GetSignalByName('Sc6:I_PFE1 - Instantaneous Current').DataPoints)
    IPFE2 = np.array(job.GetSignalByName('Sc6:I_PFE2 - Instantaneous Current').DataPoints)
    IPFE3 = np.array(job.GetSignalByName('Sc6:I_PFE3 - Instantaneous Current').DataPoints)
    IPFE4 = np.array(job.GetSignalByName('Sc6:I_PFE4 - Instantaneous Current').DataPoints)
    IPFE5 = np.array(job.GetSignalByName('Sc6:I_PFE5 - Instantaneous Current').DataPoints)

    VL1PCC = np.array(job.GetSignalByName('Sc19:PCC - Out').DataPoints)
    IL1AFE = np.array(job.GetSignalByName('Sc19:I_AFE - Instantaneous Current').DataPoints)
    IL1PFE1 = np.array(job.GetSignalByName('Sc19:I_PFE1 - Instantaneous Current').DataPoints)
    IL1PFE2 = np.array(job.GetSignalByName('Sc19:I_PFE2 - Instantaneous Current').DataPoints)
    IL1PFE3 = np.array(job.GetSignalByName('Sc19:I_PFE3 - Instantaneous Current').DataPoints)

    VL2PCC = np.array(job.GetSignalByName('Sc5:PCC - Out').DataPoints)
    IL2AFE = np.array(job.GetSignalByName('Sc5:I_AFE - Instantaneous Current').DataPoints)
    IL2PFE1 = np.array(job.GetSignalByName('Sc5:I_PFE1 - Instantaneous Current').DataPoints)
    IL2PFE2 = np.array(job.GetSignalByName('Sc5:I_PFE2 - Instantaneous Current').DataPoints)
    IL2PFE3 = np.array(job.GetSignalByName('Sc5:I_PFE3 - Instantaneous Current').DataPoints)

    job.ClearScopesData()
    return [t,VAFE,IAFE,IPFE1,IPFE2,IPFE3,IPFE4,IPFE5,VL1PCC,IL1AFE,IL1PFE1,IL1PFE2,IL1PFE3,VL2PCC,IL2AFE,IL2PFE1,IL2PFE2,IL2PFE3]

def display(i):
    # calcul des grandeurs
    [t,VAFE,IAFE,IPFE1,IPFE2,IPFE3,IPFE4,IPFE5,VL1PCC,IL1AFE,IL1PFE1,IL1PFE2,IL1PFE3,VL2PCC,IL2AFE,IL2PFE1,IL2PFE2,IL2PFE3] = get_results()

    # filling arrays with latest results
    for i in range(len(t)):
        array_t.append(t[i])
        array_VAFE.append(VAFE[i])
        array_IAFE.append(IAFE[i])

        array_IPFE1.append(IPFE1[i])
        array_IPFE2.append(IPFE2[i])
        array_IPFE3.append(IPFE3[i])
        array_IPFE4.append(IPFE4[i])
        array_IPFE5.append(IPFE5[i])

        array_VL1PCC.append(VL1PCC[i])
        array_IL1AFE.append(IL1AFE[i])
        array_IL1PFE1.append(IL1PFE1[i])
        array_IL1PFE2.append(IL1PFE2[i])
        array_IL1PFE3.append(IL1PFE3[i])

        array_VL2PCC.append(VL2PCC[i])
        array_IL2AFE.append(IL2AFE[i])
        array_IL2PFE1.append(IL2PFE1[i])
        array_IL2PFE2.append(IL2PFE2[i])
        array_IL2PFE3.append(IL2PFE3[i])
    # Deleting oldest values from arrays
    if (len(array_t) > Nb_display_points):
        del array_t[0:Nb_sim_points]
        del array_VAFE[0:Nb_sim_points]
        del array_IAFE[0:Nb_sim_points]
        del array_IPFE1[0:Nb_sim_points]
        del array_IPFE2[0:Nb_sim_points]
        del array_IPFE3[0:Nb_sim_points]
        del array_IPFE4[0:Nb_sim_points]
        del array_IPFE5[0:Nb_sim_points]
        del array_VL1PCC[0:Nb_sim_points]
        del array_IL1AFE[0:Nb_sim_points]
        del array_IL1PFE1[0:Nb_sim_points]
        del array_IL1PFE2[0:Nb_sim_points]
        del array_IL1PFE3[0:Nb_sim_points]
        del array_VL2PCC[0:Nb_sim_points]
        del array_IL2AFE[0:Nb_sim_points]
        del array_IL2PFE1[0:Nb_sim_points]
        del array_IL2PFE2[0:Nb_sim_points]
        del array_IL2PFE3[0:Nb_sim_points]
    # Update Data
    ln_VAFE.set_data(array_t, array_VAFE)
    ln_IAFE.set_data(array_t, array_IAFE)   
    ln_IPFE1.set_data(array_t, array_IPFE1)
    ln_IPFE2.set_data(array_t, array_IPFE2)
    ln_IPFE3.set_data(array_t, array_IPFE3)
    ln_IPFE4.set_data(array_t, array_IPFE4)
    ln_IPFE5.set_data(array_t, array_IPFE5)
    ln_VL1PCC.set_data(array_t, array_VL1PCC)
    ln_IL1AFE.set_data(array_t, array_IL1AFE)
    ln_IL1PFE1.set_data(array_t, array_IL1PFE1)
    ln_IL1PFE2.set_data(array_t, array_IL1PFE2)
    ln_IL1PFE3.set_data(array_t, array_IL1PFE3)
    ln_VL2PCC.set_data(array_t, array_VL2PCC)
    ln_IL2AFE.set_data(array_t, array_IL2AFE)
    ln_IL2PFE1.set_data(array_t, array_IL2PFE1)
    ln_IL2PFE2.set_data(array_t, array_IL2PFE2)
    ln_IL2PFE3.set_data(array_t, array_IL2PFE3)
    # update Figure
    ax1.relim()
    ax1.autoscale_view(scalex=True, scaley=False)
    ax2.relim()
    ax2.autoscale_view(scalex=True, scaley=False)
    ax3.relim()
    ax3.autoscale_view(scalex=True, scaley=False)
    ax4.relim()
    ax4.autoscale_view(scalex=True, scaley=False)

def update_parameters():
    SP_H2_val = parameter_h2.get()
    SP_UPS_val = parameter_ups.get()
    SP_BESS_val = parameter_bess.get()
    SP_H2.Value = SP_H2_val
    SP_UPS.Value = SP_UPS_val
    SP_BESS.Value = SP_BESS_val
    print("SP H2: " + SP_H2_val)
    print("SP UPS: " + SP_UPS_val)
    print("SP BESS: " + SP_BESS_val)

def quit():
    sys.exit()

#%%  START PROCESS
[job,SP_H2,SP_UPS,SP_BESS] = circuit_init()

#%%  BUILD WINDOW
window = Tk()

# window parameters
window.title('interface for microgrid continuous run')
window.geometry('1200x680')
window.minsize(480, 360)
window.config(background='white')
# table configuration
window.rowconfigure(0,weight=3)
window.rowconfigure(1,weight=1)
window.rowconfigure(2,weight=1)
window.rowconfigure(3,weight=1)
window.rowconfigure(4,weight=3)
window.columnconfigure(0,weight=1)
window.columnconfigure(0,weight=1)
window.columnconfigure(2,weight=3)

# building blocks
block_title = Frame(window)
block_plots = Frame(window)
block_buttons = Frame(window)
block_entry1 = Frame(window)
block_entry2 = Frame(window)
block_entry3 = Frame(window)
block_label1 = Frame(window)
block_label2 = Frame(window)
block_label3 = Frame(window)

# placing blocks
block_title.grid(row=0, column=0, columnspan = 2)
block_plots.grid(row=0, column=2, rowspan=5)
block_buttons.grid(row=4, column=0, columnspan = 2)
block_entry1.grid(row=1, column=1)
block_entry2.grid(row=2, column=1)
block_entry3.grid(row=3, column=1)
block_label1.grid(row=1, column=0)
block_label2.grid(row=2, column=0)
block_label3.grid(row=3, column=0)

# creating labels
label_title = Label(block_title,text="Continuous time Run of DC Microgrid",fg="black",font=("Helvetica", 12),background='white')
label_h2 = Label(block_label1,text="Set Point for H2:",fg="black",font=("Helvetica", 10),background='white',width=20,anchor="e")
label_ups = Label(block_label2,text="Set Point for UPS:",fg="black",font=("Helvetica", 10),background='white',width=20,anchor="e")
label_bess = Label(block_label3,text="Set Point for BESS:",fg="black",font=("Helvetica", 10),background='white',width=20,anchor="e")
label_title.pack()
label_h2.pack()
label_ups.pack()
label_bess.pack()

# interaction widgets
parameter_button = Button(block_buttons, text="Update Parameter", command=update_parameters)
parameter_button.pack()

# text fields
parameter_h2 = StringVar()
parameter_h2.set('0')
entry_h2 = Entry(block_entry1, textvariable=parameter_h2)
entry_h2.pack(fill='x', expand=True)
parameter_ups = StringVar()
parameter_ups.set('0')
entry_ups = Entry(block_entry2, textvariable=parameter_ups)
entry_ups.pack(fill='x', expand=True)
parameter_bess = StringVar()
parameter_bess.set('0')
entry_bess = Entry(block_entry3, textvariable=parameter_bess)
entry_bess.pack(fill='x', expand=True)

# graphic
[ax1,ax2,ax3,ax4,fig,ln_VAFE,ln_VL1PCC,ln_VL2PCC,ln_IAFE,ln_IPFE1,ln_IPFE2,ln_IPFE3,ln_IPFE4,ln_IPFE5, \
 ln_IL1AFE,ln_IL1PFE1,ln_IL1PFE2,ln_IL1PFE3,ln_IL2AFE,ln_IL2PFE1,ln_IL2PFE2,ln_IL2PFE3] = graph_init()
canvas_plots = FigureCanvasTkAgg(fig, block_plots)
canvas_plots.get_tk_widget().pack(expand=YES)
ani = animation.FuncAnimation(fig, display, interval=1,save_count=Nb_display_points+Nb_sim_points)

# display window
window.mainloop()
