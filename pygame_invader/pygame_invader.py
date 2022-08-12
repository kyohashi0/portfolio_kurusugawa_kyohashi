import pygame
from pygame import mixer
import random
import math
import sys
import numpy as np

# Initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Title
pygame.display.set_caption('Space Invaders')

# Player
playerImg = pygame.image.load('player.png')
playerX, playerY = 370, 480
playerX_change = 0

# Enemy
enemyImg = pygame.image.load('enemy.png')
enemyX = random.randint(0, 736)
enemyY = random.randint(50, 150)
enemyX_change, enemyY_change = 0, 20


# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX, bulletY = 0, 480
bulletX_change, bulletY_change = 0, 3
bullet_state = 'ready'

#Bullet2
bulletX2, bulletY2 = enemyX, enemyY
bulletX2_change, bulletY2_change = 0, -3
bullet_state2 = 'ready'

#Count
count = 0
count2 = 0
def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y):
    screen.blit(enemyImg, (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))
    
def fire_bullet2(x, y):
    global bullet_state2
    bullet_state2 = 'fire'
    screen.blit(bulletImg, (x - 16, y - 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False
    
def isCollision2(playerX, playerY, bulletX2, bulletY2):
    distance = math.sqrt(math.pow(playerX - bulletX2, 2) + math.pow(playerY - bulletY2, 2))
    if distance < 27:
        return True
    else:
        return False
    
    
        
def main():
    global playerX,playerX_change,enemyX,enemyY,enemyX_change,bulletX,bulletY,bullet_state,bulletX2,bulletY2,bullet_state2,count,count2
    running = True
    FPS = 180
    clock = pygame.time.Clock()
    while running:
        clock.tick(FPS)
        # RGB = Red, Green, Blue
        screen.fill((0, 0, 0))
        # playerX += 0.1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -2.5
                if event.key == pygame.K_RIGHT:
                    playerX_change = 2.5
                if event.key == pygame.K_SPACE:
                    if bullet_state is 'ready':
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)


        # Player
        playerX += playerX_change   
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        # Enemy
        if enemyY > 410:
            pygame.init()
            gameover_menu()
        
        count += 1
        if count >= 150:
            enemyY += enemyY_change
            count = 0
            
        move = np.random.choice([4, -4], p=[0.5, 0.5])
        enemyX += enemyX_change
        count2 += 1
        if count2 > 50:
            enemyX_change = move
            count2 = 0
        if enemyX <= 0:
            enemyX_change = 4
            enemyY += enemyY_change
        elif enemyX >=736:
            enemyX_change = -4
            
        if bullet_state2 == 'ready':
            fire_bullet2(bulletX2, bulletY2)
            


        collision = isCollision(enemyX, enemyY, bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = 'ready'
            enemyX = random.randint(0, 736)
            enemyY = random.randint(50, 150)
        enemy(enemyX, enemyY)
        
        collision2 = isCollision2(playerX, playerY, bulletX2, bulletY2)
        if collision2:
            gameover_menu()
            bullet_state = 'ready'
            
            


        # Bullet Movement
        if bulletY <=0:
            bulletY = 480
            bullet_state = 'ready'

        if bullet_state is 'fire':
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change 
            
        # Bullet2 Movement
        if bulletY2 >= 700:
            bulletX2 = enemyX
            bulletY2 = enemyY
            bullet_state2 = 'ready'

        if bullet_state2 is 'fire':
            fire_bullet2(bulletX2, bulletY2)
            bulletY2 -= bulletY2_change 



        player(playerX, playerY)
        pygame.display.update()
        
def game_menu():
    title_font = pygame.font.Font("ipag.ttf", 70)
    title_font2 = pygame.font.Font("ipag.ttf", 50)
    running = True
    while running:
        game_name = title_font.render('Space Invaders', 1, (255,0,0))
        title = title_font.render('Start？', 1, (255,255,255))
        key_botton = title_font2.render('スペースキーを押してください', 1, (255,255,255))
        screen.blit(game_name,(160, 180))
        screen.blit(title, (300, 250))
        screen.blit(key_botton, (50, 320))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pygame.init()
                main()
            
    pygame.quit()
    
def gameover_menu():
    title_font = pygame.font.Font("ipag.ttf", 70)
    running = True
    while running:
        title = title_font.render('GAMEOVER', 1, (255,255,255))
        screen.blit(title, (250, 250))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.init()
                running = False
    pygame.quit()



game_menu()