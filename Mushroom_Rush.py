import pygame
import os
import time

# Window information
WIDTH, HEIGHT = 1200, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
BG_IMAGE = pygame.transform.scale(pygame.image.load(
    os.path.join("Assets", "forest.png")), (WIDTH, HEIGHT))
BLACK = (0, 0, 0)
DINO_VEL = 15
FPS = 60


# Assets
SPRITE_SHEET_IMG = pygame.image.load(
    os.path.join("Assets", "dino_sheets", "doux.png"))


# Returns sprites image
def get_image(sheet, frame, width, height, scale, color):

    # Create a new surface for the sprites to be drawn onto
    image = pygame.Surface((width, height)).convert_alpha()

    # Blit the sprite sheet on the surface that was just created, but just a cutout of a single frame
    image.blit(SPRITE_SHEET_IMG, (0, 0), ((frame * width), 0, width, height))

    # Scale the entire surface with the sprite already drawn onto it
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey(BLACK)
    return image




# All running frames in a list with 8 in total. 0 Being the Standing position
frames_run_R = [get_image(SPRITE_SHEET_IMG, 0, 24, 24, 5, BLACK), get_image(SPRITE_SHEET_IMG, 16, 24, 24, 5, BLACK), get_image(SPRITE_SHEET_IMG, 17, 24, 24, 5, BLACK),
          get_image(SPRITE_SHEET_IMG, 18, 24, 24, 5, BLACK), get_image(
              SPRITE_SHEET_IMG, 19, 24, 24, 5, BLACK), get_image(SPRITE_SHEET_IMG, 20, 24, 24, 5, BLACK),
          get_image(SPRITE_SHEET_IMG, 21, 24, 24, 5, BLACK), get_image(SPRITE_SHEET_IMG, 22, 24, 24, 5, BLACK), get_image(SPRITE_SHEET_IMG, 23, 24, 24, 5, BLACK)]


frames_run_R = [get_image(SPRITE_SHEET_IMG, 0, 24, 24, 5, BLACK), get_image(SPRITE_SHEET_IMG, 16, 24, 24, 5, BLACK), get_image(SPRITE_SHEET_IMG, 17, 24, 24, 5, BLACK),
          get_image(SPRITE_SHEET_IMG, 18, 24, 24, 5, BLACK), get_image(
              SPRITE_SHEET_IMG, 19, 24, 24, 5, BLACK), get_image(SPRITE_SHEET_IMG, 20, 24, 24, 5, BLACK),
          get_image(SPRITE_SHEET_IMG, 21, 24, 24, 5, BLACK), get_image(SPRITE_SHEET_IMG, 22, 24, 24, 5, BLACK), get_image(SPRITE_SHEET_IMG, 23, 24, 24, 5, BLACK)]




# Handles surface drawings
def draw_screen(dino, is_running, frame_pos):
    WIN.blit(BG_IMAGE, (0, 0))

    # Checks if the run key is pressed
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_d]:
        is_running = True

    # Calls running animation if run key is pressed
    action = run(frames_run_R, dino, is_running, frame_pos)

    pygame.display.update()
    return action




# Handles the running animation
def run(frames_run_R, dino, is_running, frame_pos):
    if is_running and frame_pos < 9:
        WIN.blit(frames_run_R[frame_pos], (dino.x, dino.y))
        dino.x += DINO_VEL
        time.sleep(.0525)
        frame_pos += 1
    else:
        WIN.blit(frames_run_R[0], (dino.x, dino.y))

    return frame_pos





# Main game function
def main():

    # Creates a rectangle representing the dino to move the image based on it's position
    dino = pygame.Rect(50, 515, 24, 24)
    clock = pygame.time.Clock()

    # Running animation variables
    is_running = False
    frame_pos = 2
    action = 2

    # Main game loop
    run = True
    while run:
        clock.tick(FPS)

        # Checks if the user quits the program
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Handles surface drawings, returns the frame of the running animation stored in "action"
        action = draw_screen(dino, is_running, frame_pos)
        if action > 8:
            frame_pos = 2
        else:
            frame_pos += 1


if __name__ == "__main__":
    main()
