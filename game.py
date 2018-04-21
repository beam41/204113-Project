import pygame

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Initialize
pygame.init()
size = (800, 600)
screen = pygame.display.set_mode(size)
maindone = False
pygame.display.set_caption("Loading...")
clock = pygame.time.Clock()


class Character():
    def __init__(self):
        self.x = -100
        self.y = 330

    def moving(self, mouse_x):
        mousemid = mouse_x -75
        if self.x != mousemid:
            if abs(mousemid - self.x) < 10:
                self.x = mousemid
            elif mousemid > self.x:
                self.x += 10
            else:
                self.x -= 10

    def drawing(self):
        player_image = pygame.image.load("resource/user1.png").convert()
        player_image.set_colorkey(GREEN)
        player_image = pygame.transform.scale(player_image, (125, 181))
        screen.blit(player_image, (self.x, self.y))



def mainmenu():  # incomplete
    global maindone
    pygame.display.set_caption("Main menu")
    done = False
    select = None
    clicklocation = (-1, -1)
    while not done:
        # EVENT PROCESSING STEP
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                maindone = True
            if event.type == pygame.MOUSEBUTTONUP:
                clicklocation = pygame.mouse.get_pos()
            # Event here
        # GAME LOGIC STEP
        # Logic here
        # DRAWING STEP
        screen.fill(WHITE)
        # Draw here
        pygame.display.flip()
        # Set fps
        clock.tick_busy_loop(60)


def lvl1():  # incomplete
    global maindone
    pygame.display.set_caption("Level 1")
    background_image = pygame.image.load("resource/new2-1.png").convert()
    done = False
    char = Character()
    mpos = (100,0)
    while not done:
        # EVENT PROCESSING STEP
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                maindone = True
            if event.type == pygame.MOUSEBUTTONUP:
                mpos = pygame.mouse.get_pos()
            # Event here
        # GAME LOGIC STEP
        char.moving(mpos[0])
        # Logic here
        # DRAWING STEP
        screen.blit(background_image, (0, 0))
        char.drawing()
        # Draw here
        pygame.display.flip()
        # Set fps
        clock.tick_busy_loop(60)


def main():
    global maindone

    if not maindone:
        levelselect = lvl1()


main()
pygame.quit()
