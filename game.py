import math
def collision(playerX,playerY,enemyX,enemyY):
    return math.sqrt(math.pow(playerX - enemyX,2) + math.pow(playerY - enemyY,2)) <= 27

