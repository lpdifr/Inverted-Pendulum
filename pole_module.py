import math
import pygame
import glfw
from OpenGL.GL import *
class Pole:
    def __init__(self, mass_of_weight , pole_length ,pole_angle, cart , world ):
        # Inicializtion World and Cart
        self.screen = world.screen
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

    # Drawing Pole weight , line , attachment point
    def drawpole(self):
        # Pole line
        glColor3f(0, 1, 0)
        glLineWidth(7)

        glBegin(GL_LINES)
        glVertex2f(self.polepointx, self.polepointy)
        glVertex2f(self.x1, self.y1)
        glEnd()
        # Attachment point OpenGL
        glBegin(GL_TRIANGLE_FAN)
        glColor3f(1, 1, 0)
        glVertex2f(self.polepointx , self.polepointy)
        for i in range(self.segments + 1):
            angle = 2.0 * math.pi * i / self.segments
            x = self.radius * math.cos(angle)
            y = self.radius * math.sin(angle)
            glVertex2f(self.polepointx + x, self.polepointy + y)
            
        glEnd()
        glBegin(GL_TRIANGLE_FAN)
        glColor3f(0, 1, 1)
        glVertex2f(self.x1 , self.y1)
        for i in range(self.segments + 1):
            angle = 2.0 * math.pi * i / self.segments
            x = self.radius * math.cos(angle)
            y = self.radius * math.sin(angle)
            glVertex2f(self.x1 + x, self.y1 + y)
            
        glEnd()
        # Attachment point
        #pygame.draw.circle(self.screen , (255 , 255 , 0) , (self.polepointx , self.polepointy) ,15)

        # Weight
        #pygame.draw.circle(self.screen , (0 , 255 , 255) , (self.x1 , self.y1) ,15)


#Creating Cart: Phisics , Drawing , Data