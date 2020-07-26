import pygame
import random


def load_image(name):
    image = pygame.image.load(name)
    return image


################################
screen_width = 1024
screen_height = 768
BAR_LENGTH = 100
BAR_HEIGHT = 10
FPS = 60  #frames per second

########### define colors
WHITE = (255,255,255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

########### initialize pygame and create window
pygame.init()
pygame.mixer.init()  ## For sound
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()     ## For syncing the FPS

############ sounds 
shooting_sound = pygame.mixer.Sound("sounds/rocket.ogg")
expl1 = pygame.mixer.Sound("sounds/expl1.wav")
main_sound= pygame.mixer.Sound("sounds/main.ogg")
getready_sound = pygame.mixer.Sound("sounds/getready.ogg")
levelup_sound = pygame.mixer.Sound("sounds/levelup.wav")
menu_sound = pygame.mixer.Sound("sounds/menu.ogg")

############ fonts
font_name = pygame.font.match_font('arial')

background_img = pygame.transform.scale(load_image("assets/background.png"),(screen_width,screen_height))


def draw_text(surf, text, size, x, y):
    ## selecting a cross platform font to display the score
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)       ## True denotes the font to be anti-aliased 
    text_rect = text_surface.get_rect()
    text_rect.midtop = (round(x), round(y))
    surf.blit(text_surface, text_rect)

def draw_shield_bar(surf, x, y, pct):
    # if pct < 0:
    #     pct = 0
    pct = max(pct, 0) 
    ## moving them to top
    # BAR_LENGTH = 100
    # BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(int(x), int(y), fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect= img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

def main_menu():
    global screen


    menu_sound.play(-1)
    background1 = Background((0,-screen_height))
    background2 = Background((0,0))
    screen.blit(background1.surf, (background1.x,background1.y))
    screen.blit(background2.surf, (background2.x,background2.y))

    Backgrounds = pygame.sprite.Group()
    Backgrounds.add(background1)
    Backgrounds.add(background2)
    pygame.display.update()

    while True:
        ev = pygame.event.poll()
        Backgrounds.update()

        for b in Backgrounds :
            screen.blit(b.surf, (b.x,b.y))
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_RETURN:
                break
            elif ev.key == pygame.K_q:
                pygame.quit()
                quit()
        elif ev.type == pygame.QUIT:
                pygame.quit()
                quit() 
        else:
            draw_text(screen, "Press [ENTER] To Begin", 30, screen_width/2, screen_height/2)
            draw_text(screen, "or [Q] To Quit", 30, screen_width/2, (screen_height/2)+40)
            pygame.display.update()
    menu_sound.stop()

    Backgrounds.update()

    for b in Backgrounds :
        screen.blit(b.surf, (b.x,b.y))
    
    getready_sound.play()

    draw_text(screen, "GET READY!", 40, screen_width/2, screen_height/2)
    pygame.display.update()

    for i in range(0,4) :
        screen.blit(background_img, (0,0))
        draw_text(screen, str(i), 40, screen_width/2, screen_height/2)
        pygame.display.update()
        pygame.time.wait(1000)


class Background(pygame.sprite.Sprite):
    def __init__(self,pos):
         pygame.sprite.Sprite.__init__(self)
         self.surf = pygame.transform.scale(load_image("assets/background.png"),(screen_width,screen_height))
         self.x=pos[0]
         self.y=pos[1]
         
    def update(self):
        self.y+=4

        if self.y >= screen_height :
            self.y = -screen_height


class Powerup(pygame.sprite.Sprite):
    def __init__(self, center, type):
        pygame.sprite.Sprite.__init__(self)
        if type=="bolt":
            self.surf=load_image("assets/powerupGreen_bolt.png")
        elif type=="shield":
            self.surf=load_image("assets/powerupGreen_shield.png")
        
        self.rect = self.surf.get_rect()
        self.rect.center = center
        self.type=type

    def update(self):
        if self.rect.top > screen_height:
            self.kill
        self.rect.move_ip(0, 5)


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.images=[]
        self.images.append(load_image('assets/regularExplosion00.png'))
        self.images.append(load_image('assets/regularExplosion01.png'))
        self.images.append(load_image('assets/regularExplosion02.png'))
        self.images.append(load_image('assets/regularExplosion03.png'))
        self.images.append(load_image('assets/regularExplosion04.png'))
        self.images.append(load_image('assets/regularExplosion05.png'))
        self.images.append(load_image('assets/regularExplosion06.png'))
        self.images.append(load_image('assets/regularExplosion07.png'))
        self.images.append(load_image('assets/regularExplosion08.png'))        
        self.size = size
        self.frame = 0 
        self.surf = pygame.transform.scale(self.images[self.frame],self.size)
        self.rect = self.surf.get_rect()
        self.rect.center = center
        
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.images):
                self.kill()
            else:
                center = self.rect.center
                self.surf = pygame.transform.scale(self.images[self.frame],self.size)
                self.rect = self.surf.get_rect()
                self.rect.center = center



class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y,type):
        super(Bullet,self).__init__()
        self.type = type
        if type=="A" :
            self.images=[]
            self.images.append(load_image('assets/Missile_3_Flying_000.png'))
            self.images.append(load_image('assets/Missile_3_Flying_001.png'))
            self.images.append(load_image('assets/Missile_3_Flying_002.png'))
            self.images.append(load_image('assets/Missile_3_Flying_003.png'))
            self.images.append(load_image('assets/Missile_3_Flying_004.png'))
            self.images.append(load_image('assets/Missile_3_Flying_005.png'))
            self.images.append(load_image('assets/Missile_3_Flying_006.png'))
            self.images.append(load_image('assets/Missile_3_Flying_007.png'))
            self.images.append(load_image('assets/Missile_3_Flying_008.png'))
            self.images.append(load_image('assets/Missile_3_Flying_009.png'))
            self.index = 0

            self.surf=pygame.transform.scale(self.images[self.index],(18,48))
            self.surf.set_colorkey((255, 255, 255))
            self.rect=self.surf.get_rect(center=(x,y))
            self.speed=-10
        
        elif type=="B":
            self.surf=pygame.transform.scale(load_image("assets/laser.png"),(15,screen_height))
            self.surf.set_colorkey((255, 255, 255))
            self.rect=self.surf.get_rect(center=(x,y))
            self.start = pygame.time.get_ticks()

    def update(self):
        if self.type == "A" :
            self.rect.move_ip(0, self.speed)
            self.index+=1

            if self.index > len(self.images)-1 :
                self.index = 0

            self.surf=pygame.transform.scale(self.images[self.index],(18,48))
            
            if self.rect.bottom < 0:
                self.kill()
        
        elif self.type=="B" :
            now = pygame.time.get_ticks()
            if now - self.start > 20:
                self.kill()


        


class Spaceship(pygame.sprite.Sprite):
    def __init__(self):
        super(Spaceship,self).__init__()


        self.surf = load_image("assets/spaceship.png")
        self.surf.set_colorkey((255, 255, 255))
        self.rect=self.surf.get_rect(center=(screen_width//2,screen_height-80))
        self.level=1   
        self.bullets = pygame.sprite.Group()
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.speed = 15
        self.shield=100
        self.lives = 3

    def move(self, pressed_keys):
    
        if pressed_keys[pygame.K_w]:
        
            self.rect.move_ip(0, -self.speed)

        if pressed_keys[pygame.K_s]:

            self.rect.move_ip(0, self.speed)

        if pressed_keys[pygame.K_a]:

            self.rect.move_ip(-self.speed, 0)

        if pressed_keys[pygame.K_d]:

            self.rect.move_ip(self.speed, 0)

        if pressed_keys[pygame.K_SPACE] :
            if self.level <4 :
                now = pygame.time.get_ticks()
                if now - self.last_shot > self.shoot_delay:
                    self.last_shot = now
                    
                    if self.level ==1 :
                        new_bul = Bullet(self.rect.left+56,self.rect.top+30,"A")
                        self.bullets.add(new_bul)
                        shooting_sound.play()
                    
                    if self.level == 2:
                        new_bul1 = Bullet(self.rect.left+10,self.rect.top+50,"A")
                        new_bul2 = Bullet(self.rect.right-15,self.rect.top+50,"A")
                        self.bullets.add(new_bul1)
                        self.bullets.add(new_bul2)
                        shooting_sound.play()
                        shooting_sound.play()

                    if self.level == 3 :
                        new_bul1 = Bullet(self.rect.left+10,self.rect.top+50,"A")
                        new_bul2 = Bullet(self.rect.right-15,self.rect.top+50,"A")
                        self.bullets.add(new_bul1)
                        self.bullets.add(new_bul2)
                        new_bul3 = Bullet(self.rect.left+56,self.rect.top+30,"A")
                        self.bullets.add(new_bul3)
                        shooting_sound.play()
                        shooting_sound.play()
                        shooting_sound.play()

            elif self.level==4 :
                now = pygame.time.get_ticks()
                if now - self.last_shot > 20:
                    self.last_shot = now
                    laser1=Bullet(self.rect.left+20,self.rect.top-330,"B")
                    laser2=Bullet(self.rect.right-25,self.rect.top-330,"B")
                    self.bullets.add(laser1)
                    self.bullets.add(laser2)
                

        self.bullets.update()

        
        if self.rect.left < 0:
        
            self.rect.left = 0

        if self.rect.right > screen_width:

            self.rect.right = screen_width

        if self.rect.top <= 0:

            self.rect.top = 0

        if self.rect.bottom >= screen_height:

            self.rect.bottom = screen_height


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy,self).__init__()
        name = "assets/enemy"+str(random.randint(1,7))+".png"
        self.image = load_image(name)
        self.surf = self.image
        self.size = self.surf.get_size()
        self.rect = self.surf.get_rect()
        self.rect.center = (random.randint(0,screen_width),-150)
        self.speedy = random.randrange(5, 20)        ## for randomizing the speed of the Mob

        ## randomize the movements a little more 
        self.speedx = random.randrange(-3, 3)

        ## adding rotation to the mob element
        self.rotation = 0
        self.rotation_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()  ## time when the rotation has to happen


    def rotate(self):
        time_now = pygame.time.get_ticks()
        if time_now - self.last_update > 50: # in milliseconds
            self.last_update = time_now
            self.rotation = (self.rotation + self.rotation_speed) % 360 
            new_image = pygame.transform.rotate(self.image, self.rotation)
            old_center = self.rect.center
            self.surf = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center


    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        ## now what if the mob element goes out of the screen

        if (self.rect.top > screen_height) or (self.rect.left > screen_width) or (self.rect.right < 0):
            self.kill()



def game():
    while 1 :
        main_menu()
        player = Spaceship()

        background1 = Background((0,-screen_height))
        background2 = Background((0,0))
        Backgrounds = pygame.sprite.Group()
        Backgrounds.add(background1)
        Backgrounds.add(background2)

        number_enemies = 3
        enemies = pygame.sprite.Group()
        explosions = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        score =0
        for i in range(number_enemies) :
            en = Enemy()
            enemies.add(en)
        
        enemies_killed = 0
        main_sound.play(-1) 

        while 1 :
            if player.lives <= 0 :
                break
            if len(enemies) < number_enemies :
                for i in range(number_enemies-len(enemies)):
                    en = Enemy()
                    enemies.add(en)

            ev = pygame.event.poll()
            if ev.type == pygame.QUIT:
                pygame.quit()
                quit() 
            if player.shield <= 0 :
                player.shield = 100
                player.lives -=1
            ens = pygame.sprite.spritecollide(player, enemies,True)
            for en in ens :
                    en.kill()
                    exp=Explosion(en.rect.center,en.size)
                    explosions.add(exp)
                    player.shield -= 20
                    if player.level >=2:
                        player.level -=1
                    expl1.play()
            for bullet in player.bullets :
                    ens = pygame.sprite.spritecollide(bullet, enemies,True)
                    for en in ens :
                        en.kill()
                        bullet.kill()
                        exp=Explosion(en.rect.center,en.size)
                        explosions.add(exp)
                        enemies_killed += 1
                        expl1.play()

                        if enemies_killed % 5 ==0 :
                            number_enemies+=1
                            if random.randint(0,100) % 2 ==0:
                                type = "shield"
                            else :
                                type = "bolt"
                            pow = Powerup(en.rect.center,type)
                            powerups.add(pow)
            pows = pygame.sprite.spritecollide(player, powerups,True)
            for pow in pows :
                    pow.kill()
                    if pow.type =="bolt" :
                        if player.level <=3:
                            player.level +=1
                    else :
                        if player.lives <=2 :
                            player.lives +=1
                    levelup_sound.play()
                    levelup_sound.play()
                    levelup_sound.play()
                    levelup_sound.play()
            
            Backgrounds.update()

            for b in Backgrounds :
                screen.blit(b.surf, (b.x,b.y))
            pressed_keys = pygame.key.get_pressed()
            player.move(pressed_keys)
            enemies.update()
            explosions.update()
            powerups.update()
            
            for bullet in player.bullets:
                screen.blit(bullet.surf, bullet.rect)
            screen.blit(player.surf, player.rect)

            for pow in powerups:
                screen.blit(pow.surf, pow.rect)

            for exp in explosions :
                 screen.blit(exp.surf, exp.rect)

            for en in enemies:
                screen.blit(en.surf, en.rect)



            score +=1
            draw_text(screen, str(score), 18, screen_width / 2, 10)     ## 10px down from the screen
            draw_shield_bar(screen, 5, 5, player.shield)

            # Draw lives
            draw_lives(screen, screen_width - 100, 5, player.lives, pygame.transform.scale(player.surf, (25, 19)))
            pygame.display.flip()

            clock.tick(FPS)
        main_sound.stop()              





    
    
            

            






if __name__ == '__main__':
    game()
    


        
