import pygame
from pygame import mixer
import random
import resources
import game

pygame.init()

screen = pygame.display.set_mode((1000,1000))
#SoundSetting
backgroundSound = mixer.Sound('background.wav')
backgroundSound.play()

explosionSound = mixer.Sound('explosion.wav')
laserSound = mixer.Sound('laser.wav')


#player_initilize
playerX = 500
playerY = 800
playerX_change = 0
playerY_change = 0
playerSpeed = 1.5
def player(x,y):
    screen.blit(resources.spaceshipImg,(x,y))
    
#enemy_initilize
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
def enemy(id):
    screen.blit(resources.enemyImg,(enemyX[id],enemyY[id]))
    
number_of_enemy = 10
for i in range(number_of_enemy):
    enemyX.append(random.randint(0,940))
    enemyY.append(random.randint(0,500))
    enemyX_change.append(random.randint(1,2))
    enemyY_change.append(random.randint(50,60))

#bullet_initilize
bullet_state = 'ready'
bulletX = 500
bulletY = 780
bulletY_change = 0
bulletSpeed = 1.5
def bullet(x,y):
    screen.blit(resources.bulletImg,(x,y))

#score_text
score = 0
score_font = pygame.font.Font("freesansbold.ttf",32)
def showScore(x,y):
    scoreText = score_font.render("Score: " + str(score), True, (255,255,255))
    screen.blit(scoreText,(x,y))

#gameOver
gameOver = pygame.font.Font("freesansbold.ttf",64)
def gameEnd(x,y):
    gameOverText = gameOver.render("Game Over",True,(255,255,255))
    screen.blit(gameOverText,(x,y))


flag = False
running = True
while running:
    screen.blit(resources.backgroundImg,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -playerSpeed
            elif event.key == pygame.K_RIGHT:
                playerX_change = playerSpeed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
        #bulletMovement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    laserSound.play()
                    bulletY_change = bulletSpeed
                    bullet_state  = 'fire'
                    bulletX = playerX
                
    #bulletMovement
    bulletY -= bulletY_change
    if bulletY <= 0:
        bullet_state = 'ready'
        bulletY = 780
        bulletY_change = 0
    if bullet_state == 'ready':
        bullet(playerX,bulletY)
    if bullet_state == 'fire':
        bullet(bulletX,bulletY)
    #playerMovement            
    playerX += playerX_change
    if playerX <=0: playerX = 0
    if playerX >= 940: playerX = 940
    player(playerX,playerY)

    #enemyMovement
    for id in range(number_of_enemy):
        enemyX[id] +=  enemyX_change[id]
        if flag:
            for j in range(number_of_enemy):
                enemyX[j] = 2000
            gameEnd(resources.gameOverX,resources.gameOverY)
            break
        if enemyX[id] >= 940: 
            enemyX[id] = 940
            enemyY[id] += enemyY_change[id]
            enemyX_change[id] = -enemyX_change[id]
        
        if enemyX[id] <= 0: 
            enemyX[id] = 0
            enemyX_change[id] = -enemyX_change[id]
            enemyY[id] += enemyY_change[id]
        enemy(id)
        if game.collision(enemyX[id],enemyY[id],bulletX,bulletY):
            if bullet_state == "ready":
                flag = True
                explosionSound.play()
            score += 1
            enemyX[id] = random.randint(0,940)
            enemyY[id] = random.randint(0,500)
            enemyX_change[id] = random.randint(1,2)
            enemyY_change[id] = random.randint(50,60)
        showScore(resources.textX,resources.textY)
    
    pygame.display.update()