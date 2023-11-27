import pygame
import sys
import random


pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SCREEN_WIDTH = 980
SCREEN_HEIGHT = 980
ASTEROID_COUNT = 10
ASTEROID_SIZE = (50, 50)
BULLET_SIZE = (10, 30)

class Game:
    def __init__(self):
        self.game_over = False
        self.game_paused = False
        self.in_menu = False
        self.score = 0
        self.asteroid_list = pygame.sprite.Group()
        self.all_sprite_list = pygame.sprite.Group()
        self.bullet_list = pygame.sprite.Group()
        self.enemy_ship_list = pygame.sprite.Group()
        self.enemy_bullet_list = pygame.sprite.Group()
       

            
        self.can_player_shoot = True
        self.level = 1

        self.background_music = pygame.mixer.Sound("assets/sounds/music.ogg")
         # Play Music
        if not pygame.mixer.get_busy():
            self.background_music.play(loops=-1)
      
        
        #Create asteroids randomly at the top of the screen
        for i in range(ASTEROID_COUNT):
            asteroid = Asteroid()
            asteroid.resize(ASTEROID_SIZE)
            asteroid.rect.x = random.randint(0, SCREEN_WIDTH - asteroid.rect.width)
            asteroid.rect.y = random.randrange(-100, 0)
            asteroid.speed = random.uniform(1, 3)
            self.asteroid_list.add(asteroid)
            self.all_sprite_list.add(asteroid)

        # Player 
        self.player = Player()
        self.player.resize((100, 100))
        self.all_sprite_list.add(self.player)

        # Pause button
        self.pause_button = PauseButton()
        self.all_sprite_list.add(self.pause_button)


        # Instances of the music buttons' images.
        self.music_on_img = pygame.image.load("assets/images/music_on.png").convert_alpha()
        self.music_off_img = pygame.image.load("assets/images/music_off.png").convert_alpha()

        button_size = (50, 50) 
        self.music_on_img = pygame.transform.scale(self.music_on_img, button_size)
        self.music_off_img = pygame.transform.scale(self.music_off_img, button_size)

        # Positions
        self.music_on_button = MusicButton(self.music_on_img, (830, 235))
        self.music_off_button = MusicButton(self.music_off_img, (835, 300))

        # Adding to sprites
        self.all_sprite_list.add(self.music_on_button)
        self.all_sprite_list.add(self.music_off_button)


        #load button images
        resume_img = pygame.image.load("assets/images/button_resume.png").convert_alpha()
        options_img = pygame.image.load("assets/images/button_options.png").convert_alpha()
        quit_img = pygame.image.load("assets/images/button_quit.png").convert_alpha()
        video_img = pygame.image.load('assets/images/button_video.png').convert_alpha()
        audio_img = pygame.image.load('assets/images/button_audio.png').convert_alpha()
        keys_img = pygame.image.load('assets/images/button_keys.png').convert_alpha()
        back_img = pygame.image.load('assets/images/button_back.png').convert_alpha()

        #create button instances
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2

        self.resume_button = Button(center_x - 90, center_y - 250, resume_img, 1)
        self.options_button = Button(center_x - 97, center_y - 120, options_img, 1)
        self.quit_button = Button(center_x - 63, center_y - 0, quit_img, 1)
        self.video_button = Button(center_x - 194, center_y - 175, video_img, 1)
        self.audio_button = Button(center_x - 195, center_y - 50, audio_img, 1)
        self.keys_button = Button(center_x - 174, center_y + 75, keys_img, 1)
        self.back_button = Button(center_x - 88, center_y + 200, back_img, 1)

        self.visible_buttons = [self.resume_button, self.options_button, self.quit_button]
        

        # Menu buttons
        self.menu_button = MenuButton()
        self.all_sprite_list.add(self.menu_button)

        

        # background image
        self.background = pygame.image.load("assets/images/game_background.png").convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Sound
        self.sound = pygame.mixer.Sound("assets/sounds/shot.ogg")

        
        self.font = pygame.font.Font("assets/fonts/Orbitron-SemiBold.ttf", 36)

        # Timer for asteroid appearance
        self.asteroid_timer = pygame.time.get_ticks()

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

            if not self.in_menu:  
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.can_player_shoot:
                        bullet = Bullet()
                        bullet.rect.x = self.player.rect.x + 45
                        bullet.rect.y = self.player.rect.y - 20
                        self.all_sprite_list.add(bullet)
                        self.bullet_list.add(bullet)
                        self.sound.play()

                if event.type == pygame.MOUSEBUTTONDOWN and self.game_over:
                    # Restart the game if clicked after a Game Over
                    self.__init__()

                if event.type == pygame.MOUSEBUTTONDOWN and self.pause_button.rect.collidepoint(event.pos):
                    self.toggle_pause()

                if event.type == pygame.MOUSEBUTTONDOWN and self.music_on_button.rect.collidepoint(event.pos):
                    pygame.mixer.unpause()

                if event.type == pygame.MOUSEBUTTONDOWN and self.music_off_button.rect.collidepoint(event.pos):
                    pygame.mixer.pause()

                if event.type == pygame.MOUSEBUTTONDOWN and self.menu_button.rect.collidepoint(event.pos):
                    self.in_menu = True
                    pygame.mixer.pause()
                

            else:  
                if event.type == pygame.MOUSEBUTTONDOWN and self.menu_button.rect.collidepoint(event.pos):
                    self.in_menu = False
                

        return False

    def run_logic(self):
        if not self.game_over and not self.game_paused and not self.in_menu:
            # Control of the timer for asteroid appearance.
            current_time = pygame.time.get_ticks()
            if self.level == 1 and current_time - self.asteroid_timer > 1000:  
                asteroid = Asteroid()
                asteroid.resize(ASTEROID_SIZE)
                asteroid.rect.x = random.randint(0, SCREEN_WIDTH - asteroid.rect.width)
                asteroid.rect.y = random.randrange(-100, 0)
                asteroid.speed = random.uniform(1, 3)
                self.asteroid_list.add(asteroid)
                self.all_sprite_list.add(asteroid)
                self.asteroid_timer = current_time

            self.all_sprite_list.update()

            # collisions with asteroids.
            for bullet in self.bullet_list:
                asteroid_hit_list = pygame.sprite.spritecollide(bullet, self.asteroid_list, True)
                for asteroid in asteroid_hit_list:
                    bullet.kill()
                    self.score += 1

            # collisions with the screen
            for asteroid in self.asteroid_list:
                if asteroid.rect.y > SCREEN_HEIGHT:
                    self.game_over = True
                elif self.game_over == True:
                    self.background_music.stop()

                    
                    

            # collisions with the player
            if pygame.sprite.spritecollide(self.player, self.asteroid_list, False):
                self.game_over = True
                self.background_music.stop()

            
            # collisions with enemy bullets
            for enemy_bullet in self.enemy_bullet_list:
                if pygame.sprite.collide_rect(enemy_bullet, self.player):
                    self.game_over = True
                    self.background_music.stop()


            
            if self.score == 10 and self.level == 1:
                self.level = 2
                self.can_player_shoot = False
                for asteroid in self.asteroid_list:
                    asteroid.kill()

           
                for bullet in self.bullet_list:
                    bullet.kill()

                enemy_ship = EnemyShip()
                enemy_ship.resize((200, 200))  
                self.enemy_ship = enemy_ship  
                self.all_sprite_list.add(enemy_ship)

            
    

    def display_frame(self, screen):
        screen.blit(self.background, [0, 0])
        self.all_sprite_list.draw(screen)

        
        score_text = self.font.render("Score: {}".format(self.score), True, BLACK)
        screen.blit(score_text, [100, 100])

       
        level_message_text = self.font.render("Nivel {}".format(self.level), True, BLACK)
        center_x = (SCREEN_WIDTH // 2) - (level_message_text.get_width() // 2)
        center_y = (SCREEN_HEIGHT // 2) - (level_message_text.get_height() // 2)
        screen.blit(level_message_text, [center_x, center_y])

        if self.game_over:
            game_over_rect = pygame.Rect((SCREEN_WIDTH - 600) // 2, (SCREEN_HEIGHT - 50) // 2, 600, 50)
            pygame.draw.rect(screen, BLACK, game_over_rect)
            game_over_text = self.font.render("Game Over, Click To Continue", True, WHITE)
            center_x = (SCREEN_WIDTH // 2) - (game_over_text.get_width() // 2)
            center_y = (SCREEN_HEIGHT // 2) - (game_over_text.get_height() // 2)
            screen.blit(game_over_text, [center_x, center_y])

        if self.game_paused:
           
            pause_rect = pygame.Rect((SCREEN_WIDTH - 200) // 2, (SCREEN_HEIGHT - 50) // 2, 200, 50)
            pygame.draw.rect(screen, WHITE, pause_rect)
            pause_text = self.font.render("Paused", True, BLACK)
            center_x = (SCREEN_WIDTH // 2) - (pause_text.get_width() // 2)
            center_y = (SCREEN_HEIGHT // 2) - (pause_text.get_height() // 2)
            screen.blit(pause_text, [center_x, center_y])



        if self.in_menu:
          
            center_x = SCREEN_WIDTH // 2
            center_y = SCREEN_HEIGHT // 2

          
            for button in self.visible_buttons:
                button.draw(screen)
            
           
            music_buttons = [sprite for sprite in self.all_sprite_list if isinstance(sprite, Button)]
            for button in music_buttons:
                button.draw(screen)


        
            for button in self.visible_buttons:
                if button.rect.collidepoint(pygame.mouse.get_pos()):
                    if button.draw(screen):
                        if button == self.resume_button:
                            self.in_menu = False
                        elif button == self.options_button:
                            self.visible_buttons = [self.video_button, self.audio_button, self.resume_button, self.quit_button]
                            self.video_button.rect.center = (center_x - 0, center_y - 175)
                            self.audio_button.rect.center = (center_x - 0, center_y - 50)
                            self.resume_button.rect.center = (center_x - 0, center_y + 75)
                            self.quit_button.rect.center = (center_x - 0, center_y + 200)
                            for button in self.visible_buttons:
                                button.draw(screen)
                        elif button == self.quit_button:
                            pygame.quit()

                            for button in self.visible_buttons:
                                button.draw(screen)

        pygame.display.flip()

    def toggle_pause(self):
        self.game_paused = not self.game_paused


        

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load("assets/images/player.png").convert()
        self.original_image.set_colorkey(BLACK)
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.speed = 0

    def resize(self, new_size):
        self.image = pygame.transform.scale(self.original_image, new_size)
        self.rect = self.image.get_rect()

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= 5
        if keys[pygame.K_d]:
            self.rect.x += 5

        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))
        self.rect.y = SCREEN_HEIGHT - 100

class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load("assets/images/asteroid.png").convert()
        self.original_image.set_colorkey(BLACK)
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.speed = 1  

    def resize(self, new_size):
        self.image = pygame.transform.scale(self.original_image, new_size)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y += self.speed

        if self.rect.y > SCREEN_HEIGHT:
            self.reset_position()
            game.game_over = True

    def reset_position(self):
        self.rect.y = -10
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load("assets/images/bullet.png").convert()
        self.original_image.set_colorkey(BLACK)
        self.image = pygame.transform.scale(self.original_image, BULLET_SIZE)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y -= 5

        if self.rect.y < -10:
            self.kill()

class LevelMessage(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font("assets/fonts/Orbitron-SemiBold.ttf", 48)
        self.image = self.font.render("Nivel 2", True, WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

class EnemyShip(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

       
        self.original_image = pygame.image.load("assets/images/enemy_ship.png").convert_alpha()
        self.original_image.set_colorkey((0, 0, 0)) 
        self.image = self.original_image.copy()

        
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(50, 200)

       
        self.speed = 3

       
        self.shoot_time_range = (300, 800)
        self.reset_shoot_timer()

    def reset_shoot_timer(self):
      
        self.shoot_timer = pygame.time.get_ticks() + random.randint(*self.shoot_time_range)

    def resize(self, new_size):
        self.image = pygame.transform.scale(self.original_image, new_size)
        self.rect = self.image.get_rect()

    def update(self):
       
        self.rect.x += self.speed

     
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.speed = -self.speed

       
        current_time = pygame.time.get_ticks()
        if current_time > self.shoot_timer:
            self.shoot_laser()
            self.reset_shoot_timer()

    def shoot_laser(self):
        enemy_bullet = EnemyBullet(self.rect.x + self.rect.width // 2 - BULLET_SIZE[0] // 2,
                                   self.rect.y + self.rect.height)
        game.all_sprite_list.add(enemy_bullet)
        game.enemy_bullet_list.add(enemy_bullet)  

        


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = pygame.image.load("assets/images/enemy_bullet.png").convert()
        self.original_image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.original_image, BULLET_SIZE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y += 5  

        if self.rect.y > SCREEN_HEIGHT:
            self.kill()


class PauseButton(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        original_image = pygame.image.load("assets/images/pause-play-button.png").convert()
        original_image.set_colorkey((255, 255, 255))  

        
        scaled_width = int(original_image.get_width() * 0.1)
        scaled_height = int(original_image.get_height() * 0.1)
        self.image = pygame.transform.scale(original_image, (scaled_width, scaled_height))

        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH - self.rect.width - 100
        self.rect.y = 100

    def update(self):
        
        pass

class MenuButton(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load("assets/images/settings.png").convert_alpha()  
        scaled_width = int(self.original_image.get_width() * 0.1)  
        scaled_height = int(self.original_image.get_height() * 0.1)  
        self.image = pygame.transform.scale(self.original_image, (scaled_width, scaled_height))
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH - self.rect.width - 100
        self.rect.y = 170


    def update(self):
        
        pass

class MusicButton(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=position)

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
      
        surface.blit(self.image, (self.rect.x, self.rect.y))

        
        if pygame.mouse.get_pressed()[0] == 1 and self.rect.collidepoint(pygame.mouse.get_pos()):
            self.clicked = True
        else:
            self.clicked = False

        return self.clicked




screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
clock = pygame.time.Clock()
done = False
game = Game()



while not done:
    done = game.process_events()

    game.music_on_button.draw(screen)
    game.music_off_button.draw(screen)

    game.run_logic()
    game.display_frame(screen)
    clock.tick(60)

pygame.quit()
sys.exit()