#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 12:16:12 2019

@author: ophir
"""

from math import sin, cos, atan, sqrt, acos
import numpy as np


class FourBarMechanism:
    
    '''Models a four bar mechanism. Data must be input in rad, s and mm. Data is outputted in rad, s and mm. 
    Theory taken from "Kinematics and Dyanamics of Machinery", 2010 by Robert L. Norton and Alexandre Scari's classes. 
    Any doubt about the modelling can probably be answered by reading the book.'''
    
    #
    
    '''Important properties and methods:
        
        - Methods:
            
        * updateTheta2(theta2) = Updates theta2 angle property and all other properties relating to theta2. It is mainly called to produce animations
        * isGrashof = Returns a boolean value stating whether the mechanism obeys (True) or not (False) the Grashof condition
        
        - Real numbers:

        * theta2 = Theta2 angle
        * omega2 = Omega2 angular velocity
        * alpha2 = Alpha2 angular acceleration
        * alpha3 = Alpha3 angular acceleration
        * alpha4 = Alpha4 angular acceleration
        * L1 = Length of Link 1
        * L2 = Length of Link 2
        * L3 = Length of Link 3
        * L4 = Length of Link 4
        * Rpa = Length of fixed joint (AP joint)
        * delta3 = angle between the AB joint and the fixed (AP) joint 
        
        - Real number Tuples (index 0 stands for open mechanism, index 1 stands for closed mechanism):

        * theta2sing = Singularty angles of the mechanism (if one or both of the angles are non-existent, the function returns a "None" type value)
        * theta3 = Theta3 angle
        * theta4 = Theta4 angle
        * omega3 = Omega3 angular velocity
        * omega4 = Omega4 angular velocity
        
        - Complex numbers (the mechanism is modeled in 2D space using complex numbers as coordinates. Turns out complex algebra is just more convenient
                           in describing the mechanism state and vectors):
        
        * Va = Va velocity vector
        * Aa = Aa acceleration vector
        * Ro2 = position of node O2 (R stands for displacement vector between the graph's origin and the O2 point)
        * Ro4 = position of node O2
        * Ra = position of node A
        
        - Complex number tuples (basically contains coordinates/vectors that change between open and closed mechanism configurations):
        
        * Vba = Vba velocity vector
        * Vb = Vb velocity vector
        * Aba = Aba acceleration vector
        * Ab = Ab acceleration vector
        * Vpa = Vpa velocity vector (fixed joint velocity)
        * Apa = Apa acceleration vector (fixed joint acceleration)
        * Rb = position of node B
        * Rp = position of node P
        
        There are other methods and properties for this class, but they are mainly for internal usage and don't need to be modified. These include:
            
        * A, B, C, D, E, F, K1, K2, K3, K4 and K5 calculation constants
        * Methods for calculating positions, velocities and accelerations
        * The method for calculating theta2 singularity angles
        
        The algorithm has been tested with a few exercises from Norton's book (like Exercise ), obtaining the correct answers. This should provide enough
        benchmark. If not, please open an issue at https://github.com/ophirnt/FourBarMechanism or send me an e-mail at: ophir.neto@engenharia.ufjf.br.
        
        '''
    
    def solveTheta3(self):
        '''Solves theta3 angle for open (a) and closed (c) positions of the mechanism.'''
        
        theta3a = 2 * atan( (-self.E - sqrt(self.E**2 - 4 * self.D * self.F))/(2*self.D) ) 
        theta3c = 2 * atan( (-self.E + sqrt(self.E**2 - 4 * self.D * self.F))/(2*self.D) )
        
        self.theta3 = np.array((theta3a, theta3c))

    def solveTheta4(self):
        '''Solves theta4 angle for open (a) and closed (c) positions of the mechanism.'''
        
        theta4a = 2 * atan( (-self.B - sqrt(self.B**2 - 4 * self.A * self.C))/(2*self.A) )
        theta4c = 2 * atan( (-self.B + sqrt(self.B**2 - 4 * self.A * self.C))/(2*self.A) )
        
        self.theta4 = np.array((theta4a, theta4c))
    
    
    def solveOmega3(self):
        '''Solves omega3 angular velocity for open (a) and closed (c) positions of the mechanism.'''
        
        omega3a = self.a * self.omega2/self.b * \
        sin(self.theta4[0] - self.theta2) / \
        sin(self.theta3[0] - self.theta4[0])
        
        omega3c = self.a * self.omega2/self.b * \
        sin(self.theta4[1] - self.theta2) / \
        sin(self.theta3[1] - self.theta4[1])
        
        self.omega3 = np.array([omega3a, omega3c])
                                                      
        
    def solveOmega4(self):
        '''Solves omega4 angular velocity for open (a) and closed (c) positions of the mechanism.'''
        
        omega4a = self.a * self.omega2/self.c * \
        sin(self.theta2 - self.theta3[0]) / \
        sin(self.theta4[0] - self.theta3[0])
        
        omega4c = self.a * self.omega2/self.c * \
        sin(self.theta2 - self.theta3[1]) / \
        sin(self.theta4[1] - self.theta3[1])
        
        self.omega4 = np.array([omega4a, omega4c])
        
    
    def solveAlpha(self):
        '''Solves alpha3 and alpha4 angular accelerations of the mechanism.'''
        
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
        '''Calculates the Va velocity vector of the mechanism.'''
        
        self.Va = self.a * self.omega2 * (- sin(self.theta2) + 1j * cos(self.theta2))
        
    def solveVba(self):
        '''Calculates the Vba velocity vector of the mechanism.'''
        
        self.Vba = self.b * self.omega3 * (-np.sin(self.theta3) + 1j * np.cos(self.theta3))
        
    def solveVb(self):
        '''Calculates the Vb velocity vector of the mechanism.'''
        
        self.Vb = self.c * self.omega4 * (-np.sin(self.theta4) + 1j * np.cos(self.theta4))

    def solveAa(self):
        '''Calculates the Aa acceleration vector of the mechanism.'''
        
        self.Aa = self.a * self.alpha2 * (-sin(self.theta2) + 1j * cos(self.theta2)) - \
                  self.a * self.omega2**2 * (cos(self.theta2) + 1j * sin(self.theta2))
    
    def solveAab(self):
        '''Calculates the Aab acceleration vector of the mechanism.'''
        
        self.Aab = self.b * self.alpha3 * (-np.sin(self.theta3) + 1j * np.cos(self.theta3)) - \
                   self.b * self.omega3**2 * (np.cos(self.theta3) + 1j * np.sin(self.theta3))
    
    def solveAb(self):
        '''Calculates the Ab acceleration vector of the mechanism.'''
        
        self.Ab = self.c * self.alpha4 * (-np.sin(self.theta4) + 1j * np.cos(self.theta4)) - \
                  self.c * self.omega4**2 * (np.cos(self.theta4) + 1j * np.sin(self.theta4))
        
    def solvePositions(self):
        '''Calculates the positions of the nodes O2, O4, A, B and P of the mechanism.'''
        
        
        self.Ro2 = 0 + 0j
        self.Ro4 = self.d + 0j
        
        self.Ra = self.a * np.e**(1j * self.theta2)
        
        Ra = np.array([self.Ra, self.Ra])
        self.Rb = Ra + self.c * np.e**(1j * self.theta3)
        self.Rp = Ra + self.Rpa * np.e**(1j * ( self.theta3 + np.array([self.delta3, self.delta3]) ))
        
        
    def solveVelocities(self):
        '''Calls the velocity solving functions.'''
        
        self.solveVa()
        self.solveVba()
        self.solveVb()
        
    
    def solveAccelerations(self):
        '''Calls the acceleration solving functions.'''
        
        self.solveAa()
        self.solveAab()
        self.solveAb()

    def solveVpa(self):
        '''Calculates the Vpa velocity vector of the mechanism.'''
        
        delta = np.array([self.delta3, self.delta3]) + self.theta3
        
        self.Vpa = self.Rpa * self.omega3 * (- np.sin(delta) + 1j * np.cos(delta))
    
    def solveApa(self):
        '''Calculates the Apa acceleration vector of the mechanism.'''
        
        
        delta = np.array([self.delta3, self.delta3]) + self.theta3
        
        self.Apa = self.Rpa * self.alpha3 * (-np.sin(delta) + 1j * np.cos(delta)) - \
                   self.Rpa * self.omega3**2 * (np.cos(delta) + 1j * np.sin(delta))
                   
    def solveRpaJunction(self):
        '''Calls the velocity and acceleration solving functions of the fixed joint.'''
        
        self.solveVpa()
        self.solveApa()   
        
        
    
    def isGrashof(self):
        '''Determines wheter the mechanism obeys or not the Grashof condition.'''
        
        elos = np.array((self.a, self.b, self.c, self.d))
        elos = np.sort(elos)
        
        return elos[0] + elos[3] < elos[1] + elos[2]
    
    def solveTheta2sing(self):
        '''Determines the singularity points of the mechanism.'''
        
        
        if(self.isGrashof()):
            print("Mechanism is Grashof. This formulation is said to work only\
                  in non-Grashof mechanisms, so it might not give off correct results.")
        
        theta2_1 =  (self.a**2 + self.d**2 - self.b**2 -self.c**2) \
                           /(2 * self.a * self.d) + (self.b * self.c) \
                           /(self.a * self.d) 
        
        theta2_2 = (self.a**2 + self.d**2 - self.b**2 -self.c**2) \
                             /(2 * self.a * self.d) - (self.b * self.c) \
                             /(self.a * self.d) 
                             
        if (theta2_1 > -1 and theta2_1 < 1): # Checks if the calculated value can be a cosine of some angle.
            theta2_1 = acos(theta2_1)
        else:
            print("Unable to determine theta2_1 singularity angle. Value is not contained in arccosine's domain")
            theta2_1 = None
        
        if(theta2_2 > -1 and theta2_2 < 1): # Checks if the calculated value can be a cosine of some angle.
            theta2_2 = acos(theta2_2)
        else:
            print("Unable to determine theta2_2 singularity angle. Value is not contained in arccosine's domain")
            theta2_2 = None
        
        self.theta2sing = np.array((theta2_1, theta2_2))
        
        
    def updateTheta2(self, theta2):
        '''Calculates all the poistions, velocities and accelerations of the mechanism, based on the informed input values (omega2, alpha2, Rpa, delta3, L1, L2, L3 and L4)
        and a new theta2 angular position for the input linkage. This is mainly used for initial calculations or for producing four bar mechanism animations in an
        iterative process. '''
        
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
        '''Initializes object properties values and calculates all kinematic properties of the mechanism. 
        Also defines the mechanism's singularity angles and whether it obeys or not the Grashof condition.'''
        
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
        
        
        