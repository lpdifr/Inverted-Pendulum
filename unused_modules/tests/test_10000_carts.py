import pygame
import sys
import random
screen = pygame.display.set_mode((800 , 600))
pygame.display.set_caption("Chrome Dino")

class Dino:
    def __init__(self):
        self.x , self.y = 100 , 500
        self.width , self.height = 50 ,50
        self.jumping = False
        self.y_gravity = 1
        self.jump_height = 15
        self.y_velocity = self.jump_height
class Enemy:
    def __init__(self , speed , player , ):
        self.width , self.height = random.randint(10 , 20) , random.randint(30 , 50)
        self.x , self.y = 800 , 500 
        
        self.speed = speed
        self.player = player
    def Move(self):
        self.x -= self.speed
        if self.x > 50 and self.x < 100:
           
            if self.player.y+self.player.height > 500 + self.height:
                print("Game over")
                pygame.quit()
                sys.exit()
class World:
    def __init__(self , dino):
        self.enemies = []
        self.dino = dino
    def CreateEnemy(self):
        self.enemies.append(Enemy(10 + 10 * pygame.time.get_ticks()/100000 , self.dino))
    def MoveEnemy(self):
        for enemy in self.enemies:
            enemy.Move()
            enemy_rect = pygame.Rect(enemy.x ,enemy.y ,enemy.width , enemy.height)
            print(self.dino.y ,enemy.x ,enemy.y ,enemy.width , enemy.height)
            pygame.draw.rect(screen , (50 , 50 , 50) , enemy_rect)
            
            if enemy.x-enemy.width < 0:
                index = self.enemies.index(enemy)
                self.enemies.remove(enemy)
clock = pygame.time.Clock()
running = True
dino = Dino()
world = World(dino)
timer = pygame.time.get_ticks()
next_enemy = timer + 2000
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    timer = pygame.time.get_ticks()
    if timer >= next_enemy:
        next_enemy = timer + 2000 - 2000 * pygame.time.get_ticks()/100000
        world.CreateEnemy()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        dino.jumping = True
    if dino.jumping:
        dino.y -= dino.y_velocity
        dino.y_velocity -= dino.y_gravity
        if dino.y_velocity < -dino.jump_height:
            dino.jumping = False
            dino.y_velocity = dino.jump_height
    screen.fill((0 , 0 , 0))
    world.MoveEnemy() 
    dino_rect = pygame.Rect(dino.x , dino.y , dino.width , dino.height)
    pygame.draw.rect(screen , (50 , 50 , 50) , dino_rect)
    pygame.display.update()
    clock.tick(60)
sys.exit()