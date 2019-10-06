# Sina Eskandari
# Student number = 97521054
# for more information read 'readme.txt'




import pygame
import sys
import random
from pygame.locals import *

# This part is for initializing the pygame
pygame.init()
# Variables for window
windowWidth = 680
windowHeight = 680
window = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption('Game')
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
FPS = 60
# Choosing a font for displaying texts
font_obj = pygame.font.Font('freesansbold.ttf', 20)


class Ship(pygame.sprite.Sprite):
    '''With This class we can initialize our player(It's a space ship) '''
    global windowWidth, windowHeight

    def __init__(self):
        '''Create the player'''
        # Call the parent class (Sprite) constructor
        super().__init__()
        # Create the image of the ship
        self.image = pygame.image.load('ship.png') # Download from here : http://s9.picofile.com/file/8350448434/ship.png
        # Fetch the rectangle object that has the dimensions of the ship
        self.rect = self.image.get_rect()
        self.shipSize = self.image.get_rect().size
        # Some black part bellow of the ship
        self.distanceFromBottom = 45
        # Define location of ship
        self.X = (windowWidth - self.shipSize[0]) / 2
        self.Y = windowHeight - self.distanceFromBottom
        # Define velocity of ship
        self.velShip = 5

    def update(self):
        '''Update the location of ship'''
        # Moving right
        if keys[K_RIGHT]:
            self.X += self.velShip
            if self.X + self.shipSize[0] > windowWidth:
                self.X = windowWidth - self.shipSize[0]
        # Moving left
        if keys[K_LEFT]:
            self.X -= self.velShip
            if self.X < 0:
                self.X = 0


class Invader(pygame.sprite.Sprite):
    '''This class is for enemy soldiers('Invaders')'''
    def __init__(self):
        '''Create Invaders'''
        # Call the parent class (Sprite) constructor
        super().__init__()
        # Create the image of the invader
        self.image = pygame.image.load('invader1.png') # Download from : http://s8.picofile.com/file/8350448284/invader1.png
        # Fetch the rectangle object that has the dimensions of the invader
        self.rect = self.image.get_rect()
        # Bellow part is not necessary.It's just for reducing the typing
        self.size = self.image.get_rect().size


class Bullet(pygame.sprite.Sprite):
    '''Class for the bullets that our spaceship shoots'''
    def __init__(self):
        '''Create the bullets'''
        # Call the parent class (Sprite) constructor
        super().__init__()
        # Create the image of the bullet and fill it with red
        self.image = pygame.Surface([2, 10])
        self.image.fill((255, 0, 0))
        # Fetch the rectangle object that has the dimensions of the bullet
        self.rect = self.image.get_rect()

    def update(self):
        '''Updating the location of bullets'''
        # With this method our bullets will rise up
        self.rect.y -= 5


class Obstacle(pygame.sprite.Sprite):
    '''This class is for making some obstacles for protecting our spaceship'''
    def __init__(self):
        '''Create the obstacles'''
        # Call the parent class (Sprite) constructor
        super().__init__()
        # Create the image of the obstacle
        self.image = pygame.image.load('obstacle1.png') # Download from: http://s8.picofile.com/file/8350438384/obstacle1.png
        # Fetch the rectangle object that has the dimensions of the obstacle
        self.rect = self.image.get_rect()


class InvBullet(pygame.sprite.Sprite):
    '''This class is for making invaders bullets so they can attack our spaceship'''
    def __init__(self):
        '''Create the bullets'''
        # Call the parent class (Sprite) constructor
        super().__init__()
        # Create the image of the bullet and fill it with blue
        self.image = pygame.Surface([2, 10])
        self.image.fill((0, 0, 255))
        # Fetch the rectangle object that has the dimensions of the obstacle
        self.rect = self.image.get_rect()

    def update(self):
        '''Updating th location of bullets'''
        # With this method bullets can descend and hurt our spaceship
        self.rect.y += 5


class BossFight(pygame.sprite.Sprite):
    '''This class is for making 'THE BOSSFIGHT'
    the boss fight shoots our space ship and if the spaceship kills its invaders he will die and we win the game '''
    def __init__(self):
        '''Creating the bossfight'''
        super().__init__()
        # Create the image of the bossfight
        self.image = pygame.image.load('bossfight.png') # Download from here : http://s9.picofile.com/file/8350449134/bossfight.png
        # Fetch the rectangle object that has the dimensions of the obstacle
        self.rect = self.image.get_rect()

# Define a object of BossFight class
boss = BossFight()
# Define a object of Ship class
ship = Ship()
# Make some sprite groups for drawing and colliding the
shipGroup = pygame.sprite.Group()
inv_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()
bullet_list = pygame.sprite.Group()
obstacle_list = pygame.sprite.Group()
inv_bullet_list = pygame.sprite.Group()
# Add ship and boss to sprite groups
all_sprites_list.add(ship)
all_sprites_list.add(boss)
shipGroup.add(ship)
# This is for making invaders and adding them to sprite groups
for i in range(17):
    for j in range(10):
        invader = Invader()
        invader.rect.x = 50 + (35 * i)
        invader.rect.y = 90 + (27 * j)
        inv_list.add(invader)
        all_sprites_list.add(invader)
# This is for making obstacles and adding them to sprite groups
for i in range(6):
    obstacle = Obstacle()
    obstacle.rect.y = 515
    obstacle.rect.x = 40 + (110 * i)
    obstacle_list.add(obstacle)
    all_sprites_list.add(obstacle)


def collide():
    '''This function checks if enemy's bullets hits the obstacles don't pass from them'''
    for iBullet in inv_bullet_list:
        for obs in obstacle_list:
            if pygame.sprite.collide_rect(iBullet, obs):
                all_sprites_list.remove(iBullet)
                inv_bullet_list.remove(iBullet)


def game_over():
    '''This function quits the game'''
    pygame.quit()
    sys.exit()
# User Score and health
score = 0
health = 100
while True:
    # Fill our surface with black
    window.fill((0, 0, 0))
    # A variable for checking when a key got pressed
    # Actually this for pressing and holding a key because with handling the events if we hold a key the function just calls one time
    keys = pygame.key.get_pressed()
    # Handling the events in game
    for event in pygame.event.get():
        if event.type == QUIT:
            game_over()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                game_over()
        # When we press the space;Makes a bullet and shoots it
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                bullet = Bullet()
                bullet.rect.x = ship.rect.x + (ship.shipSize[0]) / 2
                bullet.rect.y = ship.rect.y
                all_sprites_list.add(bullet)
                bullet_list.add(bullet)
    # Win or lose the game
    if (health <= 0) or (score >= 170):
        game_over()
    # Check if the bullet hits any invader, the invader will be killed
    for bullet in bullet_list:
        hit_list = pygame.sprite.spritecollide(bullet, inv_list, True)

        # This is for removing the bullet when hits the invader
        for i in hit_list:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)

        # If the bullets leave the window gets destroyed
        if bullet.rect.y < -10:
            bullet_list.remove(bullet)
        # We get a score if we kill a invader
        for i in hit_list:
                score += 1
    # Locating the bossfight with rectangular method
    boss.rect.x = 50
    boss.rect.y = 0
    # Making the enemy's bullets
    inv_bullet = InvBullet()
    inv_bullet.rect.x = random.randrange(boss.rect.x, boss.rect.x + boss.rect.size[0])
    inv_bullet.rect.y = boss.rect.size[1]
    inv_bullet_list.add(inv_bullet)
    all_sprites_list.add(inv_bullet)
    for invbullet in inv_bullet_list:
        # If the bullets leave the window gets destroyed
        if invbullet.rect.y > 710:
            inv_bullet_list.remove(invbullet)
        # If the bullet hits us, our health get reduced and also the bullet get destroyed
        if pygame.sprite.collide_rect(invbullet, ship):
            inv_bullet_list.remove(invbullet)
            all_sprites_list.remove(invbullet)
            health -= 2
    # Printing the score and health
    score_text = font_obj.render('Score=' + str(score), True, (255, 255, 255))
    score_text_rect = score_text.get_rect()
    score_text_rect.x = 0
    score_text_rect.y = 0
    health_text = font_obj.render('Health=' + str(health), True, (255, 255, 255))
    health_text_rect = health_text.get_rect()
    health_text_rect.top = 0
    health_text_rect.right = windowWidth
    window.blit(health_text, health_text_rect)
    window.blit(score_text, score_text_rect)
    # Call 'update' method for all sprites
    all_sprites_list.update()
    # Locating our spaceship
    ship.rect.x = ship.X
    ship.rect.y = ship.Y
    # drawing all of sprites
    all_sprites_list.draw(window)
    collide()
    clock.tick(FPS)
    pygame.display.update()
