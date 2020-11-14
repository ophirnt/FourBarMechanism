#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 12:16:12 2019

@author: ophir
"""

from math import sin, cos, atan, sqrt, acos
import numpy as np


class FourBarMechanism:
    
    '''Models a four bar mechanism. Input in rad, s and mm. Output in rad, s and mm'''
    
    def solveTheta3(self):
        theta3a = 2 * atan( (-self.E - sqrt(self.E**2 - 4 * self.D * self.F))/(2*self.D) ) 
        theta3c = 2 * atan( (-self.E + sqrt(self.E**2 - 4 * self.D * self.F))/(2*self.D) )
        
        self.theta3 = np.array((theta3a, theta3c))

    def solveTheta4(self):
        theta4a = 2 * atan( (-self.B - sqrt(self.B**2 - 4 * self.A * self.C))/(2*self.A) )
        theta4c = 2 * atan( (-self.B + sqrt(self.B**2 - 4 * self.A * self.C))/(2*self.A) )
        
        self.theta4 = np.array((theta4a, theta4c))
    
    
    def solveOmega3(self):
        omega3a = self.a * self.omega2/self.b * \
        sin(self.theta4[0] - self.theta2) / \
        sin(self.theta3[0] - self.theta4[0])
        
        omega3c = self.a * self.omega2/self.b * \
        sin(self.theta4[1] - self.theta2) / \
        sin(self.theta3[1] - self.theta4[1])
        
        self.omega3 = np.array([omega3a, omega3c])
                                                      
        
    def solveOmega4(self):
        
        omega4a = self.a * self.omega2/self.c * \
        sin(self.theta2 - self.theta3[0]) / \
        sin(self.theta4[0] - self.theta3[0])
        
        omega4c = self.a * self.omega2/self.c * \
        sin(self.theta2 - self.theta3[1]) / \
        sin(self.theta4[1] - self.theta3[1])
        
        self.omega4 = np.array([omega4a, omega4c])
        
    
    def solveAlpha(self):
        
        theta2 = np.array([self.theta2, self.theta2])
        omega2 = np.array([self.omega2, self.omega2])
        alpha2 = np.array([self.alpha2, self.alpha2])
        
        A = self.c * np.sin(self.theta4)
        B = self.b * np.sin(self.theta3)
        C = self.a * alpha2 * np.sin(theta2) + \
            self.a * omega2**2 * np.cos(theta2) + \
            self.b * self.omega3**2 * np.cos(self.theta3) - \
            self.c * self.omega4**2 * np.cos(self.theta4)
        D = self.c * np.cos(self.theta4)
        E = self.b * np.cos(self.theta3)
        F = self.a * alpha2 * np.cos(theta2) - \
            self.a * omega2**2 * np.sin(theta2) - \
            self.b * self.omega3**2 * np.sin(self.theta3) + \
            self.c * self.omega4**2 * np.sin(self.theta4)
            
        
        
        self.alpha3 = (C*D - A*F)/(A*E - B*D)
        self.alpha4 = (C*E - B*F)/(A*E - B*D)
        
        
        
    def solveVa(self):
        self.Va = self.a * self.omega2 * (- sin(self.theta2) + 1j * cos(self.theta2))
        
    def solveVba(self):
            self.Vba = self.b * self.omega3 * (-np.sin(self.theta3) + 1j * np.cos(self.theta3))
        
    def solveVb(self):
        self.Vb = self.c * self.omega4 * (-np.sin(self.theta4) + 1j * np.cos(self.theta4))

    def solveAa(self):
        self.Aa = self.a * self.alpha2 * (-sin(self.theta2) + 1j * cos(self.theta2)) - \
                  self.a * self.omega2**2 * (cos(self.theta2) + 1j * sin(self.theta2))
    
    def solveAab(self):
        self.Aab = self.b * self.alpha3 * (-np.sin(self.theta3) + 1j * np.cos(self.theta3)) - \
                   self.b * self.omega3**2 * (np.cos(self.theta3) + 1j * np.sin(self.theta3))
    
    def solveAb(self):
        self.Ab = self.c * self.alpha4 * (-np.sin(self.theta4) + 1j * np.cos(self.theta4)) - \
                  self.c * self.omega4**2 * (np.cos(self.theta4) + 1j * np.sin(self.theta4))
        
    def solvePositions(self):
        
        self.Ro2 = 0 + 0j
        self.Ro4 = self.d + 0j
        
        self.Ra = self.a * np.e**(1j * self.theta2)
        
        Ra = np.array([self.Ra, self.Ra])
        self.Rb = Ra + self.c * np.e**(1j * self.theta3)
        self.Rp = Ra + self.Rpa * np.e**(1j * ( self.theta3 + np.array([self.delta3, self.delta3]) ))
        
        
    def solveVelocities(self):
        self.solveVa()
        self.solveVba()
        self.solveVb()
        
    
    def solveAccelerations(self):
        self.solveAa()
        self.solveAab()
        self.solveAb()

    def solveVpa(self):
        
        delta = np.array([self.delta3, self.delta3]) + self.theta3
        
        self.Vpa = self.Rpa * self.omega3 * (- np.sin(delta) + 1j * np.cos(delta))
    
    def solveApa(self):
        
        delta = np.array([self.delta3, self.delta3]) + self.theta3
        
        self.Apa = self.Rpa * self.alpha3 * (-np.sin(delta) + 1j * np.cos(delta)) - \
                   self.Rpa * self.omega3**2 * (np.cos(delta) + 1j * np.sin(delta))
                   
    def solveRpaJunction(self):
        self.solveVpa()
        self.solveApa()   
        
        
    
    def isGrashof(self):
        elos = np.array((self.a, self.b, self.c, self.d))
        elos = np.sort(elos)
        
        return elos[0] + elos[3] < elos[1] + elos[2]
    
    def solveTheta2sing(self):
        
        #L2 = self.a
        #L3 = self.b
        #L4 = self.c
        #L1 = self.d
        
        
        if(self.isGrashof()):
            print("Mechanism is Grashof. This formulation is said to work only\
                  in non-Grashof mechanisms, so it might not give off correct results.")
        
        theta2_1 =  (self.a**2 + self.d**2 - self.b**2 -self.c**2) \
                           /(2 * self.a * self.d) + (self.b * self.c) \
                           /(self.a * self.d) 
        
        theta2_2 = (self.a**2 + self.d**2 - self.b**2 -self.c**2) \
                             /(2 * self.a * self.d) - (self.b * self.c) \
                             /(self.a * self.d) 
                             
        if (theta2_1 > -1 and theta2_1 < 1):
            theta2_1 = acos(theta2_1)
        else:
            print("Unable to determine theta2_1 singularity angle. Value is not contained in arccosine's domain")
            theta2_1 = None
        
        if(theta2_2 > -1 and theta2_2 < 1):
            theta2_2 = acos(theta2_2)
        else:
            print("Unable to determine theta2_2 singularity angle. Value is not contained in arccosine's domain")
            theta2_2 = None
        
        self.theta2sing = np.array((theta2_1, theta2_2))
        
        
    def updateTheta2(self, theta2):
        self.theta2 = theta2
        
        self.A = cos(self.theta2) - self.K1 - self.K2 * cos(self.theta2) + self.K3
        self.B = -2 * sin(self.theta2)
        self.C = self.K1 - (self.K2 + 1) * cos(self.theta2) + self.K3
        self.D = cos(self.theta2) - self.K1 + self.K4 * cos(self.theta2) + self.K5
        self.E = -2 * sin(self.theta2)
        self.F = self.K1 + (self.K4 - 1) * cos(self.theta2) + self.K5
        
        self.solveTheta3()
        self.solveTheta4()
        self.solvePositions()
        
        self.solveOmega3()
        self.solveOmega4()
        self.solveVelocities()
        
        self.solveAlpha()
        self.solveAccelerations()
        
        self.solveRpaJunction()
        
         
    def __init__(self, L1, L2, L3, L4, theta2, omega2 = 0, alpha2 = 0, Rpa = 0, \
                 delta3 = 0):
        self.a = L2
        self.b = L3
        self.c = L4
        self.d = L1
        self.theta2 = theta2
        self.omega2 = omega2
        self.alpha2 = alpha2
        self.Rpa = Rpa
        self.delta3 = delta3
        
        self.K1 = self.d/self.a
        self.K2 = self.d/self.c
        self.K3 = (self.a**2 - self.b**2 + self.c**2 + self.d**2)/(2*self.a*self.c)
        self.K4 = self.d/self.b
        self.K5 = (self.c**2 - self.d**2 - self.a**2 - self.b**2)/(2*self.a*self.b)
        
        
        self.solveTheta2sing()
        self.updateTheta2(theta2)
        
        
        