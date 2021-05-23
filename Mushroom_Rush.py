# Nujabes counter: 2
import pygame
import os
import time
pygame.mixer.init()

# Window information
WIDTH, HEIGHT = 1200, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
BG_IMAGE = pygame.transform.scale(pygame.image.load(
    os.path.join("Assets", "forest.png")), (WIDTH, HEIGHT))
BLACK = (0, 0, 0)
DINO_VEL = 25
FPS = 60


# Assets
SPRITE_SHEET_IMG = pygame.image.load(
    os.path.join("Assets", "dino_sheets", "doux.png"))
FOOTSTEPS = pygame.mixer.Sound(os.path.join("Assets", "foot1.wav"))
MUSIC = pygame.mixer.Sound(os.path.join("Assets", "Mushroom_Rush_Theme.mp3"))


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


# Removes black box around image
def del_black(img):
    img.set_colorkey(BLACK)
    return img


# All running frames in a list with 8 in total. 0 Being the Standing position
frames_run_R = [get_image(SPRITE_SHEET_IMG, 0, 24, 24, 5, BLACK), get_image(SPRITE_SHEET_IMG, 16, 24, 24, 5, BLACK), get_image(SPRITE_SHEET_IMG, 17, 24, 24, 5, BLACK),
                get_image(SPRITE_SHEET_IMG, 18, 24, 24, 5, BLACK), get_image(
    SPRITE_SHEET_IMG, 19, 24, 24, 5, BLACK), get_image(SPRITE_SHEET_IMG, 20, 24, 24, 5, BLACK),
    get_image(SPRITE_SHEET_IMG, 21, 24, 24, 5, BLACK), get_image(SPRITE_SHEET_IMG, 22, 24, 24, 5, BLACK), get_image(SPRITE_SHEET_IMG, 23, 24, 24, 5, BLACK)]

frames_run_L = [pygame.transform.flip(frames_run_R[0], True, False), pygame.transform.flip(frames_run_R[1], True, False), pygame.transform.flip(frames_run_R[2], True, False),
                pygame.transform.flip(frames_run_R[3], True, False), pygame.transform.flip(frames_run_R[4], True, False), pygame.transform.flip(
                    frames_run_R[5], True, False), pygame.transform.flip(frames_run_R[6], True, False),
                pygame.transform.flip(frames_run_R[7], True, False), pygame.transform.flip(frames_run_R[8], True, False)]


# Idle animation frames
frames_idle = [get_image(SPRITE_SHEET_IMG, 0, 24, 24, 5, BLACK), get_image(SPRITE_SHEET_IMG, 1, 24, 24, 5, BLACK), get_image(
    SPRITE_SHEET_IMG, 2, 24, 24, 5, BLACK), get_image(SPRITE_SHEET_IMG, 3, 24, 24, 5, BLACK)]
frames_idle_LEFT = [pygame.transform.flip(get_image(SPRITE_SHEET_IMG, 0, 24, 24, 5, BLACK), True, False), pygame.transform.flip(get_image(SPRITE_SHEET_IMG, 1, 24, 24, 5, BLACK), True, False),
                    pygame.transform.flip(get_image(SPRITE_SHEET_IMG, 2, 24, 24, 5, BLACK), True, False), pygame.transform.flip(get_image(SPRITE_SHEET_IMG, 3, 24, 24, 5, BLACK), True, False)]


# Initiate idle animation
def idle_init_R(frames_idle, dino, idle_pos):
    print("idle")
    if idle_pos <= 3:
        WIN.blit(frames_idle[idle_pos], (dino.x, dino.y))
    time.sleep(.0525)
    pygame.display.update()


def idle_init_L(frames_idle_LEFT, dino, idle_pos):
    print("idle")
    if idle_pos <= 3:
        WIN.blit(del_black(frames_idle_LEFT[idle_pos]), (dino.x, dino.y))
    time.sleep(.0525)
    pygame.display.update()


# Handles surface drawings
def draw_screen(dino, is_running_R, frame_pos, is_running_L, face_left, face_right, frames_idle, idle_pos):
    WIN.blit(BG_IMAGE, (0, 0))

    # Checks if the RIGHT run key is pressed
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_d]:
        is_running_R = True
        face_right.append("1")
        face_left.clear()

    # Checks if the LEFT run key is pressed
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_a]:
        is_running_L = True
        face_left.append("1")

    # Calls running animation if run key is pressed
    returns = run(frames_run_R, dino, is_running_R, frame_pos,
                  is_running_L, face_left, face_right, idle_pos)

    pygame.display.update()
    return returns


# Handles the running animation
def run(frames_run_R, dino, is_running_R, frame_pos, is_running_L, face_left, face_right, idle_pos):

    # IF RUNNING AT ALL
    if is_running_L or is_running_R:
        print("running")

        # Running right
        if is_running_R and frame_pos < 9:
            WIN.blit(frames_run_R[frame_pos], (dino.x, dino.y))

            # Boundary control
            if dino.x < 1075:
                dino.x += DINO_VEL

            pygame.display.update()
            time.sleep(.0525)
            frame_pos += 1

        # Running left
        elif is_running_L and frame_pos < 9:
            WIN.blit(del_black(frames_run_L[frame_pos]), (dino.x, dino.y))

            # Boundary control
            if dino.x > 0:
                dino.x -= DINO_VEL
            time.sleep(.0525)
            pygame.display.update()
            frame_pos += 1

    # IF NOT RUNNING STAR IDLE ANIMATION
    elif len(face_left) > 0:
        face_right.clear()
        idle_init_L(frames_idle_LEFT, dino, idle_pos)
        idle_pos += 1

    elif len(face_right) > 0:
        face_left.clear()
        idle_init_R(frames_idle, dino, idle_pos)
        idle_pos += 1

    returns = (frame_pos, idle_pos)
    return returns


face_right = []
face_left = []
# Main game function


def main():
    MUSIC.play()

    # Creates a rectangle representing the dino to move the image based on it's position
    dino = pygame.Rect(50, 515, 24, 24)
    clock = pygame.time.Clock()

    # Running animation variables
    is_running_R = False
    is_running_L = False
    frame_pos = 2
    action = 2
    idle_pos = 0

    # Main game loop
    run = True
    while run:
        clock.tick(FPS)

        #idle_init(frames_idle, dino, idle_pos, is_running_L, is_running_R)

        # Checks if the user quits the program
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Handles surface drawings, returns the frame of the running animation stored in "action"
        returns = draw_screen(dino, is_running_R, frame_pos,
                              is_running_L, face_left, face_right, frames_idle, idle_pos)
        if returns[0] > 8:
            frame_pos = 2
        else:
            frame_pos += 1

        if returns[1] > 3:
            idle_pos = 0
        else:
            idle_pos += 1


if __name__ == "__main__":
    main()
