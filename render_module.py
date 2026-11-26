import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
from numpy import array
import math


class Render:
        def LoadTexture(self ,texture):
            try:
                text = Image.open(texture)
            except IOError as ex:
                print("Failed to open texture file: ", texture)
                text = Image.open("0.png")

            textData = array(list(text.getdata()))
            textID = glGenTextures(1)
            glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
            glBindTexture(GL_TEXTURE_2D, textID)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_BASE_LEVEL, 0)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAX_LEVEL, 0)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, text.size[0], text.size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, textData)
            text.close()
            return textID
        def __init__(self ):
            self.width , self.height = 200 , 100 #Cart width height
            self.radius = 15
            self.segments = 20
            self.wheel_img = self.LoadTexture("textures/wheel.png")
            self.weight_img = self.LoadTexture("textures/weight.png")
        def drawQuad(self , centerX, centerY, textureID):
            glColor3f(1, 1, 1)
            verts = ((15, 15), (15,-15), (-15,-15), (-15,15))
            

            texts = ((1, 0), (1, 1), (0, 1), (0, 0))
            surf = (0, 1, 2, 3)

            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, textureID)

            glBegin(GL_QUADS)
            for i in surf:
                glTexCoord2f(texts[i][0], texts[i][1])
                glVertex2f(centerX + verts[i][0], centerY + verts[i][1])
            glEnd()
            
            glDisable(GL_TEXTURE_2D)
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
            self.drawQuad(x , y , self.weight_img)

        def pole_line(self , x0 , y0 , x1 , y1):

            glColor3f(0, 1, 0)



            glVertex2f(x0, y0)
            glVertex2f(x1, y1)
