import pygame
import sys

pygame.init()

res = width, height = 750, 550
screen = pygame.display.set_mode(res)
clock = pygame.time.Clock()
fps = 60
font = pygame.font.SysFont("Consolas", 24)

class Shape:
    def __init__(self, x, y, duration, color, shape = "circle"):
        self.x, self.y = x, y
        self.duration = duration
        self.color = color
        self.shape = shape
        self.ticks = 0

    def draw(self):
        if self.shape == "circle":
            if self.ticks <= 15:
                pygame.draw.circle(screen, self.color, (self.x, self.y), self.ticks * 2)
            elif self.ticks > 15:
                pygame.draw.circle(screen, self.color, (self.x, self.y), 30)

    def update(self):
        self.ticks += 1

class LevelTemplate:
    def __init__(self):
        self.duration = 60
        self.song = None
        self.shapes = []
        self.tick = 0
        
    def update(self):
        self.tick += 1
        for shape in self.shapes:
            shape.update()
            if shape.ticks >= shape.duration:
                self.shapes.remove(shape)

    def draw(self):
        for shape in self.shapes:
            shape.draw()

class LevelPlayer:
    def __init__(self, level: LevelTemplate):
        self.level = level
        self.player = Player()
        self.exited = False
    
    def collidePlayer(self):
        for shape in self.level.shapes:
            if pygame.Rect(shape.x - 30, shape.y - 30, 60, 60).collidepoint(self.player.x, self.player.y) and shape.ticks >= 15:
                self.exited = True
        
    def run(self):
        if self.level.song != None:
            pygame.mixer.Channel(0).play(pygame.mixer.Sound(self.level.song))
        while True:
            screen.fill((0, 0, 0))

            self.collidePlayer()

            self.level.update()
            self.level.draw()
            self.player.update()
            self.player.draw()

            if self.level.tick >= self.level.duration or self.exited:
                pygame.mixer.stop()
                break
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
            clock.tick(fps)

class Button:
    def __init__(self, x, y, image, function):
        self.x, self.y = x, y
        self.image = pygame.image.load(image)
        self.function = function

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def clickevent(self):
        if pygame.Rect(self.x, self.y, self.image.get_rect().width, self.image.get_rect().height).collidepoint(*pygame.mouse.get_pos()):
            self.function()

class StylizedButton(Button):
    def __init__(self, x, y, text, function):
        super().__init__(x, y, "Assets/buttonBackground.png", function)
        self.text = font.render(text, True, "black")

    def draw(self):
        super().draw()
        screen.blit(self.text, (self.image.get_rect().width // 2 - self.text.get_rect().width // 2, self.image.get_rect().height // 2 - self.text.get_rect().height // 2))

class Player:
    def __init__(self, x = width // 2, y = height // 2):
        self.x, self.y = x, y
        self.speed = 1
        
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_s]:
            self.y += self.speed
        if keys[pygame.K_d]:
            self.x += self.speed

    def draw(self):
        pygame.draw.circle(screen, (255, 100, 100), (self.x, self.y), 20)

class MenuTemplate:
    def __init__(self):
        self.buttons = []
        self.background = None
        self.backgroundMusic = None
        self.exited = False
        
    def run(self):
        if self.backgroundMusic != None:
            pygame.mixer.Channel(0).play(pygame.mixer.Sound(self.backgroundMusic), loops = 10000, fade_ms = 1000)
        while True:
            screen.fill((0, 0, 0))
            if self.background != None:
                screen.blit(self.background, (0, 0, width, height))

            if self.exited == True:
                pygame.mixer.stop()
                break

            for button in self.buttons:
                button.draw()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        button.clickevent()

            pygame.display.update()
            clock.tick(fps)