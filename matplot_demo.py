# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 01:01:14 2019

@author: ASUS
"""

import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

style.use('fivethirtyeight')

fig = plt.figure()

def create_plots():
    xs = []
    ys = []

    for i in range(10):
        x = i
        y = random.randrange(10)

        xs.append(x)
        ys.append(y)
    return xs, ys

ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223)
ax4 = fig.add_subplot(224)
def animate(i):
    x,y = create_plots()
    ax1.clear()
    ax1.plot(x,y)

    x,y = create_plots()
    ax2.clear()
    ax2.plot(x,y)

    x,y = create_plots()
    ax3.clear()
    ax3.plot(x,y)

    x,y = create_plots()
    ax4.clear()
    ax4.plot(x,y)

ani = animation.FuncAnimation(fig,animate, interval=1000)

plt.show()