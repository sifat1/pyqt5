# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 18:23:09 2019

@author: ASUS
"""
import serial
from PyQt5.QtCore import QRect
from PyQt5 import QtWidgets,QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import threading
import time

def update_label(label,ser):
    i=0
    while i!=20:
        data = ser.readline().decode("utf-8")
        print("running file")
        label.setText(data)
        i+=1
    ser.close()
def window():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(200,200,800,600)
    win.setWindowTitle("demo tittle")
    
    #create label
    
    label_air_name = QtWidgets.QLabel(win)
    label_gps_name = QtWidgets.QLabel(win)
    label_battary_name = QtWidgets.QLabel(win)
    label_temp_name = QtWidgets.QLabel(win)
    label_speed_name = QtWidgets.QLabel(win)
    label_mission_time_name = QtWidgets.QLabel(win)
    label_air_pressure=QtWidgets.QLabel(win)
    label_gps=QtWidgets.QLabel(win)
    label_battary=QtWidgets.QLabel(win)
    label_temp=QtWidgets.QLabel(win)
    label_speed=QtWidgets.QLabel(win)
    label_mission_time=QtWidgets.QLabel(win)
    
    #row1
    #lebel alignment of air pressure
    label_air_name.setText("Air Pressure")
    #label_air_name.setWordWrap(True)
    label_air_name.setStyleSheet("height: 10px;width: 100px;")
    label_air_name.move(50,40)
    label_air_name.setFont(QtGui.QFont("Times", 15, QtGui.QFont.Bold))
    label_air_name.adjustSize()
    label_air_pressure.setText("Air_value");
    label_air_pressure.setStyleSheet("padding-right: 20px;border: 1px solid #EF233C;border-radius: 3PX;background-color: #ffffff;text-align: center")
    
    label_air_pressure.move(50,70)
    #lebel alignment of battary volt
    label_battary_name.setText("Battary volt")
    label_battary_name.move(220,40)
    label_battary_name.setFont(QtGui.QFont("Times", 15, QtGui.QFont.Bold))
    label_battary_name.adjustSize()
    label_battary.setText("battary_value")
    label_battary.move(220,70)
    label_battary.setStyleSheet("padding-right: 20px;border: 1px solid #EF233C;border-radius: 3PX;background-color: #ffffff;text-align: center")
    #lebel alignment of temp
    label_temp_name.setText("Tempreatue")
    label_temp_name.move(420,40)
    label_temp_name.setFont(QtGui.QFont("Times", 15, QtGui.QFont.Bold))
    label_temp_name.adjustSize()
    label_temp.setText("temp_value")
    label_temp.move(420,70)
    label_temp.setStyleSheet("padding-right: 20px;border: 1px solid #EF233C;border-radius: 3PX;background-color: #ffffff;text-align: center")
    
    #row2
    #label alignment of gps
    label_gps_name.setText("Gps Data")
    label_gps_name.move(50,150)
    label_gps_name.setFont(QtGui.QFont("Times", 15, QtGui.QFont.Bold))
    label_gps_name.adjustSize()
    label_gps.setText("gps val")
    label_gps.move(50,180)
    label_gps.setStyleSheet("padding-right: 20px;border: 1px solid #EF233C;border-radius: 3PX;background-color: #ffffff;text-align: center")
   
    #label alignment of speed
    label_speed_name.setText("Speed")
    label_speed_name.move(220,150)
    label_speed_name.setFont(QtGui.QFont("Times", 15, QtGui.QFont.Bold))
    label_speed_name.adjustSize()
    label_speed.setText("speed val")
    label_speed.move(220,180)
    label_speed.setStyleSheet("padding-right: 20px;border: 1px solid #EF233C;border-radius: 3PX;background-color: #ffffff;text-align: center")
    #label alignment of mission time
    label_mission_time_name.setText("Mission Time")
    label_mission_time_name.move(420,150)
    label_mission_time_name.setFont(QtGui.QFont("Times", 15, QtGui.QFont.Bold))
    label_mission_time_name.adjustSize()
    label_mission_time.setText("speed val")
    label_mission_time.move(420,180)
    label_mission_time.setStyleSheet("padding-right: 20px;border: 1px solid #EF233C;border-radius: 3PX;background-color: #ffffff;text-align: center")
    
                                     
    
    
    '''
    #create serial data
    ser = serial.Serial("COM3",baudrate=9600,timeout=1)
    t = threading.Thread(target=update_label,
    args=(label_air_pressure,
    label_gps,
    label_battary,
    label_temp,
    label_speed,
    label_mission_time,
    ser), name='update_label')
    t.start()
    '''
    #show window
    win.show()
    
    sys.exit(app.exec_())



window()