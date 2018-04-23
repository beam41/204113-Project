import pygame
import os
from math import sin, cos, atan2

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


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
        self.oldpage = 0
        self.select = -1
        self.font = pygame.font.SysFont('Calibri', 25, True, False)
        self.speak = pygame.font.SysFont('Calibri', 30, True, False)
        self.leftarrow = pygame.image.load(os.path.join(
            "resource", "leftarrow.png")).convert_alpha()
        self.rightarrow = pygame.image.load(os.path.join(
            "resource", "rightarrow.png")).convert_alpha()
        self.rightarrow_g = pygame.image.load(os.path.join(
            "resource", "rightarrow_g.png")).convert_alpha()


class MainMenu(Page):  # TODO: Mainmenu page
    def __init__(self):
        Page.__init__(self)
        pygame.display.set_caption("Wonderwild: Main Menu")
        self.select = 0

    def run(self):
        global save
        while not self.done:
            self.clickpos = pygame.mouse.get_pos()
            # EVENT PROCESSING STEP
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                    self.select = -2
                if event.type == pygame.MOUSEBUTTONUP:
                    if 250 < self.clickpos[0] < 270 and 210 < self.clickpos[1] < 260 and self.select > 0:  # previous level
                        self.select -= 1
                    elif 350 < self.clickpos[0] < 370 and 210 < self.clickpos[1] < 260 and save[self.select] == 1:  # next level
                        self.select += 1
                    elif 250 < self.clickpos[0] < 350 and 310 < self.clickpos[1] < 410:
                        self.done = True
                # Event here
            # GAME LOGIC STEP
            # Logic here
            # DRAWING STEP
            screen.fill(WHITE)
            text = self.font.render("%i" % (self.select + 1), True, BLACK)
            screen.blit(text, (305, 200))
            pygame.draw.rect(screen, BLACK, (250, 210, 20, 50))
            pygame.draw.rect(screen, BLACK, (350, 210, 20, 50))
            pygame.draw.rect(screen, BLACK, (250, 310, 100, 100))
            # Draw here
            pygame.display.flip()
            # Set fps
            clock.tick_busy_loop(60)
        return self.select


class LevelNo1(Page):  # Finished
    def __init__(self):
        Page.__init__(self)
        pygame.display.set_caption("Wonderwild: Level 1")
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
        self.onmap = {self.torch, self.fire}
        self.inventory = {self.bucket}

    def run(self):
        global save
        text = None
        texttime = 0
        while not self.done:
            # EVENT PROCESSING STEP
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                    self.select = -2
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.sep = True
                elif event.type == pygame.MOUSEBUTTONUP:  # heart of click based game
                    self.mpos = pygame.mouse.get_pos()
                    self.clickpos = pygame.mouse.get_pos()
            # GAME LOGIC STEP
            if self.fire in self.onmap and self.page == 1:
                if self.mpos[0] > 180:
                    if self.bucketstate != 3:
                        text = "I need something to put out fire."
                        texttime = 120
                    self.mpos = list(self.mpos)
                    self.mpos[0] = 180
                    self.mpos = tuple(self.mpos)
            elif self.page == 1:
                if self.mpos[0] > 490:
                    if self.torchstate != 1:
                        text = "I think I need fire to scare bat."
                        texttime = 120
                    self.mpos = list(self.mpos)
                    self.mpos[0] = 490
                    self.mpos = tuple(self.mpos)
            # ***page transition block***
            if self.page == self.oldpage:
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
            else:
                self.clickpos = (-1, -1)
                self.oldpage = self.page
            # ***page transition block***
            # ***pickup blah blah***
            if self.page == 0:
                if 175 < self.mpos[0] < 280 and 525 < self.mpos[1] < 560:
                    if self.torch in self.onmap:
                        if self.char.pickup((175, 280)):
                            self.onmap.remove(self.torch)
                            self.inventory.add(self.torch)
                elif 559 < self.mpos[0] < 647 and 450 < self.mpos[1] < 568:
                    if self.bucket in self.inventory:
                        if self.char.pickup((559, 647)) and self.sep:
                            if self.bucketstate != 3:
                                self.bucketstate += 1
                                self.sep = False
                            elif self.bucketstate == 3:
                                text = "This bucket is full!"
                                texttime = 60
            elif self.page == 1:
                if 179 < self.clickpos[0] < 490 and 290 < self.clickpos[1] < 600:
                    if self.fire in self.onmap and self.sep:
                        if self.torch in self.inventory and self.torchstate == 0:
                            if self.char.pickup((179, 490)):
                                self.torchstate = 1
                                self.sep = False
                        elif self.bucket in self.inventory and self.bucketstate == 3:
                            self.onmap.remove(self.fire)
                            self.bucketstate = 0
                            self.sep = False
                elif 489 < self.mpos[0] < 774 and 250 < self.mpos[1] < 395:
                    if self.torch in self.inventory and self.torchstate == 1 and self.sep and self.fire not in self.onmap:
                        if self.char.pickup((489, 774)):
                            self.batstate = 1
                            self.batfly = True
            # ***pickup blah blah***
            if self.batfly:
                self.batlo = (self.batlo[0] + 10, self.batlo[1] - 20)
            if self.batlo[0] > 820:  # game complete
                self.complete = True
                save[0] = 1
                self.select = 1
            # DRAWING STEP
            # look weird but it works (draw current page)
            self.pagelist[self.page]()
            self.char.drawing()
            if self.bucket in self.inventory:
                bucky = pygame.transform.scale(self.bucket[self.bucketstate], (50, 64))
                screen.blit(bucky, (10, 22))
            if self.torch in self.inventory:
                torchy = pygame.transform.scale(self.torch[self.torchstate], (100, 95))
                screen.blit(torchy, (70, 4))
            if self.page != 0:
                screen.blit(self.leftarrow, (10, 250))
            if self.page != 1 or self.complete:
                if self.complete:
                    screen.blit(self.rightarrow_g, (740, 250))
                else:
                    screen.blit(self.rightarrow, (740, 250))
            if text:
                wtext = self.speak.render(text, True, WHITE)
                btext = self.speak.render(text, True, BLACK)
                screen.blit(btext, (self.char.x, self.char.y - 52))
                screen.blit(btext, (self.char.x + 2, self.char.y - 52))
                screen.blit(btext, (self.char.x + 2, self.char.y - 50))
                screen.blit(btext, (self.char.x + 2, self.char.y - 48))
                screen.blit(btext, (self.char.x, self.char.y - 48))
                screen.blit(btext, (self.char.x - 2, self.char.y - 48))
                screen.blit(btext, (self.char.x - 2, self.char.y - 50))
                screen.blit(btext, (self.char.x - 2, self.char.y - 52))
                # Above is outline
                screen.blit(wtext, (self.char.x, self.char.y - 50))
                texttime -= 1
                if texttime == 0:
                    text = None
            pygame.display.flip()
            # Set fps
            clock.tick_busy_loop(60)
        return self.select

    # game page
    def draw0(self):
        screen.blit(self.background_image_1, (0, 0))
        if self.torch in self.onmap:
            torchy = pygame.transform.scale(self.torch[self.torchstate], (125, 118))
            torchy = pygame.transform.rotate(torchy, -42)
            screen.blit(torchy, (150, 450))
        screen.blit(self.water, (405, 340))

    def draw1(self):
        screen.blit(self.background_image_2, (0, 0))
        screen.blit(self.bat[self.batstate], self.batlo)
        if self.fire in self.onmap:
            screen.blit(self.fire, (200, 290))


class LevelNo2(Page):  # Finished
    def __init__(self):
        Page.__init__(self)
        pygame.display.set_caption("Wonderwild: Level 2")
        self.background_image_1 = pygame.image.load(
            os.path.join("resource", "new3-1.png")).convert()
        self.background_image_2 = pygame.image.load(
            os.path.join("resource", "new3-2.png")).convert()
        self.background_image_3 = pygame.image.load(
            os.path.join("resource", "new3-3.png")).convert()
        self.pagelist = (self.draw0, self.draw1, self.draw2)
        self.bucket = (pygame.image.load(os.path.join("resource", "bucket0.png")).convert_alpha(),
                       pygame.image.load(os.path.join("resource", "bucket1.png")).convert_alpha(),
                       pygame.image.load(os.path.join("resource", "bucket2.png")).convert_alpha(),
                       pygame.image.load(os.path.join("resource", "bucket3.png")).convert_alpha())
        self.bucketstate = 0
        self.walkway = (pygame.image.load(os.path.join("resource", "walkway-a.png")).convert_alpha(),
                        pygame.image.load(os.path.join("resource", "walkway-e.png")).convert_alpha(),
                        pygame.image.load(os.path.join("resource", "walkway-up.png")).convert_alpha(),
                        pygame.image.load(os.path.join("resource", "walkway-down.png")).convert_alpha())
        self.well = (pygame.image.load(os.path.join("resource", "well-0.png")).convert_alpha(),
                     pygame.image.load(os.path.join("resource", "well-1.png")).convert_alpha(),
                     pygame.image.load(os.path.join("resource", "well-2.png")).convert_alpha())
        self.wellstate = 0
        self.bush = (pygame.image.load(os.path.join("resource", "bush.png")).convert_alpha(),
                     pygame.image.load(os.path.join("resource", "bush-h.png")).convert_alpha())
        self.bushgrow = False
        self.wood = (pygame.image.load(os.path.join("resource", "wood.png")).convert_alpha(),
                     pygame.image.load(os.path.join("resource", "wood-a.png")).convert_alpha(),
                     pygame.image.load(os.path.join("resource", "wood-b.png")).convert_alpha(),
                     pygame.image.load(os.path.join("resource", "wood-c.png")).convert_alpha())
        self.woodstate = 0
        self.axe = pygame.image.load(os.path.join("resource", "axe.png")).convert_alpha()
        self.bridge = pygame.image.load(os.path.join("resource", "bridge.png")).convert_alpha()
        self.rope = pygame.image.load(os.path.join("resource", "rope.png")).convert_alpha()
        self.onmap = {self.axe, self.rope}
        self.inventory = {self.bucket}

    def run(self):
        global save
        text = None
        texttime = 0
        while not self.done:
            # EVENT PROCESSING STEP
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                    self.select = -2
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.sep = True
                elif event.type == pygame.MOUSEBUTTONUP:  # heart of click based game
                    self.mpos = pygame.mouse.get_pos()
                    self.clickpos = pygame.mouse.get_pos()
            # GAME LOGIC STEP
            if self.bushgrow:
                if self.page == 0:
                    if self.mpos[0] < 600:
                        self.mpos = list(self.mpos)
                        self.mpos[0] = 600
                        self.mpos = tuple(self.mpos)
                if self.page == 0:
                    self.char.y = 10
                elif self.page == 1:
                    self.char.y = 330
                elif self.page == 2:
                    self.char.y = 350
            if self.woodstate != 2 and self.page == 1:
                if self.mpos[0] > 338:
                    text = "I can't cross this"
                    texttime = 120
                    self.mpos = list(self.mpos)
                    self.mpos[0] = 338
                    self.mpos = tuple(self.mpos)
            if self.page == 2:
                if self.mpos[0] > 478:
                    if self.bridge in self.inventory:
                        self.inventory.remove(self.bridge)
                        self.onmap.add(self.bridge)
                    elif self.bridge not in self.onmap:
                        if self.rope in self.inventory:
                            text = "Only rope can't do anything"
                            texttime = 120
                        elif self.wood[3] not in self.inventory:
                            text = "I think some wood can use to cross"
                            texttime = 120
                        elif self.wood[3] in self.inventory and self.rope not in self.inventory:
                            text = "I need something to join stick together"
                            texttime = 120
                        else:
                            text = "I can't cross this"
                            texttime = 120
                        self.mpos = list(self.mpos)
                        self.mpos[0] = 478
                        self.mpos = tuple(self.mpos)
            # ***page transition block***
            if self.page == self.oldpage:
                if 10 < self.clickpos[0] < 60 and 250 < self.clickpos[1] < 350 and self.page != 0:
                    self.page, self.mpos = self.char.transition(
                        self.page, "left", self.mpos, self.complete)
                elif (740 < self.clickpos[0] < 790 and 250 < self.clickpos[1] < 350 and self.page != 2 and self.bushgrow and (self.page == 0 or self.woodstate == 2)) or self.complete:
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
            else:
                self.clickpos = (-1, -1)
                self.oldpage = self.page
            # ***page transition block***
            # ***pickup blah blah***
            if self.page == 0:
                if 720 < self.mpos[0] < 790 and 460 < self.mpos[1] < 531:
                    if self.axe in self.onmap:
                        if self.char.pickup((720, 790)):
                            if not self.bushgrow:
                                self.onmap.remove(self.axe)
                                self.inventory.add(self.axe)
                if 270 < self.mpos[0] < 383 and 363 < self.mpos[1] < 505:
                    if self.bucket in self.inventory:
                        if self.char.pickup((270, 383)) and self.sep:
                            if self.bucketstate != 3:
                                if self.wellstate != 2:
                                    self.wellstate += 2 / 3
                                self.bucketstate += 1
                            elif self.bucketstate == 3:
                                text = "This bucket is full!"
                                texttime = 60
                            self.sep = False
                if 485 < self.mpos[0] < 715 and 430 < self.mpos[1] < 525:
                    if self.char.pickup((485, 715)):
                        if self.bucketstate == 3:
                            self.bucketstate = 0
                            self.bushgrow = True
                        elif self.bushgrow is False:
                            text = "I can grow this bush"
                            texttime = 120
            elif self.page == 1:
                if 239 < self.mpos[0] < 297 and 134 < self.mpos[1] < 519:
                    if self.char.pickup((239, 297)) and self.sep:
                        if self.axe in self.inventory:
                            if self.woodstate != 2:
                                self.woodstate += 1
                            self.sep = False
                        else:
                            text = "I need axe to cut this tree"
                            texttime = 120
                if 318 < self.mpos[0] < 652 and 472 < self.mpos[1] < 527:
                    if self.char.pickup((318, 652)):
                        if self.axe in self.inventory:
                            if self.woodstate == 2:
                                self.inventory.add(self.wood[3])

            elif self.page == 2:
                if 298 < self.mpos[0] < 400 and 515 < self.mpos[1] < 577:
                    if self.rope in self.onmap:
                        if self.char.pickup((298, 400)):
                            self.onmap.remove(self.rope)
                            self.inventory.add(self.rope)
            # ***pickup blah blah***
            if self.wood[3] in self.inventory and self.rope in self.inventory:
                self.inventory.remove(self.wood[3])
                self.inventory.remove(self.rope)
                self.inventory.add(self.bridge)
            if self.bridge in self.onmap:   # game complete
                self.complete = True
                save[1] = 1
                self.select = 2
            # DRAWING STEP
            # look weird but it works (draw current page)
            self.pagelist[self.page]()
            if self.bucket in self.inventory:
                bucky = pygame.transform.scale(self.bucket[self.bucketstate], (50, 64))
                screen.blit(bucky, (10, 22))
            if self.axe in self.inventory:
                axy = pygame.transform.scale(self.axe, (70, 71))
                screen.blit(axy, (90, 22))
            if self.bridge in self.inventory:
                bridgy = pygame.transform.scale(self.bridge, (160, 66))
                screen.blit(bridgy, (190, 21))
            elif self.wood[3] in self.inventory:
                wooddy = pygame.transform.scale(self.wood[3], (106, 66))
                screen.blit(wooddy, (190, 21))
            elif self.rope in self.inventory:
                ropy = pygame.transform.scale(self.rope, (100, 66))
                screen.blit(ropy, (180, 21))
            if self.page != 0:
                screen.blit(self.leftarrow, (10, 250))
            if self.page != 2 and self.bushgrow or self.complete:
                if self.complete:
                    screen.blit(self.rightarrow_g, (740, 250))
                else:
                    screen.blit(self.rightarrow, (740, 250))
            if text:
                wtext = self.speak.render(text, True, WHITE)
                btext = self.speak.render(text, True, BLACK)
                screen.blit(btext, (self.char.x, self.char.y - 52))
                screen.blit(btext, (self.char.x + 2, self.char.y - 52))
                screen.blit(btext, (self.char.x + 2, self.char.y - 50))
                screen.blit(btext, (self.char.x + 2, self.char.y - 48))
                screen.blit(btext, (self.char.x, self.char.y - 48))
                screen.blit(btext, (self.char.x - 2, self.char.y - 48))
                screen.blit(btext, (self.char.x - 2, self.char.y - 50))
                screen.blit(btext, (self.char.x - 2, self.char.y - 52))
                # Above is outline
                screen.blit(wtext, (self.char.x, self.char.y - 50))
                texttime -= 1
                if texttime == 0:
                    text = None
            pygame.display.flip()
            # Set fps
            clock.tick_busy_loop(60)
        return self.select

    # game page
    def draw0(self):
        screen.blit(self.background_image_1, (0, 0))
        welly = pygame.transform.scale(self.well[int(self.wellstate)], (395, 296))
        screen.blit(welly, (150, 280))
        screen.blit(self.walkway[2], (350, -80))
        self.char.drawing()
        bushy = pygame.transform.scale(self.bush[0], (300, 150))
        if self.bushgrow:
            screen.blit(self.bush[1], (100, 120))
        else:
            screen.blit(bushy, (450, 400))
        if self.axe in self.onmap:
            axy = pygame.transform.scale(self.axe, (70, 71))
            screen.blit(axy, (720, 460))

    def draw1(self):
        screen.blit(self.background_image_2, (0, 0))
        screen.blit(self.walkway[3], (-400, 220))
        screen.blit(self.walkway[0], (600, 205))
        if 270 < self.char.x < 540:
            self.char.y = 300
        self.char.drawing()
        woody = pygame.transform.scale(self.wood[self.woodstate], (700, 525))
        screen.blit(woody, (20, 40))

    def draw2(self):
        screen.blit(self.background_image_3, (0, 0))
        screen.blit(self.walkway[0], (-300, 195))
        screen.blit(self.walkway[1], (550, 220))
        if self.bridge in self.onmap:
            screen.blit(self.bridge, (480, 490))
        self.char.drawing()
        if self.rope in self.onmap:
            ropy = pygame.transform.scale(self.rope, (100, 66))
            screen.blit(ropy, (300, 510))


class LevelNo3(Page):
    def __init__(self):
        Page.__init__(self)
        pygame.display.set_caption("Wonderwild: Level 1")
        self.background_image_1 = pygame.image.load(
            os.path.join("resource", "new1-1.png")).convert()
        self.fox = (pygame.image.load(os.path.join("resource", "fox1.png")).convert_alpha(),
                    pygame.image.load(os.path.join("resource", "fox2.png")).convert_alpha(),
                    pygame.image.load(os.path.join("resource", "fox3.png")).convert_alpha(),
                    pygame.image.load(os.path.join("resource", "fox4.png")).convert_alpha(),
                    pygame.image.load(os.path.join("resource", "fox5.png")).convert_alpha(),
                    pygame.image.load(os.path.join("resource", "fox6.png")).convert_alpha(),
                    pygame.image.load(os.path.join("resource", "fox7.png")).convert_alpha(),
                    pygame.image.load(os.path.join("resource", "fox8.png")).convert_alpha(),
                    pygame.image.load(os.path.join("resource", "fox9.png")).convert_alpha())
        self.foxanimation = 0
        self.stone = (pygame.image.load(os.path.join("resource", "stone1.png")).convert_alpha(),
                      pygame.image.load(os.path.join("resource", "stone2.png")).convert_alpha(),
                      pygame.image.load(os.path.join("resource", "stone3.png")).convert_alpha())
        self.tree = (pygame.image.load(os.path.join("resource", "tree1.png")).convert_alpha(),
                     pygame.image.load(os.path.join("resource", "tree2.png")).convert_alpha(),
                     pygame.image.load(os.path.join("resource", "tree3.png")).convert_alpha(),
                     pygame.image.load(os.path.join("resource", "tree4.png")).convert_alpha())
        self.treeanimation = 0
        self.axe = pygame.image.load(os.path.join("resource", "axe2.png")).convert_alpha()
        self.bird = pygame.image.load(os.path.join("resource", "bird.png")).convert_alpha()
        self.wood2 = pygame.image.load(os.path.join("resource", "wood2.png")).convert_alpha()
        self.birdfall = False
        self.rockthrow = False
        self.rock_x = 0
        self.rock_y = 0
        self.bird_x = 420
        self.bird_y = 233
        self.bird_rotate = 0
        self.foxgo = False
        self.fox_x = 550
        self.treefall = pygame.USEREVENT + 1
        self.finished = pygame.USEREVENT + 2
        self.clickable = True
        self.onmap = {self.axe, self.stone[2], self.fox}
        self.inventory = set()

    def run(self):
        global save
        text = None
        texttime = 0
        speed = 0
        gravity = 9.8 / 2
        while not self.done:
            # EVENT PROCESSING STEP
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                    self.select = -2
                if event.type == pygame.MOUSEBUTTONDOWN and self.clickable:
                    self.sep = True
                elif event.type == pygame.MOUSEBUTTONUP and self.clickable:  # heart of click based game
                    self.clickpos = pygame.mouse.get_pos()
                    if 462 < self.clickpos[0] < 491 and 242 < self.clickpos[1] < 299 and self.stone[2] in self.inventory:
                        self.rockthrow = True
                    else:
                        self.mpos = pygame.mouse.get_pos()
                if event.type == self.treefall:
                    if self.treeanimation != 3:
                        self.treeanimation += 1
                if event.type == self.finished:  # when finished
                    self.complete = True
                    self.select = 3
            # GAME LOGIC STEP
            if not self.foxgo or self.treeanimation != 3:
                if self.mpos[0] > 500:
                    text = "Fox is in my way."
                    texttime = 120
                    self.mpos = list(self.mpos)
                    self.mpos[0] = 500
                    self.mpos = tuple(self.mpos)
            else:
                if self.fox in self.onmap:
                    self.onmap.remove(self.fox)
                if self.clickable:
                    pygame.time.set_timer(self.finished, 500)
                save[2] = 1
                self.clickable = False
            if self.foxgo:
                if self.fox_x != self.bird_x - 80:
                    self.fox_x -= 10
                    self.foxanimation += 8 / 11
            elif self.birdfall:
                if self.bird_y < 450:
                    self.bird_x += 10
                    self.bird_rotate -= 9
                    self.bird_y += speed
                    speed += gravity
                else:
                    self.foxgo = True
            elif self.rockthrow:
                if self.stone[2] in self.inventory:
                    self.inventory.remove(self.stone[2])
                    self.rock_x = self.char.x + 75
                    self.rock_y = self.char.y + 75
                    tangent = atan2(self.clickpos[1] - self.rock_y, self.clickpos[0] - self.rock_x)
                self.rock_x += cos(tangent) * 30
                self.rock_y += sin(tangent) * 30
            if 462 < self.rock_x < 491 and 242 < self.rock_y < 299:
                self.birdfall = True
            # ***page transition block***
            if self.page == self.oldpage:
                if self.complete:
                    self.gone, self.mpos = self.char.transition(
                        self.page, "right", self.mpos, self.complete)
                    if self.gone is True:
                        self.done = True
                else:
                    self.char.moving(self.mpos[0])
            else:
                self.clickpos = (-1, -1)
                self.oldpage = self.page
            # ***page transition block***
            # ***pickup blah blah***
            if 174 < self.mpos[0] < 252 and 387 < self.mpos[1] < 440:
                if self.char.pickup((174, 252)):
                    if self.axe in self.onmap:
                        self.onmap.remove(self.axe)
                        self.inventory.add(self.axe)
            if 59 < self.mpos[0] < 164 and 461 < self.mpos[1] < 497:
                if self.char.pickup((59, 164)):
                    if self.stone[2] in self.onmap:
                        self.onmap.remove(self.stone[2])
                        self.inventory.add(self.stone[2])
            if 369 < self.mpos[0] < 404 and 380 < self.mpos[1] < 468:
                if self.char.pickup((369, 404)) and self.sep:
                    if self.axe in self.inventory:
                        pygame.time.set_timer(self.treefall, 20)
                    else:
                        text = "I can cut tree with axe"
                        texttime = 120
            if 462 < self.mpos[0] < 491 and 242 < self.mpos[1] < 299:
                if self.char.pickup((462, 491)) and not self.birdfall:
                    text = "This bird doesn't have wings"
                    texttime = 120
            # ***pickup blah blah***
            # DRAWING STEP
            self.draw0()
            self.char.drawing()
            if self.axe in self.inventory:
                axy = pygame.transform.scale(self.axe, (150, 113))
                screen.blit(axy, (-10, 0))
            if self.stone[2] in self.inventory:
                screen.blit(self.stone[2], (150, 25))
            if self.complete:
                screen.blit(self.rightarrow_g, (740, 250))
            if text:
                wtext = self.speak.render(text, True, WHITE)
                btext = self.speak.render(text, True, BLACK)
                screen.blit(btext, (self.char.x, self.char.y - 52))
                screen.blit(btext, (self.char.x + 2, self.char.y - 52))
                screen.blit(btext, (self.char.x + 2, self.char.y - 50))
                screen.blit(btext, (self.char.x + 2, self.char.y - 48))
                screen.blit(btext, (self.char.x, self.char.y - 48))
                screen.blit(btext, (self.char.x - 2, self.char.y - 48))
                screen.blit(btext, (self.char.x - 2, self.char.y - 50))
                screen.blit(btext, (self.char.x - 2, self.char.y - 52))
                # Above is outline
                screen.blit(wtext, (self.char.x, self.char.y - 50))
                texttime -= 1
                if texttime == 0:
                    text = None
            pygame.display.flip()
            # Set fps
            clock.tick_busy_loop(60)
        return self.select

    # game page
    def draw0(self):
        screen.blit(self.background_image_1, (0, 0))
        woody = pygame.transform.scale(self.wood2, (200, 120))
        screen.blit(woody, (100, 400))
        if self.stone[2] in self.onmap:
            stony = pygame.transform.scale(self.stone[0], (250, 188))
        else:
            stony = pygame.transform.scale(self.stone[1], (250, 188))
        screen.blit(stony, (-10, 370))
        if self.treeanimation != 3:
            screen.blit(self.tree[self.treeanimation], (120, 15))
        if self.axe in self.onmap:
            axy = pygame.transform.scale(self.axe, (150, 111))
            screen.blit(axy, (130, 357))
        if self.rockthrow and not self.birdfall:
            rocky = pygame.transform.scale(self.stone[2], (20, 15))
            screen.blit(rocky, (self.rock_x, self.rock_y))
        if self.treeanimation == 0 or self.birdfall:
            birdy = pygame.transform.scale(self.bird, (100, 75))
            birdy = pygame.transform.rotate(birdy, self.bird_rotate)
            screen.blit(birdy, (self.bird_x, self.bird_y))
        if self.treeanimation == 3:
            screen.blit(self.tree[self.treeanimation], (120, 15))
        if self.fox in self.onmap:
            foxy = pygame.transform.scale(self.fox[int(self.foxanimation)], (600, 450))
            screen.blit(foxy, (self.fox_x, 200))


# Initialize
pygame.init()
size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Wonderwild")
clock = pygame.time.Clock()
try:
    with open("save", "r+") as file:
        if not file.read():
            file.write("0\n0\n0\n0\n0")
    with open("save", "r+") as file:
        a = file.readlines()
        save = [int(x.rstrip("\n")) for x in a]
except FileNotFoundError:
    with open("save", "w") as file:
        file.write("0\n0\n0\n0\n0")


def main():  # global level selection logic
    global save
    select = -1
    while select != -2:
        if select == -1:
            mainmenu = MainMenu()
            select = mainmenu.run()
            del mainmenu
        elif select == 0:
            lvl1 = LevelNo1()
            select = lvl1.run()
            del lvl1
        elif select == 1:
            lvl2 = LevelNo2()
            select = lvl2.run()
            del lvl2
        elif select == 2:
            lvl3 = LevelNo3()
            select = lvl3.run()
            del lvl3
        elif select == 3:
            lvl4 = LevelNo4()
            select = lvl4.run()
            del lvl4
        elif select == 4:
            lvl5 = LevelNo5()
            select = lvl5.run()
            del lvl5
        with open("save", "w") as file:
            file.write("\n".join(map(str, save)))


main()
pygame.quit()
