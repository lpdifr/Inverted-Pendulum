import pygame
import sys
import math
import random
from gen_saver import SaveLoadGen
pygame.init()

slg = SaveLoadGen()
screen = pygame.display.set_mode((1700, 900))
sys_font = pygame.font.SysFont("arial", 36, bold=True)
default_font = pygame.font.Font(None, 42)
pygame.display.set_caption("Inverted Pendulum")
# Creating Enviroment
class Environment:
    def __init__(self):
        self.gravity = 900# Gravity pixel per second^2
        self.k = 4# Environment resist
        self.dt = 0# Delta time
        self.b = 4# Environment resist another


class Pole:
    def __init__(self, mass_of_weight , pole_length ,pole_angle, cart , world ):
        # Inicializtion World and Cart
        self.world = world
        self.cart = cart

        # Setting position
        self.polepointx , self.polepointy = 0 , 0

        # Setting Angle and Lenght of Pole
        self.angle_of_pole = pole_angle
        self.L = pole_length

        # Creating varibles of end of pole
        self.x1 , self.y1 = 0 , 0

        # Setting phisics of pole
        self.M = mass_of_weight

        self.angle_speed = 0

    # Function that calculates end pole`s position 
    def endofpole(self):
        self.x1 = self.polepointx + self.L*math.sin(self.angle_of_pole)
        self.y1 = self.polepointy - self.L*math.cos(self.angle_of_pole)

    # Calculate motion phisics 
    def PhisicsCalculate(self):
        self.alpha_angle = (self.world.gravity*math.sin(self.angle_of_pole) - self.cart.a*math.cos(self.angle_of_pole))/self.L
        self.angle_speed = self.angle_speed + self.alpha_angle * self.world.dt
        self.angle_of_pole = self.angle_of_pole + self.angle_speed * self.world.dt

    # Drawing Pole weight , line , attachment point
    def drawpole(self):
        # Pole line
        pygame.draw.line(screen , (0 ,255 ,0) , (self.polepointx , self.polepointy) , (self.x1 , self.y1) , 7)

        # Attachment point
        pygame.draw.circle(screen , (255 , 255 , 0) , (self.polepointx , self.polepointy) ,15)

        # Weight
        pygame.draw.circle(screen , (0 , 255 , 255) , (self.x1 , self.y1) ,15)


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
        pygame.draw.circle(screen , (30 , 30 , 30) , (self.cartx+15 , self.carty+ 100) ,15)

        #Right wheel
        pygame.draw.circle(screen , (30 , 30 , 30) , (self.cartx+185 , self.carty+ 100) ,15)

        #Drawing trunk with rectangle
        pygame.draw.rect(screen , (0 , 50 , 255) , rect  )

#Class of AI learning
class NerualNerwork:
    def __init__(self):
        
        # Setting variables that we gonna collect
        self.cartx = 0
        self.cartv = 0
        self.poleangle = 0
        self.polespeed = 0

        # Creating Weights
        self.w1 = 0
        self.w2 = 0
        self.w3 = 0
        self.w4 = 0
        self.W = [self.w1 ,self.w2 ,self.w3 , self.w4]

        # Creating Neuron
        self.S = [self.cartx , self.cartv , self.poleangle , self.polespeed]
        self.z = 0
        self.b = 0

    # Collecting data and putting it in variables
    def GetVars(self , cartx , cartv , poleangle , polespeed):
        self.cartx = cartx
        self.cartv = cartv
        self.poleangle = poleangle
        self.polespeed = polespeed

    # Creating random weights
    def RandomWeights(self , reduce):# we can reduce weight by changing var "reduce" 

        # Weights coefficient
        a = -10 / reduce
        b = 10/ reduce

        # Putting random vaule in weights
        self.w1 = random.uniform(a , b)
        self.w2 = random.uniform(a , b)
        self.w3 = random.uniform(a , b)
        self.w4 = random.uniform(a , b)

    # Setting weights if we got father
    def SetWeights(self , weights):
        self.w1= weights[0]
        self.w2= weights[1]
        self.w3= weights[2]
        self.w4= weights[3]
    # Setting vector
    def GetVector(self , show_vector:int = 0):
        # Putting values in vector
        self.S = [self.cartx , self.cartv , self.poleangle , self.polespeed]

        # If we want to get information about vector
        if show_vector:
            print(self.S)

    # Setting weights in weight
    def GetWeight(self , show_weights:int = 0):
        # Puttig weights in weight
        self.W = [self.w1 ,self.w2 ,self.w3 , self.w4]

        # If we want to get information about weights
        if show_weights:
            print(self.W)

    # Calculating Neuron by weights and vector
    def CalculateNeuron(self):
        # Setting Z variable
        self.z = 0

        # Calculating Z
        for i in range(len(self.S)):
            self.z += self.S[i]*self.W[i]

        # Changing Z by b value 
        self.z += self.b

        # Returning vector Z between -1 ; 1
        return math.tanh(self.z)


# Creating simulation enviorment
class Simulation:
    # Creating subclass Score to reward AI
    class Score:
        def __init__(self , pole , cart):
            # Creating score variable
            self.score = 0

            # Importing pole and cart to collect info and give rewards
            self.pole = pole
            self.cart = cart

            # Creating variables
            self.if_balance_score = 0
            self.in_top_time = 0

            # Inicialization simulation to have connection
            self.simulation = None

        # Score system. Rewards and punishment
        def ScoreSystem(self):

            # If end of pole in top then 
            radwraped = (self.pole.angle_of_pole+math.pi)%(2*math.pi)-math.pi
            radiansnormal = radwraped/math.pi
            if radiansnormal < 0.1 and radiansnormal > -0.1:
                if self.pole.angle_speed < 0 and self.cart.a > 0 or self.pole.angle_speed > 0 and self.cart.a < 0:
                    self.score += 1
                # Adding time 
                self.in_top_time += 1
                #print("Time+")

                # If timer is full then give reward
                if self.in_top_time > 50:
                    #print("+Score")

                    # Stabilization angle
                    angle = ((math.degrees(self.pole.angle_of_pole)+ 180)%360)-180

                    # Give reward with buff
                    self.score += 1 + 1 - abs(angle)/ 100
            else:
                self.in_top_time = 0
                #print("Reseting timer")

            #If cart is out of screen restart simulation
            if self.cart.cartx<-200 or self.cart.cartx>screen.width:
                self.simulation.reset()#type:ignore


            
    def __init__ (self , world , neuralnetwork):
        # Inicialization of systems of AI learning
        self.world = world
        self.neuralnetwork = neuralnetwork
        self.if_father = 0

        # Creating system of perfect timing if AI catches perfect condition , we break it with 1 degrees in random side
        self.if_perfect_time = 0
        self.if_perfect = 0

        # Creating Cart and Pole
        self.cart = Cart((screen.width//2) - 100 ,(screen.height//2) +300 , self.world)
        self.pole = Pole(0.2 , 150 , math.radians(180) , self.cart , self.world)

        # Adding pole to main cart
        self.cart.mainpole = self.pole#type:ignore


        # Inicialization of Score system
        self.score = self.Score(self.pole , self.cart)
        self.a = 0

    #Reseting simulation
    def reset(self):
        
        # Creatin random weights
        if self.if_father:
            self.neuralnetwork.RandomWeights(1)# If we dont have Father
            self.neuralnetwork.GetWeight() # If we dont have Father

        # Old system of reseting
        self.cart = Cart((screen.width//2) - 100 ,(screen.height//2) +300 , self.world)
        self.pole = Pole(0.2 , 150 , math.radians(180) , self.cart , self.world)

        #Setting pole to cart
        self.cart.mainpole = self.pole#type:ignore

        #Reseting score
        self.score = self.Score(self.pole , self.cart)

        #Assing simulation to score
        self.score.simulation = self #type:ignore
        self.a = 0

    # Next step simulation
    def step(self , show_values:int = 0):
        if show_values:
            print(f"Cart F: {self.cart.F}")
            print(f"Cart v: {self.cart.v}")

            print(f"____________________________")
            print(math.degrees(self.pole.angle_of_pole))


        # Normalize cartx pos to -1 to 1
        cartxnormal = (self.cart.cartx - 750)/750

        # Normalize angle to -1 ; 1 
        radwraped = (self.pole.angle_of_pole+math.pi)%(2*math.pi)-math.pi
        radiansnormal = radwraped/math.pi

        # Normolize velocity
        vnorm = self.cart.v/300
        anglespeednorm = self.pole.angle_speed / 10

        # Collecting values and putting it to variables
        self.neuralnetwork.GetVars( cartxnormal, vnorm , radiansnormal , anglespeednorm)

        # Getting Vector
        self.neuralnetwork.GetVector()
        
        # Calculating neouron and saving it to variable a
        a = self.neuralnetwork.CalculateNeuron()

        


        # Anti perfect-condition system
        if ((math.degrees(self.pole.angle_of_pole)+ 180)%360)-180  == 0:
            if self.if_perfect_time == 100:
                self.pole.angle_of_pole = math.radians(random.uniform(-0.1 , 0.1))
                self.if_perfect_time = 0
            self.if_perfect_time += 1

            

        # Setting force to zero
        self.cart.F = 0

        # Adding force multiplied by neuron
        self.cart.F += a * 1500


                
        # Calculation and Drawing Cart
        self.cart.PhisicsCalculate()
        self.cart.drawcart()
            
        # Calculation phisics , moving , drawing pole 
        self.pole.PhisicsCalculate()
        self.pole.polepointx , self.pole.polepointy = self.cart.cartx+100 , self.cart.carty
        self.pole.endofpole()
        self.pole.drawpole()

        # Calling ScoreSystem() to calculate score to add
        self.score.ScoreSystem()

        # Rendering Score
        scoredisplay = sys_font.render(f"Score: {self.score.score:.2f}", True, (255, 255, 255))

        # Display Score
        screen.blit(scoredisplay , (0 , 0))

        # Frame counter  increasing
        self.a += 1

#class AIWarden

# MainLoop variables
running = True
clock = pygame.time.Clock()

# Inicialization Systems
world = Environment()
# Best unit : [-9.117011746541309, 4.569619100723747, -7.344724531657647, -5.944618933983124]
class Unit:
    def __init__(self , unit_weights):
        self.unit_weights = unit_weights
        #___________________________________________________________
        self.neuralnetwork = NerualNerwork()
        #___________________________________________________________
        self.simulation = Simulation(world , self.neuralnetwork)
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
    def __init__(self):
        self.units = []
        self.best_score = 0
        self.if_simulation = 0
        self.quantity = 0
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
            unit = Unit(new_weights)

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
units = Units()
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