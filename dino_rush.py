# Nujabes counter:
import pygame
import os
import time
import random
pygame.font.init()
pygame.mixer.init()

# Window information
WIDTH, HEIGHT = 1200, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
BG_IMAGE = pygame.transform.scale(pygame.image.load(
    os.path.join("Assets", "forest.png")), (WIDTH, HEIGHT))
BLACK = (0, 0, 0)
DINO_VEL = 30
FPS = 60
HEALTH_FONT = pygame.font.SysFont("comicsans", 50)
LOSE_FONT = pygame.font.SysFont("comicsans", 130)
SPEAR_W, SPEAR_H = 40, 180
SPEAR_HIT = pygame.USEREVENT + 1


# Assets
SPRITE_SHEET_IMG = pygame.image.load(
    os.path.join("Assets", "dino_sheets", "doux.png"))
FOOTSTEPS = pygame.mixer.Sound(os.path.join("Assets", "foot1.wav"))
MUSIC = pygame.mixer.Sound(os.path.join("Assets", "Mushroom_Rush_Theme.mp3"))
SPEAR_IMG = pygame.transform.scale(pygame.transform.rotate(pygame.image.load(
    os.path.join("Assets", "spear_1.png")), 270), (SPEAR_W, SPEAR_H))
SPEAR_IMG2 = pygame.transform.scale(pygame.transform.rotate(pygame.image.load(
    os.path.join("Assets", "spear_1.png")), 270), (SPEAR_W, SPEAR_H))
SPEAR_IMG3 = pygame.transform.scale(pygame.transform.rotate(pygame.image.load(
    os.path.join("Assets", "spear_1.png")), 270), (SPEAR_W, SPEAR_H))
SPEAR_IMG4 = pygame.transform.scale(pygame.transform.rotate(pygame.image.load(
    os.path.join("Assets", "spear_2.png")), 270), (SPEAR_W, SPEAR_H))
blood_img = [pygame.transform.scale(pygame.image.load(os.path.join("Assets", "blood1.png")), (75, 75)), pygame.transform.scale(pygame.image.load(
    os.path.join("Assets", "blood2.png")), (77, 77)), pygame.transform.scale(pygame.image.load(os.path.join("Assets", "blood3.png")), (80, 80))]
ROCKS_IMG = [pygame.image.load(os.path.join("Assets", "rock1.png")), (pygame.image.load(os.path.join("Assets", "rock2.png")))]
FART = pygame.mixer.Sound(os.path.join("Assets", "fart.mp3"))




# Returns sprites image
def get_image(sheet, frame, width, height, scale, color):

    # Create a new surface for the sprites to be drawn onto
    image = pygame.Surface((width, height)).convert_alpha()

    # Blit the sprite sheet on the surface that was just created, but just a cutout of a single frame
    image.blit(sheet, (0, 0), ((frame * width), 0, width, height))

    # Scale the entire surface with the sprite already drawn onto it
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey(color)
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


# Rock sprites
rocks = [get_image(ROCKS_IMG[0], 0, 110, 85, 1, (255, 255, 255)), get_image(ROCKS_IMG[1], 0, 119, 95, 1, (255, 255, 255))]


# Initiate idle animation
def idle_init_R(frames_idle, dino, idle_pos):
    if idle_pos <= 3:
        WIN.blit(frames_idle[idle_pos], (dino.x, dino.y))
    time.sleep(.0525)


def idle_init_L(frames_idle_LEFT, dino, idle_pos):
    if idle_pos <= 3:
        WIN.blit(del_black(frames_idle_LEFT[idle_pos]), (dino.x, dino.y))
    time.sleep(.0525)




def draw_rocks(rocks, rock1, rock2, dino):
    if dino.x != 400:
        rock1.y += 40
        WIN.blit(rocks[0], (rock1.x, rock1.y))
    if rock1.y > HEIGHT:
        rock1.y = -777
        rock1.x = random.randint(100, WIDTH/2)



# Handles surface drawings
def draw_screen(dino, is_running_R, frame_pos, is_running_L, face_left, face_right, frames_idle, idle_pos, dino_health, spear, SPEAR_IMG, spear2, spear3, spear4, rocks, rock1, rock2):
    WIN.blit(BG_IMAGE, (0, 0))


    # Spear
    draw_spear(spear, SPEAR_IMG, dino, spear2, spear3, spear4)

    # Health
    health_text = HEALTH_FONT.render(
        "Health: " + str(dino_health), 1, (33, 75, 69))
    WIN.blit(health_text, (10, 5))

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



    return returns


# Handles the running animation
def run(frames_run_R, dino, is_running_R, frame_pos, is_running_L, face_left, face_right, idle_pos):

    # IF RUNNING AT ALL
    if is_running_L or is_running_R:

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


def draw_spear(spear, SPEAR_IMG, dino, spear2, spear3, spear4):
    if spear.y != HEIGHT * 3 and dino.x != 400:
        spear.y += 40
        spear2.y += 45
        spear3.y += 46
        spear4.y += 40
        WIN.blit(SPEAR_IMG, (spear.x, spear.y))
        WIN.blit(SPEAR_IMG2, (spear2.x, spear2.y))
        WIN.blit(SPEAR_IMG3, (spear3.x, spear3.y))
        WIN.blit(SPEAR_IMG4, (spear4.x, spear4.y))
    if spear.y > HEIGHT:
        spear.y = -450
        spear.x = random.randint(100, WIDTH/2)
    if spear2.y > HEIGHT:
        spear2.y = -250
        spear2.x = random.randint(100, WIDTH/2)
    if spear3.y > HEIGHT:
        spear3.y = -150
        spear3.x = random.randint(WIDTH/2, WIDTH - 50)
    if spear4.y > HEIGHT:
        spear4.y = -350
        spear4.x = random.randint(WIDTH/2, WIDTH - 50)


def draw_blood(blood, dino):
    WIN.blit(blood_img[0], (dino.x, dino.y - 48))


face_right = []
face_left = []
# Main game function
def main():
    MUSIC.play()

    # Creates a rectangle representing the dino to move the image based on it's position
    dino = pygame.Rect(400, 520, 100, 75)
    spear = pygame.Rect(250, -1000, SPEAR_W / 2, SPEAR_H)
    spear2 = pygame.Rect(700, -8000, SPEAR_W / 2, SPEAR_H)
    spear3 = pygame.Rect(400, -1200, SPEAR_W / 2, SPEAR_H)
    spear4 = pygame.Rect(500, -1700, SPEAR_W / 2, SPEAR_H)
    clock = pygame.time.Clock()
    rock1 = pygame.Rect(350, -1000, 110, 85)
    rock2 = pygame.Rect(350, -1000, 119, 95)

    # Running animation variables
    is_running_R = False
    is_running_L = False
    frame_pos = 2
    action = 2
    idle_pos = 0
    dino_health = 15
    blood_pos = 0
    spear_ct = 0

    # Main game loop
    run = True
    while dino_health != 0:
        clock.tick(FPS)

        # Spear collision
        if dino.colliderect(spear):
            pygame.event.post(pygame.event.Event(SPEAR_HIT))

        if dino.colliderect(spear2):
            pygame.event.post(pygame.event.Event(SPEAR_HIT))
            spear_ct += 2
        if dino.colliderect(spear3):
            pygame.event.post(pygame.event.Event(SPEAR_HIT))
            spear_ct += 3
        if dino.colliderect(spear4):
            pygame.event.post(pygame.event.Event(SPEAR_HIT))
            spear_ct += 4



        # Checks if the user quits the program
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            # Spear collision
            if event.type == SPEAR_HIT and dino_health >= 1 and spear_ct == 0:
                dino_health -= 1
                if blood_pos < 3:
                    WIN.blit(blood_img[blood_pos], (spear.x -
                             20, spear.y + spear.height / 2 + 25))
                    blood_pos += 1
                    pygame.display.update()
                if blood_pos == 3:
                    spear.y = -450
                    spear.x = random.randint(100, WIDTH -100)
                    blood_pos = 0


            if event.type == SPEAR_HIT and dino_health >= 1 and spear_ct == 2:
                dino_health -= 1
                if blood_pos < 3:
                    WIN.blit(blood_img[blood_pos], (spear2.x -
                             20, spear2.y + spear2.height / 2 + 25))
                    blood_pos += 1
                    pygame.display.update()
                if blood_pos == 3:
                    spear2.y = -450
                    spear2.x = random.randint(100, WIDTH -100)
                    blood_pos = 0
                spear_ct -= 2

            if event.type == SPEAR_HIT and dino_health >= 1 and spear_ct == 3:
                dino_health -= 1
                if blood_pos < 3:
                    WIN.blit(blood_img[blood_pos], (spear3.x -
                             20, spear3.y + spear3.height / 2 + 25))
                    blood_pos += 1
                    pygame.display.update()
                if blood_pos == 3:
                    spear3.y = -450
                    spear3.x = random.randint(100, WIDTH -100)
                    blood_pos = 0
                spear_ct -= 3


            if event.type == SPEAR_HIT and dino_health >= 1 and spear_ct == 4:
                dino_health -= 1
                if blood_pos < 3:
                    WIN.blit(blood_img[blood_pos], (spear4.x -
                             20, spear4.y + spear4.height / 2 + 25))
                    blood_pos += 1
                    pygame.display.update()
                if blood_pos == 3:
                    spear4.y = -450
                    spear4.x = random.randint(100, WIDTH -100)
                    blood_pos = 0
                spear_ct -= 4



        # Handles surface drawings, returns the frame of the running animation stored in "action"
        returns = draw_screen(dino, is_running_R, frame_pos,
                              is_running_L, face_left, face_right, frames_idle, idle_pos, dino_health, spear, SPEAR_IMG, spear2, spear3, spear4, rocks, rock1, rock2)
        if returns[0] > 8:
            frame_pos = 2
        else:
            frame_pos += 1

            if returns[1] > 3:
                idle_pos = 0
            else:
                idle_pos += 1
        pygame.display.update()

    # If you lose
    FART.play()
    MUSIC.stop()
    LOSE_TEXT = LOSE_FONT.render(
        "RIPPERINO", 1, (BLACK))
    draw_screen(dino, is_running_R, frame_pos, is_running_L, face_left, face_right, frames_idle, idle_pos, dino_health, spear, SPEAR_IMG, spear2, spear3, spear4, rocks, rock1, rock2)
    WIN.blit(LOSE_TEXT, (WIDTH/2 - 265, HEIGHT/2 - 75))
    pygame.display.update()
    time.sleep(2)


if __name__ == "__main__":
    main()
