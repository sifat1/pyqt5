# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 18:38:07 2019

@author: ASUS
"""

from __future__ import annotations
from typing import *
import sys
import os
from matplotlib.backends.qt_compat import QtCore, QtWidgets
# from PyQt5 import QtWidgets, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvas
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib as mpl
import numpy as np

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        