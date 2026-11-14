import pygame
import math
import random


from cart_module import Cart
from pole_module import Pole

# Creating simulation enviorment
pygame.init()

sys_font = pygame.font.SysFont("arial", 36, bold=True)
default_font = pygame.font.Font(None, 42)

class Simulation:
    # Creating subclass Score to reward AI
    class Score:
        def __init__(self , pole , cart , world):
            # Creating score variable
            self.score = 0

            # Importing pole and cart to collect info and give rewards
            self.pole = pole
            self.cart = cart
            self.world = world
            # Creating variables
            self.if_balance_score = 0
            self.trying_to_balance = 0
            self.increase_score_timer = 0
            self.time_to_balance_pole = 500
            #self.in_top_time = 0

            # Inicialization simulation to have connection
            self.simulation = None

        # Score system. Rewards and punishment
        def ScoreSystem(self):

            # If end of pole in top then 
            radwraped = (self.pole.angle_of_pole+math.pi)%(2*math.pi)-math.pi
            radiansnormal = radwraped/math.pi
            if radiansnormal < 0.1 and radiansnormal > -0.1:
                if self.trying_to_balance:
                    pass
                else:
                    self.trying_to_balance = 1
                    self.increase_score_timer = self.world.frame_counter + self.time_to_balance_pole
                if self.pole.angle_speed < 0 and self.cart.a > 0 or self.pole.angle_speed > 0 and self.cart.a < 0:
                    self.score += 1
                # Adding time 
                #self.in_top_time += 1
                #print("Time+")

                # If timer is full then give reward
                if self.world.frame_counter > self.increase_score_timer:
                    #print("+Score")

                    # Stabilization angle
                    angle = ((math.degrees(self.pole.angle_of_pole)+ 180)%360)-180

                    # Give reward with buff
                    self.score += 1 + 1 - abs(angle)/ 100
                    self.increase_score_timer = self.world.frame_counter + self.time_to_balance_pole
            else:
                self.trying_to_balance = 0
                #print("Reseting timer")

            #If cart is out of screen restart simulation
            if self.cart.cartx<-200 or self.cart.cartx>self.cart.world.screen.width:
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
        self.cart = Cart((self.world.screen.width//2) - 100 ,(self.world.screen.height//2) +300 , self.world)
        self.pole = Pole(0.2 , 150 , math.radians(180) , self.cart , self.world)

        # Adding pole to main cart
        self.cart.mainpole = self.pole#type:ignore


        # Inicialization of Score system
        self.score = self.Score(self.pole , self.cart , self.world)
        self.a = 0

    #Reseting simulation
    def reset(self):
        
        # Creatin random weights
        if self.if_father:
            self.neuralnetwork.RandomWeights(1)# If we dont have Father
            self.neuralnetwork.GetWeight() # If we dont have Father

        # Old system of reseting
        self.cart = Cart((self.world.screen.width//2) - 100 ,(self.world.screen.height//2) +300 , self.world)
        self.pole = Pole(0.2 , 150 , math.radians(180) , self.cart , self.world)

        #Setting pole to cart
        self.cart.mainpole = self.pole#type:ignore

        #Reseting score
        self.score = self.Score(self.pole , self.cart , self.world)

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
        self.world.screen.blit(scoredisplay , (0 , 0))

        # Frame counter  increasing
        self.a += 1
