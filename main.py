
import pygame
import random

pygame.init()  # for font?

DISPLAY_WIDTH = 500
DISPLAY_HEIGHT = 400
DISPLAY = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), 0, 32)
pygame.display.set_caption("Toss a bitcoin to your Witcher")
BLACK = (0, 0, 0, 0)
bg = pygame.image.load("background.png")
game_over = pygame.image.load("gameover.jpg")
font = pygame.font.Font("Arial Bold.ttf", 32)
point_sound = pygame.mixer.Sound("soundOfPoint.wav")
sound_track = pygame.mixer.music.load("sound_track.mp3")
pygame.mixer.music.play(-1)  # playing music
pygame.mixer.music.set_volume(0.01)


class Player(pygame.sprite.Sprite):
    # sprite for player
    def __init__(self, x, y, vel, acceleration):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("witcher.png"), (50, 60))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel = vel
        self.acceleration = acceleration

        self.player_sprite = pygame.sprite.Group()
        self.player_sprite.add(self)

    def check_boundaries(self, display_width):
        if self.rect.x > display_width - 50:
            self.rect.x = display_width - 70
        if self.rect.x < 0:
            self.rect.x = 20
        if self.rect.y < -40:
            self.rect.y = 20

    def movement(self, keys):
        if keys[pygame.K_d]:
            self.vel = -3
            self.rect.x += 2
        if keys[pygame.K_a]:
            self.vel = -3
            self.rect.x -= 2
        if keys[pygame.K_w]:
            self.vel = -3

    def falling(self):
        self.rect.y += self.vel
        self.vel += self.acceleration

    def draw(self, display):
        self.player_sprite.draw(display)

    def game_over(self):
        if self.rect.y > DISPLAY_HEIGHT + 50:
            DISPLAY.blit(game_over, (0, 0))
            self.rect.y = 100000


class Points(pygame.sprite.Sprite):
    # sprite for points
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("coin.png"), (35, 35))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

def main():
    bg_scroll = -400
    bg_scroll_speed = 3
    clock = pygame.time.Clock()
    fps = 60
    points_frequency = 6000  # miliseconds
    time_of_last_points_generation = pygame.time.get_ticks() - points_frequency
    witcher = Player(100, 100, 3, 0.2)  # starting position of the player
    points_spirtes = pygame.sprite.Group()
    count_points = 0  # creating counter for points
    points = []

    # Run until the user asks to quit
    running = True
    while running:
        current_time = pygame.time.get_ticks()
        clock.tick(fps)
        # Quiting
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # drawing and moving background
        DISPLAY.blit(bg, (0, bg_scroll))
        bg_scroll += bg_scroll_speed
        if bg_scroll > -40:
            bg_scroll = -400

        # generating points
        if current_time - time_of_last_points_generation > points_frequency:
            for point in range(0, 5):
                point = Points(
                    random.randrange(0, DISPLAY_WIDTH - 45),
                    random.randrange(0, DISPLAY_HEIGHT - 85),
                )
                points_spirtes.add(point)
                points.append(point)
            time_of_last_points_generation = pygame.time.get_ticks()

        # removing points after collision and playing sound + adding point to counter
        for point in points:
            if witcher.rect.colliderect(point.rect):
                point_sound.set_volume(0.02)
                point_sound.play()
                points.remove(point)
                points_spirtes.remove(point)
                count_points += 1

        # making player fall and giving them acceleration after that
        witcher.falling()

        # player movment
        keys = pygame.key.get_pressed()
        witcher.check_boundaries(DISPLAY_WIDTH)
        witcher.movement(keys)

        # now creating the text of pointer
        counter_text = font.render("Coins: " + str(count_points), True, BLACK)
        DISPLAY.blit(counter_text, (10, 350))
        
        # drawing sprites on screen
        points_spirtes.draw(DISPLAY)
        witcher.draw(DISPLAY)
        
        # drawing gameover
        witcher.game_over()

        pygame.display.update()

main()
