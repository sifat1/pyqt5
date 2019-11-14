# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 05:18:53 2019

@author: ASUS
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 18:41:34 2019

@author: ASUS
"""

#from __future__ import annotations
from typing import *
import sys
import os
from matplotlib.backends.qt_compat import QtCore, QtWidgets
# from PyQt5 import QtWidgets, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvas
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib as mpl
import matplotlib.figure as mpl_fig
import matplotlib.animation as anim
import numpy as np
import threading
import serial
import csv


ser=None
alive_change_label_thread = True
air_pres = 0.0
accleration = 0.0
team_id=0
mission_time = 0.0
altitude = 0.0
tempreature=0.0
altitude_=0.0
speed_=0.0
state_=""
volt_=0.0
csv_save_state=False
def change_label(id_t,miss_t,alt_t,pres_t,temp_t,vt_t,gps_t,speed_t,state_t,ser):
    global air_pres,accleration,alive_change_label_thread,csv_save_state,speed_,tempreature,volt_
    while True and alive_change_label_thread:
        data = ser.readline().decode("utf-8")
        df = data.split(",")
        if df != [''] and len(df) == 10 and not "migo" in df[1]:
            id_t.setText(df[0])
            mt = "Mission time: 0 msec"
            miss_t.setText(mt)
            alti="Altitude: "+df[1]+"m"
            alt_t.setText(alti)
            air_pres= float(df[2])/10000
            pre="Pressure: "+df[2]+"pa"
            pres_t.setText(pre)
            temp ="Tempreature: "+df[3]+"'c"
            tempreature=df[3]
            temp_t.setText(temp)
            vt = "Voltage :"+df[4]+"v"
            volt_=df[4]
            vt_t.setText(vt)
            gps_ = "Gps: lat: "+df[5]+"\n"+"long: "+df[6]+"\n"+"time: "+df[7]+"sec"
            gps_t.setText(gps_)
            spee ="Speed: "+df[8]+"m/s"
            speed_ = df[8]
            speed_t.setText(spee)
            stat = "Soft state: "+df[9]
            state_t.setText(stat)
            if csv_save_state == True:
                csv.register_dialect('myDialect',
                                     quoting=csv.QUOTE_ALL,
                                     skipinitialspace=True)

                with open('demo.csv','a', newline='') as f:
                    writer = csv.writer(f, dialect='myDialect')
                    writer.writerow([df[0],'0',df[1],df[2],df[3],
                     df[4],df[5],df[6],df[7],df[8],df[9]])
                f.close()
        if df != [''] and len(df) == 11 and not "migo" in df[1]:
            #global air_pres,accleration,id,altitude,temp,speed,state
            '''
            team_id = df[0]
            mission_time = "nan"
            altitude_ = df[1]
            air_pres = df[2]
            tempreature=df[3]
            speed_=df[4]
            sate_=df[5]
            '''
            id_t.setText(df[0])
            mt = "Mission time: "+df[1]+"msec"
            miss_t.setText(mt)
            alti="Altitude: "+df[2]+"m"
            alt_t.setText(alti)
            air_pres= float(df[3])/1000
            pre="Pressure: "+df[3]+"pa"
            pres_t.setText(pre)
            temp ="Tempreature: "+df[4]+"'c"
            tempreature=df[4]
            temp_t.setText(temp)
            vt = "Voltage :"+df[5]+"v"
            volt_=df[5]
            vt_t.setText(vt)
            gps_ = "Gps: long: "+df[6]+"\n"+"lat: "+df[7]+"\n"+"time: "+df[8]+"sec"
            gps_t.setText(gps_)
            spee ="Speed: "+df[9]+"m/s"
            speed_ = df[9]
            speed_t.setText(spee)
            stat = "Soft state: "+df[10]
            state_t.setText(stat)
            if csv_save_state == True:
                csv.register_dialect('myDialect',
                                     quoting=csv.QUOTE_ALL,
                                     skipinitialspace=True)

                with open('demo.csv','a', newline='') as f:
                    writer = csv.writer(f, dialect='myDialect')
                    writer.writerow([df[0],df[1],df[2],df[3],
                     df[4],df[5],df[6],df[7],df[8],df[9],df[10]])
                f.close()
            
            '''
            accleration = float(df[1])
            air_pres = int(df[0])
            print(air_pres)
            obj.setText(df[0])
            '''
    print("change_label exited")

def get_next_speed_datapoint():
    return float(speed_)
def get_next_datapoint():
    print(air_pres)
    return float(air_pres)
def get_next_voltage_datapoint():
    return float(accleration)
def get_next_temp_datapoint():
    return float(tempreature)

class ApplicationWindow(QtWidgets.QMainWindow):
    '''
    The PyQt5 main window.

    '''
    def __init__(self):
        super().__init__()
        # 1. Window settings
        self.setGeometry(300, 300, 1200, 900)
        self.setWindowTitle("Team Amigos")
        self.frm = QtWidgets.QFrame(self)
        self.frm.setStyleSheet("QWidget { background-color: #eeeeec; }")
        self.lyt = QtWidgets.QVBoxLayout()
        self.frm.setLayout(self.lyt)
        self.setCentralWidget(self.frm)
        #labels 1
        self.hlayout = QtWidgets.QHBoxLayout()
        self.label_air_name = QtWidgets.QLabel()
        self.label_air_name.setText("Air pressure")
        self.hlayout.addWidget(self.label_air_name)
        self.label_gps_name = QtWidgets.QLabel()
        self.label_gps_name.setText("Gps: 0 e 0w")
        self.hlayout.addWidget(self.label_gps_name)
        self.label_battary_name = QtWidgets.QLabel()
        self.label_battary_name.setText("battary: 0v")
        self.hlayout.addWidget(self.label_battary_name)
        self.label_temp_name = QtWidgets.QLabel()
        self.label_temp_name.setText("temp: 0'c")
        self.hlayout.addWidget(self.label_temp_name)
        self.label_speed_name = QtWidgets.QLabel()
        self.label_speed_name.setText("speed: 0m/s")
        self.hlayout.addWidget(self.label_speed_name)
        self.label_mission_time_name = QtWidgets.QLabel()
        self.label_mission_time_name.setText("Time: 0sec")
        self.hlayout.addWidget(self.label_mission_time_name)
        self.lyt.addLayout(self.hlayout)
        #label team_id,altitude,software_state
        self.hlayout_1 = QtWidgets.QHBoxLayout()
        self.team_id = QtWidgets.QLabel()
        self.team_id.setText("Team id: #1")
        self.altitude = QtWidgets.QLabel()
        self.altitude.setText("Altitude: 0m")
        self.soft_state = QtWidgets.QLabel()
        self.soft_state.setText("Soft_state: nan")
        self.hlayout_1.addWidget(self.team_id)
        self.hlayout_1.addWidget(self.altitude)
        self.hlayout_1.addWidget(self.soft_state)
        self.lyt.addLayout(self.hlayout_1)
        
        #add csv button
        self.hlayout_button = QtWidgets.QHBoxLayout()
        #csv status label
        self.csv_stat_label = QtWidgets.QLabel()
        self.csv_stat_label.setText("CSV is not saving!")
        self.csv_stat_label.setStyleSheet("text-align: center;")
        self.hlayout_button.addWidget(self.csv_stat_label)
        self.btn = QtWidgets.QPushButton()
        self.btn2 = QtWidgets.QPushButton()
        self.btn.setText("Start")
        self.btn.setStyleSheet("background-color: green; color: white;")
        self.btn2.setText("Stop")
        self.btn2.setStyleSheet("background-color: red; color: white;")
        self.btn.clicked.connect(self.save_csv)
        self.btn2.clicked.connect(self.stop_csv)
        self.hlayout_button.addWidget(self.btn)
        self.hlayout_button.addWidget(self.btn2)
        self.lyt.addLayout(self.hlayout_button)
        #1st fig
        # 2. Place the matplotlib figure
        self.myFig = MyFigureCanvas(x_len=200, y_range=[0, 100], interval=200)
        self.lyt.addWidget(self.myFig)
        #2nd fig
        # 2. Place the matplotlib figure
        self.myFig2 = SpeedFigureCanvas(x_len=200, y_range=[0, 100], interval=200)
        self.lyt.addWidget(self.myFig2)
        #3rd fig
        self.myFig3 = tempFigureCanvas(x_len=200, y_range=[0, 100], interval=200)
        self.lyt.addWidget(self.myFig3)
        #4th fig
        self.myFig4 = voltageFigureCanvas(x_len=200, y_range=[0, 100], interval=200)
        self.lyt.addWidget(self.myFig4)
        #create csv file
        csv.register_dialect('myDialect',
                             quoting=csv.QUOTE_ALL,
                             skipinitialspace=True)

        with open('demo.csv','w', newline='') as f:
            writer = csv.writer(f, dialect='myDialect')
            writer.writerow(['id','Mission Time(sec)','Altitude(m)','Air Pressure(kpa)','Tempreature(degree celcias)',
                     'Voltage(volt)','Latitude','Longitude','Gps time','Speed(m/s)','Software State'])

        f.close()
        #connect comport
        try:
            global ser
            ser = serial.Serial("COM3",baudrate=9600,timeout=1)
            #label update thread
            self.label_change_thread = threading.Thread(target=change_label,
                             args=(self.team_id,self.label_mission_time_name,
                                   self.altitude,
                                   self.label_air_name,self.label_temp_name,
                                   self.label_battary_name,self.label_gps_name,
                                   self.label_speed_name,
                                   self.soft_state,
                                   ser), name='change_label')
            self.label_change_thread.start()
        except:
            self.csv_stat_label.setText("Error: Try reconnecting arduino and restart")
            self.csv_stat_label.setStyleSheet("color: red;")
        # 3. Show
        self.show()
        return
    def save_csv(self):
        #self.soft_state.setText("Soft_state: deployed")
        global ser,csv_save_state
        ser.write(b"on")
        csv_save_state=True
        self.csv_stat_label.setText("Csv data saving!")
        self.csv_stat_label.setStyleSheet("color: green;")
        print("clicked")
    def stop_csv(self):
        global ser,csv_save_state
        csv_save_state=False
        self.csv_stat_label.setText("Csv data stopped saving!")
        ser.write(b"off")
#ploting for air pressure
class MyFigureCanvas(FigureCanvas, anim.FuncAnimation):
    '''
    This is the FigureCanvas in which the live plot is drawn.

    '''
    def __init__(self, x_len:int, y_range:List, interval:int) -> None:
        '''
        :param x_len:       The nr of data points shown in one plot.
        :param y_range:     Range on y-axis.
        :param interval:    Get a new datapoint every .. milliseconds.

        '''
        FigureCanvas.__init__(self, mpl_fig.Figure())
        # Range settings
        self._x_len_ = x_len
        self._y_range_ = y_range

        # Store two lists _x_ and _y_
        x = list(range(0, x_len))
        y = [0] * x_len

        # Store a figure and ax
        self._ax_  = self.figure.subplots()
        self._ax_.set_ylim(ymin=self._y_range_[0], ymax=self._y_range_[1])
        self._line_, = self._ax_.plot(x, y,label='Air Pressure')
        self._ax_.legend()

        # Call superclass constructors
        anim.FuncAnimation.__init__(self, self.figure, self._update_canvas_, fargs=(y,), interval=interval, blit=True)
        return

    def _update_canvas_(self, i, y) -> None:
        '''
        This function gets called regularly by the timer.

        '''
        #y.append(round(get_next_datapoint(), 2))     # Add new datapoint
        y.append(round(get_next_datapoint(), 2)) 
        y = y[-self._x_len_:]                        # Truncate list _y_
        self._line_.set_ydata(y)
        return self._line_,
#plotting for temp
class tempFigureCanvas(FigureCanvas, anim.FuncAnimation):
    '''
    This is the FigureCanvas in which the live plot is drawn.

    '''
    def __init__(self, x_len:int, y_range:List, interval:int) -> None:
        '''
        :param x_len:       The nr of data points shown in one plot.
        :param y_range:     Range on y-axis.
        :param interval:    Get a new datapoint every .. milliseconds.

        '''
        FigureCanvas.__init__(self, mpl_fig.Figure())
        # Range settings
        self._x_len_ = x_len
        self._y_range_ = y_range

        # Store two lists _x_ and _y_
        x = list(range(0, x_len))
        y = [0] * x_len

        # Store a figure and ax
        self._ax_  = self.figure.subplots()
        self._ax_.set_ylim(ymin=self._y_range_[0], ymax=self._y_range_[1])
        self._line_, = self._ax_.plot(x, y,label='Temperature')    
        self._ax_.legend()

        # Call superclass constructors
        anim.FuncAnimation.__init__(self, self.figure, self._update_canvas_, fargs=(y,), interval=interval, blit=True)
        return

    def _update_canvas_(self, i, y) -> None:
        '''
        This function gets called regularly by the timer.

        '''
        #y.append(round(get_next_datapoint(), 2))     # Add new datapoint
        y.append(round(get_next_temp_datapoint(), 2)) 
        y = y[-self._x_len_:]                        # Truncate list _y_
        self._line_.set_ydata(y)
        return self._line_,

#plotting for voltage
class voltageFigureCanvas(FigureCanvas, anim.FuncAnimation):
    '''
    This is the FigureCanvas in which the live plot is drawn.

    '''
    def __init__(self, x_len:int, y_range:List, interval:int) -> None:
        '''
        :param x_len:       The nr of data points shown in one plot.
        :param y_range:     Range on y-axis.
        :param interval:    Get a new datapoint every .. milliseconds.

        '''
        FigureCanvas.__init__(self, mpl_fig.Figure())
        # Range settings
        self._x_len_ = x_len
        self._y_range_ = y_range

        # Store two lists _x_ and _y_
        x = list(range(0, x_len))
        y = [0] * x_len

        # Store a figure and ax
        self._ax_  = self.figure.subplots()
        self._ax_.set_ylim(ymin=self._y_range_[0], ymax=self._y_range_[1])
        self._line_, = self._ax_.plot(x, y,label='Voltage')    
        self._ax_.legend()

        # Call superclass constructors
        anim.FuncAnimation.__init__(self, self.figure, self._update_canvas_, fargs=(y,), interval=interval, blit=True)
        return

    def _update_canvas_(self, i, y) -> None:
        '''
        This function gets called regularly by the timer.

        '''
        #y.append(round(get_next_datapoint(), 2))     # Add new datapoint
        y.append(round(get_next_voltage_datapoint(), 2)) 
        y = y[-self._x_len_:]                        # Truncate list _y_
        self._line_.set_ydata(y)
        return self._line_,

#plotting for speed
class SpeedFigureCanvas(FigureCanvas, anim.FuncAnimation):
    '''
    This is the FigureCanvas in which the live plot is drawn.

    '''
    def __init__(self, x_len:int, y_range:List, interval:int) -> None:
        '''
        :param x_len:       The nr of data points shown in one plot.
        :param y_range:     Range on y-axis.
        :param interval:    Get a new datapoint every .. milliseconds.

        '''
        FigureCanvas.__init__(self, mpl_fig.Figure())
        # Range settings
        self._x_len_ = x_len
        self._y_range_ = y_range

        # Store two lists _x_ and _y_
        x = list(range(0, x_len))
        y = [0] * x_len

        # Store a figure and ax
        self._ax_  = self.figure.subplots()
        self._ax_.set_ylim(ymin=self._y_range_[0], ymax=self._y_range_[1])
        self._line_, = self._ax_.plot(x, y,label='Speed')    
        self._ax_.legend()

        # Call superclass constructors
        anim.FuncAnimation.__init__(self, self.figure, self._update_canvas_, fargs=(y,), interval=interval, blit=True)
        return

    def _update_canvas_(self, i, y) -> None:
        '''
        This function gets called regularly by the timer.

        '''
        #y.append(round(get_next_datapoint(), 2))     # Add new datapoint
        y.append(round(get_next_speed_datapoint(), 2)) 
        y = y[-self._x_len_:]                        # Truncate list _y_
        self._line_.set_ydata(y)
        return self._line_,
'''
# Data source
# ------------
n = np.linspace(0, 499, 500)
d = 50 + 25 * (np.sin(n / 8.3)) + 10 * (np.sin(n / 7.5)) - 5 * (np.sin(n / 1.5))
i = 0
def get_next_datapoint():
    global i
    i += 1
    if i > 499:
        i = 0
    print(d[i])
    return d[i]
    
'''

if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)
    app = ApplicationWindow()
    #global alive_change_label_thread
    qapp.exec_()
    alive_change_label_thread = False
    if ser != None:
        ser.close()
        print("serial closed")