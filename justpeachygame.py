import pygame

import random
pygame.init()

# Global Constants
SCREEN_HEIGHT = 400
SCREEN_WIDTH = 700
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

game_speed = 13

RUNNING = [pygame.image.load("peach1.png"),
           pygame.image.load("peach2.png")]
JUMPING = pygame.image.load("peach2.png")
DUCKING = [pygame.image.load("peachduck1.png"),
           pygame.image.load("peachduck2.png")]

FIRESHORT = []
FIRE1 = pygame.image.load("burning_loop_2_1.png")
FIRE1 = pygame.transform.scale(FIRE1,(148, 46))
FIRESHORT.append(FIRE1)
FIRE2 = pygame.image.load("burning_loop_2_2.png")
FIRE2= pygame.transform.scale(FIRE2,(148, 46))
FIRESHORT.append(FIRE2)

FIRELONG  =  []
FIRE4 = pygame.image.load("burning_loop_3_1.png")
FIRE4 = pygame.transform.scale(FIRE4,(148, 46))
FIRELONG.append(FIRE4)
FIRE5 = pygame.image.load("burning_loop_3_2.png")
FIRE5 = pygame.transform.scale(FIRE5,(148, 46))
FIRELONG.append(FIRE5)

BIRD = []
BIRD1 = pygame.image.load("bird1.png")
BIRD1 = pygame.transform.scale(BIRD1,(49, 34))
BIRD.append(BIRD1)
BIRD2 = pygame.image.load("bird2.png")
BIRD2 = pygame.transform.scale(BIRD2,(49, 34))
BIRD.append(BIRD2)

BG = pygame.image.load("background.png")
BG = pygame.transform.scale(BG,(SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock() 

class Peach:
    X_POS = 80
    Y_POS = 335
    Y_POS_DUCK = 350
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.peach_duck = False
        self.peach_run = True
        self.peach_jump = False

        self.step_index = 0
        # set and define jump function
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.peach_rect = self.image.get_rect()
        self.peach_rect.x = self.X_POS
        self.peach_rect.y = self.Y_POS

    def update(self, userInput):
        if self.peach_duck:
            self.duck()
        if self.peach_run:
            self.run()
        if self.peach_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.peach_jump:
            self.peach_duck = False
            self.peach_run = False
            self.peach_jump = True
        elif userInput[pygame.K_DOWN] and not self.peach_jump:
            self.peach_duck = True
            self.peach_run = False
            self.peach_jump = False
        elif not (self.peach_jump or userInput[pygame.K_DOWN]):
            self.peach_duck = False
            self.peach_run = True
            self.peach_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.peach_rect = self.image.get_rect()
        self.peach_rect.x = self.X_POS
        self.peach_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.peach_rect = self.image.get_rect()
        self.peach_rect.x = self.X_POS
        self.peach_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.peach_jump:
            self.peach_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.peach_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.peach_rect.x, self.peach_rect.y))

class Obstacle:
    def __init__(self, image, img_type):
        self.image = image
        self.img_type = img_type
        if self.img_type >= len(self.image):
            self.img_type = len(self.image) - 1
        self.rect = self.image[self.img_type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.img_type], self.rect)

class FireShort(Obstacle):
    def __init__(self, image):
        self.img_type = random.randint(0, 2)
        super().__init__(image, self.img_type)
        self.rect.y = 315
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1

class FireLong(Obstacle):
    def __init__(self, image):
        self.img_type = random.randint(0, 2)
        super().__init__(image, self.img_type)
        self.rect.y = 315
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1

class Bird(Obstacle):
    def __init__(self, image):
        self.img_type = 0
        super().__init__(image, self.img_type)
        self.rect.y = 310
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1

class Bird2(Obstacle):
    def __init__(self, image):
        self.img_type = 0
        super().__init__(image, self.img_type)
        self.rect.y = 100
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1


# establish main game loop 
def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = Peach()

    game_speed = 13

    x_pos_bg = 0
    y_pos_bg = 0
    points = 0

    font = pygame.font.Font('Chillax-Semibold.ttf', 15)
    obstacles = []
    death_count = 0

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1

        text = font.render("Pointer: " + str(points), True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (600,40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed
        
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()

        background()
        
        player.draw(SCREEN)
        player.update(userInput)

        if len(obstacles) == 0:
            if random.randint(0, 1) == 0:
                obstacles.append(FireShort(FIRESHORT))
            if random.randint(0, 1) == 0:
                obstacles.append(FireLong(FIRELONG))
            elif random.randint(0, 1) == 1:
                obstacles.append(Bird(BIRD))
            elif random.randint(0, 1) == 1:
                obstacles.append(Bird2(BIRD))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.peach_rect.colliderect(obstacle.rect):
                pygame.time.delay(1000)
                death_count += 1
                menu(death_count)

        


        score()

        clock.tick(30)
        pygame.display.update()


def menu(death_count):
    global points,x_pos_bg, y_pos_bg
    run = True
    x_pos_bg = 0
    y_pos_bg = 0
    while run:
        SCREEN.fill((255, 255, 255))
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        font = pygame.font.Font('Chillax-Semibold.ttf', 30)

        if death_count == 0:
            text = font.render("Press any key to start!", True, (255, 255, 255))
        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, (255, 255, 255))
            score = font.render("Your Score: " + str(points), True, (255, 255, 255))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()

    pygame.quit()

menu(death_count=0)
