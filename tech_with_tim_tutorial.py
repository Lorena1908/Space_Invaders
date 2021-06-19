import pygame
import random
pygame.font.init()

width, height = 750, 750
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Space Invaders')

# LOAD IMAGES
red_ship = pygame.image.load('assets/pixel_ship_red_small.png')
green_ship = pygame.image.load('assets/pixel_ship_green_small.png')
blue_ship = pygame.image.load('assets/pixel_ship_blue_small.png')

# PLAYER SHIP
yellow_ship = pygame.image.load('assets/pixel_ship_yellow.png')

# LASERS
pixel_laser_red = pygame.image.load('assets/pixel_laser_red.png')
pixel_laser_green = pygame.image.load('assets/pixel_laser_green.png')
pixel_laser_blue = pygame.image.load('assets/pixel_laser_blue.png')
pixel_laser_yellow = pygame.image.load('assets/pixel_laser_yellow.png')

# BACKGROUND
background = pygame.transform.scale(pygame.image.load('assets/background-black.png'), (width, height))

pygame.display.set_icon(yellow_ship)

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
    
    def draw(self):
        win.blit(self.img, (self.x, self.y))
    
    def move(self, vel):
        self.y += vel

    def off_screen(self):
        return not(0 <= self.y <= height)
    
    def colision(self, obj):
        return collide(self, obj)

class Ship:
    COOLDOWN = 30 
    # it is 30 because as the loop will run 60 times every second than the laser will only be shot once 
    # every half a second

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0
    
    def draw(self):
        for laser in self.lasers:
            laser.draw()

        win.blit(self.ship_img, (self.x, self.y))
    
    def move_lasers(self, vel, obj): # This will run every time the main loop runs
        # This method checks if any of the lasers shot by the enemies has hit the player
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)

            if laser.off_screen():
                self.lasers.remove(laser)
            elif laser.colision(obj):
                obj.health -= 10
                self.lasers.remove(laser)
    
    def get_width(self):
        return self.ship_img.get_width()
    
    def get_height(self):
        return self.ship_img.get_height()
    
    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

        # This is set so that it only increments the self.cool_down_counter in i hit the space bar to shoot
        # which means that self.cool_down_counter will become 1, and this cooldown() method will be able to 
        # increment self.cool_down_counter every time the main loop runs

    def shoot(self):
        if self.cool_down_counter == 0:
            self.lasers.append(Laser(self.x, self.y, self.laser_img))
            self.cool_down_counter = 1

class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health) # Initialize the Ship parent class and pass to it the x, y, and health values
        self.ship_img = yellow_ship
        self.laser_img = pixel_laser_yellow
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.health = health
        self.max_health = 100
    
    def move_lasers(self, vel, objs): # This will run every time the main loop runs
        # This method checks if any of the lasers shot by the player has hit the enemies
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)

            if laser.off_screen():
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.colision(obj):
                        objs.remove(obj)
                        self.lasers.remove(laser)
    def draw(self):
        super().draw()
        self.healthbar()
    
    def healthbar(self):
        pygame.draw.rect(win, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(win, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))

class Enemy(Ship):
    color_map = {
        'red': (red_ship, pixel_laser_red),
        'green': (green_ship, pixel_laser_green),
        'blue': (blue_ship, pixel_laser_blue)
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health) # Initialize the Ship parent class and pass to it the x, y, and health values
        self.ship_img, self.laser_img = self.color_map[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
    
    def move(self, vel):
        self.y += vel
    
    def shoot(self):
        if self.cool_down_counter == 0:
            if self.ship_img == blue_ship:
                self.lasers.append(Laser(self.x-self.ship_img.get_width()/2, self.y, self.laser_img))
            else:
                self.lasers.append(Laser(self.x-self.ship_img.get_width()/5, self.y, self.laser_img))
            self.cool_down_counter = 1
    

def collide(obj1, obj2):
    offset_x = int(obj2.x - obj1.x)
    offset_y = int(obj2.y - obj1.y)
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def main():
    run = True
    fps = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont('comicsans', 50)
    lost_font = pygame.font.SysFont('comicsans', 70)
    enemies = []
    wave_length = 5
    player_vel = 5
    enemy_vel = 1
    laser_vel = 4
    lost = False
    lost_count = 0

    player = Player(width/2 - 50, height - 120)

    clock = pygame.time.Clock()

    def redraw_window():
        win.blit(background, (0,0))
        
        # DRAW TEXT
        lives_label = main_font.render(f'Lives: {lives}', 1, (255,255,255))
        level_label = main_font.render(f'Level: {level}', 1, (255,255,255))

        win.blit(lives_label, (10,10))
        win.blit(level_label, (width - level_label.get_width() - 10,10))

        for enemy in enemies:
            enemy.draw()

        player.draw()

        if lost:
            lost_label = lost_font.render('Lost!', 1, (255,255,255))
            win.blit(lost_label, (width/2 - lost_label.get_width()/2, height/2 - lost_label.get_height()/2))

        pygame.display.update()

    while run:
        clock.tick(fps) # It makes the game run at fps times each second
        # It makes the game run at the same speed for any computer, it doesn't matter if one computer 
        # is faster than the other

        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1
        
        if lost:
            if lost_count > fps * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 5

            for i in range(wave_length):
                enemies.append(Enemy(random.randrange(50,width-100), random.randrange(-1500, -100), random.choice(['red', 'green', 'blue'])))

        for event in pygame.event.get(): 
            # Getting input keys inside this event loop isn't really good because it only registers one 
            # key press at a time. It also runs slower than the next way
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0:
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < width:
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0:
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() < height:
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()
        
        for enemy in enemies:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player) # Move lasers and check if any of them hit the player

            if random.randrange(0, 2*fps) == 1: #1:38:13
                enemy.shoot()

            if collide(player, enemy):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > height:
                lives -= 1
                enemies.remove(enemy)
            
        player.move_lasers(-laser_vel, enemies)

def main_menu():
    title_font = pygame.font.SysFont('comicsans', 70)
    run = True

    while run:
        win.blit(background, (0,0))
        text = title_font.render('Press Any Key to Play!', 1, (255,255,255))
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False

            if event.type == pygame.KEYDOWN:
                main()

main_menu()