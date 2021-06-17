import pygame
pygame.font.init()

width, height = 600, 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Space Invaders')
font = pygame.font.SysFont('comicsans', 70)

# ASSETS
background = pygame.transform.scale(pygame.image.load('assets/background-black.png'), (width, height))
red_ship = pygame.image.load('assets/pixel_ship_red_small.png')
green_ship = pygame.image.load('assets/pixel_ship_green_small.png')
blue_ship = pygame.image.load('assets/pixel_ship_blue_small.png')
yellow_ship = pygame.image.load('assets/pixel_ship_yellow.png')
pixel_laser_red = pygame.image.load('assets/pixel_laser_red.png')
pixel_laser_green = pygame.image.load('assets/pixel_laser_green.png')
pixel_laser_blue = pygame.image.load('assets/pixel_laser_blue.png')
pixel_laser_yellow = pygame.image.load('assets/pixel_laser_yellow.png')

class Laser:
    def __init__(self, x, y, laser):
        self.x = x
        self.y = y
        self.laser = laser
        self.mask = pygame.mask.from_surface(self.laser)
    
    def draw(self):
        win.blit(self.laser, (self.x, self.y))
    
    def move(self, vel):
        self.y += vel
    
    def off_screen(self):
        return self.y > height or self.y < -40
    
    def collide(self, obj):
        return collide(self, obj)


class Ship:
    colors = {
        'red': (red_ship, pixel_laser_red),
        'green': (green_ship, pixel_laser_green),
        'blue': (blue_ship, pixel_laser_blue)
    }

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.ship = color
        self.lasers = []
        self.ship, self.laser  = self.colors[color]
        self.mask = pygame.mask.from_surface(self.ship)
    
    def draw(self):
        win.blit(self.ship, (self.x, self.y))

        for laser in self.lasers:
            if laser.off_screen():
                self.lasers.remove(laser)
            else:
                laser.draw()
                laser.move(5)
    
    def move(self, vel):
        self.y += vel
    
    def off_screen(self):
        return self.y > height or self.y < -40

class Player:
    def __init__(self):
        self.ship = yellow_ship
        self.x = width/2 - self.ship.get_width()/2
        self.y = height - self.ship.get_height() - 50
        self.lasers = [] # Laser(self.x, self.y - 18)
        self.healthbar = [(0, 211, 7) for _ in range(8)] # red: (226, 22, 2)
        self.shoot = False
        self.mask = pygame.mask.from_surface(self.ship)

    def draw(self):
        win.blit(self.ship, (self.x, self.y))

        for i, color in enumerate(self.healthbar):
            pygame.draw.rect(win, color, (self.x +10 + (i*10), self.y + 100, 10, 10))
        
        for laser in self.lasers:
            if laser.off_screen():
                self.lasers.remove(laser)
            else:
                laser.draw()
                laser.move(-5)


def collide(obj1, obj2):
    offset_x = int(obj2.x - obj1.x)
    offset_y = int(obj2.y - obj1.y)
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def main():
    run = True
    player = Player()
    enemies = [Ship(width/2, 0, 'red'), Ship(width/2-150, 0, 'green')]
    health = len(player.healthbar)
    lives = 1
    level = 0
    lost = False
    clock = pygame.time.Clock()

    def draw_window():
        player.draw()

        font2 = pygame.font.SysFont('comicsans', 50)
        lives_text = font2.render(f'Lives: {lives}', 1, (255,255,255))
        level_text = font2.render(f'Level: {level}', 1, (255,255,255))
        win.blit(lives_text, (10,10))
        win.blit(level_text, (width - 10 - level_text.get_width(),10))

        for enemy in enemies:
            enemy.draw()
        
        if lost:
            text = font.render('You Lost!', 1, (255,255,255))
            win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
            pygame.display.update()
            pygame.time.wait(2000)
        
        pygame.display.update()

    while run:
        clock.tick(60)
        win.blit(background, (0,0))

        if lives <= 0:
            lost = True
            run = False
        
        draw_window()

        for enemy in enemies:
            enemy.move(1)

            if enemy.off_screen():
                enemies.remove(enemy)
                lives -= 1
            
            if collide(enemy, player):
                health -= 1
                player.healthbar[health] = (226, 22, 2)
                enemies.remove(enemy)

            for laser in enemy.lasers:
                if laser.collide(player):
                    health -= 1
                    player.healthbar[health] = (226, 22, 2)
                    enemy.lasers.remove(laser)
            
            for laser in player.lasers:
                if laser.collide(enemy):
                    enemies.remove(enemy)
                    player.lasers.remove(laser)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            pygame.key.set_repeat(600)
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP:
                    player.lasers.append(Laser(player.x, player.y - 18, pixel_laser_yellow))
            
                if event.key == pygame.K_SPACE:
                    enemies[0].lasers.append(Laser(enemies[0].x, enemies[0].y, enemies[0].laser))
        
        # The code below for user input runs faster and smoother then the one above because it is directly 
        # in the main loop and it isn't ina for loop

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] and player.x + player.ship.get_width() <= width:
            player.x += 5
        
        if keys[pygame.K_LEFT] and player.x >= 0:
            player.x -= 5
        

def menu_screen():
    run = True

    while run:
        win.blit(background, (0,0))
        text = font.render('Press Any Key to Play', 1, (255,255,255))
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                main()
        

main()