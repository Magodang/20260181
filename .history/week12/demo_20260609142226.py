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


pygame.init()

WIDTH = 1280
HEIGHT = 720

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Demo")

clock = pygame.time.Clock()

BG_COLOR = (18, 18, 18)
GROUND_COLOR = (45, 45, 45)
PLATFORM_COLOR = (90, 90, 90)
WALL_COLOR = (130, 130, 130)
PLAYER_COLOR = (220, 220, 220)
ENEMY_COLOR = (170, 170, 170)

WORLD_WIDTH = 16000

ground = pygame.Rect(0, HEIGHT - 80, WORLD_WIDTH, 80)

player_idle_sheet = SpriteSheet("week12/assets/cha/ryo_idle.png")

player_run_sheet = SpriteSheet("week12/assets/cha/ryo_run.png")

player_attack_sheet = SpriteSheet("week12/assets/cha/ryo_attack.png")

player_air_attack_sheet = SpriteSheet("week12/assets/cha/ryo_jump_attack.png")

player_jump_sheet = SpriteSheet("week12/assets/cha/ryo_jump.png")

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
}

enemy1_sheet = SpriteSheet("week12/assets/cha/en1.png")

enemy1_animations = {
    "idle": load_animation(
        enemy1_sheet,
        245,
        220,
        2,
        scale = 0.5
    )
}

enemy2_sheet = SpriteSheet("week12/assets/cha/en2.png")

enemy2_animations = {

    "idle": load_animation(

        enemy2_sheet,
        250,
        220,
        2,
        scale=0.4
    )
}

# 플랫폼
platforms = [
    pygame.Rect(300, 560, 200, 20),
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

def enemy1(x, y):

    collision_rect = pygame.Rect(
        x - 20,
        y + 10,
        70,
        70,
    )

    hurtbox = pygame.Rect(
        x + 20,
        y + 15,
        100,
        105,
    )

    return {
        "type": "enemy1",
        "rect": collision_rect,
        "hurtbox": hurtbox,
        "sprite_offset_x": -20,
        "sprite_offset_y": -35,
        "animations": enemy1_animations,
        "current_animation": "idle",
        "frame_index": 0,
        "animation_speed": 0.05,
        "health": 30,
        "speed": 1.5,
        "damage": 20,
        "direction": 1,
        "start_x": x,
        "patrol_range": 200,
        "detect_range": 400,
        "aggro": False,
        "chase_range": 700,
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
        "sprite_offset_x": -22,
        "sprite_offset_y": -13,
        "animations": enemy2_animations,
        "current_animation": "idle",
        "frame_index": 0,
        "animation_speed": 0.04,
        "health": 10,
        "speed":1,
        "damage": 20,
        "direction": 1,
        "start_x": x,
        "patrol_range": 350,
        "detect_range": 350,
        "aggro": False,
        "chase_range": 1200,
        "velocity_x": 0,
        "velocity_y": 0,
        "hitstun": 0
    }

# 적
enemies = [

        enemy1(3100, 200),
        enemy2(4750, 20),
        enemy2(4820, -100),
        enemy1(5600, 550),
        enemy1(5800, 550),
        enemy2(5900, 250),
        enemy1(6200, 550),

]

player_rect = pygame.Rect(100, 455, 60, 180)
player_hurtbox = pygame.Rect(0, 0, 380, 400)

player_animation = "idle"
player_frame_index = 0
idle_animation_speed = 0.1
run_animation_speed = 0.2
attack_animation_speed = 0.4
air_attack_animation_speed = 0.2

vel_y = 0

move_speed = 8
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

# =========================
# 게임 루프
# =========================
running = True

while running:

    dt = clock.tick(60)

    idle_animation_speed = 0.1
    run_animation_speed = 0.2
    attack_animation_speed = 0.4

    animation = player_animations[player_animation]

    if not attacking:

        animation = player_animations[player_animation]

        if player_animation == "idle":
            player_frame_index += idle_animation_speed

        elif player_animation == "run":
            player_frame_index += run_animation_speed

        elif player_animation in ("jump", "down"):
            player_frame_index = 0

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
        enemy["frame_index"] += enemy["animation_speed"]
        animation = enemy["animations"][
            enemy["current_animation"]
        ]
        if enemy["frame_index"] >= len(animation):
            enemy["frame_index"] = 0
            
    # =========================
    # 적 AI
    # =========================
    for enemy in enemies:

        if enemy["type"] == "enemy1":
            enemy["hurtbox"].topleft = (
                enemy["rect"].x - 15,
                enemy["rect"].y - 35
            )

        elif enemy["type"] == "enemy2":
            enemy["hurtbox"].topleft = (
                enemy["rect"].x - 19,
                enemy["rect"].y - 15
            )

        if enemy["hitstun"] > 0:
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

            enemy["hurtbox"].x = enemy["rect"].x - 15
            enemy["hurtbox"].y = enemy["rect"].y - 35

        elif enemy["type"] == "enemy2":

            enemy["hurtbox"].x = enemy["rect"].x - 19
            enemy["hurtbox"].y = enemy["rect"].y - 15

        # =====================
        # 플레이어 인식
        # =====================
        if abs(distance_x) < enemy["detect_range"]:
            enemy["aggro"] = True

        elif abs(distance_x) > enemy["chase_range"]:
            enemy["aggro"] = False

        # =====================
        # enemy1
        # =====================
        if enemy["type"] == "enemy1":

            # -----------------
            # X 이동
            # -----------------
            enemy_rect.x += enemy["vel_x"]

            # -----------------
            # 중력
            # -----------------
            previous_bottom = enemy_rect.bottom

            enemy["vel_y"] += enemy["gravity"]
            enemy_rect.y += enemy["vel_y"]
            enemy["on_ground"] = False

            # -----------------
            # 바닥 충돌
            # -----------------
            all_surfaces = [ground] + platforms + walls

            for surface in all_surfaces:

                if enemy_rect.colliderect(surface):

                    if (
                        previous_bottom <= surface.top
                        and enemy["vel_y"] >= 0
                    ):
                        enemy_rect.bottom = surface.top
                        enemy["vel_y"] = 0
                        enemy["on_ground"] = True

            # -----------------
            # 벽 충돌
            # -----------------
            for wall in walls:

                if enemy_rect.colliderect(wall):

                    if enemy["vel_x"] > 0:
                        enemy_rect.right = wall.left

                    elif enemy["vel_x"] < 0:
                        enemy_rect.left = wall.right

            # -----------------
            # 추적
            # -----------------
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

            if enemy["aggro"]:

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

                for wall in walls:
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
                for wall in walls:
                    if enemy_rect.colliderect(wall):
                        if enemy["velocity_y"] > 0:
                            enemy_rect.bottom = wall.top
                        elif enemy["velocity_y"] < 0:
                            enemy_rect.top = wall.bottom
                        # 벽에 가로막혔으므로 Y축 속도 초기화
                        enemy["velocity_y"] = 0
                            
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

            if event.key == pygame.K_o and player_hitstun <= 0:

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
            and player_hurtbox.colliderect(enemy["rect"])
        ):

            if player_invincible <= 0:

                # 체력 감소
                player_health -= enemy["damage"]

                # 무적 시간
                player_invincible = 100

                # 경직
                player_hitstun = 45

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
                    enemy["health"] -= (
                        player_attack_damage
                    )

                    enemy["hitstun"] = 12
                    knockback_power = 35

                    if player_rect.centerx < enemy["rect"].centerx:
                        enemy["rect"].x += knockback_power
                        
                        for wall in walls:
                            if enemy["rect"].colliderect(wall):
                                enemy["rect"].right = wall.left
                    else:
                        enemy["rect"].x -= knockback_power
                        
                        for wall in walls:
                            if enemy["rect"].colliderect(wall):
                                enemy["rect"].left = wall.right

                    hit_enemies.append(enemy)
        # 체력 0 이하 적 제거
        enemies = [
            enemy
            for enemy in enemies
            if enemy["health"] > 0
        ]

    # =====================
    # 입력 처리
    # =====================
    keys = pygame.key.get_pressed()

    dx = 0

    if player_hitstun <= 0 and not attacking:
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

    # =====================
    # X 이동
    # =====================
    player_rect.x += dx

    # 벽 X 충돌
    for wall in walls:

        if player_rect.colliderect(wall):

            # 오른쪽 이동
            if dx > 0:
                player_rect.right = wall.left

            # 왼쪽 이동
            elif dx < 0:
                player_rect.left = wall.right

    # 월드 경계
    if player_rect.left < 0:
        player_rect.left = 0

    if player_rect.right > WORLD_WIDTH:
        player_rect.right = WORLD_WIDTH

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
    if input_buffer == "jump" and player_hitstun <= 0 and not attacking:

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
    all_surfaces = [ground] + platforms + walls

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
    for wall in walls:

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

    # =====================
    # 렌더링
    # =====================
    screen.fill(BG_COLOR)

    # 바닥
    pygame.draw.rect(
        screen,
        GROUND_COLOR,
        (
            ground.x - camera_x,
            ground.y - camera_y,
            ground.width,
            ground.height
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

    # 적
    for enemy in enemies:

        animation = enemy["animations"][
            enemy["current_animation"]
        ]

        image = animation[
            int(enemy["frame_index"])
        ]

        if enemy["direction"] == 1:
            image = pygame.transform.flip(
                image,
                True,
                False
            )

        screen.blit(
            image,
            (
                int(
                    enemy["rect"].x
                    + enemy["sprite_offset_x"]
                    - camera_x
                ),
                int(
                    enemy["rect"].y
                    + enemy["sprite_offset_y"]
                    - camera_y
                )
            )
        )

        # 히트박스 보기
        pygame.draw.rect(
            screen,
            (255, 0, 0),
            (
                enemy["rect"].x - camera_x,
                enemy["rect"].y - camera_y,
                enemy["rect"].width,
                enemy["rect"].height
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

    # 플레이어
    frame = min(
        int(player_frame_index),
        len(player_animations[player_animation]) - 1
    )

    player_image = player_animations[
        player_animation
    ][
        frame
    ]
    
    if player_facing == -1:
        player_image = pygame.transform.flip(
            player_image,
            True,
            False
        )

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

    pygame.display.flip()

pygame.quit()
sys.exit()