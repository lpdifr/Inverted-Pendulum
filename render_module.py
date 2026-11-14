import glfw
from OpenGL.GL import *
import math

class render:
        def __init__(self ):
            self.width , self.height = 200 , 100 #Cart width height
            self.radius = 15
            self.segments = 20

        def cart(self , cartx , carty):
            glColor3f(0, 0.2, 1)

            #glBegin(GL_QUADS)
            glVertex2f(cartx, carty)
            glVertex2f(cartx +self.width, carty)
            glVertex2f(cartx +self.width, carty + self.height)
            glVertex2f(cartx, carty + self.height)



        def attachment_point (self , x ,y ):
            glBegin(GL_TRIANGLE_FAN)
            glColor3f(1, 1, 0)
            glVertex2f(x , y)
            for i in range(self.segments + 1):
                angle = 2.0 * math.pi * i / self.segments
                x = self.radius * math.cos(angle)
                y = self.radius * math.sin(angle)
                glVertex2f(x + x, y + y)
            glEnd()

        def weight(self , x , y):
            glBegin(GL_TRIANGLE_FAN)
            glColor3f(0, 1, 1)
            glVertex2f(x , y)
            for i in range(self.segments + 1):
                angle = 2.0 * math.pi * i / self.segments
                new_x = self.radius * math.cos(angle)
                new_y = self.radius * math.sin(angle)
                glVertex2f(x + new_x, y + new_y)
            glEnd()

        def pole_line(self , x0 , y0 , x1 , y1):

            glColor3f(0, 1, 0)
            glLineWidth(7)


            glVertex2f(x0, y0)
            glVertex2f(x1, y1)
