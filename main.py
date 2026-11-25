import pygame
import glfw
from OpenGL.GL import *
import sys
import numpy as np
import random
from gen_saver import SaveLoadGen

# Importing modules
from pole_module import Pole
from cart_module import Cart
from neuralnetwork_module import NerualNetwork
#from simulation_module import Simulation
from units_module import Units , Unit
import rust_module
from rust_module import Simulation
from render_module import Render

pygame.init()

glfw.init()

# Inicialization SaveLoadGen
slg = SaveLoadGen()

# Setting up screen

screen = glfw.create_window(1700 , 900,  "Inverted Pendulum" , None , None)
glfw.set_window_pos(screen , 100,100) 
glfw.make_context_current(screen)
glViewport(0 , 0 , 1700 , 900)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
glOrtho(0, 1700, 900, 0, -1, 1)
glMatrixMode(GL_MODELVIEW)

glLoadIdentity()
glClearColor(0 , 0 , 0 , 0)
# Creating Enviroment
class Environment:
    def __init__(self):
        self.gravity = 900# Gravity pixel per second^2
        self.k = 4# Environment resist
        self.dt = 0# Delta time
        self.b = 4# Environment resist another
        self.screen = screen
        self.frame_counter = 0
        self.width , self.height = glfw.get_window_size(screen)
        self.render = 1






# MainLoop variables
running = True
clock = pygame.time.Clock()


units_quantity = 10000
# Inicialization Systems
world = Environment()
simulation = Simulation()
simulation.create_simulation(units_quantity ,
                             [
                                [-9.117011746541309, 4.569619100723747, -7.344724531657647, -5.944618933983124],
                                [-9.117011746541309, 4.569619100723747, -7.344724531657647, -5.944618933983124],
                                [-9.117011746541309, 4.569619100723747, -7.344724531657647, -5.944618933983124],
                                [-9.117011746541309, 4.569619100723747, -7.344724531657647, -5.944618933983124],

                             ],
                            [1.0 , 0.5 , -1.2 , -0.1]
                             )
buffer = np.zeros((units_quantity, 3), dtype=np.float64)


# Best unit : [-9.117011746541309, 4.569619100723747, -7.344724531657647, -5.944618933983124]
units = Units(world)
units.CreateUnits(units_quantity , slg.LoadLastGen()['weights'] , random_change=(-10.0 , 10.0))#type:ignore
render = Render()
# Resrt flag
if_reset = 0

# Timer when reseting simulation
max_frame = 60*1000
def MiddleFPS(listoffps):
    fpssum = 0
    for fps in listoffps:
        fpssum += fps
    return fpssum/len(listoffps)
showfps = 3000
fpslist = []
world.frame_counter = 0.083333
while not glfw.window_should_close(screen):
    fpslist.append(clock.get_fps())
    glfw.poll_events()
    # Timer update
    frame_counter = pygame.time.get_ticks()


    # Event check
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    # If 5-minutes had been past reseting simulation 
    if frame_counter >= showfps:
        print(MiddleFPS(fpslist))
        showfps += 3000
        fpslist.clear()
        
    if frame_counter >= max_frame:
        units.NewGen()
        max_frame += 60*1000
    

    glClear(GL_COLOR_BUFFER_BIT)

    world.dt = clock.tick(60)/1000#type:ignore
    for unit_data in buffer:
        glBegin(GL_QUADS)
        render.cart(unit_data[0] , 700)
        glEnd()
        render.pole_line(unit_data[0] + 100 , 700 , unit_data[1] , unit_data[2])
        render.weight(unit_data[1] , unit_data[2])

    simulation.step(buffer)
    glfw.swap_buffers(screen)





print(f"Generations created: {units.gens_created}")
sys.exit()
