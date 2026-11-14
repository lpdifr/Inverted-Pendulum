import glfw
from OpenGL.GL import *
import math
class Render:
    def __init__(self , world):
        self.world = world
        
    class render:
        def __init__(self):
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
        def wheels(self , cartx , carty):
            pass


        def attachment_point (self , x ,y ):
            glColor3f(1, 1, 0)
            glVertex2f(self.polepointx , self.polepointy)
            for i in range(self.segments + 1):
                angle = 2.0 * math.pi * i / self.segments
                x = self.radius * math.cos(angle)
                y = self.radius * math.sin(angle)
                glVertex2f(self.polepointx + x, self.polepointy + y)


        def weight(self , x , y):
            glColor3f(0, 1, 1)
            glVertex2f(self.x1 , self.y1)
            for i in range(self.segments + 1):
                angle = 2.0 * math.pi * i / self.segments
                x = self.radius * math.cos(angle)
                y = self.radius * math.sin(angle)
                glVertex2f(self.x1 + x, self.y1 + y)


        def pole_line(self , x0 , y0 , x1 , y1):
            glColor3f(0, 1, 0)
            glLineWidth(7)

            glBegin(GL_LINES)
            glVertex2f(x0, y0)
            glVertex2f(x1, y1)