import pygame
import sys
import os


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class SpriteSheet:

    def __init__(self, path):

        self.sheet = pygame.image.load(
            resource_path(path)
        ).convert_alpha()

    def get_image(self, x, y, width, height):

        image = pygame.Surface(
            (width, height),
            pygame.SRCALPHA
        )

        image.blit(
            self.sheet,
            (0, 0),
            (x, y, width, height)
        )

        return image
    

def load_animation(
    sheet,
    frame_width,
    frame_height,
    frame_count,
    scale=1,
    row=0
):

    frames = []

    for i in range(frame_count):

        frame = sheet.get_image(

            i * frame_width,
            row * frame_height,

            frame_width,
            frame_height
        )

        scaled_width = int(frame_width * scale)
        scaled_height = int(frame_height * scale)

        frame = pygame.transform.scale(
            frame,
            (scaled_width, scaled_height)
        )

        frames.append(frame)

    return frames


def flip_animation(frames):
    return [
        pygame.transform.flip(frame, True, False)
        for frame in frames
    ]


pygame.init()

WIDTH = 1280
HEIGHT = 720

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Demo")

if not pygame.mixer.get_init():
    pygame.mixer.init()

pygame.mixer.music.load(
    resource_path("week12/assets/sound/rain.mp3")
)
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

fade_surface = pygame.Surface((WIDTH, HEIGHT))
fade_surface.fill((0, 0, 0))

clock = pygame.time.Clock()
fps_font = pygame.font.Font(None, 28)
ending_font = pygame.font.Font(None, 96)

BG_COLOR = (18, 18, 18)
GROUND_COLOR = (45, 45, 45)
PLATFORM_COLOR = (90, 90, 90)
WALL_COLOR = (130, 130, 130)
PLAYER_COLOR = (220, 220, 220)
ENEMY_COLOR = (170, 170, 170)
BOSS_COLOR = (150, 40, 40)
BOSS_WALL_COLOR = (220, 30, 30)
ENEMY3_COLOR = (180, 80, 210)
ENEMY4_COLOR = (210, 120, 70)

CHAPTER3_MINIBOSS_SPAWN_X = 18000
CHAPTER3_MINIBOSS_SPAWN_Y = 400
CHAPTER3_MINIBOSS_TRIGGER_X = 17000
CHAPTER3_MINIBOSS_LEFT_WALL_X = 16600
CHAPTER3_MINIBOSS_RIGHT_WALL_X = 18900

CHAPTER4_BOSS_SPAWN_X = 13000
CHAPTER4_BOSS_SPAWN_Y = 400
CHAPTER4_BOSS_TRIGGER_X = 11000

MINI3_SPAWN_X = 5000
MINI3_SPAWN_Y = 440
MINI3_TRIGGER_X = 4300
MINI3_LEFT_WALL_X = 4000
MINI3_RIGHT_WALL_X = 6000

ENEMY3_BOX_IMAGE = pygame.Surface((75, 90), pygame.SRCALPHA)
ENEMY3_BOX_IMAGE.fill(ENEMY3_COLOR)
ENEMY3_ANIMATIONS = {
    "idle": [ENEMY3_BOX_IMAGE]
}
ENEMY3_FLIPPED_ANIMATIONS = {
    "idle": [ENEMY3_BOX_IMAGE]
}

ENEMY4_BOX_IMAGE = pygame.Surface((150, 60), pygame.SRCALPHA)
ENEMY4_BOX_IMAGE.fill(ENEMY4_COLOR)
ENEMY4_ANIMATIONS = {
    "idle": [ENEMY4_BOX_IMAGE]
}
ENEMY4_FLIPPED_ANIMATIONS = {
    "idle": [ENEMY4_BOX_IMAGE]
}

BOSS_BOX_IMAGE = pygame.Surface((70, 180), pygame.SRCALPHA)
BOSS_BOX_IMAGE.fill(BOSS_COLOR)
BOSS_ANIMATIONS = {
    "idle": [BOSS_BOX_IMAGE]
}
BOSS_FLIPPED_ANIMATIONS = {
    "idle": [BOSS_BOX_IMAGE]
}

current_chapter = 1

CHAPTER_WIDTHS = {
    1: 12000,
    2: 6000,
    3: 20000,
    4: 14000,
}

CHAPTER_SPAWN = {

    1: {
        "left": 200,
        "right": 11700,
    },

    2: {
        "left": 200,
        "right": 5700,
    },

    3: {
        "left": 200,
        "right": 19700,
    },
    4: {
        "left": 200,
        "right": 13700,
    }
}

WORLD_WIDTH = CHAPTER_WIDTHS[current_chapter]

ground = pygame.Rect(
    0,
    HEIGHT - 80,
    WORLD_WIDTH,
    80
)

player_idle_sheet = SpriteSheet("week12/assets/cha/ryo/ryo_idle.png")

player_run_sheet = SpriteSheet("week12/assets/cha/ryo/ryo_run.png")

player_attack_sheet = SpriteSheet("week12/assets/cha/ryo/ryo_attack.png")

player_air_attack_sheet = SpriteSheet("week12/assets/cha/ryo/ryo_jump_attack.png")

player_jump_sheet = SpriteSheet("week12/assets/cha/ryo/ryo_jump.png")

player_knockback_sheet = SpriteSheet("week12/assets/cha/ryo/ryo_knockback.png")

down_frame = player_jump_sheet.get_image(
    128, 0,
    128, 128
)

down_frame = pygame.transform.scale(
    down_frame,
    (
        int(128 * 3.5),
        int(128 * 3.5)
    )
)

player_animations = {

    "idle": load_animation(
        player_idle_sheet,
        128,
        128,
        4,
        scale=3.5
    ),

    "run": load_animation(
        player_run_sheet,
        128,
        128,
        8,
        scale=3.5
    ),

    "attack" : load_animation(
        player_attack_sheet,
        128,
        128,
        8,
        scale = 3.5
    ),

    "jump": load_animation(
        player_jump_sheet,
        128,
        128,
        1,
        scale=3.5,
    ),

    "down": [down_frame],

    "air_attack": load_animation(
        player_air_attack_sheet,
        128,
        128,
        4,
        scale=3.5,
    ),

    "knockback": load_animation(
        player_knockback_sheet,
        128,
        128,
        2,
        scale=3.5,
    ),
}

player_flipped_animations = {
    name: flip_animation(frames)
    for name, frames in player_animations.items()
}

enemy1_idle_sheet = SpriteSheet("week12/assets/cha/en1/Idle.png")
enemy1_move_sheet = SpriteSheet("week12/assets/cha/en1/Move.png")
enemy1_attack_sheet = SpriteSheet("week12/assets/cha/en1/Attack.png")
enemy1_death_sheet = SpriteSheet("week12/assets/cha/en1/Death.png")

enemy1_animations = {
    "idle": load_animation(
        enemy1_idle_sheet,
        64,
        64,
        6,
        scale=3.0
    ),
    "move": load_animation(
        enemy1_move_sheet,
        64,
        64,
        6,
        scale=3.0
    ),
    "attack": load_animation(
        enemy1_attack_sheet,
        64,
        64,
        9,
        scale=3.0
    ),
    "death": load_animation(
        enemy1_death_sheet,
        64,
        64,
        5,
        scale=3.0
    ),
}

enemy1_flipped_animations = {
    name: flip_animation(frames)
    for name, frames in enemy1_animations.items()
}

enemy2_idle_sheet = SpriteSheet("week12/assets/cha/en2/Idle.png")
enemy2_move_sheet = SpriteSheet("week12/assets/cha/en2/Move.png")
enemy2_death_sheet = SpriteSheet("week12/assets/cha/en2/Death.png")

enemy2_animations = {
    "idle": load_animation(
        enemy2_idle_sheet,
        64,
        64,
        6,
        scale=3.0
    ),
    "move": load_animation(
        enemy2_move_sheet,
        64,
        64,
        6,
        scale=3.0
    ),
    "death": load_animation(
        enemy2_death_sheet,
        64,
        64,
        10,
        scale=3.0
    ),
}

enemy2_flipped_animations = {
    name: flip_animation(frames)
    for name, frames in enemy2_animations.items()
}

miniboss1_idle_sheet = SpriteSheet(
    "week12/assets/cha/mini1/idle.png"
)
miniboss1_move_sheet = SpriteSheet(
    "week12/assets/cha/mini1/move.png"
)
miniboss1_attack_sheet = SpriteSheet(
    "week12/assets/cha/mini1/attack.png"
)
miniboss1_death_sheet = SpriteSheet(
    "week12/assets/cha/mini1/death.png"
)

miniboss1_animations = {
    "idle": load_animation(
        miniboss1_idle_sheet,
        196,
        144,
        10,
        scale=3.5
    ),
    "move": load_animation(
        miniboss1_move_sheet,
        196,
        144,
        8,
        scale=3.5
    ),
    "attack": load_animation(
        miniboss1_attack_sheet,
        196,
        144,
        17,
        scale=3.5
    ),
    "death": load_animation(
        miniboss1_death_sheet,
        196,
        144,
        7,
        scale=3.5
    ),
}

miniboss1_flipped_animations = {
    name: flip_animation(frames)
    for name, frames in miniboss1_animations.items()
}

miniboss2_idle_sheet = SpriteSheet("week12/assets/cha/mini2/Idle.png")
miniboss2_move_sheet = SpriteSheet("week12/assets/cha/mini2/Move.png")
miniboss2_attack1_sheet = SpriteSheet("week12/assets/cha/mini2/Attack1.png")
miniboss2_attack2_sheet = SpriteSheet("week12/assets/cha/mini2/Attack2.png")
miniboss2_death_sheet = SpriteSheet("week12/assets/cha/mini2/Death.png")

miniboss2_animations = {
    "idle": load_animation(
        miniboss2_idle_sheet,
        192,
        144,
        10,
        scale=3.5
    ),

    "move": load_animation(
        miniboss2_move_sheet,
        192,
        144,
        8,
        scale=3.5
    ),

    "attack1": load_animation(
        miniboss2_attack1_sheet,
        192,
        144,
        16,
        scale=3.5
    ),

    "attack2": load_animation(
        miniboss2_attack2_sheet,
        192,
        144,
        10,
        scale=3.5
    ),

    "death": load_animation(
        miniboss2_death_sheet,
        192,
        144,
        6,
        scale=3.5
    ),
}

miniboss2_flipped_animations = {
    name: flip_animation(frames)
    for name, frames in miniboss2_animations.items()
}

mini3_idle_sheet = SpriteSheet(
    "week12/assets/cha/mini3/idle.png"
)
mini3_move_sheet = SpriteSheet(
    "week12/assets/cha/mini3/move.png"
)
mini3_attack_sheet = SpriteSheet(
    "week12/assets/cha/mini3/attack.png"
)
mini3_death_sheet = SpriteSheet(
    "week12/assets/cha/mini3/death.png"
)

mini3_animations = {
    "idle": load_animation(
        mini3_idle_sheet,
        192,
        128,
        10,
        scale=3.5
    ),
    "move": load_animation(
        mini3_move_sheet,
        192,
        128,
        12,
        scale=3.5
    ),
    "attack": load_animation(
        mini3_attack_sheet,
        192,
        128,
        11,
        scale=3.5
    ),
    "death": load_animation(
        mini3_death_sheet,
        192,
        128,
        17,
        scale=3.5
    ),
}

mini3_flipped_animations = {
    name: flip_animation(frames)
    for name, frames in mini3_animations.items()
}

chapter4_boss_idle_sheet = SpriteSheet(
    "week12/assets/cha/boss/Idle.png"
)
chapter4_boss_move_sheet = SpriteSheet(
    "week12/assets/cha/boss/Move.png"
)
chapter4_boss_attack1_sheet = SpriteSheet(
    "week12/assets/cha/boss/Attack1.png"
)
chapter4_boss_attack2_sheet = SpriteSheet(
    "week12/assets/cha/boss/Attack2.png"
)
chapter4_boss_death_sheet = SpriteSheet(
    "week12/assets/cha/boss/Death.png"
)
chapter4_boss_waa_sheet = SpriteSheet(
    "week12/assets/cha/boss/waa.png"
)

chapter4_boss_animations = {
    "idle": load_animation(
        chapter4_boss_idle_sheet,
        256,
        160,
        9,
        scale=3.5
    ),
    "move": load_animation(
        chapter4_boss_move_sheet,
        256,
        160,
        10,
        scale=3.5
    ),
    "attack1": load_animation(
        chapter4_boss_attack1_sheet,
        256,
        160,
        13,
        scale=3.5
    ),
    "attack2": load_animation(
        chapter4_boss_attack2_sheet,
        256,
        160,
        15,
        scale=3.5
    ),
    "death": load_animation(
        chapter4_boss_death_sheet,
        256,
        160,
        22,
        scale=3.5
    ),
    "waa": load_animation(
        chapter4_boss_waa_sheet,
        256,
        160,
        6,
        scale=3.5
    ),
}

chapter4_boss_flipped_animations = {
    name: flip_animation(frames)
    for name, frames in chapter4_boss_animations.items()
}

forest1 = pygame.image.load(
    resource_path("week12/assets/background/1.png")
).convert_alpha()

forest2 = pygame.image.load(
    resource_path("week12/assets/background/2.png")
).convert_alpha()

forest3 = pygame.image.load(
    resource_path("week12/assets/background/3.png")
).convert_alpha()

forest4 = pygame.image.load(
    resource_path("week12/assets/background/4.png")
).convert_alpha()

fog = pygame.image.load(
    resource_path("week12/assets/background/5.png")
).convert_alpha()

forest1 = pygame.transform.scale(forest1, (620, 320))

forest2 = pygame.transform.scale(forest2, (620, 320))

forest3 = pygame.transform.scale(forest3, (620, 320))

forest4 = pygame.transform.scale(forest4, (620, 320))

BACKGROUND_SIZE = (1448, 820)

forest1 = pygame.transform.scale(forest1, BACKGROUND_SIZE)

forest2 = pygame.transform.scale(forest2, BACKGROUND_SIZE)

forest3 = pygame.transform.scale(forest3, BACKGROUND_SIZE)

forest4 = pygame.transform.scale(forest4, BACKGROUND_SIZE)

fog = pygame.transform.scale(fog, BACKGROUND_SIZE)

def enemy1(x, y):

    collision_rect = pygame.Rect(
        x,
        y,
        64,
        96,
    )

    hurtbox = collision_rect.copy()

    return {
        "type": "enemy1",
        "rect": collision_rect,
        "hurtbox": hurtbox,
        "sprite_offset_x": -64,
        "sprite_offset_y": -48,
        "animations": enemy1_animations,
        "flipped_animations": enemy1_flipped_animations,
        "faces_right": True,
        "current_animation": "idle",
        "frame_index": 0,
        "animation_speed": 0.14,
        "health": 40,
        "speed": 4,
        "damage": 10,
        "direction": 1,
        "detect_range": 500,
        "aggro": False,
        "chase_range": 800,
        "state": "idle",
        "enemy1_attack_range": 110,
        "enemy1_attack_damage": 10,
        "enemy1_attack_has_hit": False,
        "enemy1_attack_hitbox": None,
        "enemy1_attack_hitbox_width": 120,
        "enemy1_attack_hitbox_height": 100,
        "enemy1_attack_right_x_offset": 45,
        "enemy1_attack_left_x_offset": -100,
        "enemy1_attack_y_offset": 10,
        "enemy1_recovery_timer": 0,
        "enemy1_recovery_duration": 30,
        "dead": False,
        "death_finished": False,
        "vel_x": 0,
        "vel_y": 0,
        "hitstun": 0,
        "gravity": 0.35,
        "on_ground": False,
    }

def enemy2(x, y):

    collision_rect = pygame.Rect(
        x + 40,
        y + 45,
        50,
        70,
    )

    hurtbox = pygame.Rect(
        x + 15,
        y + 10,
        85,
        100,
    )

    return {
        "type": "enemy2",
        "rect": collision_rect,
        "hurtbox": hurtbox,
        "sprite_offset_x": -70,
        "sprite_offset_y": -65,
        "animations": enemy2_animations,
        "flipped_animations": enemy2_flipped_animations,
        "faces_right": True,
        "current_animation": "idle",
        "frame_index": 0,
        "animation_speed": 0.14,
        "health": 20,
        "speed":2,
        "damage": 10,
        "direction": 1,
        "start_x": x,
        "patrol_range": 350,
        "detect_range": 350,
        "aggro": False,
        "chase_range": 1200,
        "velocity_x": 0,
        "velocity_y": 0,
        "hitstun": 0,
        "dead": False,
        "death_finished": False,
        "death_velocity_y": 0,
        "death_gravity": 0.8,
    }


def enemy3(x, y):

    enemy3_hitbox_offset_x = 18
    enemy3_hitbox_offset_y = 18
    enemy3_hitbox_width = 40
    enemy3_hitbox_height = 60

    enemy3_hurtbox_offset_x = 0
    enemy3_hurtbox_offset_y = 0
    enemy3_hurtbox_width = 75
    enemy3_hurtbox_height = 90

    collision_rect = pygame.Rect(
        x + enemy3_hitbox_offset_x,
        y + enemy3_hitbox_offset_y,
        enemy3_hitbox_width,
        enemy3_hitbox_height,
    )

    hurtbox = pygame.Rect(
        x + enemy3_hurtbox_offset_x,
        y + enemy3_hurtbox_offset_y,
        enemy3_hurtbox_width,
        enemy3_hurtbox_height,
    )

    return {
        "type": "enemy3",
        "x": float(collision_rect.x),
        "y": float(collision_rect.y),
        "rect": collision_rect,
        "hurtbox": hurtbox,
        "sprite_offset_x": -enemy3_hitbox_offset_x,
        "sprite_offset_y": -enemy3_hitbox_offset_y,
        "hurtbox_offset_x": (
            enemy3_hurtbox_offset_x
            - enemy3_hitbox_offset_x
        ),
        "hurtbox_offset_y": (
            enemy3_hurtbox_offset_y
            - enemy3_hitbox_offset_y
        ),
        "animations": ENEMY3_ANIMATIONS,
        "flipped_animations": ENEMY3_FLIPPED_ANIMATIONS,
        "current_animation": "idle",
        "frame_index": 0,
        "animation_speed": 0.04,
        "health": 10,
        "speed": 14,
        "damage": 15,
        "direction": 1,
        "detect_range": 400,
        "aggro": False,
        "chase_range": 1000,
        "velocity_x": 0,
        "velocity_y": 0,
        "hitstun": 0,
        "state": "idle",
        "pattern_timer": 0,
        "dash_timer": 0,
        "dash_x": 0,
        "dash_y": 0,
    }


def enemy4(x, y):

    enemy4_hitbox_offset_x = 0
    enemy4_hitbox_offset_y = 0
    enemy4_hitbox_width = 150
    enemy4_hitbox_height = 60

    enemy4_hurtbox_offset_x = 0
    enemy4_hurtbox_offset_y = 0
    enemy4_hurtbox_width = 150
    enemy4_hurtbox_height = 60

    collision_rect = pygame.Rect(
        x + enemy4_hitbox_offset_x,
        y + enemy4_hitbox_offset_y,
        enemy4_hitbox_width,
        enemy4_hitbox_height,
    )

    hurtbox = pygame.Rect(
        x + enemy4_hurtbox_offset_x,
        y + enemy4_hurtbox_offset_y,
        enemy4_hurtbox_width,
        enemy4_hurtbox_height,
    )

    return {
        "type": "enemy4",
        "rect": collision_rect,
        "hurtbox": hurtbox,
        "sprite_offset_x": -enemy4_hitbox_offset_x,
        "sprite_offset_y": -enemy4_hitbox_offset_y,
        "hurtbox_offset_x": (
            enemy4_hurtbox_offset_x
            - enemy4_hitbox_offset_x
        ),
        "hurtbox_offset_y": (
            enemy4_hurtbox_offset_y
            - enemy4_hitbox_offset_y
        ),
        "animations": ENEMY4_ANIMATIONS,
        "flipped_animations": ENEMY4_FLIPPED_ANIMATIONS,
        "current_animation": "idle",
        "frame_index": 0,
        "animation_speed": 0,
        "health": 30,
        "speed": 7,
        "damage": 20,
        "direction": 1,
        "start_x": x,
        "patrol_range": 500,
        "detect_range": 500,
        "aggro": False,
        "chase_range": 700,
        "vel_x": 0,
        "vel_y": 0,
        "hitstun": 0,
        "gravity": 0.35,
        "on_ground": False,
    }


def miniboss1(x, y):

    collision_rect = pygame.Rect(
        x,
        y,
        130,
        180,
    )

    return {
        "type": "miniboss1",
        "x": float(x),
        "rect": collision_rect,
        "hurtbox": collision_rect.copy(),
        "sprite_offset_x": 0,
        "sprite_offset_y": 0,
        "use_player_style_draw": True,
        "draw_offset_x": 0,
        "draw_offset_y": 115,
        "draw_right_offset_x": 0,
        "draw_left_offset_x": 0,
        "animations": miniboss1_animations,
        "flipped_animations": miniboss1_flipped_animations,
        "faces_right": True,
        "current_animation": "idle",
        "frame_index": 0,
        "animation_speed": 0.12,
        "health": 400,
        "damage": 0,
        "dash_damage": 15,
        "attack_damage": 45,
        "direction": -1,
        "hitstun": 0,
        "active": False,
        "state": "waiting",
        "pattern_timer": 0,
        "dash_timer": 0,
        "dash_speed": 22,
        "slow_move_animation_speed": 0.05,
        "normal_animation_speed": 0.14,
        "attack_has_hit": False,
        "dash_has_hit": False,
        "attack_hitbox": None,
        "attack_hitbox_width": 300,
        "attack_hitbox_height": 180,
        "attack_right_x_offset": 110,
        "attack_left_x_offset": -280,
        "attack_y_offset": 0,
        "dead": False,
        "death_finished": False,
    }


def miniboss2(x, y):

    miniboss2_hitbox_width = 140
    miniboss2_hitbox_height = 240
    miniboss2_animation_speed = 0.14

    mini2_attack1_hitbox_width = 420
    mini2_attack1_hitbox_height = 190
    mini2_attack1_right_x_offset = 0
    mini2_attack1_left_x_offset = -280
    mini2_attack1_hitbox_y_offset = 35

    mini2_attack2_hitbox_width = 260
    mini2_attack2_hitbox_height = 340
    mini2_attack2_right_x_offset = 140
    mini2_attack2_left_x_offset = -260
    mini2_attack2_hitbox_y_offset = -55

    collision_rect = pygame.Rect(
        x,
        y,
        miniboss2_hitbox_width,
        miniboss2_hitbox_height,
    )

    return {
        "type": "miniboss2",
        "rect": collision_rect,
        "hurtbox": collision_rect.copy(),
        "sprite_offset_x": 0,
        "sprite_offset_y": -200,
        "use_player_style_draw": True,
        "draw_offset_x": -110,
        "draw_offset_y": 62,
        "draw_right_offset_x": 220,
        "draw_left_offset_x": 0,
        "animations": miniboss2_animations,
        "flipped_animations": miniboss2_flipped_animations,
        "faces_right": True,
        "current_animation": "idle",
        "frame_index": 0,
        "animation_speed": miniboss2_animation_speed,
        "health": 600,
        "speed": 6,
        "damage": 20,
        "direction": -1,
        "hitstun": 0,
        "active": False,
        "state": "idle",
        "mini2_attack1_cooldown": 0,
        "mini2_attack2_cooldown": 0,
        "mini2_same_attack_cooldown": 260,
        "mini2_recovery_timer": 0,
        "mini2_recovery_duration": 90,
        "mini2_attack_has_hit": False,
        "mini2_attack_hitbox": None,
        "dead": False,
        "death_finished": False,
        "mini2_attack1_range": 430,
        "mini2_attack2_range": 190,
        "keep_distance_min": 230,
        "keep_distance_max": 360,
        "mini2_move_timer": 60,
        "mini2_move_interval": 60,
        "mini2_move_direction": 1,
        "mini2_backstep_speed_ratio": 0.8,
        "mini2_attack1_damage": 30,
        "mini2_attack2_damage": 20,
        "mini2_attack1_hitbox_width": mini2_attack1_hitbox_width,
        "mini2_attack1_hitbox_height": mini2_attack1_hitbox_height,
        "mini2_attack1_right_x_offset": mini2_attack1_right_x_offset,
        "mini2_attack1_left_x_offset": mini2_attack1_left_x_offset,
        "mini2_attack1_hitbox_y_offset": mini2_attack1_hitbox_y_offset,
        "mini2_attack2_hitbox_width": mini2_attack2_hitbox_width,
        "mini2_attack2_hitbox_height": mini2_attack2_hitbox_height,
        "mini2_attack2_right_x_offset": mini2_attack2_right_x_offset,
        "mini2_attack2_left_x_offset": mini2_attack2_left_x_offset,
        "mini2_attack2_hitbox_y_offset": mini2_attack2_hitbox_y_offset,
        "mini2_attack1_knockback": 14,
        "mini2_attack2_knockback": 40,
        "vel_x": 0,
        "vel_y": 0,
        "gravity": 0.35,
        "on_ground": False,
    }


def chapter4_boss(x, y):

    chapter4_boss_hitbox_width = 540
    chapter4_boss_hitbox_height = 180
    chapter4_boss_animation_speed = 0.12

    collision_rect = pygame.Rect(
        x,
        y,
        chapter4_boss_hitbox_width,
        chapter4_boss_hitbox_height,
    )

    return {
        "type": "chapter4_boss",
        "rect": collision_rect,
        "hurtbox": collision_rect.copy(),
        "sprite_offset_x": 0,
        "sprite_offset_y": 0,
        "use_player_style_draw": True,
        "draw_offset_x": 100,
        "draw_offset_y": 40,
        "draw_right_offset_x": 0,
        "draw_left_offset_x": -230,
        "animations": chapter4_boss_animations,
        "flipped_animations": chapter4_boss_flipped_animations,
        "faces_right": True,
        "current_animation": "idle",
        "frame_index": 0,
        "animation_speed": chapter4_boss_animation_speed,
        "health": 600,
        "speed": 4,
        "damage": 0,
        "direction": -1,
        "hitstun": 0,
        "active": False,
        "state": "idle",
        "chapter4_boss_attack1_range": 480,
        "chapter4_boss_attack2_range": 1100,
        "chapter4_boss_attack1_damage": 35,
        "chapter4_boss_attack2_damage": 45,
        "chapter4_boss_attack1_hitbox_width": 500,
        "chapter4_boss_attack1_hitbox_height": 170,
        "chapter4_boss_attack1_right_x_offset": -60,
        "chapter4_boss_attack1_left_x_offset": -480,
        "chapter4_boss_attack1_y_offset": -70,
        "chapter4_boss_attack2_hitbox_width": 500,
        "chapter4_boss_attack2_hitbox_height": 250,
        "chapter4_boss_attack2_right_x_offset": -100,
        "chapter4_boss_attack2_left_x_offset": -460,
        "chapter4_boss_attack2_y_offset": -100,
        "chapter4_boss_attack2_cooldown": 0,
        "chapter4_boss_attack2_cooldown_duration": 900,
        "chapter4_boss_recovery_timer": 0,
        "chapter4_boss_attack1_recovery_duration": 12,
        "chapter4_boss_attack_has_hit": False,
        "chapter4_boss_attack_hitbox": None,
        "chapter4_boss_attack2_launched": False,
        "chapter4_boss_attack2_speed": 12,
        "chapter4_boss_attack2_jump_power": -10,
        "chapter4_boss_next_waa_health": 500,
        "chapter4_boss_waa_knockback": 55,
        "chapter4_boss_waa_knockback_done": False,
        "chapter4_boss_waa_hold_timer": 0,
        "chapter4_boss_waa_hold_duration": 18,
        "dead": False,
        "death_finished": False,
        "vel_x": 0,
        "vel_y": 0,
        "gravity": 0.8,
        "on_ground": False,
    }


def mini3(x, y):

    mini3_hitbox_width = 200
    mini3_hitbox_height = 240
    mini3_animation_speed = 0.12

    mini3_collision_rect = pygame.Rect(
        x,
        y,
        mini3_hitbox_width,
        mini3_hitbox_height,
    )

    return {
        "type": "mini3",
        "rect": mini3_collision_rect,
        "hurtbox": mini3_collision_rect.copy(),
        "sprite_offset_x": 0,
        "sprite_offset_y": 0,
        "use_player_style_draw": True,
        "draw_offset_x": -60,
        "draw_offset_y": 60,
        "draw_right_offset_x": 100,
        "draw_left_offset_x": 0,
        "animations": mini3_animations,
        "flipped_animations": mini3_flipped_animations,
        "faces_right": True,
        "current_animation": "idle",
        "frame_index": 0,
        "animation_speed": mini3_animation_speed,
        "health": 800,
        "speed": 1,
        "damage": 15,
        "direction": -1,
        "hitstun": 0,
        "active": False,
        "aggro": False,
        "state": "idle",
        "mini3_attack_range": 360,
        "mini3_attack_damage": 15,
        "mini3_attack_has_hit": False,
        "mini3_attack_hitbox": None,
        "mini3_attack_recovery_timer": 0,
        "mini3_attack_recovery_duration": 30,
        "mini3_attack_hitbox_width": 300,
        "mini3_attack_hitbox_height": 180,
        "mini3_attack_right_x_offset": 130,
        "mini3_attack_left_x_offset": -240,
        "mini3_attack_y_offset": 60,
        "dead": False,
        "death_finished": False,
        "vel_x": 0,
        "vel_y": 0,
        "gravity": 0.8,
        "on_ground": False,
    }


def load_chapter_1():

    # 플랫폼
    platforms = [
    ]

    # 벽
    walls = [
        pygame.Rect(1300, 500, 120, 140),
        pygame.Rect(2300, 290, 250, 350),
        pygame.Rect(2460, 440, 1200, 200),
        pygame.Rect(3660, 290, 450, 350),
        pygame.Rect(4110, 170, 400, 470),
        pygame.Rect(6800, 490, 2000, 150),
    ]

    bg1_objects = [

        {
            "image": forest1,
            "x": -50,
            "y": -90,
            "w": 1448,
            "h": 820,
            "parallax_x": 0.2,
            "parallax_y": 0.04
        },

        {
            "image": forest1,
            "x": 1395,
            "y": -90,
            "w": 1448,
            "h": 820,
            "parallax_x": 0.2,
            "parallax_y": 0.04
        },

        {
            "image": forest1,
            "x": 2843,
            "y": -90,
            "w": 1448,
            "h": 820,
            "parallax_x": 0.2,
            "parallax_y": 0.04
        },

        {
            "image": forest1,
            "x": 4291,
            "y": -90,
            "w": 1448,
            "h": 820,
            "parallax_x": 0.2,
            "parallax_y": 0.04
        },

        {
            "image": forest1,
            "x": 5739,
            "y": -90,
            "w": 1448,
            "h": 820,
            "parallax_x": 0.2,
            "parallax_y": 0.04
        },


        {
            "image": forest2,
            "x": -50,
            "y": -90,
            "w": 1448,
            "h": 820,
            "parallax_x": 0.25,
            "parallax_y": 0.05
        },

        {
            "image": forest2,
            "x": 1395,
            "y": -90,
            "w": 1448,
            "h": 820,
            "parallax_x": 0.25,
            "parallax_y": 0.05
        },

        {
            "image": forest2,
            "x": 2843,
            "y": -90,
            "w": 1448,
            "h": 820,
            "parallax_x": 0.25,
            "parallax_y": 0.05
        },

        {
            "image": forest2,
            "x": 4291,
            "y": -90,
            "w": 1448,
            "h": 820,
            "parallax_x": 0.25,
            "parallax_y": 0.05
        },

        {
            "image": forest2,
            "x": 5739,
            "y": -90,
            "w": 1448,
            "h": 820,
            "parallax_x": 0.2,
            "parallax_y": 0.04
        },

        {
            "image": forest3,
            "x": -50,
            "y": -90,
            "w": 1448,
            "h": 820,
            "parallax_x": 0.3,
            "parallax_y": 0.06
        },

        {
            "image": forest3,
            "x": 1395,
            "y": -90,
            "w": 1448,
            "h": 820,
            "parallax_x": 0.3,
            "parallax_y": 0.06
        },

        {
            "image": forest3,
            "x": 2843,
            "y": -90,
            "w": 1448,
            "h": 820,
            "parallax_x": 0.3,
            "parallax_y": 0.06
        },

        {
            "image": forest3,
            "x": 4291,
            "y": -90,
            "w": 1448,
            "h": 820,
            "parallax_x": 0.3,
            "parallax_y": 0.06
        },

        {
            "image": forest3,
            "x": 5739,
            "y": -90,
            "w": 1448,
            "h": 820,
            "parallax_x": 0.2,
            "parallax_y": 0.04
        },

        {
            "image": forest4,
            "x": -50,
            "y": -105,
            "w": 1448,
            "h": 820,
            "parallax_x": 0.35,
            "parallax_y": 0.07
        },

        {
            "image": forest4,
            "x": 1395,
            "y": -105,
            "w": 1448,
            "h": 820,
            "parallax_x": 0.35,
            "parallax_y": 0.07
        },

        {
            "image": forest4,
            "x": 2843,
            "y": -105,
            "w": 1448,
            "h": 820,
            "parallax_x": 0.35,
            "parallax_y": 0.07
        },

        {
            "image": forest4,
            "x": 4291,
            "y": -105,
            "w": 1448,
            "h": 820,
            "parallax_x": 0.35,
            "parallax_y": 0.07
        },

        {
            "image": forest4,
            "x": 5739,
            "y": -105,
            "w": 1448,
            "h": 820,
            "parallax_x": 0.35,
            "parallax_y": 0.07
        },

        {
            "image": forest4,
            "x": 5739,
            "y": -90,
            "w": 1448,
            "h": 820,
            "parallax_x": 0.2,
            "parallax_y": 0.04
        },

    ]

    # 신사
    heal_objects = [
        pygame.Rect(7700, 350, 100, 140),
    ]

    # 적
    enemies = [
        enemy1(3100, 200),
        enemy2(4750, 20),
        enemy2(4820, -100),
        enemy1(5600, 500),
        enemy1(5800, 500),
        enemy2(5900, 250),
        enemy1(6200, 500),
    ]

    if not chapter1_miniboss_defeated:
        enemies.append(
            miniboss1(10500, 460)
        )

    fog_objects = [
        {
            "image": fog,
            "w": 1448,
            "h": 820
        }
    ]

    return platforms, walls, heal_objects, enemies, bg1_objects, fog_objects


def load_chapter_2():

    # 플랫폼
    platforms = [
        pygame.Rect(500, 560, 200, 20),
    ]

    # 벽
    walls = [
        pygame.Rect(1300, 500, 120, 140),
    ]

    # 신사
    heal_objects = [
        pygame.Rect(7700, 350, 100, 140),
    ]

    # 적
    enemies = [

        enemy1(3100, 200),
    ]

    (
        _,
        _,
        _,
        _,
        bg1_objects,
        _
    ) = load_chapter_1()

    fog_objects = []

    return platforms, walls, heal_objects, enemies, bg1_objects, fog_objects


def load_chapter_3():

    platforms = [
        pygame.Rect(7460, 220, 240, 20),
    ]

    walls = [
        pygame.Rect(1200, 500, 120, 140),
        pygame.Rect(2200, 460, 2700, 180),
        pygame.Rect(2500, 280, 2400, 180),
        pygame.Rect(6000, 500, 120, 140),
        pygame.Rect(7700, -140, 6700, 780),
        pygame.Rect(12000, -340, 2000, 200),
    ]
    heal_objects = [
        pygame.Rect(14150, -280, 100, 140),
    ]

    enemies = [
        enemy3(1800, 260),
        enemy3(5200, 160),
        enemy3(7200, 120),
        enemy4(3000, 400),
        enemy4(6400, 580),
    ]

    if not chapter3_miniboss_defeated:
        enemies.append(
            miniboss2(
                CHAPTER3_MINIBOSS_SPAWN_X,
                CHAPTER3_MINIBOSS_SPAWN_Y
            )
        )

    (
        _,
        _,
        _,
        _,
        bg1_objects,
        fog_objects
    ) = load_chapter_1()

    return platforms, walls, heal_objects, enemies, bg1_objects, fog_objects


def load_chapter_4():

    platforms = []
    walls = []
    heal_objects = []
    enemies = []

    if not mini3_defeated:
        enemies.append(
            mini3(
                MINI3_SPAWN_X,
                300
            )
        )

    if not chapter4_boss_defeated:
        enemies.append(
            chapter4_boss(
                CHAPTER4_BOSS_SPAWN_X,
                CHAPTER4_BOSS_SPAWN_Y
            )
        )

    (
        _,
        _,
        _,
        _,
        bg1_objects,
        fog_objects
    ) = load_chapter_1()

    return platforms, walls, heal_objects, enemies, bg1_objects, fog_objects


chapter1_miniboss_defeated = False
chapter3_miniboss_defeated = False
mini3_defeated = False
chapter4_boss_defeated = False


def load_chapter_data(chapter):

    if chapter == 1:
        return load_chapter_1()

    if chapter == 2:
        return load_chapter_2()

    if chapter == 3:
        return load_chapter_3()

    return load_chapter_4()


def warp_to_chapter(chapter, boss_start=False):

    global current_chapter, WORLD_WIDTH, ground
    global platforms, walls, heal_objects, enemies
    global bg1_objects, fog_objects, boss_walls, collision_walls
    global camera_x, camera_y, vel_y, on_ground, extra_jumps
    global coyote_timer, input_buffer, input_buffer_timer
    global attacking, attack_timer, attack_hitbox, attack_cd
    global combo_stage, combo_window, combo_input, combo_timer
    global player_animation, player_frame_index, player_hitstun
    global player_knockback_velocity, boss_fight_started
    global chapter3_boss_fight_started, mini3_boss_fight_started
    global chapter4_boss_fight_started
    global fading, fade_alpha
    global chapter_transition, next_chapter, ending

    current_chapter = chapter

    (
        platforms,
        walls,
        heal_objects,
        enemies,
        bg1_objects,
        fog_objects
    ) = load_chapter_data(chapter)

    WORLD_WIDTH = CHAPTER_WIDTHS[chapter]

    ground = pygame.Rect(
        0,
        HEIGHT - 80,
        WORLD_WIDTH,
        80
    )

    if boss_start and chapter == 3:
        player_rect.x = CHAPTER3_MINIBOSS_TRIGGER_X + 100
    else:
        player_rect.x = CHAPTER_SPAWN[chapter]["left"]
    player_rect.y = 455

    camera_x = 0
    camera_y = 0
    vel_y = 0
    on_ground = False
    extra_jumps = 1
    coyote_timer = 0
    input_buffer = None
    input_buffer_timer = 0

    attacking = False
    attack_timer = 0
    attack_hitbox = None
    attack_cd = 0
    combo_stage = 0
    combo_window = False
    combo_input = False
    combo_timer = 0

    player_animation = "idle"
    player_frame_index = 0
    player_hitstun = 0
    player_knockback_velocity = 0

    boss_fight_started = False
    chapter3_boss_fight_started = False
    mini3_boss_fight_started = False
    chapter4_boss_fight_started = False
    boss_walls = []
    collision_walls = walls

    fading = False
    fade_alpha = 0
    chapter_transition = False
    next_chapter = None
    ending = False


platforms, walls, heal_objects, enemies, bg1_objects, fog_objects = load_chapter_1()


player_rect = pygame.Rect(100, 455, 60, 180)
player_hurtbox = pygame.Rect(0, 0, 380, 400)

player_animation = "idle"
player_frame_index = 0
idle_animation_speed = 0.1
run_animation_speed = 0.2
attack_animation_speed = 0.4
air_attack_animation_speed = 0.2
knockback_animation_speed = 0.18

vel_y = 0

move_speed = 12
jump_power = -20
gravity = 0.8
on_ground = False
extra_jumps = 1
coyote_time = 8
coyote_timer = 0
input_buffer = None
input_buffer_time = 6
input_buffer_timer = 0

camera_x = 0
camera_y = 0

player_health = 100
player_max_health = 100
player_attack_damage = 10
player_facing = 1
attack_cd = 0
attack_duration = 30
attack_timer = 0
attack_hitbox = None

combo_stage = 0
combo_window = False
combo_input = False
combo_timer = 0
combo_max_timer = 12
attacking = False

draw_frames = (0,2)
attack1_frames = (2, 5)
attack2_frames = (5, 8)

hit_enemies = []

air_attack_used = False

player_invincible = 0
player_hitstun = 0
player_knockback_velocity = 0

fade_alpha = 0
fading = False
fade_direction = 1
next_chapter = None
chapter_transition = False
boss_fight_started = False
chapter3_boss_fight_started = False
mini3_boss_fight_started = False
chapter4_boss_fight_started = False
boss_walls = []
ending = False

# =========================
# 게임 루프
# =========================
running = True

while running:

    can_interact = False
    current_heal_objects = None

    for obj in heal_objects:

        if player_rect.colliderect(obj):

            can_interact = True
            current_heal_objects = obj
            break

    dt = clock.tick(60)

    idle_animation_speed = 0.1
    run_animation_speed = 0.2
    attack_animation_speed = 0.4

    chapter1_boss_alive = any(
        enemy["type"] == "miniboss1"
        for enemy in enemies
    )

    chapter3_boss_alive = any(
        enemy["type"] == "miniboss2"
        for enemy in enemies
    )

    chapter4_boss_alive = any(
        enemy["type"] == "chapter4_boss"
        for enemy in enemies
    )

    mini3_alive = any(
        enemy["type"] == "mini3"
        for enemy in enemies
    )

    if (
        current_chapter == 1
        and chapter1_boss_alive
        and player_rect.x > 9500
    ):
        boss_fight_started = True

    if current_chapter != 1 or not chapter1_boss_alive:
        boss_fight_started = False

    if (
        current_chapter == 3
        and chapter3_boss_alive
        and player_rect.x > CHAPTER3_MINIBOSS_TRIGGER_X
    ):
        chapter3_boss_fight_started = True

    if current_chapter != 3 or not chapter3_boss_alive:
        chapter3_boss_fight_started = False

    if (
        current_chapter == 4
        and mini3_alive
        and player_rect.x > MINI3_TRIGGER_X
    ):
        mini3_boss_fight_started = True

    if current_chapter != 4 or not mini3_alive:
        mini3_boss_fight_started = False

    if (
        current_chapter == 4
        and chapter4_boss_alive
        and player_rect.x > CHAPTER4_BOSS_TRIGGER_X
    ):
        chapter4_boss_fight_started = True

    if current_chapter != 4 or not chapter4_boss_alive:
        chapter4_boss_fight_started = False

    if boss_fight_started:
        boss_walls = [
            pygame.Rect(9000, -1000, 100, 3000),
            pygame.Rect(11500, -1000, 100, 3000),
        ]

    elif chapter3_boss_fight_started:
        boss_walls = [
            pygame.Rect(CHAPTER3_MINIBOSS_LEFT_WALL_X, -1000, 100, 3000),
            pygame.Rect(CHAPTER3_MINIBOSS_RIGHT_WALL_X, -1000, 100, 3000),
        ]

    elif mini3_boss_fight_started:
        boss_walls = [
            pygame.Rect(MINI3_LEFT_WALL_X, -1000, 100, 3000),
            pygame.Rect(MINI3_RIGHT_WALL_X, -1000, 100, 3000),
        ]

    else:
        boss_walls = []

    collision_walls = walls + boss_walls

    animation = player_animations[player_animation]

    if not attacking:

        animation = player_animations[player_animation]

        if player_animation == "idle":
            player_frame_index += idle_animation_speed

        elif player_animation == "run":
            player_frame_index += run_animation_speed

        elif player_animation in ("jump", "down"):
            player_frame_index = 0

        elif player_animation == "knockback":
            player_frame_index += knockback_animation_speed
            if player_frame_index >= len(animation):
                player_frame_index = len(animation) - 1

        if player_frame_index >= len(animation):
            player_frame_index = 0

    else:
        if player_animation == "air_attack":
            player_frame_index += air_attack_animation_speed

        else:
            player_frame_index += attack_animation_speed

        if combo_stage == 1:
            if player_frame_index >= 3.5:
                player_frame_index = float(attack1_frames[1] - 0.01)
                combo_window = True
                combo_timer += 1

                if combo_input:
                    combo_stage = 2
                    player_frame_index = float(attack2_frames[0])
                    combo_window = False
                    combo_input = False
                    combo_timer = 0
                    hit_enemies = []
                    attack_cd = 8

                elif combo_timer >= combo_max_timer:
                    attacking = False
                    player_animation = "idle"
                    player_frame_index = 0
                    combo_stage = 0
                    combo_window = False
                    combo_timer = 0
                    attack_hitbox = None
                    
        elif combo_stage == 2:
            if player_frame_index >= attack2_frames[1]:
                player_frame_index = float(attack2_frames[1] - 0.01)
                combo_window = True
                combo_timer += 1

                if combo_input:
                    combo_stage = 1
                    player_frame_index = float(attack1_frames[0])
                    combo_window = False
                    combo_input = False
                    combo_timer = 0
                    hit_enemies = []
                    attack_cd = 8

                elif combo_timer >= combo_max_timer:
                    attacking = False
                    player_animation = "idle"
                    player_frame_index = 0
                    combo_stage = 0
                    combo_window = False
                    combo_timer = 0
                    attack_hitbox = None

    # =========================
    # 적 애니
    # =========================
    for enemy in enemies:
        if "animations" not in enemy:
            continue

        enemy["frame_index"] += enemy["animation_speed"]
        animation = enemy["animations"][
            enemy["current_animation"]
        ]
        if enemy["frame_index"] >= len(animation):
            if (
                enemy["type"] == "enemy1"
                and enemy["current_animation"] == "death"
            ):
                enemy["frame_index"] = len(animation) - 1
                enemy["death_finished"] = True
            elif (
                enemy["type"] == "miniboss1"
                and enemy["current_animation"] == "death"
            ):
                enemy["frame_index"] = len(animation) - 1
                enemy["death_finished"] = True
            elif (
                enemy["type"] == "miniboss1"
                and enemy["current_animation"] == "attack"
            ):
                enemy["state"] = "waiting"
                enemy["current_animation"] = "move"
                enemy["frame_index"] = 0
                enemy["pattern_timer"] = 0
                enemy["dash_timer"] = 0
                enemy["attack_has_hit"] = False
                enemy["dash_has_hit"] = False
                enemy["attack_hitbox"] = None
            elif (
                enemy["type"] == "enemy2"
                and enemy["current_animation"] == "death"
            ):
                enemy["frame_index"] = len(animation) - 1
                enemy["death_finished"] = True
            elif (
                enemy["type"] == "enemy1"
                and enemy["current_animation"] == "attack"
            ):
                enemy["state"] = "recovery"
                enemy["current_animation"] = "idle"
                enemy["frame_index"] = 0
                enemy["enemy1_recovery_timer"] = (
                    enemy["enemy1_recovery_duration"]
                )
                enemy["enemy1_attack_has_hit"] = False
                enemy["enemy1_attack_hitbox"] = None
            elif (
                enemy["type"] == "miniboss2"
                and enemy["current_animation"] == "death"
            ):
                enemy["frame_index"] = len(animation) - 1
                enemy["death_finished"] = True
            elif (
                enemy["type"] == "mini3"
                and enemy["current_animation"] == "death"
            ):
                enemy["frame_index"] = len(animation) - 1
                enemy["death_finished"] = True
            elif (
                enemy["type"] == "mini3"
                and enemy["current_animation"] == "attack"
            ):
                enemy["state"] = "recovery"
                enemy["current_animation"] = "idle"
                enemy["frame_index"] = 0
                enemy["mini3_attack_recovery_timer"] = (
                    enemy["mini3_attack_recovery_duration"]
                )
                enemy["mini3_attack_has_hit"] = False
                enemy["mini3_attack_hitbox"] = None
            elif (
                enemy["type"] == "chapter4_boss"
                and enemy["current_animation"] == "death"
            ):
                enemy["frame_index"] = len(animation) - 1
                enemy["death_finished"] = True
            elif (
                enemy["type"] == "chapter4_boss"
                and enemy["current_animation"] == "waa"
            ):
                enemy["frame_index"] = len(animation) - 1
                if enemy["state"] != "waa_hold":
                    enemy["state"] = "waa_hold"
                    enemy["chapter4_boss_waa_hold_timer"] = (
                        enemy["chapter4_boss_waa_hold_duration"]
                    )
                enemy["vel_x"] = 0
            elif (
                enemy["type"] == "miniboss2"
                and enemy["current_animation"] in ("attack1", "attack2")
            ):
                mini2_finished_attack = enemy["current_animation"]
                if mini2_finished_attack == "attack1":
                    enemy["mini2_attack1_cooldown"] = (
                        enemy["mini2_same_attack_cooldown"]
                    )
                else:
                    enemy["mini2_attack2_cooldown"] = (
                        enemy["mini2_same_attack_cooldown"]
                    )
                enemy["state"] = "recovery"
                enemy["current_animation"] = "idle"
                enemy["frame_index"] = 0
                enemy["mini2_recovery_timer"] = (
                    enemy["mini2_recovery_duration"]
                )
                enemy["mini2_attack_has_hit"] = False
                enemy["mini2_attack_hitbox"] = None
            elif (
                enemy["type"] == "chapter4_boss"
                and enemy["current_animation"] in ("attack1", "attack2")
            ):
                chapter4_finished_attack = enemy["current_animation"]
                if chapter4_finished_attack == "attack1":
                    enemy["state"] = "recovery"
                    enemy["chapter4_boss_recovery_timer"] = (
                        enemy["chapter4_boss_attack1_recovery_duration"]
                    )
                else:
                    enemy["state"] = "idle"
                enemy["current_animation"] = "idle"
                enemy["frame_index"] = 0
                enemy["chapter4_boss_attack_has_hit"] = False
                enemy["chapter4_boss_attack_hitbox"] = None
                enemy["chapter4_boss_attack2_launched"] = False
                enemy["vel_x"] = 0
            else:
                enemy["frame_index"] = 0

    # =========================
    # 적 AI
    # =========================
    for enemy in enemies:

        if enemy["type"] == "enemy1":
            enemy["hurtbox"].topleft = enemy["rect"].topleft
            enemy["hurtbox"].size = enemy["rect"].size

        elif enemy["type"] == "enemy2":
            if enemy["health"] > 0:
                enemy["hurtbox"].topleft = (
                    enemy["rect"].x - 19,
                    enemy["rect"].y - 15
                )
            else:
                enemy["hurtbox"].size = (0, 0)

        elif enemy["type"] == "enemy3":
            enemy["hurtbox"].topleft = (
                enemy["rect"].x + enemy["hurtbox_offset_x"],
                enemy["rect"].y + enemy["hurtbox_offset_y"]
            )

        elif enemy["type"] == "enemy4":
            enemy["hurtbox"].topleft = (
                enemy["rect"].x + enemy["hurtbox_offset_x"],
                enemy["rect"].y + enemy["hurtbox_offset_y"]
            )

        elif enemy["type"] == "miniboss1":
            enemy["hurtbox"].topleft = enemy["rect"].topleft
            enemy["active"] = boss_fight_started

        elif enemy["type"] == "miniboss2":
            enemy["hurtbox"].topleft = enemy["rect"].topleft
            enemy["hurtbox"].size = enemy["rect"].size
            enemy["active"] = chapter3_boss_fight_started

        elif enemy["type"] == "mini3":
            enemy["hurtbox"].topleft = enemy["rect"].topleft
            enemy["hurtbox"].size = enemy["rect"].size
            enemy["active"] = mini3_boss_fight_started

        elif enemy["type"] == "chapter4_boss":
            enemy["hurtbox"].topleft = enemy["rect"].topleft
            enemy["hurtbox"].size = enemy["rect"].size
            enemy["active"] = chapter4_boss_fight_started

        if enemy["hitstun"] > 0 and enemy["health"] > 0:
            enemy["hitstun"] -= 1
            continue

        enemy_rect = enemy["rect"]

        distance_x = (
            player_rect.centerx
            - enemy_rect.centerx
        )

        distance_y = (
            player_rect.centery
            - enemy_rect.centery
        )

        # hurtbox 위치 동기화
        if enemy["type"] == "enemy1":

            enemy["hurtbox"].topleft = enemy["rect"].topleft
            enemy["hurtbox"].size = enemy["rect"].size

        elif enemy["type"] == "enemy2":

            if enemy["health"] > 0:
                enemy["hurtbox"].x = enemy["rect"].x - 19
                enemy["hurtbox"].y = enemy["rect"].y - 15
            else:
                enemy["hurtbox"].size = (0, 0)

        elif enemy["type"] == "enemy3":

            enemy["hurtbox"].x = (
                enemy["rect"].x
                + enemy["hurtbox_offset_x"]
            )
            enemy["hurtbox"].y = (
                enemy["rect"].y
                + enemy["hurtbox_offset_y"]
            )

        elif enemy["type"] == "enemy4":

            enemy["hurtbox"].x = (
                enemy["rect"].x
                + enemy["hurtbox_offset_x"]
            )
            enemy["hurtbox"].y = (
                enemy["rect"].y
                + enemy["hurtbox_offset_y"]
            )

        elif enemy["type"] == "miniboss1":

            enemy["hurtbox"].topleft = enemy["rect"].topleft

        elif enemy["type"] == "miniboss2":

            enemy["hurtbox"].topleft = enemy["rect"].topleft
            enemy["hurtbox"].size = enemy["rect"].size

        elif enemy["type"] == "mini3":

            enemy["hurtbox"].topleft = enemy["rect"].topleft
            enemy["hurtbox"].size = enemy["rect"].size

        elif enemy["type"] == "chapter4_boss":

            enemy["hurtbox"].topleft = enemy["rect"].topleft
            enemy["hurtbox"].size = enemy["rect"].size

        # =====================
        # 플레이어 인식
        # =====================
        if enemy["type"] == "miniboss1":
            enemy["aggro"] = enemy["active"]

        elif enemy["type"] == "miniboss2":
            enemy["aggro"] = enemy["active"]

        elif enemy["type"] == "mini3":
            enemy["aggro"] = enemy["active"]

        elif enemy["type"] == "chapter4_boss":
            enemy["aggro"] = enemy["active"]

        elif enemy["type"] == "enemy3":
            distance_sq = (
                distance_x * distance_x
                + distance_y * distance_y
            )

            if distance_sq < enemy["detect_range"] * enemy["detect_range"]:
                enemy["aggro"] = True

            elif distance_sq > enemy["chase_range"] * enemy["chase_range"]:
                enemy["aggro"] = False
                enemy["state"] = "idle"
                enemy["pattern_timer"] = 0
                enemy["dash_timer"] = 0

        elif abs(distance_x) < enemy["detect_range"]:
            enemy["aggro"] = True

        elif abs(distance_x) > enemy["chase_range"]:
            enemy["aggro"] = False

        if (
            enemy["type"] == "enemy2"
            and enemy["health"] > 0
            and not enemy["aggro"]
        ):
            enemy["velocity_x"] *= 0.9
            enemy["velocity_y"] *= 0.9

            if enemy["current_animation"] != "idle":
                enemy["current_animation"] = "idle"
                enemy["frame_index"] = 0

        # =====================
        # enemy1
        # =====================
        if enemy["type"] == "enemy1":
            enemy["vel_x"] = 0

            if enemy["enemy1_recovery_timer"] > 0:
                enemy["enemy1_recovery_timer"] -= 1

            if enemy["health"] <= 0:
                if not enemy["dead"]:
                    enemy["health"] = 0
                    enemy["dead"] = True
                    enemy["state"] = "death"
                    enemy["current_animation"] = "death"
                    enemy["frame_index"] = 0
                    enemy["enemy1_attack_hitbox"] = None

            elif enemy["state"] == "attack":
                enemy1_attack_frame = int(enemy["frame_index"])
                enemy1_attack_active = enemy1_attack_frame == 5

                if enemy["direction"] == 1:
                    enemy1_attack_x = (
                        enemy_rect.x
                        + enemy["enemy1_attack_right_x_offset"]
                    )
                else:
                    enemy1_attack_x = (
                        enemy_rect.x
                        + enemy["enemy1_attack_left_x_offset"]
                    )

                enemy1_attack_rect = pygame.Rect(
                    enemy1_attack_x,
                    enemy_rect.y + enemy["enemy1_attack_y_offset"],
                    enemy["enemy1_attack_hitbox_width"],
                    enemy["enemy1_attack_hitbox_height"],
                )

                if enemy1_attack_active:
                    enemy["enemy1_attack_hitbox"] = enemy1_attack_rect
                else:
                    enemy["enemy1_attack_hitbox"] = None

                if (
                    enemy1_attack_active
                    and not enemy["enemy1_attack_has_hit"]
                    and player_invincible <= 0
                    and enemy1_attack_rect.colliderect(player_rect)
                ):
                    player_health -= enemy["enemy1_attack_damage"]
                    player_health = max(player_health, 0)
                    player_invincible = 70
                    player_hitstun = 25
                    player_animation = "knockback"
                    player_frame_index = 0
                    attacking = False
                    combo_stage = 0
                    combo_window = False
                    combo_input = False
                    combo_timer = 0
                    attack_timer = 0
                    attack_hitbox = None
                    enemy["enemy1_attack_has_hit"] = True

                    enemy1_knockback = 14
                    if player_rect.centerx < enemy_rect.centerx:
                        player_knockback_velocity = -enemy1_knockback
                        player_facing = 1
                    else:
                        player_knockback_velocity = enemy1_knockback
                        player_facing = -1

            elif enemy["state"] == "recovery":
                enemy["enemy1_attack_hitbox"] = None

                if enemy["current_animation"] != "idle":
                    enemy["current_animation"] = "idle"
                    enemy["frame_index"] = 0

                if enemy["enemy1_recovery_timer"] <= 0:
                    enemy["state"] = "idle"

            elif enemy["aggro"]:
                if abs(distance_x) <= enemy["enemy1_attack_range"]:
                    if distance_x > 0:
                        enemy["direction"] = 1
                    elif distance_x < 0:
                        enemy["direction"] = -1

                    enemy["state"] = "attack"
                    enemy["current_animation"] = "attack"
                    enemy["frame_index"] = 0
                    enemy["enemy1_attack_has_hit"] = False

                else:
                    if distance_x > 0:
                        enemy["vel_x"] = enemy["speed"]
                        enemy["direction"] = 1

                    elif distance_x < 0:
                        enemy["vel_x"] = -enemy["speed"]
                        enemy["direction"] = -1

                    enemy["state"] = "move"

                    if enemy["current_animation"] != "move":
                        enemy["current_animation"] = "move"
                        enemy["frame_index"] = 0

            else:
                enemy["state"] = "idle"
                enemy["enemy1_attack_hitbox"] = None
                if enemy["current_animation"] != "idle":
                    enemy["current_animation"] = "idle"
                    enemy["frame_index"] = 0

            enemy_rect.x += enemy["vel_x"]

            for wall in collision_walls:
                if enemy_rect.colliderect(wall):
                    if enemy["vel_x"] > 0:
                        enemy_rect.right = wall.left
                    elif enemy["vel_x"] < 0:
                        enemy_rect.left = wall.right

            enemy1_previous_bottom = enemy_rect.bottom
            enemy["vel_y"] += enemy["gravity"]
            enemy_rect.y += enemy["vel_y"]
            enemy["on_ground"] = False

            enemy1_surfaces = [ground] + platforms + collision_walls

            for enemy1_surface in enemy1_surfaces:
                if (
                    enemy_rect.colliderect(enemy1_surface)
                    and enemy1_previous_bottom <= enemy1_surface.top
                    and enemy["vel_y"] >= 0
                ):
                    enemy_rect.bottom = enemy1_surface.top
                    enemy["vel_y"] = 0
                    enemy["on_ground"] = True

            enemy["hurtbox"].topleft = enemy_rect.topleft
            enemy["hurtbox"].size = enemy_rect.size

        elif enemy["type"] == "enemy4":

            enemy_rect.x += enemy["vel_x"]

            previous_bottom = enemy_rect.bottom

            enemy["vel_y"] += enemy["gravity"]
            enemy_rect.y += enemy["vel_y"]
            enemy["on_ground"] = False

            all_surfaces = [ground] + platforms + collision_walls

            for surface in all_surfaces:

                if enemy_rect.colliderect(surface):

                    if (
                        previous_bottom <= surface.top
                        and enemy["vel_y"] >= 0
                    ):
                        enemy_rect.bottom = surface.top
                        enemy["vel_y"] = 0
                        enemy["on_ground"] = True

            for wall in collision_walls:

                if enemy_rect.colliderect(wall):

                    if enemy["vel_x"] > 0:
                        enemy_rect.right = wall.left
                        enemy["direction"] = -1

                    elif enemy["vel_x"] < 0:
                        enemy_rect.left = wall.right
                        enemy["direction"] = 1

            enemy["vel_x"] = 0

            if enemy["aggro"]:

                if distance_x > 0:
                    enemy["vel_x"] = enemy["speed"]
                    enemy["direction"] = 1

                elif distance_x < 0:
                    enemy["vel_x"] = -enemy["speed"]
                    enemy["direction"] = -1

            else:
                enemy["vel_x"] = (
                    enemy["speed"]
                    * enemy["direction"]
                )

                if enemy_rect.x < (
                    enemy["start_x"]
                    - enemy["patrol_range"]
                ):
                    enemy["direction"] = 1

                if enemy_rect.x > (
                    enemy["start_x"]
                    + enemy["patrol_range"]
                ):
                    enemy["direction"] = -1

        # =====================
        # enemy2 (수정된 충돌 로직)
        # =====================
        elif enemy["type"] == "enemy2":

            if enemy["health"] <= 0:
                if not enemy["dead"]:
                    enemy["health"] = 0
                    enemy["dead"] = True
                    enemy["current_animation"] = "death"
                    enemy["frame_index"] = 0
                    enemy["velocity_x"] = 0
                    enemy["velocity_y"] = 0
                    enemy["death_velocity_y"] = 0
                    enemy["hurtbox"].size = (0, 0)

                enemy2_previous_bottom = enemy_rect.bottom
                enemy["death_velocity_y"] += enemy["death_gravity"]
                enemy_rect.y += enemy["death_velocity_y"]

                enemy2_death_surfaces = (
                    [ground] + platforms + collision_walls
                )

                for enemy2_surface in enemy2_death_surfaces:
                    if (
                        enemy_rect.colliderect(enemy2_surface)
                        and enemy2_previous_bottom
                        <= enemy2_surface.top
                        and enemy["death_velocity_y"] >= 0
                    ):
                        enemy_rect.bottom = enemy2_surface.top
                        enemy["death_velocity_y"] = 0

            elif enemy["aggro"]:
                if enemy["current_animation"] != "move":
                    enemy["current_animation"] = "move"
                    enemy["frame_index"] = 0

                # -----------------
                # 목표 속도
                # -----------------
                target_vel_x = 0
                target_vel_y = 0

                if distance_x > 0:
                    target_vel_x = enemy["speed"]
                    enemy["direction"] = 1

                elif distance_x < 0:
                    target_vel_x = -enemy["speed"]
                    enemy["direction"] = -1

                if distance_y > 0:
                    target_vel_y = enemy["speed"]

                elif distance_y < 0:
                    target_vel_y = -enemy["speed"]

                # -----------------
                # 부드러운 이동 속도 계산
                # -----------------
                enemy["velocity_x"] += (
                    target_vel_x
                    - enemy["velocity_x"]
                ) * 0.05

                enemy["velocity_y"] += (
                    target_vel_y
                    - enemy["velocity_y"]
                ) * 0.05

                # -----------------
                # 1. X축 이동 및 충돌 처리
                # -----------------
                enemy_rect.x += enemy["velocity_x"]

                for wall in collision_walls:
                    if enemy_rect.colliderect(wall):
                        if enemy["velocity_x"] > 0:
                            enemy_rect.right = wall.left
                        elif enemy["velocity_x"] < 0:
                            enemy_rect.left = wall.right
                        # 벽에 가로막혔으므로 X축 속도 초기화
                        enemy["velocity_x"] = 0

                # -----------------
                # 2. Y축 이동 및 충돌 처리
                # -----------------
                enemy_rect.y += enemy["velocity_y"]

                # 바닥(ground) 충돌
                if enemy_rect.colliderect(ground):
                    if enemy["velocity_y"] > 0:
                        enemy_rect.bottom = ground.top
                    elif enemy["velocity_y"] < 0:
                        enemy_rect.top = ground.bottom
                    enemy["velocity_y"] = 0

                # 벽(wall) Y축 충돌
                for wall in collision_walls:
                    if enemy_rect.colliderect(wall):
                        if enemy["velocity_y"] > 0:
                            enemy_rect.bottom = wall.top
                        elif enemy["velocity_y"] < 0:
                            enemy_rect.top = wall.bottom
                        # 벽에 가로막혔으므로 Y축 속도 초기화
                        enemy["velocity_y"] = 0
                            
        elif enemy["type"] == "enemy3":

            if enemy["aggro"]:

                if enemy["state"] == "idle":
                    enemy["state"] = "ready"
                    enemy["pattern_timer"] = 0
                    enemy["velocity_x"] = 0
                    enemy["velocity_y"] = 0

                elif enemy["state"] == "ready":
                    enemy["pattern_timer"] += 1

                    if player_rect.centerx >= enemy_rect.centerx:
                        enemy["direction"] = 1
                    else:
                        enemy["direction"] = -1

                    if enemy["pattern_timer"] >= 65:
                        length = max(
                            1,
                            (
                                distance_x * distance_x
                                + distance_y * distance_y
                            ) ** 0.5
                        )

                        enemy["dash_x"] = (
                            distance_x
                            / length
                            * enemy["speed"]
                        )
                        enemy["dash_y"] = (
                            distance_y
                            / length
                            * enemy["speed"]
                        )
                        enemy["dash_timer"] = 28
                        enemy["state"] = "dash"
                        enemy["pattern_timer"] = 0

                elif enemy["state"] == "dash":
                    enemy["x"] += enemy["dash_x"]
                    enemy_rect.x = int(enemy["x"])

                    for wall in collision_walls:
                        if enemy_rect.colliderect(wall):
                            if enemy["dash_x"] > 0:
                                enemy_rect.right = wall.left
                            elif enemy["dash_x"] < 0:
                                enemy_rect.left = wall.right

                            enemy["x"] = float(enemy_rect.x)
                            enemy["dash_timer"] = 0

                    enemy["y"] += enemy["dash_y"]
                    enemy_rect.y = int(enemy["y"])

                    for wall in collision_walls:
                        if enemy_rect.colliderect(wall):
                            if enemy["dash_y"] > 0:
                                enemy_rect.bottom = wall.top
                            elif enemy["dash_y"] < 0:
                                enemy_rect.top = wall.bottom

                            enemy["y"] = float(enemy_rect.y)
                            enemy["dash_timer"] = 0

                    enemy["dash_timer"] -= 1

                    if enemy["dash_timer"] <= 0:
                        enemy["state"] = "ready"
                        enemy["pattern_timer"] = 0

            else:
                enemy["state"] = "idle"
                enemy["pattern_timer"] = 0
                enemy["dash_timer"] = 0

            enemy["hurtbox"].x = (
                enemy["rect"].x
                + enemy["hurtbox_offset_x"]
            )
            enemy["hurtbox"].y = (
                enemy["rect"].y
                + enemy["hurtbox_offset_y"]
            )

        elif enemy["type"] == "miniboss1":

            if enemy["health"] <= 0:
                if not enemy["dead"]:
                    enemy["health"] = 0
                    enemy["dead"] = True
                    enemy["state"] = "death"
                    enemy["current_animation"] = "death"
                    enemy["frame_index"] = 0
                    enemy["animation_speed"] = (
                        enemy["normal_animation_speed"]
                    )
                    enemy["attack_hitbox"] = None
                    enemy["hurtbox"].size = (0, 0)

                continue

            if not enemy["active"]:
                enemy["state"] = "waiting"
                enemy["current_animation"] = "idle"
                enemy["animation_speed"] = 0.12
                continue

            enemy["pattern_timer"] += 1

            if enemy["state"] == "waiting":
                enemy["current_animation"] = "move"
                enemy["animation_speed"] = (
                    enemy["slow_move_animation_speed"]
                )

                if player_rect.centerx >= enemy_rect.centerx:
                    enemy["direction"] = 1
                else:
                    enemy["direction"] = -1

                enemy["x"] += (
                    0.3
                    * enemy["direction"]
                )
                enemy_rect.x = int(enemy["x"])

                for wall in collision_walls:
                    if enemy_rect.colliderect(wall):
                        if enemy["direction"] > 0:
                            enemy_rect.right = wall.left
                        else:
                            enemy_rect.left = wall.right

                        enemy["x"] = float(enemy_rect.x)

                if enemy["pattern_timer"] >= 210:
                    enemy["state"] = "ready"
                    enemy["pattern_timer"] = 0
                    enemy["current_animation"] = "idle"
                    enemy["frame_index"] = 0
                    enemy["animation_speed"] = 0.12

                    if player_rect.centerx >= enemy_rect.centerx:
                        enemy["direction"] = 1
                    else:
                        enemy["direction"] = -1

            elif enemy["state"] == "ready":
                if enemy["pattern_timer"] >= 45:
                    enemy["state"] = "dash"
                    enemy["pattern_timer"] = 0
                    enemy["dash_timer"] = 30
                    enemy["current_animation"] = "move"
                    enemy["frame_index"] = 0
                    enemy["animation_speed"] = (
                        enemy["normal_animation_speed"]
                    )
                    enemy["dash_has_hit"] = False

            elif enemy["state"] == "dash":
                enemy_rect.x += (
                    enemy["dash_speed"]
                    * enemy["direction"]
                )
                enemy["x"] = float(enemy_rect.x)

                for wall in collision_walls:
                    if enemy_rect.colliderect(wall):
                        if enemy["direction"] > 0:
                            enemy_rect.right = wall.left
                        else:
                            enemy_rect.left = wall.right

                        enemy["x"] = float(enemy_rect.x)
                        enemy["dash_timer"] = 0

                if (
                    not enemy["dash_has_hit"]
                    and player_invincible <= 0
                    and enemy_rect.colliderect(player_rect)
                ):
                    player_health -= enemy["dash_damage"]
                    player_health = max(player_health, 0)
                    player_invincible = 6
                    player_hitstun = 20
                    player_animation = "knockback"
                    player_frame_index = 0
                    player_knockback_velocity = (
                        18 * enemy["direction"]
                    )
                    player_facing = -enemy["direction"]
                    enemy["dash_has_hit"] = True

                enemy["attack_hitbox"] = None
                enemy["dash_timer"] -= 1

                if enemy["dash_timer"] <= 0:
                    enemy["state"] = "attack"
                    enemy["current_animation"] = "attack"
                    enemy["frame_index"] = 0
                    enemy["animation_speed"] = (
                        enemy["normal_animation_speed"]
                    )
                    enemy["attack_has_hit"] = False

            elif enemy["state"] == "attack":
                miniboss1_attack_frame = int(enemy["frame_index"])
                miniboss1_attack_active = miniboss1_attack_frame == 7

                if enemy["direction"] == 1:
                    miniboss1_attack_x = (
                        enemy_rect.x
                        + enemy["attack_right_x_offset"]
                    )
                else:
                    miniboss1_attack_x = (
                        enemy_rect.x
                        + enemy["attack_left_x_offset"]
                    )

                miniboss1_attack_rect = pygame.Rect(
                    miniboss1_attack_x,
                    enemy_rect.y + enemy["attack_y_offset"],
                    enemy["attack_hitbox_width"],
                    enemy["attack_hitbox_height"],
                )

                if miniboss1_attack_active:
                    enemy["attack_hitbox"] = miniboss1_attack_rect
                else:
                    enemy["attack_hitbox"] = None

                if (
                    miniboss1_attack_active
                    and not enemy["attack_has_hit"]
                    and player_invincible <= 0
                    and miniboss1_attack_rect.colliderect(player_rect)
                ):
                    player_health -= enemy["attack_damage"]
                    player_health = max(player_health, 0)
                    player_invincible = 70
                    player_hitstun = 25
                    player_animation = "knockback"
                    player_frame_index = 0
                    player_knockback_velocity = (
                        24 * enemy["direction"]
                    )
                    player_facing = -enemy["direction"]
                    enemy["attack_has_hit"] = True

            enemy["hurtbox"].topleft = enemy["rect"].topleft

        elif enemy["type"] == "miniboss2":

            if enemy["health"] <= 0:
                if not enemy["dead"]:
                    enemy["dead"] = True
                    enemy["state"] = "death"
                    enemy["current_animation"] = "death"
                    enemy["frame_index"] = 0
                    enemy["vel_x"] = 0
                    enemy["active"] = False
                    enemy["mini2_attack_hitbox"] = None

                enemy["hurtbox"].topleft = enemy["rect"].topleft
                enemy["hurtbox"].size = enemy["rect"].size
                continue

            previous_bottom = enemy_rect.bottom

            enemy["vel_y"] += enemy["gravity"]
            enemy_rect.y += enemy["vel_y"]
            enemy["on_ground"] = False

            all_surfaces = [ground] + platforms + collision_walls

            for surface in all_surfaces:

                if enemy_rect.colliderect(surface):

                    if (
                        previous_bottom <= surface.top
                        and enemy["vel_y"] >= 0
                    ):
                        enemy_rect.bottom = surface.top
                        enemy["vel_y"] = 0
                        enemy["on_ground"] = True

            enemy["vel_x"] = 0

            if enemy["mini2_attack1_cooldown"] > 0:
                enemy["mini2_attack1_cooldown"] -= 1

            if enemy["mini2_attack2_cooldown"] > 0:
                enemy["mini2_attack2_cooldown"] -= 1

            if enemy["mini2_recovery_timer"] > 0:
                enemy["mini2_recovery_timer"] -= 1

            if enemy["active"]:
                mini2_is_attacking = (
                    enemy["state"] in ("attack1", "attack2")
                )

                if not mini2_is_attacking:
                    if distance_x > 0:
                        enemy["direction"] = 1

                    elif distance_x < 0:
                        enemy["direction"] = -1

                abs_distance_x = abs(distance_x)

                if enemy["state"] == "recovery":
                    enemy["mini2_attack_hitbox"] = None

                    if enemy["current_animation"] != "idle":
                        enemy["current_animation"] = "idle"
                        enemy["frame_index"] = 0

                    if enemy["mini2_recovery_timer"] <= 0:
                        enemy["state"] = "idle"

                elif enemy["state"] in ("attack1", "attack2"):
                    mini2_attack_frame = int(enemy["frame_index"])

                    if enemy["state"] == "attack1":
                        mini2_attack_is_active = (
                            8 <= mini2_attack_frame <= 9
                        )
                        mini2_attack_damage = enemy["mini2_attack1_damage"]
                        mini2_attack_width = (
                            enemy["mini2_attack1_hitbox_width"]
                        )
                        mini2_attack_height = (
                            enemy["mini2_attack1_hitbox_height"]
                        )
                        mini2_attack_right_x_offset = (
                            enemy["mini2_attack1_right_x_offset"]
                        )
                        mini2_attack_left_x_offset = (
                            enemy["mini2_attack1_left_x_offset"]
                        )
                        mini2_attack_y = (
                            enemy_rect.y
                            + enemy["mini2_attack1_hitbox_y_offset"]
                        )
                    else:
                        mini2_attack_is_active = (
                            6 <= mini2_attack_frame <= 7
                        )
                        mini2_attack_damage = enemy["mini2_attack2_damage"]
                        mini2_attack_width = (
                            enemy["mini2_attack2_hitbox_width"]
                        )
                        mini2_attack_height = (
                            enemy["mini2_attack2_hitbox_height"]
                        )
                        mini2_attack_right_x_offset = (
                            enemy["mini2_attack2_right_x_offset"]
                        )
                        mini2_attack_left_x_offset = (
                            enemy["mini2_attack2_left_x_offset"]
                        )
                        mini2_attack_y = (
                            enemy_rect.y
                            + enemy["mini2_attack2_hitbox_y_offset"]
                        )

                    if enemy["direction"] == 1:
                        mini2_attack_rect = pygame.Rect(
                            enemy_rect.x + mini2_attack_right_x_offset,
                            mini2_attack_y,
                            mini2_attack_width,
                            mini2_attack_height
                        )
                    else:
                        mini2_attack_rect = pygame.Rect(
                            enemy_rect.x + mini2_attack_left_x_offset,
                            mini2_attack_y,
                            mini2_attack_width,
                            mini2_attack_height
                        )

                    if mini2_attack_is_active:
                        enemy["mini2_attack_hitbox"] = mini2_attack_rect
                    else:
                        enemy["mini2_attack_hitbox"] = None

                    if (
                        mini2_attack_is_active
                        and not enemy["mini2_attack_has_hit"]
                        and player_invincible <= 0
                        and mini2_attack_rect.colliderect(player_rect)
                    ):
                        player_health -= mini2_attack_damage
                        if player_health < 0:
                            player_health = 0

                        player_invincible = 70
                        player_hitstun = 25
                        player_animation = "knockback"
                        player_frame_index = 0
                        attacking = False
                        combo_stage = 0
                        combo_window = False
                        combo_input = False
                        combo_timer = 0
                        attack_timer = 0
                        attack_hitbox = None
                        enemy["mini2_attack_has_hit"] = True

                        if enemy["state"] == "attack2":
                            knockback_power = enemy["mini2_attack2_knockback"]
                        else:
                            knockback_power = enemy["mini2_attack1_knockback"]

                        if player_rect.centerx < enemy_rect.centerx:
                            player_knockback_velocity = -knockback_power
                            player_facing = 1
                        else:
                            player_knockback_velocity = knockback_power
                            player_facing = -1

                else:
                    mini2_can_use_attack2 = (
                        enemy["mini2_attack2_cooldown"] <= 0
                        and abs_distance_x <= enemy["mini2_attack2_range"]
                    )
                    mini2_can_use_attack1 = (
                        enemy["mini2_attack1_cooldown"] <= 0
                        and abs_distance_x <= enemy["mini2_attack1_range"]
                    )

                    mini2_use_attack2 = (
                        mini2_can_use_attack2
                        or (
                            not mini2_can_use_attack1
                            and enemy["mini2_attack2_cooldown"] <= 0
                            and abs_distance_x
                            <= enemy["mini2_attack1_range"]
                        )
                    )

                    if mini2_use_attack2:
                        enemy["state"] = "attack2"
                        enemy["current_animation"] = "attack2"
                        enemy["frame_index"] = 0
                        enemy["mini2_attack_has_hit"] = False

                    elif mini2_can_use_attack1:
                        enemy["state"] = "attack1"
                        enemy["current_animation"] = "attack1"
                        enemy["frame_index"] = 0
                        enemy["mini2_attack_has_hit"] = False

                    else:
                        enemy["mini2_move_timer"] -= 1

                        if enemy["mini2_move_timer"] <= 0:
                            enemy["mini2_move_direction"] *= -1
                            enemy["mini2_move_timer"] = (
                                enemy["mini2_move_interval"]
                            )

                        if abs_distance_x < enemy["keep_distance_min"]:
                            enemy["vel_x"] = (
                                -enemy["speed"]
                                * enemy["direction"]
                                * enemy["mini2_backstep_speed_ratio"]
                            )
                        elif abs_distance_x > enemy["keep_distance_max"]:
                            enemy["vel_x"] = (
                                enemy["speed"]
                                * enemy["direction"]
                            )
                        elif enemy["mini2_move_direction"] > 0:
                            enemy["vel_x"] = (
                                enemy["speed"]
                                * enemy["direction"]
                            )
                        else:
                            enemy["vel_x"] = (
                                -enemy["speed"]
                                * enemy["direction"]
                                * enemy["mini2_backstep_speed_ratio"]
                            )

                        if enemy["current_animation"] != "move":
                            enemy["current_animation"] = "move"
                            enemy["frame_index"] = 0

            else:
                if enemy["current_animation"] != "idle":
                    enemy["current_animation"] = "idle"
                    enemy["frame_index"] = 0

            enemy_rect.x += enemy["vel_x"]

            for wall in collision_walls:

                if enemy_rect.colliderect(wall):

                    if enemy["vel_x"] > 0:
                        enemy_rect.right = wall.left

                    elif enemy["vel_x"] < 0:
                        enemy_rect.left = wall.right

                    enemy["mini2_move_direction"] *= -1
                    enemy["mini2_move_timer"] = (
                        enemy["mini2_move_interval"]
                    )

            enemy["hurtbox"].topleft = enemy["rect"].topleft
            enemy["hurtbox"].size = enemy["rect"].size

        elif enemy["type"] == "mini3":
            mini3_previous_bottom = enemy_rect.bottom

            enemy["vel_x"] = 0

            if enemy["mini3_attack_recovery_timer"] > 0:
                enemy["mini3_attack_recovery_timer"] -= 1

            if enemy["health"] <= 0:
                if not enemy["dead"]:
                    enemy["health"] = 0
                    enemy["dead"] = True
                    enemy["state"] = "death"
                    enemy["current_animation"] = "death"
                    enemy["frame_index"] = 0
                    enemy["mini3_attack_hitbox"] = None

            elif enemy["active"]:
                mini3_distance_x = abs(distance_x)

                if enemy["state"] == "attack":
                    mini3_attack_frame = int(enemy["frame_index"])
                    mini3_attack_active = mini3_attack_frame == 5

                    if enemy["direction"] == 1:
                        mini3_attack_x = (
                            enemy_rect.x
                            + enemy["mini3_attack_right_x_offset"]
                        )
                    else:
                        mini3_attack_x = (
                            enemy_rect.x
                            + enemy["mini3_attack_left_x_offset"]
                        )

                    mini3_attack_rect = pygame.Rect(
                        mini3_attack_x,
                        enemy_rect.y + enemy["mini3_attack_y_offset"],
                        enemy["mini3_attack_hitbox_width"],
                        enemy["mini3_attack_hitbox_height"],
                    )

                    if mini3_attack_active:
                        enemy["mini3_attack_hitbox"] = mini3_attack_rect
                    else:
                        enemy["mini3_attack_hitbox"] = None

                    if (
                        mini3_attack_active
                        and not enemy["mini3_attack_has_hit"]
                        and player_invincible <= 0
                        and mini3_attack_rect.colliderect(player_rect)
                    ):
                        player_health -= enemy["mini3_attack_damage"]
                        player_health = max(player_health, 0)
                        player_invincible = 70
                        player_hitstun = 25
                        player_animation = "knockback"
                        player_frame_index = 0
                        attacking = False
                        combo_stage = 0
                        combo_window = False
                        combo_input = False
                        combo_timer = 0
                        attack_timer = 0
                        attack_hitbox = None
                        enemy["mini3_attack_has_hit"] = True

                        mini3_knockback = 18
                        if player_rect.centerx < enemy_rect.centerx:
                            player_knockback_velocity = -mini3_knockback
                            player_facing = 1
                        else:
                            player_knockback_velocity = mini3_knockback
                            player_facing = -1

                elif enemy["state"] == "recovery":
                    enemy["mini3_attack_hitbox"] = None

                    if enemy["current_animation"] != "idle":
                        enemy["current_animation"] = "idle"
                        enemy["frame_index"] = 0

                    if enemy["mini3_attack_recovery_timer"] <= 0:
                        enemy["state"] = "idle"

                elif mini3_distance_x <= enemy["mini3_attack_range"]:
                    if distance_x > 0:
                        enemy["direction"] = 1
                    elif distance_x < 0:
                        enemy["direction"] = -1

                    enemy["state"] = "attack"
                    enemy["current_animation"] = "attack"
                    enemy["frame_index"] = 0
                    enemy["mini3_attack_has_hit"] = False

                else:
                    if distance_x > 0:
                        enemy["direction"] = 1
                    elif distance_x < 0:
                        enemy["direction"] = -1

                    enemy["state"] = "move"
                    enemy["vel_x"] = enemy["speed"] * enemy["direction"]

                    if enemy["current_animation"] != "move":
                        enemy["current_animation"] = "move"
                        enemy["frame_index"] = 0

            else:
                enemy["state"] = "idle"
                enemy["mini3_attack_hitbox"] = None
                if enemy["current_animation"] != "idle":
                    enemy["current_animation"] = "idle"
                    enemy["frame_index"] = 0

            enemy_rect.x += enemy["vel_x"]

            for mini3_wall in collision_walls:
                if enemy_rect.colliderect(mini3_wall):
                    if enemy["vel_x"] > 0:
                        enemy_rect.right = mini3_wall.left
                    elif enemy["vel_x"] < 0:
                        enemy_rect.left = mini3_wall.right

            enemy["vel_y"] += enemy["gravity"]
            enemy_rect.y += enemy["vel_y"]
            enemy["on_ground"] = False

            mini3_surfaces = [ground] + platforms + collision_walls

            for mini3_surface in mini3_surfaces:
                if (
                    enemy_rect.colliderect(mini3_surface)
                    and mini3_previous_bottom <= mini3_surface.top
                    and enemy["vel_y"] >= 0
                ):
                    enemy_rect.bottom = mini3_surface.top
                    enemy["vel_y"] = 0
                    enemy["on_ground"] = True

            enemy["hurtbox"].topleft = enemy_rect.topleft
            enemy["hurtbox"].size = enemy_rect.size

        elif enemy["type"] == "chapter4_boss":
            previous_bottom = enemy_rect.bottom

            if enemy["health"] <= 0 and not enemy["dead"]:
                enemy["health"] = 0
                enemy["dead"] = True
                enemy["state"] = "death"
                enemy["current_animation"] = "death"
                enemy["frame_index"] = 0
                enemy["vel_x"] = 0
                enemy["chapter4_boss_attack_hitbox"] = None

            elif (
                enemy["health"] > 0
                and enemy["state"] not in ("waa", "waa_hold", "death")
                and enemy["health"]
                <= enemy["chapter4_boss_next_waa_health"]
            ):
                enemy["state"] = "waa"
                enemy["current_animation"] = "waa"
                enemy["frame_index"] = 0
                enemy["vel_x"] = 0
                enemy["chapter4_boss_attack_hitbox"] = None
                enemy["chapter4_boss_attack2_cooldown"] = 0
                enemy["chapter4_boss_next_waa_health"] -= 100
                enemy["chapter4_boss_waa_knockback_done"] = False

            if (
                enemy["state"] in ("waa", "waa_hold")
                and int(enemy["frame_index"]) >= 5
                and not enemy["chapter4_boss_waa_knockback_done"]
            ):
                if player_rect.centerx < enemy_rect.centerx:
                    player_knockback_velocity = (
                        -enemy["chapter4_boss_waa_knockback"]
                    )
                    player_facing = 1
                else:
                    player_knockback_velocity = (
                        enemy["chapter4_boss_waa_knockback"]
                    )
                    player_facing = -1

                player_hitstun = 35
                player_animation = "knockback"
                player_frame_index = 0
                attacking = False
                combo_stage = 0
                combo_window = False
                combo_input = False
                combo_timer = 0
                attack_timer = 0
                attack_hitbox = None
                enemy["chapter4_boss_waa_knockback_done"] = True

            if enemy["state"] == "waa_hold":
                if enemy["chapter4_boss_waa_hold_timer"] > 0:
                    enemy["chapter4_boss_waa_hold_timer"] -= 1
                else:
                    enemy["state"] = "idle"
                    enemy["current_animation"] = "idle"
                    enemy["frame_index"] = 0

            if enemy["chapter4_boss_attack2_cooldown"] > 0:
                enemy["chapter4_boss_attack2_cooldown"] -= 1

            if enemy["chapter4_boss_recovery_timer"] > 0:
                enemy["chapter4_boss_recovery_timer"] -= 1

            chapter4_boss_is_attacking = (
                enemy["state"] in ("attack1", "attack2")
            )
            chapter4_boss_is_locked = (
                chapter4_boss_is_attacking
                or enemy["state"] in (
                    "recovery",
                    "waa",
                    "waa_hold",
                    "death",
                )
            )

            if not chapter4_boss_is_locked:
                if distance_x > 0:
                    enemy["direction"] = 1
                elif distance_x < 0:
                    enemy["direction"] = -1

            enemy["vel_x"] = 0

            if enemy["active"]:
                chapter4_boss_distance = abs(distance_x)

                if enemy["state"] in ("waa", "waa_hold", "death"):
                    chapter4_boss_attack_active = False
                    chapter4_boss_attack_rect = None
                    enemy["chapter4_boss_attack_hitbox"] = None

                elif enemy["state"] == "recovery":
                    chapter4_boss_attack_active = False
                    chapter4_boss_attack_rect = None
                    enemy["chapter4_boss_attack_hitbox"] = None

                    if enemy["chapter4_boss_recovery_timer"] <= 0:
                        enemy["state"] = "idle"

                elif enemy["state"] == "attack1":
                    chapter4_boss_attack_frame = int(enemy["frame_index"])
                    chapter4_boss_attack_active = (
                        chapter4_boss_attack_frame == 8
                    )
                    chapter4_boss_attack_damage = (
                        enemy["chapter4_boss_attack1_damage"]
                    )

                    if enemy["direction"] == 1:
                        chapter4_boss_attack_x_offset = (
                            enemy[
                                "chapter4_boss_attack1_right_x_offset"
                            ]
                        )
                    else:
                        chapter4_boss_attack_x_offset = (
                            enemy[
                                "chapter4_boss_attack1_left_x_offset"
                            ]
                        )

                    chapter4_boss_attack_rect = pygame.Rect(
                        (
                            enemy_rect.centerx
                            + chapter4_boss_attack_x_offset
                        ),
                        (
                            enemy_rect.centery
                            + enemy["chapter4_boss_attack1_y_offset"]
                        ),
                        enemy["chapter4_boss_attack1_hitbox_width"],
                        enemy["chapter4_boss_attack1_hitbox_height"],
                    )

                elif enemy["state"] == "attack2":
                    chapter4_boss_attack_frame = int(enemy["frame_index"])
                    chapter4_boss_attack_active = (
                        chapter4_boss_attack_frame == 10
                    )
                    chapter4_boss_attack_damage = (
                        enemy["chapter4_boss_attack2_damage"]
                    )

                    if (
                        7 <= chapter4_boss_attack_frame <= 12
                        and not enemy["chapter4_boss_attack2_launched"]
                    ):
                        enemy["vel_y"] = (
                            enemy["chapter4_boss_attack2_jump_power"]
                        )
                        enemy["chapter4_boss_attack2_launched"] = True

                    if 7 <= chapter4_boss_attack_frame <= 12:
                        enemy["vel_x"] = (
                            enemy["chapter4_boss_attack2_speed"]
                            * enemy["direction"]
                        )

                    if enemy["direction"] == 1:
                        chapter4_boss_attack_x_offset = (
                            enemy[
                                "chapter4_boss_attack2_right_x_offset"
                            ]
                        )
                    else:
                        chapter4_boss_attack_x_offset = (
                            enemy[
                                "chapter4_boss_attack2_left_x_offset"
                            ]
                        )

                    chapter4_boss_attack_rect = pygame.Rect(
                        (
                            enemy_rect.centerx
                            + chapter4_boss_attack_x_offset
                        ),
                        (
                            enemy_rect.centery
                            + enemy["chapter4_boss_attack2_y_offset"]
                        ),
                        enemy["chapter4_boss_attack2_hitbox_width"],
                        enemy["chapter4_boss_attack2_hitbox_height"],
                    )

                else:
                    chapter4_boss_attack_active = False
                    chapter4_boss_attack_rect = None

                    if (
                        chapter4_boss_distance
                        <= enemy["chapter4_boss_attack2_range"]
                        and enemy["chapter4_boss_attack2_cooldown"] <= 0
                    ):
                        enemy["state"] = "attack2"
                        enemy["current_animation"] = "attack2"
                        enemy["frame_index"] = 0
                        enemy["chapter4_boss_attack_has_hit"] = False
                        enemy["chapter4_boss_attack2_launched"] = False
                        enemy["chapter4_boss_attack2_cooldown"] = (
                            enemy[
                                "chapter4_boss_attack2_cooldown_duration"
                            ]
                        )

                    elif (
                        chapter4_boss_distance
                        <= enemy["chapter4_boss_attack1_range"]
                    ):
                        enemy["state"] = "attack1"
                        enemy["current_animation"] = "attack1"
                        enemy["frame_index"] = 0
                        enemy["chapter4_boss_attack_has_hit"] = False

                    else:
                        enemy["state"] = "move"
                        enemy["vel_x"] = (
                            enemy["speed"] * enemy["direction"]
                        )
                        if enemy["current_animation"] != "move":
                            enemy["current_animation"] = "move"
                            enemy["frame_index"] = 0

                if chapter4_boss_is_attacking:
                    if chapter4_boss_attack_active:
                        enemy["chapter4_boss_attack_hitbox"] = (
                            chapter4_boss_attack_rect
                        )
                    else:
                        enemy["chapter4_boss_attack_hitbox"] = None

                    if (
                        chapter4_boss_attack_active
                        and not enemy["chapter4_boss_attack_has_hit"]
                        and player_invincible <= 0
                        and chapter4_boss_attack_rect.colliderect(player_rect)
                    ):
                        player_health -= chapter4_boss_attack_damage
                        player_health = max(player_health, 0)
                        player_invincible = 70
                        player_hitstun = 30
                        player_animation = "knockback"
                        player_frame_index = 0
                        attacking = False
                        combo_stage = 0
                        combo_window = False
                        combo_input = False
                        combo_timer = 0
                        attack_timer = 0
                        attack_hitbox = None
                        enemy["chapter4_boss_attack_has_hit"] = True

                        chapter4_boss_knockback = 30
                        if player_rect.centerx < enemy_rect.centerx:
                            player_knockback_velocity = (
                                -chapter4_boss_knockback
                            )
                            player_facing = 1
                        else:
                            player_knockback_velocity = (
                                chapter4_boss_knockback
                            )
                            player_facing = -1

            else:
                enemy["state"] = "idle"
                enemy["chapter4_boss_attack_hitbox"] = None
                if enemy["current_animation"] != "idle":
                    enemy["current_animation"] = "idle"
                    enemy["frame_index"] = 0

            enemy_rect.x += enemy["vel_x"]

            for wall in collision_walls:
                if enemy_rect.colliderect(wall):
                    if enemy["vel_x"] > 0:
                        enemy_rect.right = wall.left
                    elif enemy["vel_x"] < 0:
                        enemy_rect.left = wall.right

            enemy["vel_y"] += enemy["gravity"]
            enemy_rect.y += enemy["vel_y"]
            enemy["on_ground"] = False

            all_surfaces = [ground] + platforms + collision_walls

            for surface in all_surfaces:
                if (
                    enemy_rect.colliderect(surface)
                    and previous_bottom <= surface.top
                    and enemy["vel_y"] >= 0
                ):
                    enemy_rect.bottom = surface.top
                    enemy["vel_y"] = 0
                    enemy["on_ground"] = True

            enemy["hurtbox"].topleft = enemy_rect.topleft
            enemy["hurtbox"].size = enemy_rect.size

    # =====================
    # 이벤트 처리
    # =====================
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # 점프 입력
        if event.type == pygame.KEYDOWN:

            if (
                event.key == pygame.K_SPACE
                or event.key == pygame.K_w
                or event.key == pygame.K_UP
            ):

                # 점프 입력 저장
                input_buffer = "jump"
                input_buffer_timer = input_buffer_time

            if event.key == pygame.K_i:
                if can_interact:
                    player_health = player_max_health

            if event.key == pygame.K_1:
                warp_to_chapter(1)

            if event.key == pygame.K_2:
                warp_to_chapter(2)

            if event.key == pygame.K_3:
                warp_to_chapter(3)

            if event.key == pygame.K_4:
                warp_to_chapter(3, boss_start=True)

            if event.key == pygame.K_5:
                warp_to_chapter(4)

            if event.key == pygame.K_6:
                warp_to_chapter(4)
                player_rect.x = CHAPTER4_BOSS_SPAWN_X - 700
                player_rect.y = 455

            if event.key == pygame.K_7:
                warp_to_chapter(4)
                player_rect.x = MINI3_TRIGGER_X + 100
                player_rect.y = 455

            if (
                event.key == pygame.K_o
                and player_hitstun <= 0
                and not chapter_transition
                and not ending
            ):

                if attacking and combo_window:
                    combo_input = True

                elif not attacking and attack_cd <= 0:

                    if not on_ground and not air_attack_used:
                        attacking = True
                        player_animation = "air_attack"
                        player_frame_index = 0
                        attack_timer = 8
                        attack_cd = 20
                        hit_enemies = []
                        vel_y = -12

                        if player_facing == 1:

                            attack_hitbox = pygame.Rect(
                                player_rect.centerx - 155,
                                player_rect.centery - 280,
                                380, 440,
                            )
                        else:
                            attack_hitbox = pygame.Rect(
                                player_rect.centerx - 225,
                                player_rect.centery - 280,
                                380, 440,
                            )

                        air_attack_used = True

                    elif on_ground:
                        attacking = True
                        player_animation = "attack"
                        player_frame_index = float(draw_frames[0])
                        attack_timer = 9999999
                        combo_stage = 1
                        combo_window = False
                        combo_input = False
                        combo_timer = 0
                        attack_cd = 8
                        hit_enemies = []

                        attack_width = 300
                        attack_height = 150
                        if player_facing == 1:
                            attack_hitbox = pygame.Rect(
                                player_rect.x - 70,
                                player_rect.y + 20,
                                attack_width, attack_height,
                            )
                        else:
                            attack_hitbox = pygame.Rect(
                                player_rect.x - 170,
                                player_rect.y + 20,
                                attack_width, attack_height,
                            )

    # =====================
    # 플레이어 피격 판정
    # =====================

    if player_invincible > 0:
        player_invincible -= 1

    if player_hitstun > 0:
        player_hitstun -= 1

    if attack_cd > 0:
        attack_cd -= 1
    
    if attack_timer > 0:
        attack_timer -= 1
    else:
        attack_hitbox = None
        attacking = False

        if player_animation == "attack":
            player_animation = "idle"
            player_frame_index = 0

    player_hurtbox.x = player_rect.x
    player_hurtbox.y = player_rect.y

    player_hurtbox.width = player_rect.width
    player_hurtbox.height = player_rect.height

    for enemy in enemies:

        if (
            player_animation != "air_attack"
            and enemy["type"] not in (
                "enemy1",
                "miniboss1",
                "miniboss2",
                "mini3",
                "chapter4_boss",
            )
            and enemy["health"] > 0
            and player_hurtbox.colliderect(enemy["rect"])
        ):

            if player_invincible <= 0:

                # 체력 감소
                enemy_damage = enemy["damage"]
                if (
                    enemy["type"] == "miniboss1"
                    and enemy["state"] == "dash"
                ):
                    enemy_damage = enemy["dash_damage"]

                player_health -= enemy_damage

                # 무적 시간
                player_invincible = 70

                # 경직
                player_hitstun = 25
                player_animation = "knockback"
                player_frame_index = 0
                attacking = False
                combo_stage = 0
                combo_window = False
                combo_input = False
                combo_timer = 0
                attack_timer = 0
                attack_hitbox = None

                knockback_power = 14
                if player_rect.centerx < enemy["rect"].centerx:
                    player_knockback_velocity = -knockback_power
                    player_facing = 1
                else:
                    player_knockback_velocity = knockback_power
                    player_facing = -1

            if player_health < 0:
                player_health = 0
    
    # =====================
    # 플레이어 피격 판정
    # =====================

    if attack_hitbox:

        for enemy in enemies:

            if enemy not in hit_enemies:

                if attack_hitbox.colliderect(
                    enemy["hurtbox"]
                ):
                    damage_to_enemy = player_attack_damage

                    if (
                        enemy["type"] == "chapter4_boss"
                        and enemy["state"] in ("waa", "waa_hold")
                    ):
                        damage_to_enemy *= 0.25

                    enemy["health"] -= damage_to_enemy

                    if enemy["type"] in (
                        "enemy1",
                        "enemy2",
                        "enemy3",
                        "enemy4",
                    ):
                        if player_rect.centerx > enemy["rect"].centerx:
                            enemy["direction"] = 1
                        elif player_rect.centerx < enemy["rect"].centerx:
                            enemy["direction"] = -1

                    if enemy["type"] not in (
                        "miniboss1",
                        "miniboss2",
                        "mini3",
                        "chapter4_boss",
                    ):
                        enemy["hitstun"] = 12
                        knockback_power = 50

                        if player_rect.centerx < enemy["rect"].centerx:
                            enemy["rect"].x += knockback_power
                            
                            for wall in collision_walls:
                                if enemy["rect"].colliderect(wall):
                                    enemy["rect"].right = wall.left

                            if enemy["type"] == "enemy3":
                                enemy["x"] = float(enemy["rect"].x)
                        else:
                            enemy["rect"].x -= knockback_power
                            
                            for wall in collision_walls:
                                if enemy["rect"].colliderect(wall):
                                    enemy["rect"].left = wall.right

                            if enemy["type"] == "enemy3":
                                enemy["x"] = float(enemy["rect"].x)

                    hit_enemies.append(enemy)
        # 체력 0 이하 적 제거
        if any(
            enemy["type"] == "miniboss1"
            and enemy.get("death_finished", False)
            for enemy in enemies
        ):
            chapter1_miniboss_defeated = True
            boss_fight_started = False
            boss_walls = []

        if any(
            enemy["type"] == "miniboss2"
            and enemy["health"] <= 0
            for enemy in enemies
        ):
            chapter3_miniboss_defeated = True
            chapter3_boss_fight_started = False
            boss_walls = []

        if any(
            enemy["type"] == "mini3"
            and enemy.get("death_finished", False)
            for enemy in enemies
        ):
            mini3_defeated = True
            mini3_boss_fight_started = False
            boss_walls = []

        if any(
            enemy["type"] == "chapter4_boss"
            and enemy.get("death_finished", False)
            for enemy in enemies
        ):
            chapter4_boss_defeated = True
            chapter4_boss_fight_started = False

        enemies = [
            enemy
            for enemy in enemies
            if (
                enemy["health"] > 0
                or (
                    enemy["type"] == "enemy1"
                    and not enemy.get("death_finished", False)
                )
                or (
                    enemy["type"] == "enemy2"
                    and not enemy.get("death_finished", False)
                )
                or (
                    enemy["type"] == "miniboss1"
                    and not enemy.get("death_finished", False)
                )
                or (
                    enemy["type"] == "miniboss2"
                    and not enemy.get("death_finished", False)
                )
                or (
                    enemy["type"] == "mini3"
                    and not enemy.get("death_finished", False)
                )
                or (
                    enemy["type"] == "chapter4_boss"
                    and not enemy.get("death_finished", False)
                )
            )
        ]

    if any(
        enemy["type"] == "miniboss1"
        and enemy.get("death_finished", False)
        for enemy in enemies
    ):
        chapter1_miniboss_defeated = True
        boss_fight_started = False
        boss_walls = []

    if any(
        enemy["type"] == "mini3"
        and enemy.get("death_finished", False)
        for enemy in enemies
    ):
        mini3_defeated = True
        mini3_boss_fight_started = False
        boss_walls = []

    if any(
        enemy["type"] == "chapter4_boss"
        and enemy.get("death_finished", False)
        for enemy in enemies
    ):
        chapter4_boss_defeated = True
        chapter4_boss_fight_started = False

    enemies = [
        enemy
        for enemy in enemies
        if not (
            enemy["type"] in (
                "enemy1",
                "enemy2",
                "miniboss1",
                "miniboss2",
                "mini3",
                "chapter4_boss",
            )
            and enemy.get("death_finished", False)
        )
    ]

    can_interact = False
    current_heal_objects = None

    for obj in heal_objects:

        if player_rect.colliderect(obj):

            can_interact = True
            current_heal_objects = obj
            break
    # =====================
    # 입력 처리
    # =====================
    keys = pygame.key.get_pressed()

    dx = 0

    if (
        player_hitstun <= 0
        and not attacking
        and not chapter_transition
        and not ending
    ):
        if keys[pygame.K_a]:
            dx = -move_speed
            player_facing = -1
        
        if keys[pygame.K_d]:
            dx = move_speed
            player_facing = 1

        if not attacking:
            if not on_ground:
                if vel_y < 0:
                    new_animation = "jump"
                
                else:
                    new_animation = "down"
            
            else:
                if dx != 0:
                    new_animation = "run"
                else:
                    new_animation = "idle"

            if new_animation != player_animation:
                player_animation = new_animation
                player_frame_index = 0

    elif player_hitstun > 0:
        dx = int(player_knockback_velocity)
        player_knockback_velocity *= 0.86

        if abs(player_knockback_velocity) < 0.2:
            player_knockback_velocity = 0

    if ending:
        dx = 0

    # =====================
    # X 이동
    # =====================
    player_rect.x += dx

    # 벽 X 충돌
    for wall in collision_walls:

        if player_rect.colliderect(wall):

            # 오른쪽 이동
            if dx > 0:
                player_rect.right = wall.left

            # 왼쪽 이동
            elif dx < 0:
                player_rect.left = wall.right

    if current_chapter == 1 and player_rect.left < 0:
        player_rect.left = 0

    if current_chapter == 4 and player_rect.right >= WORLD_WIDTH:
        player_rect.right = WORLD_WIDTH

        if chapter4_boss_defeated:
            ending = True

    # 월드 경계
    if (
        current_chapter == 1
        and player_rect.right >= WORLD_WIDTH
        and not fading
    ):
        fading = True
        chapter_transition = True
        fade_direction = 1
        next_chapter = 2

    elif (
        current_chapter == 2
        and player_rect.right >= WORLD_WIDTH
        and not fading
    ):
        fading = True
        chapter_transition = True
        fade_direction = 1
        next_chapter = 3

    elif (
        current_chapter == 3
        and player_rect.right >= WORLD_WIDTH
        and not fading
    ):
        fading = True
        chapter_transition = True
        fade_direction = 1
        next_chapter = 4

    elif (
        current_chapter == 2
        and player_rect.left <= 0
        and not fading
    ):
        fading = True
        chapter_transition = True
        fade_direction = 1
        next_chapter = 1

    elif (
        current_chapter == 3
        and player_rect.left <= 0
        and not fading
    ):
        fading = True
        chapter_transition = True
        fade_direction = 1
        next_chapter = 2

    elif (
        current_chapter == 4
        and player_rect.left <= 0
        and not fading
    ):
        fading = True
        chapter_transition = True
        fade_direction = 1
        next_chapter = 3

    # =====================
    # Y 이동 준비
    # =====================
    previous_bottom = player_rect.bottom

    was_on_ground = on_ground

    on_ground = False

    # =====================
    # 점프 버퍼 감소
    # =====================
    if input_buffer_timer > 0:
        input_buffer_timer -= 1
    else:
        input_buffer = None

    # =====================
    # 코요테 감소
    # =====================
    if coyote_timer > 0:
        coyote_timer -= 1

    # =====================
    # 점프 실행
    # =====================
    if (
        input_buffer == "jump"
        and player_hitstun <= 0
        and not attacking
        and not chapter_transition
        and not ending
    ):

        # 일반 점프
        if was_on_ground or coyote_timer > 0:

            vel_y = jump_power
            on_ground = False
            coyote_timer = 0
            input_buffer_timer = 0

        # 공중 점프
        elif extra_jumps > 0:
            vel_y = jump_power
            extra_jumps -= 1
            input_buffer = None

    # =====================
    # 중력
    # =====================
    vel_y += gravity

    # Y 이동
    player_rect.y += vel_y

    # =====================
    # 플랫폼 충돌
    # =====================
    all_surfaces = [ground] + platforms + collision_walls

    for surface in all_surfaces:

        if player_rect.colliderect(surface):

            # 위에서 떨어졌을 때만
            if previous_bottom <= surface.top and vel_y >= 0:

                player_rect.bottom = surface.top
                vel_y = 0
                on_ground = True
                extra_jumps = 1
                coyote_timer = coyote_time
                air_attack_used = False

    # =====================
    # 벽 Y 충돌
    # =====================
    for wall in collision_walls:

        if player_rect.colliderect(wall):

            # 떨어지는 중
            if vel_y > 0:

                player_rect.bottom = wall.top
                vel_y = 0
                on_ground = True
                extra_jumps = 1
                coyote_timer = coyote_time
                air_attack_used = False

            # 위로 점프 중
            elif vel_y < 0:

                player_rect.top = wall.bottom

                vel_y = 0

    if not attacking and player_hitstun <= 0:

        if not on_ground:

            if vel_y < 0:
                new_animation = "jump"
            else:
                new_animation = "down"

        else:

            if dx != 0:
                new_animation = "run"
            else:
                new_animation = "idle"

        if new_animation != player_animation:
            player_animation = new_animation
            player_frame_index = 0

    # =====================
    # 카메라
    # =====================
    target_x = player_rect.centerx - WIDTH // 2
    target_y = player_rect.centery - HEIGHT // 2 - 60

    camera_x += (target_x - camera_x) * 0.1
    camera_y += (target_y - camera_y) * 0.1

    if camera_x < 0:
        camera_x =0
    
    if camera_x > WORLD_WIDTH - WIDTH:
        camera_x = WORLD_WIDTH - WIDTH

    if fading:

        fade_alpha += fade_direction * 12

        if fade_alpha >= 255:

            fade_alpha = 255

            previous_chapter = current_chapter
            current_chapter = next_chapter

            if current_chapter == 1:

                (
                    platforms,
                    walls,
                    heal_objects,
                    enemies,
                    bg1_objects,
                    fog_objects
                ) = load_chapter_1()

                WORLD_WIDTH = CHAPTER_WIDTHS[1]

                player_rect.x = CHAPTER_SPAWN[1]["right"]
                player_rect.y = 455

                camera_x = WORLD_WIDTH - WIDTH

            elif current_chapter == 2:

                (
                    platforms,
                    walls,
                    heal_objects,
                    enemies,
                    bg1_objects,
                    fog_objects
                ) = load_chapter_2()

                WORLD_WIDTH = CHAPTER_WIDTHS[2]

                if previous_chapter == 3:
                    player_rect.x = CHAPTER_SPAWN[2]["right"]
                else:
                    player_rect.x = CHAPTER_SPAWN[2]["left"]
                player_rect.y = 455

                if previous_chapter == 3:
                    camera_x = WORLD_WIDTH - WIDTH
                else:
                    camera_x = 0

            elif current_chapter == 3:

                (
                    platforms,
                    walls,
                    heal_objects,
                    enemies,
                    bg1_objects,
                    fog_objects
                ) = load_chapter_3()

                WORLD_WIDTH = CHAPTER_WIDTHS[3]

                if previous_chapter == 4:
                    player_rect.x = CHAPTER_SPAWN[3]["right"]
                else:
                    player_rect.x = CHAPTER_SPAWN[3]["left"]
                player_rect.y = 455

                if previous_chapter == 4:
                    camera_x = WORLD_WIDTH - WIDTH
                else:
                    camera_x = 0

            else:

                (
                    platforms,
                    walls,
                    heal_objects,
                    enemies,
                    bg1_objects,
                    fog_objects
                ) = load_chapter_4()

                WORLD_WIDTH = CHAPTER_WIDTHS[4]

                player_rect.x = CHAPTER_SPAWN[4]["left"]
                player_rect.y = 455

                camera_x = 0

            ground = pygame.Rect(
                0,
                HEIGHT - 80,
                WORLD_WIDTH,
                80
            )
            boss_walls = []
            collision_walls = walls

            fade_direction = -1

        elif fade_alpha <= 0:

            fade_alpha = 0
            fading = False
            chapter_transition = False

    # =====================
    # 렌더링
    # =====================
    screen.fill(BG_COLOR)

    # 배경
    for obj in bg1_objects:

        image = obj["image"]

        draw_x = (
            obj["x"]
            - camera_x * obj["parallax_x"]
        )

        draw_y = (
            obj["y"]
            - camera_y * obj["parallax_y"]
        )

        screen.blit(
            image,
            (
                draw_x,
                draw_y
            )
        )

    # 바닥
    pygame.draw.rect(
        screen,
        GROUND_COLOR,
        (
            ground.x - camera_x,
            ground.y - camera_y,
            ground.width,
            300#ground.height
        )
    )

    # 플랫폼
    for platform in platforms:

        pygame.draw.rect(
            screen,
            PLATFORM_COLOR,
            (
                platform.x - camera_x,
                platform.y - camera_y,
                platform.width,
                platform.height
            )
        )

    # 벽
    for wall in walls:

        pygame.draw.rect(
            screen,
            WALL_COLOR,
            (
                wall.x - camera_x,
                wall.y - camera_y,
                wall.width,
                wall.height
            )
        )

    for wall in boss_walls:

        pygame.draw.rect(
            screen,
            BOSS_WALL_COLOR,
            (
                wall.x - camera_x,
                wall.y - camera_y,
                wall.width,
                wall.height
            )
        )

    for obj in heal_objects:

        pygame.draw.rect(
            screen,
            (0, 255, 255),
            (
                obj.x - camera_x,
                obj.y - camera_y,
                obj.width,
                obj.height
            )
        )

    # 적
    for enemy in enemies:

        if enemy.get("faces_right", False):
            should_flip = enemy["direction"] == -1
        else:
            should_flip = enemy["direction"] == 1

        if should_flip:
            animation = enemy["flipped_animations"][
                enemy["current_animation"]
            ]
        else:
            animation = enemy["animations"][
                enemy["current_animation"]
            ]

        image = animation[
            int(enemy["frame_index"])
        ]

        if enemy.get("use_player_style_draw", False):
            enemy_draw_x = (
                enemy["rect"].centerx
                - image.get_width() // 2
            )
            enemy_draw_x += enemy["draw_offset_x"]

            enemy_draw_y = (
                enemy["rect"].bottom
                - image.get_height()
            )
            enemy_draw_y += enemy["draw_offset_y"]

            if enemy["direction"] == 1:
                enemy_draw_x += enemy["draw_right_offset_x"]
            elif enemy["direction"] == -1:
                enemy_draw_x += enemy["draw_left_offset_x"]

        else:
            enemy_draw_x = (
                enemy["rect"].x
                + enemy["sprite_offset_x"]
            )
            enemy_draw_y = (
                enemy["rect"].y
                + enemy["sprite_offset_y"]
            )

        screen.blit(
            image,
            (
                int(enemy_draw_x - camera_x),
                int(enemy_draw_y - camera_y)
            )
        )

        # 히트박스 보기
        pygame.draw.rect(
            screen,
            (255, 0, 0),
            (
                enemy["rect"].x - camera_x,
                enemy["rect"].y - camera_y,
                (
                    0
                    if enemy.get("dead", False)
                    else enemy["rect"].width
                ),
                (
                    0
                    if enemy.get("dead", False)
                    else enemy["rect"].height
                )
            ),
            2
        )

        pygame.draw.rect(
            screen,
            (0, 0, 255),
            (
                enemy["hurtbox"].x - camera_x,
                enemy["hurtbox"].y - camera_y,
                enemy["hurtbox"].width,
                enemy["hurtbox"].height,
            ),
            2
        )

        if enemy.get("mini2_attack_hitbox") is not None:
            pygame.draw.rect(
                screen,
                (255, 220, 0),
                (
                    enemy["mini2_attack_hitbox"].x - camera_x,
                    enemy["mini2_attack_hitbox"].y - camera_y,
                    enemy["mini2_attack_hitbox"].width,
                    enemy["mini2_attack_hitbox"].height,
                ),
                3
            )

        if enemy.get("enemy1_attack_hitbox") is not None:
            pygame.draw.rect(
                screen,
                (255, 220, 0),
                (
                    enemy["enemy1_attack_hitbox"].x - camera_x,
                    enemy["enemy1_attack_hitbox"].y - camera_y,
                    enemy["enemy1_attack_hitbox"].width,
                    enemy["enemy1_attack_hitbox"].height,
                ),
                3
            )

        if enemy.get("attack_hitbox") is not None:
            pygame.draw.rect(
                screen,
                (255, 170, 0),
                (
                    enemy["attack_hitbox"].x - camera_x,
                    enemy["attack_hitbox"].y - camera_y,
                    enemy["attack_hitbox"].width,
                    enemy["attack_hitbox"].height,
                ),
                3
            )

        if enemy.get("mini3_attack_hitbox") is not None:
            pygame.draw.rect(
                screen,
                (255, 220, 0),
                (
                    enemy["mini3_attack_hitbox"].x - camera_x,
                    enemy["mini3_attack_hitbox"].y - camera_y,
                    enemy["mini3_attack_hitbox"].width,
                    enemy["mini3_attack_hitbox"].height,
                ),
                3
            )

        if enemy.get("chapter4_boss_attack_hitbox") is not None:
            pygame.draw.rect(
                screen,
                (255, 180, 0),
                (
                    enemy["chapter4_boss_attack_hitbox"].x - camera_x,
                    enemy["chapter4_boss_attack_hitbox"].y - camera_y,
                    enemy["chapter4_boss_attack_hitbox"].width,
                    enemy["chapter4_boss_attack_hitbox"].height,
                ),
                3
            )

    # 플레이어
    frame = min(
        int(player_frame_index),
        len(player_animations[player_animation]) - 1
    )

    if player_facing == -1:
        player_image = player_flipped_animations[
            player_animation
        ][
            frame
        ]
    else:
        player_image = player_animations[
            player_animation
        ][
            frame
        ]

    draw_x = (
        player_rect.centerx
        - player_image.get_width() // 2
    )
    draw_x += 30

    draw_y = (
        player_rect.bottom- player_image.get_height()
    )
    draw_y += 110

    if player_facing == 1:
        draw_x -= 60
    elif player_facing == -1:
        draw_x += 0

    screen.blit(
        player_image,
        (
            draw_x - camera_x,
            draw_y - camera_y
        )
    )

    #허트박스
    pygame.draw.rect(
        screen,
        (0, 255, 0),
        (
            player_hurtbox.x - camera_x,
            player_hurtbox.y - camera_y,
            player_hurtbox.width,
            player_hurtbox.height
        ),
        2
    )
        

    # 플레이어 공격 히트박스
    if attack_hitbox:
        pygame.draw.rect(
            screen,
            (255, 0, 0),
            (
                attack_hitbox.x - camera_x,
                attack_hitbox.y - camera_y,
                attack_hitbox.width,
                attack_hitbox.height
            ),
            2
        )

    for obj in fog_objects:

        image = obj["image"]

        draw_x = (WIDTH - obj["w"]) // 2
        draw_y = (HEIGHT - obj["h"]) // 2

        screen.blit(
            image,
            (
                draw_x,
                draw_y
            )
        )

    # =====================
    # 체력바 배경
    #=====================

    pygame.draw.rect(
        screen,
        (50, 50, 50),
        (30, 30, 600, 30)
    )

    # =====================
    # 현재 체력
    # =====================

    health_width = int(
        (player_health / player_max_health)
        *600
    )

    health_width = max(
        0,
        min(600, health_width)
    )

    pygame.draw.rect(
        screen,
        (220, 40, 40),
        (30, 30, health_width, 30)
    )

    # 테두리
    pygame.draw.rect(
        screen,
        (255, 255, 255),
        (30, 30, 600, 30),
        2
    )

    if can_interact:

        font = pygame.font.Font(None, 40)

        text = font.render(
            "Press I",
            True,
            (255,255,255)
        )

        screen.blit(
            text,
            (
                player_rect.x - camera_x,
                player_rect.y - 50 - camera_y
            )
        )

    fps_text = fps_font.render(
        f"FPS {int(clock.get_fps())}",
        True,
        (255, 255, 255)
    )

    screen.blit(
        fps_text,
        (30, 65)
    )

    chapter4_boss_enemy = next(
        (
            enemy
            for enemy in enemies
            if enemy["type"] == "chapter4_boss"
        ),
        None
    )

    if (
        current_chapter == 4
        and chapter4_boss_fight_started
        and chapter4_boss_enemy is not None
    ):
        boss_bar_width = 700
        boss_bar_height = 24
        boss_bar_x = (WIDTH - boss_bar_width) // 2
        boss_bar_y = HEIGHT - 55
        boss_health_ratio = max(
            0,
            min(1, chapter4_boss_enemy["health"] / 600)
        )

        pygame.draw.rect(
            screen,
            (35, 35, 35),
            (
                boss_bar_x,
                boss_bar_y,
                boss_bar_width,
                boss_bar_height,
            )
        )
        pygame.draw.rect(
            screen,
            (180, 35, 35),
            (
                boss_bar_x,
                boss_bar_y,
                int(boss_bar_width * boss_health_ratio),
                boss_bar_height,
            )
        )
        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (
                boss_bar_x,
                boss_bar_y,
                boss_bar_width,
                boss_bar_height,
            ),
            2
        )

    if fade_alpha > 0:

        fade_surface.set_alpha(
            int(fade_alpha)
        )

        screen.blit(
            fade_surface,
            (0, 0)
        )

    if ending:
        ending_overlay = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )
        ending_overlay.fill((0, 0, 0, 230))
        screen.blit(ending_overlay, (0, 0))

        ending_text = ending_font.render(
            "ENDING",
            True,
            (255, 255, 255)
        )
        screen.blit(
            ending_text,
            ending_text.get_rect(
                center=(WIDTH // 2, HEIGHT // 2)
            )
        )

    pygame.display.flip()

pygame.quit()
sys.exit()
