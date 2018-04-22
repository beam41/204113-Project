import pygame
import os

# Colors
WHITE = (255, 255, 255)


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
        player_image = pygame.image.load(os.path.join(
            "resource", "user%i-%s.png" % (self.frame, self.turn))).convert_alpha()
        player_image = pygame.transform.scale(player_image, (125, 181))
        screen.blit(player_image, (self.x, self.y))

    def transition(self, page, direction, pos, complete):
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
            elif complete:
                return True, (100, 0)
            else:
                self.x = -50
                return page + 1, (100, 0)

    def pickup(self, itempos):
        if itempos[0] < self.x + 75 < itempos[1]:
            return True


class Page:
    def __init__(self):
        self.done = False
        self.sep = False
        self.complete = False
        self.char = Character()
        self.mpos = (100, 0)
        self.clickpos = (-1, -1)
        self.page = 0
        self.leftarrow = pygame.image.load(os.path.join(
            "resource", "leftarrow.png")).convert_alpha()
        self.rightarrow = pygame.image.load(os.path.join(
            "resource", "rightarrow.png")).convert_alpha()
        self.rightarrow_g = pygame.image.load(os.path.join(
            "resource", "rightarrow_g.png")).convert_alpha()


class MainMenu(Page):
    def __init__(self):
        Page.__init__(self)
        pygame.display.set_caption("Main menu")
        self.select = None

    def run(self):
        global maindone
        while not self.done:
            # EVENT PROCESSING STEP
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                    maindone = True
                if event.type == pygame.MOUSEBUTTONUP:
                    self.clickpos = pygame.mouse.get_pos()
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
        self.background_image_1 = pygame.image.load(
            os.path.join("resource", "new2-1.png")).convert()
        self.background_image_2 = pygame.image.load(
            os.path.join("resource", "new2-2.png")).convert()
        self.pagelist = (self.draw0, self.draw1)
        self.bucket = (pygame.image.load(os.path.join("resource", "bucket0.png")).convert_alpha(),
                       pygame.image.load(os.path.join("resource", "bucket1.png")).convert_alpha(),
                       pygame.image.load(os.path.join("resource", "bucket2.png")).convert_alpha(),
                       pygame.image.load(os.path.join("resource", "bucket3.png")).convert_alpha())
        self.bucketstate = 0
        self.bat = (pygame.image.load(os.path.join("resource", "bat-l.png")).convert_alpha(),
                    pygame.image.load(os.path.join("resource", "bat-r.png")).convert_alpha())
        self.batstate = 0
        self.batlo = (550, 250)
        self.batfly = False
        self.torch = (pygame.image.load(os.path.join("resource", "torch-o.png")).convert_alpha(),
                      pygame.image.load(os.path.join("resource", "torch-l.png")).convert_alpha())
        self.torchstate = 0
        self.water = pygame.image.load(os.path.join("resource", "water.png")).convert_alpha()
        self.fire = pygame.image.load(os.path.join("resource", "fire.png")).convert_alpha()
        self.onmap = [self.bat, self.torch, self.water, self.fire]
        self.inventory = [self.bucket]

    def run(self):
        global maindone
        while not self.done:
            # EVENT PROCESSING STEP
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                    maindone = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.sep = True
                elif event.type == pygame.MOUSEBUTTONUP:  # heart of click based game
                    self.mpos = pygame.mouse.get_pos()
                    self.clickpos = pygame.mouse.get_pos()
            # GAME LOGIC STEP
            if self.fire in self.onmap and self.page == 1:
                if self.mpos[0] > 180:
                    self.mpos = list(self.mpos)
                    self.mpos[0] = 180
                    self.mpos = tuple(self.mpos)
            elif self.bat in self.onmap and self.page == 1:
                if self.mpos[0] > 490:
                    self.mpos = list(self.mpos)
                    self.mpos[0] = 490
                    self.mpos = tuple(self.mpos)
            # ***page transition block***
            if 10 < self.clickpos[0] < 60 and 250 < self.clickpos[1] < 350 and self.page != 0:
                self.page, self.mpos = self.char.transition(
                    self.page, "left", self.mpos, self.complete)
            elif (740 < self.clickpos[0] < 790 and 250 < self.clickpos[1] < 350 and self.page != 1) or self.complete:
                if self.complete:
                    self.gone, self.mpos = self.char.transition(
                        self.page, "right", self.mpos, self.complete)
                    if self.gone is True:
                        self.done = True
                else:
                    self.page, self.mpos = self.char.transition(
                        self.page, "right", self.mpos, self.complete)
            else:
                self.char.moving(self.mpos[0])
            # ***page transition block***
            # ***pickup blah blah***
            if 175 < self.mpos[0] < 280 and 525 < self.mpos[1] < 560 and self.page == 0:
                if self.torch in self.onmap:
                    if self.char.pickup((175, 280)):
                        self.onmap.remove(self.torch)
                        self.inventory.append(self.torch)
            if 559 < self.mpos[0] < 647 and 450 < self.mpos[1] < 568 and self.page == 0:
                if self.bucket in self.inventory:
                    if self.char.pickup((559, 647)) and self.sep:
                        if self.bucketstate != 3:
                            self.bucketstate += 1
                            self.sep = False
            if 179 < self.clickpos[0] < 490 and 290 < self.clickpos[1] < 600 and self.page == 1:
                if self.fire in self.onmap and self.sep:
                    if self.torch in self.inventory and self.torchstate == 0:
                        if self.char.pickup((179, 490)):
                            self.torchstate = 1
                            self.sep = False
                    elif self.bucket in self.inventory and self.bucketstate == 3:
                        self.onmap.remove(self.fire)
                        self.bucketstate = 0
                        self.sep = False
            if 489 < self.mpos[0] < 774 and 250 < self.mpos[1] < 395 and self.page == 1:
                if self.torch in self.inventory and self.torchstate == 1 and self.sep and self.fire not in self.onmap:
                    if self.char.pickup((489, 774)):
                        self.batstate = 1
                        self.batfly = True
            # ***pickup blah blah***
            if self.batfly:
                self.batlo = (self.batlo[0] + 10, self.batlo[1] - 20)
            if self.batlo[0] > 820:
                self.complete = True
                maindone[0] = 1
            # DRAWING STEP
            # look weird but it works (draw current page)
            self.pagelist[self.page]()
            self.char.drawing()
            for item in self.inventory:
                if item == self.bucket:
                    bucky = pygame.transform.scale(self.bucket[self.bucketstate], (50, 64))
                    screen.blit(bucky, (10, 22))
                if item == self.torch:
                    torchy = pygame.transform.scale(self.torch[self.torchstate], (100, 95))
                    screen.blit(torchy, (70, 4))
            if self.page != 0:
                screen.blit(self.leftarrow, (10, 250))
            if self.page != 1 or self.complete:
                if self.complete:
                    screen.blit(self.rightarrow_g, (740, 250))
                else:
                    screen.blit(self.rightarrow, (740, 250))
            pygame.display.flip()
            # Set fps
            clock.tick_busy_loop(60)

    # game page
    def draw0(self):
        screen.blit(self.background_image_1, (0, 0))
        for i in self.onmap:
            if i == self.torch:
                torchy = pygame.transform.scale(self.torch[self.torchstate], (125, 118))
                torchy = pygame.transform.rotate(torchy, -42)
                screen.blit(torchy, (150, 450))
            if i == self.water:
                screen.blit(self.water, (405, 340))

    def draw1(self):
        screen.blit(self.background_image_2, (0, 0))
        for i in self.onmap:
            if i == self.bat:
                screen.blit(self.bat[self.batstate], self.batlo)
            if i == self.fire:
                screen.blit(self.fire, (200, 290))


# Initialize
pygame.init()
size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Loading...")
clock = pygame.time.Clock()
try:
    with open("save", "r+") as file:
        if not file.read():
            file.write("0\n0\n0\n0\n0")
    with open("save", "r+") as file:
        a = file.readlines()
        maindone = [int(x.rstrip("\n")) for x in a]
        print(maindone)
except FileNotFoundError:
    with open("save", "w") as file:
        file.write("0\n0\n0\n0\n0")


def main():  # TODO: global logic of game still figure how to make stage change
    global maindone
    if True:
        lvl1 = LevelNo1()
        lvl1.run()
    with open("save", "w") as file:
        file.write("\n".join(map(str, maindone)))


main()
pygame.quit()
