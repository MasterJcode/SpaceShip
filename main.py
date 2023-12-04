import pygame 
import random
import math
from pygame import mixer

#Initialize the pygame
pygame.init()

#Create the screen 
screen = pygame.display.set_mode((1000, 1000))

#Caption and icon
pygame.display.set_caption("Snake Game")
icon = pygame.image.load('snake.png')
pygame.display.set_icon(icon)

#backgroundSound
mixer.music.load('background.wav')
mixer.music.play(-1)
explosion_sound = mixer.Sound('explosion.wav')
laser_sound = mixer.Sound('laser.wav')
#mainPlayer
playerImg = pygame.image.load('spaceship.png')
playerX = 500
playerY = 800
speed = 0.4
def player(x,y):
    #blit() actually means to draw
    screen.blit(playerImg, (x,y))
    
xChange = 0
yChange = 0

#bullet 
bulletImg = pygame.image.load('bullet.png')
bulletX = 500
bulletY = 800
bulletY_change = 1.5
bullet_state = "ready"

def fire(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x+16,y-5))
    

#enemy
enemyImg = pygame.image.load('enemy.png')
enemyX = random.randint(0,735)
enemyY = random.randint(200,500)
enemyX_change = 1
enemyY_change = 60

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
numEnemies = 5

for i in range(numEnemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(200,500))
    enemyX_change.append(4)
    enemyY_change.append(60)
    
def enemy(i):
    screen.blit(enemyImg[i],(enemyX[i],enemyY[i]))
#background_image
background = pygame.image.load('background.jpg')

def isCollison(x,y,u,v):
    distance = math.sqrt(math.pow(abs(x - u),2) + math.pow(abs(y - v),2))
    if distance < 27: 
        return True
    else:
        return False
    
#score
score_value = 0
font = pygame.font.Font("freesansbold.ttf",32)
textX = 10
textY = 10

over_font = pygame.font.Font("freesansbold.ttf",64)

def gameEnd(x,y):
    gameOverText = over_font.render("GAME OVER", True, (255,255,255))
    screen.blit(gameOverText,(x,y))
    
def showScore(x,y):
    score = font.render("Score : " + str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))
    
#Here's the game loop
running = True
while running:
    
    #RGB - Red, Green, Blue
    #screen.fill((0,255,255))
    
    #Draw background
    screen.blit(background,(0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        #KeyEvent
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                xChange = -speed
            if event.key == pygame.K_RIGHT:
                xChange = speed
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                xChange = 0
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and bullet_state is "ready":
                laser_sound.play()
                bulletX = playerX
                fire(bulletX,playerY)
                
    #add boundary
    playerX += xChange
    playerY += yChange
    if playerX >= 936: playerX = 936     #substract playerIMG pixel
    if playerX <= 0: playerX = 0
    player(playerX,playerY)
    
    #add bullet movement
    if bulletY <= 0: 
        bulletY = 800
        bullet_state = "ready"
        
    if bullet_state is "fire":
        fire(bulletX,bulletY)
        bulletY -= bulletY_change
    
    #add enemy's movement vs boudary
    for i in range(numEnemies):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] >= 936: 
            enemyX_change[i] = -enemyX_change[i]
            enemyY[i] += enemyY_change[i]
        if enemyX[i] <=0:
            enemyX_change[i] = -enemyX_change[i]
            enemyY[i] += enemyY_change[i]
        enemy(i)  
        
        gameOver = (enemyY[i] >= 800)
        if gameOver:
            for j in range(numEnemies):
                enemyY[j] = 2000
            gameEnd(500,500)
            break 
        
        collision = isCollison(bulletX,bulletY,enemyX[i],enemyY[i])
        if collision:
            explosion_sound.play()
            enemyX[i] = random.randint(0,800)
            enemyY[i] = random.randint(200,500)
            bulletY = 800
            bullet_state = "ready"
            score_value += 1    
            
    showScore(textX,textY)
    pygame.display.update()

