import pygame

# Colors
WHITE = (255, 255, 255)

# Initialize
pygame.init()
size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("")
done = False
clock = pygame.time.Clock()

# -------- Main Program Loop -----------
while not done:
    # EVENT PROCESSING STEP
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        # Event here
    # GAME LOGIC STEP
    # Logic here
    # DRAWING STEP
    screen.fill(WHITE)
    # Draw here
    pygame.display.flip()
    # Set fps
    clock.tick(60)

pygame.quit()
