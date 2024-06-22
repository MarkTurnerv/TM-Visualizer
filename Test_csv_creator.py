# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 16:08:17 2024

@author: Mark Turner

Creates mock csv files to imitate the LPC instrument for testing TMplotter.py
"""
import time
f = open("TM_LPCtest.csv", "w")
f.write('Instrument:,LPC,Measurerment End Time: ,"06/10/2024, 07:06:59",LASP Optical Particle Counter on Strateole 2 Super Pressure Balloons\n')
f.write('GPS Position at start of Measurement ,Latitude: ,-273.15,Longitude: ,-273.15,Altitude [m]:,-273.15\n')
f.write("Time,Pump1_I,Pump2_I,PHA_I,PHA_12V,PHA_3V3,Input_V,Flow,CPU_V,Pump1_PWM,Pump2_PWM,Pump1_T,Pump2_T,Laser_T,PCB_T,Inlet_T,275,300,325,350,375,400,450,500,550,600,650,700,750,800,900,1000,1200,1400,1600,1800,2000,2500,3000,3500,4000,6000,8000,10000,13000,16000,24000,24000\n")
f.close()

i=0
while i<1000:
    f = open("TM_LPCtest.csv", "a")
    dataString = f"{i},{i},{i},{i},{i},{i},{i},{i},{i},{i},{i},{i},{i},{i},{i},{i},{i},{i},{i},{i},{i},{i},{i},{i},{i},{i},{i},{i},{i},{i},{i},{i},{i},{i},{i},{i},{i},{i},{i+6},{i+8},{i+10},{i},{i},{i+15},{i},{i},{i},{i}\n"
    f.write(dataString)
    i = i+1
    time.sleep(1)
    f.close()
