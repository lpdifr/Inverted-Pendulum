import pygame
import sys

import random
from gen_saver import SaveLoadGen

# Importing modules
from pole_module import Pole
from cart_module import Cart
from neuralnetwork_module import NerualNetwork
from simulation_module import Simulation
from units_module import Units , Unit
pygame.init()


slg = SaveLoadGen()
screen = pygame.display.set_mode((1700, 900))

pygame.display.set_caption("Inverted Pendulum")

# Creating Enviroment



class Environment:
    def __init__(self):
        self.gravity = 900# Gravity pixel per second^2
        self.k = 4# Environment resist
        self.dt = 0# Delta time
        self.b = 4# Environment resist another
        self.screen = screen







#class AIWarden

# MainLoop variables
running = True
clock = pygame.time.Clock()

# Inicialization Systems
world = Environment()
# Best unit : [-9.117011746541309, 4.569619100723747, -7.344724531657647, -5.944618933983124]

units = Units(world)
units.CreateUnits(1000 , slg.LoadLastGen()['weights'] , random_change=(-1.0 , 1.0))#type:ignore
if_reset = 0

max_frame = 300000
while running:
    frame_counter = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pass
                #print("dasdd")
                #units.NewGen()
    if frame_counter >= max_frame:
        units.NewGen()
        max_frame += 300000
    screen.fill((0 , 0 , 0))
    world.dt = clock.tick(60)/1000#type:ignore
    units.SimulationStep()


    pygame.display.update()
    
sys.exit()
"""        # Manual control
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_a]:
            self.cart.F -= 1500#type:ignore
        if keys[pygame.K_d]:
            self.cart.F += 1500#type:ignore

"""