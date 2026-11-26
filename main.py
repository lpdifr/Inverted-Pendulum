import pygame
import glfw
from OpenGL.GL import *
import sys
import numpy as np
import random
import win32api, win32con, win32console
import multiprocessing
from gen_saver import SaveLoadGen
from console_module import DeveloperConsole


import rust_module
from rust_module import Simulation
from render_module import Render
if __name__ == "__main__":
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
    steps = 0

    units_quantity = 10000
    # Inicialization Systems
    world = Environment()
    simulation = Simulation()
    def CreateRandomSimulation(start_angle : float = 180.0):
        simulation.create_simulation(units_quantity ,
                                    [
                                        [random.uniform(-10.0 , 10.0), random.uniform(-10.0 , 10.0), random.uniform(-10.0 , 10.0), random.uniform(-10.0 , 10.0)],
                                        [random.uniform(-10.0 , 10.0), random.uniform(-10.0 , 10.0), random.uniform(-10.0 , 10.0), random.uniform(-10.0 , 10.0)],
                                        [random.uniform(-10.0 , 10.0), random.uniform(-10.0 , 10.0), random.uniform(-10.0 , 10.0), random.uniform(-10.0 , 10.0)],
                                        [random.uniform(-10.0 , 10.0), random.uniform(-10.0 , 10.0), random.uniform(-10.0 , 10.0), random.uniform(-10.0 , 10.0)],

                                    ],
                                    [random.uniform(-10.0 , 10.0), random.uniform(-10.0 , 10.0), random.uniform(-10.0 , 10.0), random.uniform(-10.0 , 10.0)],
                                    start_angle
                                    )
    CreateRandomSimulation(5.0)
    buffer = np.zeros((units_quantity, 3), dtype=np.float64)


    # Best unit : [-9.117011746541309, 4.569619100723747, -7.344724531657647, -5.944618933983124]

    render = Render()


    # Timer when reseting simulation
    max_frame = 2.5 * 60000

    showfps = 3000
    gens_created = 0

    world.frame_counter = 0.083333

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    multiprocessing.freeze_support()
    devcon = DeveloperConsole()
    p = multiprocessing.Process(target=devcon.ShowConsole)
    p.start()

    running = True
    while running:
        glfw.poll_events()
        if devcon.quit_com.value:
            running = False
        if devcon.brandnewsim.value:
            CreateRandomSimulation()
            simulation.reset_simulation()
            devcon.brandnewsim.value = False
        # Timer update
        frame_counter = pygame.time.get_ticks()

            
        if steps > 18000:
            steps = 0
            slg.SaveGen(*simulation.reset_simulation())
            lastgen = slg.LoadLastGen()
            simulation.create_simulation(units_quantity , lastgen["weights"] , lastgen["bias"] , 0.0)
            max_frame += 2.5 * 60000
            gens_created += 1
            print(steps)
        
        # Screen Clear
        glClear(GL_COLOR_BUFFER_BIT)

        # Render first 100 units
        world.dt = clock.tick(60)/1000#type:ignore
        for unit_data in buffer[devcon.render_range[0]:devcon.render_range[1]]:

                glBegin(GL_QUADS)
                render.cart(unit_data[0] , 700)
                glEnd()
                glLineWidth(7)
                glBegin(GL_LINES)

                render.pole_line(unit_data[0] + 100 , 700 , unit_data[1] , unit_data[2])
                glEnd()
                render.weight(unit_data[1] , unit_data[2])

        if not devcon.pause_com.value:
            simulation.step(buffer)
            steps += 1


        glfw.swap_buffers(screen)


    print(f"Generations created: {gens_created}")
    sys.exit()
