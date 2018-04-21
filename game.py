import pygame

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Initialize
pygame.init()
size = (800, 600)
screen = pygame.display.set_mode(size)
maindone = False
pygame.display.set_caption("Loading...")
clock = pygame.time.Clock()


class Character:
    def __init__(self):
        self.x = -100
        self.y = 330
        self.frame = 1
        self.turn = "r"
        self.ani = 0

    def moving(self, mouse_x):
        self.mousemid = mouse_x - 75
        if self.x != self.mousemid:
            if abs(self.mousemid - self.x) < 17:
                self.x = self.mousemid
            elif self.mousemid > self.x:
                self.x += 17
                self.turn = "r"
            else:
                self.x -= 17
                self.turn = "l"

    def drawing(self):
        if self.x != self.mousemid:
            self.ani += 1
        else:
            self.ani = 0
            self.frame = 1
        if self.ani == 2:
            self.ani = 0
            self.frame += 1
            if self.frame == 4:
                self.frame = 2
        player_image = pygame.image.load(
            "resource/user%i-%s.png" % (self.frame, self.turn)).convert()
        player_image.set_colorkey(GREEN)
        player_image = pygame.transform.scale(player_image, (125, 181))
        screen.blit(player_image, (self.x, self.y))

    def transition(self, page, direction, pos):
        if direction == "left":
            if self.x > -50:
                self.moving(-100)
                return page, pos
            else:
                self.x = 750
                return page - 1, (700, 0)
        elif direction == "right":
            if self.x < 800:
                self.moving(900)
                return page, pos
            else:
                self.x = -50
                return page + 1, (100, 0)


class Page:
    def __init__(self):
        global maindone
        self.done = False


class MainMenu(Page):
    def __init__(self):
        Page.__init__(self)
        pygame.display.set_caption("Main menu")
        self.select = None
        self.click = (-1, -1)

    def run(self):
        while not self.done:
            # EVENT PROCESSING STEP
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                    maindone = True
                if event.type == pygame.MOUSEBUTTONUP:
                    self.click = pygame.mouse.get_pos()
                # Event here
            # GAME LOGIC STEP
            # Logic here
            # DRAWING STEP
            screen.fill(WHITE)
            # Draw here
            pygame.display.flip()
            # Set fps
            clock.tick_busy_loop(60)


class LevelNo1(Page):
    def __init__(self):
        Page.__init__(self)
        pygame.display.set_caption("Level 1")
        self.background_image = pygame.image.load(
            "resource/new2-1.png").convert()
        self.char = char = Character()
        self.mpos = (100, 0)
        self.page = 0
        self.pagelist = (self.draw0, self.draw1, self.draw2)

    def run(self):
        while not self.done:
            # EVENT PROCESSING STEP
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                    maindone = True
                if event.type == pygame.MOUSEBUTTONUP:  # heart of click based game
                    self.mpos = pygame.mouse.get_pos()
            # GAME LOGIC STEP
            # ***page transition block***
            if 10 < self.mpos[0] < 60 and 250 < self.mpos[1] < 350 and self.page != 0:
                self.page, self.mpos = self.char.transition(self.page, "left", self.mpos)
            elif 740 < self.mpos[0] < 790 and 250 < self.mpos[1] < 350 and self.page != 2:
                self.page, self.mpos = self.char.transition(self.page, "right", self.mpos)
            else:
                self.char.moving(self.mpos[0])
            # ***page transition block***
            # DRAWING STEP
            screen.blit(self.background_image, (0, 0))
            self.pagelist[self.page]()  # look weird but it works (draw current page)
            self.char.drawing()
            if self.page != 0:
                pygame.draw.rect(screen, WHITE, (10, 250, 50, 100))
            if self.page != 2:
                pygame.draw.rect(screen, WHITE, (740, 250, 50, 100))
            pygame.display.flip()
            # Set fps
            clock.tick_busy_loop(60)

    # game page change
    def draw0(self):
        pygame.draw.rect(screen, RED, (90, 250, 50, 100))

    def draw1(self):
        pygame.draw.rect(screen, GREEN, (90, 250, 50, 100))

    def draw2(self):
        pygame.draw.rect(screen, BLUE, (90, 250, 50, 100))


def main():  # TODO: global logic of game still figure how to make stage change
    global maindone
    if not maindone:
        lvl1 = LevelNo1()
        lvl1.run()


main()
pygame.quit()
