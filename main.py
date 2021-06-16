import pygame
pygame.font.init()

width, height = 600, 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Space Invaders')

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
    
    def draw(self):
        win.blit(self.laser, (self.x, self.y))
    
    def move(self, vel):
        self.y += vel
    
    def off_screen(self):
        return self.y > height or self.y < -40


class Ship:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.ship = color
        self.lasers = []

        if self.ship == 'red':
            self.ship, self.laser = (red_ship, pixel_laser_red)
        elif self.ship == 'green':
            self.ship, self.laser = (green_ship, pixel_laser_green)
        elif self.ship == 'blue':
            self.ship, self.laser = (blue_ship, pixel_laser_blue)
    
    def draw(self):
        win.blit(self.ship, (self.x, self.y))

        for laser in self.lasers:
            if laser.off_screen():
                self.lasers.remove(laser)
            else:
                laser.draw()
                laser.move(5)
    
    def move(self):
        self.y += 0.8
    
    def shoot(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            pygame.key.set_repeat(100)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.lasers.append(Laser(self.x, self.y, self.laser))

class Player:
    def __init__(self):
        self.show_ship = yellow_ship
        self.x = width/2 - self.show_ship.get_width()/2
        self.y = height - self.show_ship.get_height() - 50
        
        self.lasers = [] # Laser(self.x, self.y - 18)
        
        self.healthbar = [(0, 211, 7) for _ in range(8)] # red: (226, 22, 2)
        self.shoot = False

    def draw(self):
        win.blit(self.show_ship, (self.x, self.y))

        for i, color in enumerate(self.healthbar):
            pygame.draw.rect(win, color, (self.x +10 + (i*10), self.y + 100, 10, 10))
        
        for laser in self.lasers:
            if laser.off_screen():
                self.lasers.remove(laser)
            else:
                laser.draw()
                laser.move(-5)
    

def main():
    run = True
    player = Player()
    ship = Ship(width/2, 0, 'red')

    while run:
        win.blit(background, (0,0))
        player.draw()
        ship.draw()
        ship.move()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            pygame.key.set_repeat(100)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and player.x + player.show_ship.get_width() <= width:
                    player.x += 20

                if event.key == pygame.K_LEFT and player.x >= 0:
                    player.x -= 20
                
                if event.key == pygame.K_UP:
                    player.lasers.append(Laser(player.x, player.y - 18, pixel_laser_yellow))
                
                if event.key == pygame.K_SPACE:
                    ship.lasers.append(Laser(ship.x, ship.y, ship.laser))
                    
        
        pygame.display.update()

def menu_screen():
    run = True

    while run:
        win.blit(background, (0,0))
        font = pygame.font.SysFont('comicsans', 70)
        text = font.render('Press Any Key to Play', 1, (255,255,255))
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                main()
        

main()