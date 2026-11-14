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


# Inicialization SaveLoadGen
slg = SaveLoadGen()

# Setting up screen
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
        self.frame_counter = 0








# MainLoop variables
running = True
clock = pygame.time.Clock()



# Inicialization Systems
world = Environment()


# Best unit : [-9.117011746541309, 4.569619100723747, -7.344724531657647, -5.944618933983124]
units = Units(world)
units.CreateUnits(1 , slg.LoadLastGen()['weights'] , random_change=(-1.0 , 1.0))#type:ignore

# Resrt flag
if_reset = 0

# Timer when reseting simulation
max_frame = 300000
new_gen = 1
def NewGenFlag():
    new_gen = 0
while running:
    # Timer update
    frame_counter = pygame.time.get_ticks()
    world.frame_counter = frame_counter

    # Event check
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    # If 5-minutes had been past reseting simulation 
    if new_gen:
        units.NewGen()
        pygame.time.set_timer(NewGenFlag() , 5000)
        new_gen = 0


    screen.fill((0 , 0 , 0))


    world.dt = clock.tick(60)/1000#type:ignore


    units.SimulationStep()


    pygame.display.update()


print(f"Generations created: {units.gens_created}")
sys.exit()
