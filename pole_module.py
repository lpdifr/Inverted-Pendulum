import math
import pygame
import glfw
from OpenGL.GL import *
class Pole:
    def __init__(self, mass_of_weight , pole_length ,pole_angle, cart , world ):
        # Inicializtion World and Cart
        #
        self.world = world
        self.cart = cart
        self.radius = 15
        self.segments = 10
        # Setting position
        self.polepointx , self.polepointy = 0 , 0

        # Setting Angle and Lenght of Pole
        self.angle_of_pole = pole_angle
        self.L = pole_length
        

        # Creating varibles of end of pole
        self.x1 , self.y1 = 0 , 0
        self.delta_angle_speed = 0
        # Setting phisics of pole
        self.M = mass_of_weight

        self.angle_speed = 0

    # Function that calculates end pole`s position 
    def endofpole(self):
        self.x1 = self.polepointx + self.L*math.sin(self.angle_of_pole)
        self.y1 = self.polepointy - self.L*math.cos(self.angle_of_pole)

    # Calculate motion phisics 
    def PhisicsCalculate(self):
        self.alpha_angle = (self.world.gravity*math.sin(self.angle_of_pole) - self.cart.a*math.cos(self.angle_of_pole))/self.L
        old_angle_speed = self.angle_speed
        self.angle_speed = self.angle_speed + self.alpha_angle * self.world.dt
        self.delta_angle_speed = self.angle_speed - old_angle_speed
        #print(self.delta_angle_speed)# Show delta
        self.angle_of_pole = self.angle_of_pole + self.angle_speed * self.world.dt




#Creating Cart: Phisics , Drawing , Data