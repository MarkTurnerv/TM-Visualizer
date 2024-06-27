# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 14:36:29 2024

Last Revision: 6.21.2024

@author: Mark Turner

Telemetry Message Plotter

Plots values from csv file created by TMdecoder. Test files are located in the folder 'TelemetryMessages'.

User Inputs (command line): Instrument Type (LPC or RS41)
                            csv filename
"""

import PySimpleGUI as sg           
import sys 
import time
import numpy as np # Import numpy
import matplotlib  #Use to move figure to upper right corner
import matplotlib.pyplot as plt #import matplotlib library
import pandas as pd

HG_Sizes = []
LG_Sizes = []

Frame = 0

hg_m = 7.524e-4
hg_b = -2.543e-2
lg_m = 5.979e-3
lg_b = -0.1895
c4 = -71.05
c3 = 282.74
c2 = 329.18
c1 = 1132.3
c0 = 297.09
flow = 20.0
cal_val = np.array([999,hg_m,hg_b,lg_m, lg_b, c4, c3, c2, c1, c0, flow])
diams = [275,300,325,350,375,400,450,500,550,600,650,700,750,800,900,1000,1200,1400,1600,1800,2000,2500,3000,3500,4000,6000,8000,10000,13000,16000,24000]
#Instrument_name = input("Enter Instrument (LPC or RS41):")
#filename = input("Enter filename: ")

plt.ion() #Tell matplotlib you want interactive mode to plot live data
'''LPC String Header
Time,Pump1_I,Pump2_I,PHA_I,PHA_12V,PHA_3V3,Input_V,Flow,CPU_V,Pump1_PWM,Pump2_PWM,Pump1_T,Pump2_T,Laser_T,PCB_T,Inlet_T,275,300,325,350,375,400,450,500,550,600,650,700,750,800,900,1000,1200,1400,1600,1800,2000,2500,3000,3500,4000,6000,8000,10000,13000,16000,24000,24000
[Unix Time],[mA],[mA],[mA],[V],[V],[V],[SLPM],[V],[#],[#],[C],[C],[C],[C],[C],[diam >nm],[diam >nm],[diam >nm],[diam >nm],[diam >nm],[diam >nm],[diam >nm],[diam >nm],[diam >nm],[diam >nm],[diam >nm],[diam >nm],[diam >nm],[diam >nm],[diam >nm],[diam >nm],[diam >nm],[diam >nm],[diam >nm],[diam >nm],[diam >nm],[diam >nm],[diam >nm],[diam >nm],[diam >nm],[diam >nm],[diam >nm],[diam >nm],[diam >nm],[diam >nm],[diam >nm],[diam >nm]

valid,frame_count,air_temp_degC,humdity_percent,pres_mb,module_error                                                   
'''
'''
def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth
'''
#Function to search for csv file
def find_csv():
    import os
    global filename
    global filepath
    global Instrument_name
    csv_files = []
    filepaths = []
    # This is to get the directory that the program is currently running in
    dir_path = os.path.dirname(os.path.realpath(__file__))
     
    for root, dirs, files in os.walk(dir_path):
        for file in files: 
     
            # search for .csv files
            if file.endswith('.csv'):
                csv_files.append(file)
                filepaths.append(root)
    Instrument_list = ['LPC','RS41']
    Inst_layout = [[sg.InputCombo(values=Instrument_list, key = '_inst_',  font = ('any', 16))]]
    file_layout = [[sg.InputCombo(values=csv_files, key = '_file_',  font = ('any', 16))]]
    
    layout_find_csv = [[sg.Frame('Select Instrument Type: ', Inst_layout, font = 'any 16')],
                        [sg.Frame('Select csv File: ', file_layout, font = 'any 16')],
                        [sg.Submit( font = ('any', 16)), sg.Cancel( font = ('any', 16))]]
    
    serial_window = sg.Window('Select Instrument Tpye and File', layout_find_csv, keep_on_top = True)
    event, values = serial_window.Read()
    serial_window.Close()

    if event is None or event == 'Cancel':
        sys.exit()
    if event == 'Submit':
        filename = values['_file_']
        if filename in csv_files:
            filepath = filepaths[csv_files.index(filename)]
            filename = filepath + '\\' + filename
        Instrument_name = values['_inst_']

        


# Function to read in the user-defined filename into a PANDAS DataFrame
def read_csv(filename):
    if 'LPC' in Instrument_name:
        global LPC_data
        LPC_data = pd.read_table(filename, sep=",",skiprows=2) #, header = [2],index_col="Time"
        LPC_data.drop(0, inplace=True)
        LPC_data.rename(columns=lambda x: x.strip(), inplace=True)
    elif 'RS41' in Instrument_name:
        global RS41_data
        RS41_data = pd.read_table(filename, sep=",", header=[0])
        #RS41_data.drop(0,axis='index')
        RS41_data.rename(columns=lambda x: x.strip(), inplace=True)
    else:
        print("Invalid filename")

#Function to graph the data. Takes bool input 'log_lin', which is True by default and switches when
#the button in the PySimpleGUI window is pressed
def make_LPC_fig(log_lin):  #Plot the CN Counts
    '''
    global moveBool
    moveBool = False
    def move_figure(f, x, y):
        """Move figure's upper left corner to pixel (x, y)"""
        backend = matplotlib.get_backend()
        if backend == 'TkAgg':
            f.canvas.manager.window.wm_geometry("+%d+%d" % (x, y))
        elif backend == 'WXAgg':
            f.canvas.manager.window.SetPosition((x, y))
        else:
            # This works for QT and GTK
            # You can also use window.setGeometry
            f.canvas.manager.window.move(x, y)
    '''
    try:
        if 'LPC' in Instrument_name:
            plt.subplot2grid((4,1), (3, 0))
            plt.ylim(0, 1000)
            plt.title('Currents', fontsize = 'x-small')      #Plot the title
            plt.grid(True)                                  #Turn the grid on
            plt.ylabel('mA')                            #Set ylabels
            plt.plot(LPC_data["Time"], LPC_data["Pump1_I"], 'k-', label='Pump1 I')       #plot the channels
            plt.plot(LPC_data["Time"], LPC_data["Pump2_I"], 'r-', label='Pump2 I')
            plt.legend(loc='upper left', fontsize = 'x-small')
            plt.xlabel('Elapsed Time [s]', fontsize = 'x-small')
            plt.tight_layout()
            
            plt2=plt.twinx()
            plt2.plot(LPC_data["Time"], LPC_data["Pump1_T"], 'b-', label='Pump1 T')
            plt2.plot(LPC_data["Time"], LPC_data["Pump2_T"], 'g-', label='Pump2 T')
            plt2.legend(loc='upper right', fontsize = 'x-small')
            
            graphcounts = counts.mean()
            graphcounts = graphcounts.transpose()
            plt.subplot2grid((4,1), (0,0), colspan = 1, rowspan = 2)
            plt.fontsize = 'small'
            plt.title(Instrument_name, fontsize = 'x-small')      #Plot the title
            plt.ylabel('dN/dD')                            #Set ylabels
            plt.xlabel('Diameter [nm]', fontsize = 'small')
            plt.plot(diams, graphcounts, 'k-', label='High Gain')       #plot the channels
            plt.xlim(300,10000)
            plt.xscale('log')
            xticks = [300,400, 500, 700, 1000, 2000, 5000]
            plt.grid(True)
            plt.xticks(xticks, ['%d'  % i for i in xticks] )
            #plt.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
            if log_lin == True:
                plt.yscale('log')
            plt.tight_layout()
            '''
            plt.subplot2grid((4,1), (0,0), colspan = 1, rowspan = 2)
            plt.fontsize = 'small'
            plt.title(Instrument_name, fontsize = 'x-small')      #Plot the title
            plt.ylabel('dN/dD')                            #Set ylabels
            plt.xlabel('Diameter [nm]', fontsize = 'small')
            plt.bar(diams,)
            '''
            plt.subplot2grid((4,1), (2, 0))
            plt.title('Cumulative', fontsize = 'x-small')      #Plot the title
            plt.grid(True)                                  #Turn the grid on
            plt.ylabel('#/cc')                            
            plt.plot(LPC_data["Time"], LPC_data['300'], 'k-', label='300nm')
            plt.plot(LPC_data["Time"], LPC_data['500'], 'r-', label='500nm')
            plt.plot(LPC_data["Time"], LPC_data['1000'], 'b-', label='1000nm')
            plt.plot(LPC_data["Time"], LPC_data['2000'], 'g-', label='2000nm')
            if log_lin == True:
                plt.yscale('log')
            plt.legend(loc='upper left', fontsize = 'x-small')
            plt.tight_layout()
            '''
            if (moveBool != True):
                fig = plt.gcf()
                figsize = fig.get_size_inches()*fig.dpi
                move_figure(1, screen_width-figsize, 25)
                moveBool = True
            '''
        elif 'RS41' in Instrument_name:
            plt.subplot2grid((4,1),(0,0))
            #plt.ylim()
            plt.title('RS41 Air Temperature')
            plt.xlabel("Frame Count", fontsize = 'x-small')
            plt.ylabel("Air Temperature [C]", fontsize = 'x-small')
            plt.grid()
            plt.plot(RS41_data['frame_count'],RS41_data['air_temp_degC'], label='Air Temp [C]')
            plt.legend(loc='upper left', fontsize = 'x-small')
            plt.tight_layout()
            
            plt.title('RS41 Humidity')
            plt.subplot2grid((4,1),(1,0))
            plt.plot(RS41_data['frame_count'],RS41_data['humdity_percent'], label='Humidity Percent')
            plt.ylabel("Humidity Percent", fontsize = 'x-small')
            plt.legend(loc='upper left', fontsize = 'x-small')
            
            plt.subplot2grid((4,1),(2,0))
            #plt.ylim()
            plt.title('RS41 Pressure')
            plt.xlabel("Frame Count", fontsize = 'x-small')
            plt.ylabel("Pressure [mb]", fontsize = 'x-small')
            plt.grid()
            plt.plot(RS41_data['frame_count'],RS41_data['pres_mb'], label='Air Temp [C]')
            plt.legend(loc='upper left', fontsize = 'x-small')
            plt.tight_layout()
            
            plt.subplot2grid((4,1),(3,0))
            #plt.ylim()
            plt.title('RS41 Error')
            plt.xlabel("Frame Count", fontsize = 'x-small')
            plt.ylabel("Error", fontsize = 'x-small')
            plt.grid()
            plt.plot(RS41_data['frame_count'],RS41_data['module_error'], label='Air Temp [C]')
            plt.legend(loc='upper left', fontsize = 'x-small')
            plt.tight_layout()
            
        else:
            print("Invalid filename")
            
    except:
        print('Plotting Exception')
 
#main function runs the other funcions when TMplotter.py is run as a script
def main():
    #set global variables to be accessed across all functions
    global LPC_data
    global RS41_data
    log_plot = True
    find_csv()
    
    #initialize PySimpleGUI interactive window and Housekeeping window
    plot_frame_layout = [[sg.Text('Plot Axis Type: ', font = ('any', 16))],
                         [sg.Button('Log', font = ('any', 16), border_width = 3), sg.Button('Linear', font = ('any', 16),border_width = 3)],
                         [sg.Button('Exit',  font = ('any', 16),border_width = 3, button_color = ('black', 'red'))]]
    
    window1 = sg.Window("Graphing Axis", plot_frame_layout, keep_on_top=True, finalize = True)
    global screen_width
    global screen_height
    screen_width, screen_height = window1.get_screen_dimensions()
    win1_width, win1_height = window1.size
    x, y = (screen_width - win1_width - 75), (screen_height - win1_height - 75)
    window1.move(x,y)
    
    if 'LPC' in Instrument_name:
        layout_hk =[[sg.Text('LPC House Keeping', font = ('any', 16, 'underline'))],
                    [sg.Text('')],
                    [sg.Text('OPC Time: ',  font = ('any', 16)), sg.Text('', key='_OPC_Time_',  font = ('any', 16))],
                    [sg.Text('LOPC Raw Counts: ',  font = ('any', 16)), sg.Text('', key='_CN_Counts_',  font = ('any', 16))],
                    [sg.Text('Pump 1 Temp: ',  font = ('any', 16)), sg.Text('', key='_Pump1_T_',  font = ('any', 16))],
                    [sg.Text('Pump 1 I: ',  font = ('any', 16)), sg.Text('', key='_Pump1_I_',  font = ('any', 16))],
                    [sg.Text('Pump 1 Drive: ',  font = ('any', 16)), sg.Text('', key='_Pump1_PWM_',  font = ('any', 16))],
                    [sg.Text('')],
                    [sg.Text('Pump 2 Temp: ',  font = ('any', 16)), sg.Text('', key='_Pump2_T_',  font = ('any', 16))],
                    [sg.Text('Pump 2 I: ',  font = ('any', 16)), sg.Text('', key='_Pump2_I_',  font = ('any', 16))],
                    [sg.Text('Pump 2 Drive: ',  font = ('any', 16)), sg.Text('', key='_Pump2_PWM_',  font = ('any', 16))],
                    [sg.Text('')],
                    [sg.Text('Internal Temp: ',  font = ('any', 16)), sg.Text('', key='_PCB_T_',  font = ('any', 16))],
                    [sg.Text('Battery Voltage: ',  font = ('any', 16)), sg.Text('', key='_Batt_V_',  font = ('any', 16))],
                    [sg.Text('Flow: ',  font = ('any', 16)), sg.Text('', key='_Flow_',  font = ('any', 16))]]
        hk_name = 'LPC House Keeping'
    elif 'RS41' in Instrument_name:
        layout_hk = [[sg.Text('LPC House Keeping', font = ('any', 16, 'underline'))],
                    [sg.Text('')],
                    [sg.Text('Frame Count: ',  font = ('any', 16)), sg.Text('', key='_Frame_Count_',  font = ('any', 16))],
                    [sg.Text('Air Temp [C]: ',  font = ('any', 16)), sg.Text('', key='_Air_Temp_',  font = ('any', 16))],
                    [sg.Text('Humidity Percent: ',  font = ('any', 16)), sg.Text('', key='_humidity_percent_',  font = ('any', 16))],
                    [sg.Text('Pressure: ',  font = ('any', 16)), sg.Text('', key='_pres_mb_',  font = ('any', 16))]]
        hk_name = 'RS41 House Keeping'
    else:
        print('Invalid instrument name')  
              
    window2 = sg.Window(hk_name, layout_hk, finalize = True)
    win2_width, win2_height = window2.size
    x2, y2 = screen_width // 2, (screen_height - win2_height - 75)
    window2.move(x2,y2)
    
    while True:
        #check if either PYSimpleGUI window has been closed or 'Exit' has been pressed
        event, values = window1.Read(timeout=0)
        event2, values2 = window2.Read(timeout=0)
        if event is None or event == 'Exit':
            window1.close()
            window2.close()
            sys.exit()
            break
        #if event2 is None or event2 == 'Exit':
            #window2.close()
        
        #check if the y-axis scaling has been switched from log to linear
        if event == 'Log':
              log_plot = True
              print('Switching to Log')
        if event == 'Linear':
              log_plot = False
              print('Switching to Linear')
            
        #Plot data
        time.sleep(0.01)
        plt.clf()
        read_csv(filename)
        if 'LPC' in Instrument_name:
            global counts
            counts = LPC_data[['275','300','325','350','375','400','450','500','550','600','650','700','750','800','900','1000','1200','1400','1600','1800','2000','2500','3000','3500','4000','6000','8000','10000','13000','16000','24000']].tail(20).apply(pd.to_numeric)
        #counts = 
        make_LPC_fig(log_plot)
        time.sleep(0.01) 
        plt.draw()
        time.sleep(0.01)        #Pause Briefly. Important to keep drawnow from crashing

        #Update Housekeeping window
        if 'LPC' in Instrument_name:
            window2.Element('_OPC_Time_').Update(LPC_data['Time'].iloc[-1])
            window2.Element('_CN_Counts_').Update(int(float(LPC_data['300'].iloc[-1])*(flow*1000.0/30.0)))
            window2.Element('_PCB_T_').Update(LPC_data['PCB_T'].iloc[-1])
            window2.Element('_Pump1_T_').Update(LPC_data['Pump1_T'].iloc[-1])
            window2.Element('_Pump2_T_').Update(LPC_data['Pump2_T'].iloc[-1])
            window2.Element('_Pump1_I_').Update(LPC_data['Pump1_I'].iloc[-1])
            window2.Element('_Pump2_I_').Update(LPC_data['Pump2_I'].iloc[-1])
            window2.Element('_Pump1_PWM_').Update(LPC_data['Pump1_PWM'].iloc[-1])
            window2.Element('_Pump2_PWM_').Update(LPC_data['Pump2_PWM'].iloc[-1])
            window2.Element('_Batt_V_').Update(LPC_data['Input_V'].iloc[-1])
            window2.Element('_Flow_').Update(LPC_data['Flow'].iloc[-1])
        elif 'RS41' in Instrument_name:
            window2.Element('_Frame_Count_').Update(RS41_data['frame_count'].iloc[-1])
            window2.Element('_Air_Temp_').Update(RS41_data['air_temp_degC'].iloc[-1])
            window2.Element('_humidity_percent_').Update(RS41_data['humdity_percent'].iloc[-1])
            window2.Element('_pres_mb_').Update(RS41_data['pres_mb'].iloc[-1])
        
        #If you have 150 or more points (5 minutes), delete the first one from the array
        if 'LPC' in Instrument_name:
            if(len(LPC_data)>150):
                LPC_data = LPC_data.tail(LPC_data.shape[0]-1)
        elif 'RS41' in Instrument_name:
            if(len(RS41_data)>150):
                RS41_data = RS41_data.tail(RS41_data.shape[0]-1)
            
#Run main if run as a script. If called in another script, functions will be available but main will not run on its own
if (__name__ == '__main__'): 
    main()          
