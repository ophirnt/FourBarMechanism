#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 17:58:09 2019

@author: ophir
"""

''' This script provides a good example on how to produce four bar mechanism animations using the FourBarMechanism class. Plots of the mechanism
are produced and animated using plotnine, a ggplot2 port for Python. '''

from FourBarMechanism import FourBarMechanism
from math import pi
import pandas as pd
import numpy as np

from plotnine import ggplot, aes, geom_point, theme_bw, \
labs, geom_segment, animation, arrow, coord_cartesian, annotate


INPUT_DATA = (
        152.4, # L1
        50.8, # L2
        177.8, # L3
        228.6, # L4
        0, # theta2
        10, # omega2
        0, # alpha2
        152.4, # Rpa
        pi/6 # delta3
        )

FPS = 72 # Frames per second of animation
START_TIME = 0
END_TIME = 5 # 3.125 mechanism turns
SLOWING_FACTOR = 4 # Slowing factor. 1x is normal speed
TIME_STEPS = int( (END_TIME-START_TIME) * FPS)
ACC_SCALE = 0.01 # scale acceleration vector (otherwise they may get disproportionately long)
SCALE_X = (-125, 175) # sets the X limits for the plot frame
SCALE_Y = (-100, 350) # sets the Y limits for the plot frame

###

mech = FourBarMechanism(*INPUT_DATA) # instantiates a FourBarMechanism object

solution = pd.DataFrame(columns = ['time', 'theta2', 'omega2', 'alpha2', 'Ro2', 'Ro4', 'Ra', 'Rba', 'Rbc', 'Rpa', 'Rpc',
                                   'Va', 'Vba', 'Vbc', 'Vpaa', 'Vpac', 'Aa', 'Aba', 'Abc', 'Apaa', 'Apac', 'theta3a',
                                   'theta3c', 'theta4a', 'theta4c', 'omega3a', 'omega3c', 'alpha3a', 'alpha3c',
                                   'alpha4a', 'alpha4c'\
                                   ]) # Data frame which shall store the four bar mechanism propreties for plotting

theta2_0 = mech.theta2 # Initial position of theta2   
steps = np.linspace(START_TIME, END_TIME, TIME_STEPS) # Time steps of the simulation


# Calculates the mechanism movements and stores them in the DataFrame
for time in steps:

    print('Time step:', time, 's')
    
    # Uses the uniformly accelerated movement position equation to determine new theta2 position and determine new mechanism properties
    mech.updateTheta2(theta2_0 + mech.omega2 * time + mech.alpha2 * time**2/2) 
    
    new = pd.DataFrame({'time': time, 
                        'theta2': mech.theta2, 
                        'omega2': mech.omega2, 
                        'alpha2': mech.alpha2, 
                        'Ro2': mech.Ro2, 
                        'Ro4': mech.Ro4, 
                        'Ra': mech.Ra, 
                        'Rba': mech.Rb[0], 
                        'Rbc': mech.Rb[1], 
                        'Rpa': mech.Rp[0], 
                        'Rpc': mech.Rp[1],
                        'Va': mech.Va, 
                        'Vba': mech.Vb[0], 
                        'Vbc': mech.Vb[1], 
                        'Vpaa': mech.Vpa[0], 
                        'Vpac': mech.Vpa[1], 
                        'Aa': mech.Aa, 
                        'Aba': mech.Ab[0], 
                        'Abc': mech.Ab[1], 
                        'Apaa': mech.Apa[0], 
                        'Apac': mech.Apa[1], 
                        'theta3a': mech.theta3[0],
                        'theta3c': mech.theta3[1], 
                        'theta4a': mech.theta4[0], 
                        'theta4c': mech.theta4[1], 
                        'omega3a': mech.omega3[0], 
                        'omega3c': mech.omega3[1], 
                        'alpha3a': mech.alpha3[0], 
                        'alpha3c': mech.alpha3[1],
                        'alpha4a': mech.alpha4[0],
                        'alpha4c': mech.alpha4[1]},
                        index = [0])
    #print(new)
    
    solution = solution.append(new, ignore_index=True)
    
def plot(solu, k):
    
    # Generates a plot of the four bar mechanism, which represents a frame in the animation
    
    print("Frame: ", k)
    
    sol = solu[k:k+1]
    
    p = ( ggplot(sol) + 
         # MAIN LINKAGE
         geom_segment(aes(x = 0, y = 0, xend = sol.Ro4[k].real, yend = sol.Ro4[k].imag)) +
         geom_point(aes(x=0, y=0), shape = 'o', size = 3) +
         geom_point(aes(x = sol.Ro4[k].real, y = sol.Ro4[k].imag), shape = 'o', size = 3) +
         # 2ND LINKAGE
         geom_segment(aes(x = 0, y = 0, xend = sol.Ra[k].real, yend = sol.Ra[k].imag)) +
         geom_point(aes(x = sol.Ra[k].real, y = sol.Ra[k].imag), shape = 'o', size = 3) +
         # AP LINKAGE
         geom_segment(aes(x = sol.Ra[k].real, y = sol.Ra[k].imag, xend = sol.Rpa[k].real, yend = sol.Rpa[k].imag)) +
         geom_point(aes(x = sol.Rpa[k].real, y = sol.Rpa[k].imag), shape = 'o', size = 3) +
         # 3RD LINKAGE
         geom_segment(aes(x = sol.Ra[k].real, y = sol.Ra[k].imag, xend = sol.Rba[k].real, yend = sol.Rba[k].imag)) +
         geom_point(aes(x = sol.Rba[k].real, y = sol.Rba[k].imag), shape = 'o', size = 3) +
         # 4TH LINKAGE
         geom_segment(aes(x = sol.Rba[k].real, y = sol.Rba[k].imag, xend = sol.Ro4[k].real, yend = sol.Ro4[k].imag)) +
         geom_point(aes(x = sol.Rba[k].real, y = sol.Rba[k].imag), shape = 'o', size = 3) +
         # NODES IDENTIFICATION
         annotate("text", x = 0, y = -20, label = "$O_1$") +
         annotate("text", x = sol.Ro4[k].real, y = sol.Ro4[k].imag -20, label = "$O_4$") +
         annotate("text", x = sol.Ra[k].real+10, y = sol.Ra[k].imag, label = "$A$") +
         annotate("text", x = sol.Rba[k].real +20, y = sol.Rba[k].imag -10, label = "$B$") +
         annotate("text", x = sol.Rpa[k].real, y = sol.Rpa[k].imag -40, label = "$P$") +
         # ACCELERATIONS ARROWS (you may remove if you wish to remove acceleration informations)
         geom_segment(aes(x = sol.Rba[k].real, y = sol.Rba[k].imag, \
                          xend = sol.Rba[k].real + sol.Aba[k].real * ACC_SCALE, \
                          yend = sol.Rba[k].imag + sol.Aba[k].imag * ACC_SCALE),\
                      colour='red', arrow=arrow()) + # Point B
        geom_segment(aes(x = sol.Ra[k].real, y = sol.Ra[k].imag, \
                          xend = sol.Ra[k].real + sol.Aa[k].real * ACC_SCALE, \
                          yend = sol.Ra[k].imag + sol.Aa[k].imag * ACC_SCALE),\
                      colour='red', arrow=arrow()) + # Point A
        geom_segment(aes(x = sol.Rpa[k].real, y = sol.Rpa[k].imag, \
                          xend = sol.Rpa[k].real + sol.Apaa[k].real * ACC_SCALE, \
                          yend = sol.Rpa[k].imag + sol.Apaa[k].imag * ACC_SCALE),\
                      colour='red', arrow=arrow()) + # Point C
         # ACCELERATIONS TEXTS (you may comment if you wish to remove acceleration informations)
         # inputting text between '$ $' makes plotnine produce beautiful LaTeX text
         annotate("text", x = sol.Rba[k].real-30, y = sol.Rba[k].imag+10, label = f'${np.absolute(sol.Aba[k])/1000:.2f}~m/s^2$', colour='red') +
         annotate("text", x = sol.Ra[k].real+20, y = sol.Ra[k].imag-20, label = f'${np.absolute(sol.Aa[k])/1000:.2f}~m/s^2$', colour='red') +
         annotate("text", x = sol.Rpa[k].real+10, y = sol.Rpa[k].imag+20, label = f'${np.absolute(sol.Apaa[k])/1000:.2f}~m/s^2$', colour='red') +
         # TIME IDENTIFICATION
         annotate("label", x = 120, y = -80, label = f'Time: ${sol.time[k]:.2f}~s$', alpha = 1) +
         # 
         labs(x='$x~[mm]$', y='$y~[mm]$') +
         coord_cartesian(xlim=SCALE_X, ylim=SCALE_Y) + # Scales plot limits, avoiding it to be bigger than necessary. You may comment this out if you wish to do so.
         theme_bw() # Plot is prettier with this theme compared to the default.
         ) 
    
    return p

pd.options.mode.chained_assignment = None # Avoids annoying warning that makes the code run slow 

# Iterates on the solution DataFrame and produces animation frames, storing them on a list
plotlist = [plot(solution, k) for k in range(TIME_STEPS)]

#%%
# Creates and saves an animation based on the frames list. You may change the interval value to make the animation faster or slower.
# Interval represents the delay between frames in miliseconds.If the interval is too long, the animation becomes very static and slow. Otherwise, 
# it gets very stuttery and fast. It is recommended to only alter the FPS, START_TIME, END_TIME and SLOWING_FACTOR parameters to adjust the animation.

print("Creating animation file. This may take a while.")

anim = animation.PlotnineAnimation(plotlist, interval = 1/FPS * 1000 * SLOWING_FACTOR) 

print("Saving animation file. This may take a while.")

anim.save('Animation.mp4')

print("Animation file saved.")