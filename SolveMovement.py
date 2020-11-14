#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 17:58:09 2019

@author: ophir
"""

from FourBarMechanism import FourBarMechanism
from math import pi
import pandas as pd
import numpy as np

from plotnine import ggplot, aes, geom_line, geom_point, \
scale_linetype_manual, scale_shape_manual, scale_size_manual, theme_bw, \
labs, theme, element_blank, element_text, element_rect, geom_segment, animation, \
arrow, geom_label, geom_text, coord_cartesian


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

START_TIME = 0
END_TIME = 10
TIME_STEPS = 300
ACC_SCALE = 0.01 #scale acceleration
SCALE_X = (-150, 150) 
SCALE_Y = (-100, 300)

###

mech = FourBarMechanism(*INPUT_DATA)

solution = pd.DataFrame(columns = ['time', 'theta2', 'omega2', 'alpha2', 'Ro2', 'Ro4', 'Ra', 'Rba', 'Rbc', 'Rpa', 'Rpc',
                                   'Va', 'Vba', 'Vbc', 'Vpaa', 'Vpac', 'Aa', 'Aba', 'Abc', 'Apaa', 'Apac', 'theta3a',
                                   'theta3c', 'theta4a', 'theta4c', 'omega3a', 'omega3c', 'alpha3a', 'alpha3c',
                                   'alpha4a', 'alpha4c'\
                                   ])

steps = np.linspace(START_TIME, END_TIME, TIME_STEPS)
deltaT = 0

for time in steps:
    
    deltaT = time - deltaT
    print('Time step:', time, 's')
    
    mech.updateTheta2(mech.theta2 + mech.omega2 * deltaT + mech.alpha2 * deltaT**2/2)
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
    
    print("frame: ", k)
    
    sol = solu[k:k+1]
    
    p = ( ggplot(sol) + 
         # MAIN ELO
         geom_segment(aes(x = 0, y = 0, xend = sol.Ro4[k].real, yend = sol.Ro4[k].imag)) +
         geom_point(aes(x=0, y=0), shape = 'o', size = 3) +
         geom_point(aes(x = sol.Ro4[k].real, y = sol.Ro4[k].imag), shape = 'o', size = 3) +
         # 2ND ELO
         geom_segment(aes(x = 0, y = 0, xend = sol.Ra[k].real, yend = sol.Ra[k].imag)) +
         geom_point(aes(x = sol.Ra[k].real, y = sol.Ra[k].imag), shape = 'o', size = 3) +
         # P ELO
         geom_segment(aes(x = sol.Ra[k].real, y = sol.Ra[k].imag, xend = sol.Rpa[k].real, yend = sol.Rpa[k].imag)) +
         geom_point(aes(x = sol.Rpa[k].real, y = sol.Rpa[k].imag), shape = 'o', size = 3) +
         # 3RD ELO
         geom_segment(aes(x = sol.Ra[k].real, y = sol.Ra[k].imag, xend = sol.Rba[k].real, yend = sol.Rba[k].imag)) +
         geom_point(aes(x = sol.Rba[k].real, y = sol.Rba[k].imag), shape = 'o', size = 3) +
         # 4TH ELO
         geom_segment(aes(x = sol.Rba[k].real, y = sol.Rba[k].imag, xend = sol.Ro4[k].real, yend = sol.Ro4[k].imag)) +
         geom_point(aes(x = sol.Rba[k].real, y = sol.Rba[k].imag), shape = 'o', size = 3) +
         # ACCELERATIONS ARROWS
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
         # ACCELERATIONS TEXT
         geom_text(aes(x = sol.Rba[k].real+10, y = sol.Rba[k].imag+10, label = np.absolute(sol.Aba[k])), colour='red') +
         geom_text(aes(x = sol.Ra[k].real+10, y = sol.Ra[k].imag+10, label = np.absolute(sol.Aa[k])), colour='red') +
         geom_text(aes(x = sol.Rpa[k].real+10, y = sol.Rpa[k].imag+10, label = np.absolute(sol.Apaa[k])), colour='red') +
         #
         labs(x='x', y='y') +
         coord_cartesian(xlim=SCALE_X, ylim=SCALE_Y)
         
         ) 
    
    return p

pd.options.mode.chained_assignment = None # Avoids annoying warning that makes the code run slow 

plotlist = (plot(solution, k) for k in range(TIME_STEPS))



anim = animation.PlotnineAnimation(plotlist, interval = 20)

anim.save('teste6_fixed_deltaT.mp4')
