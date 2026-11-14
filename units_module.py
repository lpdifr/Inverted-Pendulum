import pygame
import sys

import random
from gen_saver import SaveLoadGen

# Importing modules
from pole_module import Pole
from cart_module import Cart
from neuralnetwork_module import NerualNetwork
from simulation_module import Simulation
from gen_saver import SaveLoadGen
pygame.init()
slg = SaveLoadGen()
class Unit:
    def __init__(self , unit_weights , world):
        self.unit_weights = unit_weights
        self.world = world
        #___________________________________________________________
        self.neuralnetwork = NerualNetwork()
        #___________________________________________________________
        self.simulation = Simulation(self.world , self.neuralnetwork)
        #___________________________________________________________
        self.simulation.score.simulation = self.simulation#type:ignore
        #___________________________________________________________

        # If we dont have father

        #neuralnetwork.RandomWeights(1)
        #___________________________________________________________
        self.neuralnetwork.SetWeights(unit_weights)#Few models father

        # Assing weights
        self.neuralnetwork.GetWeight()


class Units:
    def __init__(self , world):
        self.units = []
        self.best_score = 0
        self.if_simulation = 0
        self.quantity = 0
        self.world = world
        self.gens_created = 0
    def CreateUnits(self , quantity , weights , random_change:tuple = (-0.1 , 0.1)):
        # Reduce or increase weigths coeficient
        acof , bcof = random_change
        self.quantity = quantity
        self.if_simulation = 1
        # Creating n quantity Units
        for unit_creating in range(quantity):

            # Coping original weights to create new 
            new_weights = weights.copy()

            #Changing every weight for random value setted by acof and bcof
            for index ,weight in enumerate(new_weights):
                new_weights[index] = weight + random.uniform(acof , bcof)

            # Creating new Unit with changed weights
            unit = Unit(new_weights , self.world)

            # Adding new unit to unit list
            self.units.append(unit)

    # Make a step in simulation
    def SimulationStep(self):
        for unit in self.units:
            unit.simulation.step()

    # Reseting
    def SimulationReset(self):
        for unit in self.units:
            unit.simulation.reset()


    def NewGen(self):
        if not self.if_simulation:
            return
        
        best_score , weights = self.ReturnBestUnit()
        print(best_score)
        self.units.clear()
        self.CreateUnits(self.quantity , weights)
        if best_score > self.best_score:
            slg.SaveGen(weights)
            self.gens_created += 1


        
        
    # Finding best unit 
    def ReturnBestUnit(self):

        # Creating lists with scores and weights to choose the best one soon
        scores = []
        weights = []

        # Coping units data to list
        for unit in self.units:
            scores.append(unit.simulation.score.score)
            weights.append(unit.unit_weights)

        # Searching for best score
        best_index = scores.index(max(scores))

        # Returning our winner 
        return max(scores) , weights[best_index]