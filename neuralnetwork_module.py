# Class of AI learning



import random
import math
class Neuron:
    def __init__(self):
        self.z = 0
        self.b = 0
        
class NerualNetwork:
    def __init__(self):
        
        # Setting variables that we gonna collect
        self.cartx = 0
        self.cartv = 0
        self.poleangle = 0
        self.polespeed = 0
        self.action = 0
        self.neurons = []

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
    def RandomWeights(self , reduce ):# we can reduce weight by changing var "reduce" 

        # Weights coefficient
        a = -10 / reduce
        b = 10/ reduce

        # Putting random vaule in weights
        w1 = random.uniform(a , b)
        w2 = random.uniform(a , b)
        w3 = random.uniform(a , b)
        w4 = random.uniform(a , b)
        b  = random.uniform(-1.0 , 1.0)
        return w1, w2, w3, w4
    def DeformWeights(self ,W1 , W2 , W3 , W4, diapazon : tuple = (-1.0 , 1.0)):
        a = diapazon[0]
        b = diapazon[1]
        W1 += random.uniform(a , b)
        W2 += random.uniform(a , b)
        W3 += random.uniform(a , b)
        W4 += random.uniform(a , b)
        return W1 , W2 , W3 , W4
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
    def CalculateAction(self):
        # Setting Z variable
        self.action = 0

        # Calculating Z
        for i in range(len(self.S)):
            self.a += self.S[i]*self.neurons[i]

        # Changing Z by b value 
        
        self.action += self.b

        # Returning vector Z between -1 ; 1
        return math.tanh(self.z)

nn = NerualNetwork()    
w1 , w2 , w3 , w4 = 1 , 1 , 1, 1
w1 , w2 , w3 , w4 = nn.DeformWeights(w1 , w2 ,w3 ,w4)
print(w1 , w2 ,w3 ,w4)