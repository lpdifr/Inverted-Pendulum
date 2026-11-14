import pygame
import math
#Creating Cart: Phisics , Drawing , Data
class Cart:
    def __init__(self ,cartx , carty ,world):
        # World module inicialization
        self.world = world

        # Velocity
        self.v = 0

        # Power pushing cart N/p
        self.F = 0

        # Setting Cart mass
        self.cartmass = 5

        # Setting position
        self.cartx , self.carty = cartx , carty

        # Creating pole socket variable
        self.mainpole = None

    # Debuging moving power 
    def FDebug(self ,F):

        return F

    # Calculating Movement , Friction , Resist etc.
    def PhisicsCalculate(self):
        
        # Debuging F
        self.F = self.FDebug(self.F) 

        # Calculating Movement speed including oppositioning of weight
        self.a = (self.F - self.world.b*self.v + self.mainpole.M*self.mainpole.L*self.mainpole.angle_speed**2 * math.sin(self.mainpole.angle_of_pole) - self.mainpole.M* self.world.gravity *math.sin(self.mainpole.angle_of_pole)*math.cos(self.mainpole.angle_of_pole))/(self.cartmass + self.mainpole.M*math.sin(self.mainpole.angle_of_pole)**2.)#type:ignore
        
        # Calculationg Velocity
        self.v = self.v + self.a * self.world.dt

        # Changing x position of cart
        self.cartx = self.cartx + self.v * self.world.dt


    # Drawing Cart : trunk , wheels
    def drawcart(self):
        
        #Creating trunk rectangle
        rect = pygame.Rect(self.cartx , self.carty , 200 , 100)

        #Left wheel
        pygame.draw.circle(self.world.screen , (30 , 30 , 30) , (self.cartx+15 , self.carty+ 100) ,15)

        #Right wheel
        pygame.draw.circle(self.world.screen , (30 , 30 , 30) , (self.cartx+185 , self.carty+ 100) ,15)

        #Drawing trunk with rectangle
        pygame.draw.rect(self.world.screen , (0 , 50 , 255) , rect  )