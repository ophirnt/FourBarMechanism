# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 04:45:28 2020

@author: ophir
"""

''' This script provides a good example on how to produce four bar mechanism figures using the FourBarMechanism class. Plots of the mechanism
are produced and animated using plotnine, a ggplot2 port for Python. '''

from FourBarMechanism import FourBarMechanism
from math import pi
import pandas as pd
import numpy as np

from plotnine import ggplot, aes, geom_point, theme_bw, \
labs, geom_segment, animation, arrow, coord_cartesian, annotate

L1 = 152.4
L2 = 50.8
L3 = 177.8
L4 = 228.6
theta2 = 30 * pi/180
omega2 = 10
alpha2 = 0
Rpa = 152.4
delta3 = 30 * pi/180

INPUT_DATA1 = (L1, L2, L3, L4, theta2, omega2, alpha2, Rpa, delta3)

INPUT_DATA = (
        152.4, # L1
        50.8, # L2
        177.8, # L3
        228.6, # L4
        pi/6, # theta2
        10, # omega2
        0, # alpha2
        152.4, # Rpa
        pi/6 # delta3
        )


ACC_SCALE = 0.01 # scale acceleration vectors (otherwise they may get disproportionately long or disproportionately short)
VEL_SCALE = 0.07 # scale velocity vectors (otherwise they may get disproportionately long or disproportionately short)
SCALE_X = (-125, 175) # sets the X limits for the plot frame
SCALE_Y = (-200, 350) # sets the Y limits for the plot frame

###

mech = FourBarMechanism(*INPUT_DATA1) # instantiates a FourBarMechanism object

sol = pd.DataFrame({'theta2': mech.theta2, 
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
                        'omega4a': mech.omega4[0], 
                        'omega4c': mech.omega4[1], 
                        'alpha3a': mech.alpha3[0], 
                        'alpha3c': mech.alpha3[1],
                        'alpha4a': mech.alpha4[0],
                        'alpha4c': mech.alpha4[1]},
                        index = [0])
k = 0
plot = ( ggplot(sol) + 
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
         annotate("text", x = 0, y = -10, label = "$O_1$") +
         annotate("text", x = sol.Ro4[k].real, y = sol.Ro4[k].imag -10, label = "$O_4$") +
         annotate("text", x = sol.Ra[k].real, y = sol.Ra[k].imag -10, label = "$A$") +
         annotate("text", x = sol.Rba[k].real -5, y = sol.Rba[k].imag -10, label = "$B$") +
         annotate("text", x = sol.Rpa[k].real, y = sol.Rpa[k].imag -10, label = "$P$") +
         # VELOCITIES ARROWS (you may remove if you wish to remove acceleration informations)
         geom_segment(aes(x = sol.Rba[k].real, y = sol.Rba[k].imag, \
                          xend = sol.Rba[k].real + sol.Vba[k].real * VEL_SCALE, \
                          yend = sol.Rba[k].imag + sol.Vba[k].imag * VEL_SCALE),\
                      colour='orange', arrow=arrow()) + # Point B
         geom_segment(aes(x = sol.Ra[k].real, y = sol.Ra[k].imag, \
                          xend = sol.Ra[k].real + sol.Va[k].real * VEL_SCALE, \
                          yend = sol.Ra[k].imag + sol.Va[k].imag * VEL_SCALE),\
                      colour='orange', arrow=arrow()) + # Point A
         geom_segment(aes(x = sol.Rpa[k].real, y = sol.Rpa[k].imag, \
                          xend = sol.Rpa[k].real + sol.Vpaa[k].real * VEL_SCALE, \
                          yend = sol.Rpa[k].imag + sol.Vpaa[k].imag * VEL_SCALE),\
                      colour='orange', arrow=arrow()) + # Point C
         # VELOCITIES TEXTS (you may comment if you wish to remove acceleration informations)
         # inputting text between '$ $' makes plotnine produce beautiful LaTeX text
         # positions of the velocities texts may be altered in case the plot gets hard to read
          annotate("text", x = sol.Rba[k].real-1, y = sol.Rba[k].imag-25, label = f'${np.absolute(sol.Vba[k])/1000:.2f}~m/s$', colour='orange') +
          annotate("text", x = sol.Ra[k].real, y = sol.Ra[k].imag+20, label = f'${np.absolute(sol.Va[k])/1000:.2f}~m/s$', colour='orange') +
          annotate("text", x = sol.Rpa[k].real-10, y = sol.Rpa[k].imag-10, label = f'${np.absolute(sol.Vpaa[k])/1000:.2f}~m/s$', colour='orange') +
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
          # positions of the accelerations texts may be altered in case the plot gets hard to read
          annotate("text", x = sol.Rba[k].real, y = sol.Rba[k].imag+10, label = f'${np.absolute(sol.Aba[k])/1000:.2f}~m/s^2$', colour='red') +
          annotate("text", x = sol.Ra[k].real, y = sol.Ra[k].imag-20, label = f'${np.absolute(sol.Aa[k])/1000:.2f}~m/s^2$', colour='red') +
          annotate("text", x = sol.Rpa[k].real+10, y = sol.Rpa[k].imag-20, label = f'${np.absolute(sol.Apaa[k])/1000:.2f}~m/s^2$', colour='red') +
         # MECHANISM KINEMATIC PROPERTIES
           annotate("label", x = -50, y = -100, label = f'$\\theta_2={sol.theta2[k] * 180/(2*pi):.2f}^\\circ$') +
                     # Brackets need to be doubled so Python doesn't interpret 3a or 4a as variables
           annotate("label", x = -10, y = -100, label = f'$\\theta_{{3a}}={sol.theta3a[k] * 180/(2*pi):.2f}^\\circ$, $\\theta_{{3c}}={sol.theta3c[k] * 180/(2*pi):.2f}^\\circ$') + 
           annotate("label", x = 45, y = -100, label = f'$\\theta_{{4a}}={sol.theta4a[k] * 180/(2*pi):.2f}^\\circ$, $\\theta_{{4c}}={sol.theta4c[k] * 180/(2*pi):.2f}^\\circ$') +
           
           annotate("label", x = -50, y = -150, label = f'$\\omega_2={sol.omega2[k]:.2f}~rad/s$') +
           annotate("label", x = 0, y = -150, label = f'$\\omega_{{3a}}={sol.omega3a[k]:.2f}~rad/s$, $\\omega_{{3c}}={sol.omega3c[k]:.2f}~rad/s$') +
           annotate("label", x = 70, y = -150, label = f'$\\omega_{{4a}}={sol.omega4a[k]:.2f}~rad/s$, $\\omega_{{4c}}={sol.omega4c[k]:.2f}~rad/s$') +
           
           annotate("label", x = -50, y = -200, label = f'$\\alpha_2={sol.omega2[k]:.2f}~rad/s^2$') +
           annotate("label", x = 0, y = -200, label = f'$\\alpha_{{3a}}={sol.alpha3a[k]:.2f}~rad/s^2$, $\\alpha_{{3c}}={sol.alpha3c[k]:.2f}~rad/s^2$') +
           annotate("label", x = 70, y = -200, label = f'$\\alpha_{{4a}}={sol.alpha4a[k]:.2f}~rad/s^2$, $\\alpha_{{4c}}={sol.alpha4c[k]:.2f}~rad/s^2$') +
         #
         labs(x='$x~[mm]$', y='$y~[mm]$') +
         coord_cartesian(xlim=SCALE_X, ylim=SCALE_Y) + # Scales plot limits, avoiding it to be bigger than necessary. You may comment this out if you wish to do so.
         theme_bw() # Plot is prettier with this theme compared to the default.
         ) 
    
plot.save('SolutionPlot.pdf', dpi = 330, width = 50, height = 30, units = 'cm')