import pygame
import glfw
from OpenGL.GL import *
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


# Inicialization SaveLoadGen
slg = SaveLoadGen()

# Setting up screen

screen = glfw.create_window(1700 , 900,  "Inverted Pendulum" , None , None)
glfw.set_window_pos(screen , 100,100) 
glfw.make_context_current(screen)
#screen = pygame.display.set_mode((1700, 900))
#pygame.display.set_caption("Inverted Pendulum")



# Creating Enviroment
class Environment:
    def __init__(self):
        self.gravity = 900# Gravity pixel per second^2
        self.k = 4# Environment resist
        self.dt = 0# Delta time
        self.b = 4# Environment resist another
        self.screen = screen
        self.frame_counter = 0








# MainLoop variables
running = True
clock = pygame.time.Clock()



# Inicialization Systems
world = Environment()


# Best unit : [-9.117011746541309, 4.569619100723747, -7.344724531657647, -5.944618933983124]
units = Units(world)
units.CreateUnits(2000 , slg.LoadLastGen()['weights'] , random_change=(-1.0 , 1.0))#type:ignore

# Resrt flag
if_reset = 0

# Timer when reseting simulation
max_frame = 60*1000

while not glfw.window_should_close(screen):

    # Timer update
    frame_counter = pygame.time.get_ticks()
    world.frame_counter = frame_counter

    # Event check
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    # If 5-minutes had been past reseting simulation 
    if frame_counter >= max_frame:
        units.NewGen()
        max_frame += 60*1000


    screen.fill((0 , 0 , 0))


    world.dt = clock.tick(60)/1000#type:ignore


    units.SimulationStep()


    pygame.display.update()


print(f"Generations created: {units.gens_created}")
sys.exit()
