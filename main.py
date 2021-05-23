import random
import pygame
import os

pygame.init()

WIDTH, HEIGHT = 1000, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Duckhunt")

SCORE_FONT = pygame.font.SysFont('comicsans', 40)
BULLETS = [1, 1, 1, 1, 1, 1]
CROSSHAIR_WIDTH, CROSSHAIR_HEIGHT = 55, 40
CROSSHAIR = pygame.image.load(os.path.join("Assets", "Crosshair.png"))

SKY = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "sky.png")),(WIDTH,HEIGHT))
GROUND = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "Ground.png")),(WIDTH,HEIGHT//2))
FPS = 60


def set_pos(self, x, y):
    self.x = x - 20
    self.y = y


def Draw_Ducks(ducks, LEVEL):
    for duck in ducks:
        if duck.direction == 1 and duck.rect.x >= WIDTH:
            ducks.remove(duck)
        elif duck.direction == -1 and duck.rect.x <= 0:
            ducks.remove(duck)
        else:
            duck.update(LEVEL)


def main():
    LEVEL = 1
    changed = False
    SCORE = 1
    ducks = []
    run = True
    clock = pygame.time.Clock()
    crosshair = pygame.Rect(WIDTH // 2, HEIGHT // 2, CROSSHAIR_WIDTH, CROSSHAIR_HEIGHT)
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        if event.type == pygame.MOUSEMOTION:
            temp_pos = pygame.mouse.get_pos()
            set_pos(crosshair, temp_pos[0], temp_pos[1])

        if event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEBUTTONDOWN :
            pos = pygame.mouse.get_pos()
            clicked_sprites = [s for s in ducks if s.rect.collidepoint(pos)]
            for sprites in clicked_sprites:
                SCORE += 1
                ducks.remove(sprites)

        pygame.mouse.set_visible(False)
        WIN.blit(SKY, (0, 0))
        WIN.blit(GROUND, (0,HEIGHT//2))
        i = 0
        while len(ducks) < 5:
            if i >= 5:
                i = 0
            ducks.append(Duck_Sprite(i))
            i += 1

        if SCORE % 50 == 0 and not changed:
            LEVEL += 1
            changed = True

        if SCORE % 50 != 0:
            changed = False

        Draw_Ducks(ducks, LEVEL)

        score = SCORE_FONT.render("SCORE: "+ str(SCORE), 1, (0, 0, 0))
        level = SCORE_FONT.render("LEVEL: " + str(LEVEL), 1, (0, 0, 0))
        WIN.blit(score,(50,HEIGHT-50))
        WIN.blit(level, (WIDTH - 200, HEIGHT - 50))
        WIN.blit(CROSSHAIR, (crosshair.x, crosshair.y))

        pygame.display.update()


class Duck_Sprite:
    def __init__(self, pos):
        self.images_right = []
        self.images_left = []

        for i in range(1, 4):
            self.images_right.append(
                pygame.transform.scale(pygame.image.load(os.path.join('Assets', f"Duck{i}.png")), (45, 60)))
            self.images_left.append(
                pygame.transform.scale(
                    pygame.transform.flip(pygame.image.load(os.path.join('Assets', f"Duck{i}.png")), True,
                                          False), (45,60)))
        self.index = 0
        self.counter = 0
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.direction = 1
        self.pos = pos
        self.rect.x = random.randint(0, 1)
        if self.rect.x == 0:
            self.rect.x = WIDTH
            self.direction = -1
        if self.direction == -1:
            self.image = self.images_left[self.index]
        self.rect.y = random.randint(0, HEIGHT // 2)

    def update(self, l):
        walk_buffer = 20
        self.counter += 1
        # changes walk animation
        if self.counter > walk_buffer:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images_right):
                self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]

        if self.direction == 1:
            self.rect.x += 2*l
        else:
            self.rect.x -= 2*l

        WIN.blit(self.image, self.rect)


if __name__ == '__main__':
    main()
