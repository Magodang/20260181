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

WORLD_WIDTH = 4000

ground = pygame.Rect(0, HEIGHT - 80, WORLD_WIDTH, 80)

enemy1_sheet = SpriteSheet("week12/assets/en1.png")

enemy1_animations = {
    "idle": load_animation(
        enemy1_sheet,
        245,
        220,
        2,
        scale = 0.5
    )
}

enemy2_sheet = SpriteSheet(
    "week12/assets/en2.png"
)

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
    pygame.Rect(650, 470, 180, 20),
    pygame.Rect(980, 380, 220, 20),
    pygame.Rect(1400, 500, 250, 20),
    pygame.Rect(1800, 420, 180, 20),
    pygame.Rect(2200, 320, 220, 20),
    pygame.Rect(2600, 450, 300, 20),
    pygame.Rect(3200, 350, 200, 20),
]

# 벽
walls = [
    pygame.Rect(500, 520, 80, 120),
    pygame.Rect(1200, 520, 120, 220),
    pygame.Rect(2100, 520, 100, 170),
]

def enemy1(x, y):

    collision_rect = pygame.Rect(
        x-20,
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
        "speed": 2,
        "damage": 20,
        "direction": 1,
        "start_x": x,
        "patrol_range": 200,
        "detect_range": 400,
        "aggro": False,
        "chase_range": 700,
        "vel_y": 0,
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
        "speed":3,
        "damage": 20,
        "direction": 1,
        "start_x": x,
        "patrol_range": 350,
        "detect_range": 700,
        "aggro": False,
        "chase_range": 1200,
        "velocity_x": 0,
        "velocity_y": 0,
    }

# 적
enemies = [

        enemy1(750, HEIGHT - 300),
        enemy1(1400, HEIGHT - 300),
        enemy1(2200, HEIGHT - 300),
        enemy2(1600, HEIGHT - 300),

]

player = pygame.Rect(100, HEIGHT - 200, 60, 100)

vel_y = 0

move_speed = 6
jump_power = -16
gravity = 0.8
on_ground = False
extra_jumps = 1
coyote_time = 6
coyote_timer = 0
input_buffer = None
input_buffer_time = 6
input_buffer_timer = 0

camera_x = 0
camera_y = 0

player_health = 100
player_max_health = 100

player_invincible = 0
player_hitstun = 0

# =========================
# 게임 루프
# =========================
running = True

while running:

    dt = clock.tick(60)

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

        enemy_rect = enemy["rect"]

        distance_x = (
            player.centerx
            - enemy_rect.centerx
        )

        distance_y = (
            player.centery
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
            # 중력
            # -----------------
            enemy["vel_y"] += enemy["gravity"]
            enemy_rect.y += enemy["vel_y"]
            enemy["on_ground"] = False

            # -----------------
            # 바닥 충돌
            # -----------------
            all_surfaces = [ground] + platforms

            for surface in all_surfaces:

                if enemy_rect.colliderect(surface):

                    if enemy["vel_y"] >= 0:
                        enemy_rect.bottom = surface.top
                        enemy["vel_y"] = 0
                        enemy["on_ground"] = True

            # -----------------
            # 벽 충돌
            # -----------------
            for wall in walls:

                if enemy_rect.colliderect(wall):

                    if enemy["direction"] == 1:
                        enemy_rect.right = wall.left

                    else:
                        enemy_rect.left = wall.right

            # -----------------
            # 추적
            # -----------------
            if enemy["aggro"]:

                if distance_x > 0:
                    enemy_rect.x += enemy["speed"]
                    enemy["direction"] = 1

                elif distance_x < 0:
                    enemy_rect.x -= enemy["speed"]
                    enemy["direction"] = -1

        # =====================
        # enemy2
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
                # 부드러운 이동
                # -----------------
                enemy["velocity_x"] += (
                    target_vel_x
                    - enemy["velocity_x"]
                ) * 0.05

                enemy["velocity_y"] += (
                    target_vel_y
                    - enemy["velocity_y"]
                ) * 0.05

                enemy_rect.x += enemy["velocity_x"]
                enemy_rect.y += enemy["velocity_y"]

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

    # =====================
    # 플레이어 피격 판정
    # =====================

    if player_invincible > 0:
        player_invincible -= 1

    if player_hitstun > 0:
        player_hitstun -= 1

    for enemy in enemies:

        if player.colliderect(enemy["hurtbox"]):

            if player_invincible <= 0:

                # 체력 감소
                player_health -= enemy["damage"]

                # 무적 시간
                player_invincible = 120

                # 경직
                player_hitstun = 45

            if player_health < 0:
                player_health = 0

    # =====================
    # 입력 처리
    # =====================
    keys = pygame.key.get_pressed()

    dx = 0

    if player_hitstun <= 0:
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx = -move_speed
        
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx = move_speed

    # =====================
    # X 이동
    # =====================
    player.x += dx

    # 벽 X 충돌
    for wall in walls:

        if player.colliderect(wall):

            # 오른쪽 이동
            if dx > 0:
                player.right = wall.left

            # 왼쪽 이동
            elif dx < 0:
                player.left = wall.right

    # 월드 경계
    if player.left < 0:
        player.left = 0

    if player.right > WORLD_WIDTH:
        player.right = WORLD_WIDTH

    # =====================
    # Y 이동 준비
    # =====================
    previous_bottom = player.bottom

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
    if input_buffer == "jump" and player_hitstun <= 0:

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
    player.y += vel_y

    # =====================
    # 플랫폼 충돌
    # =====================
    all_surfaces = [ground] + platforms

    for surface in all_surfaces:

        if player.colliderect(surface):

            # 위에서 떨어졌을 때만
            if previous_bottom <= surface.top and vel_y >= 0:

                player.bottom = surface.top

                vel_y = 0

                on_ground = True

                extra_jumps = 1

                coyote_timer = coyote_time

    # =====================
    # 벽 Y 충돌
    # =====================
    for wall in walls:

        if player.colliderect(wall):

            # 떨어지는 중
            if vel_y > 0:

                player.bottom = wall.top

                vel_y = 0

                on_ground = True

                extra_jumps = 1

                coyote_timer = coyote_time

            # 위로 점프 중
            elif vel_y < 0:

                player.top = wall.bottom

                vel_y = 0

    # =====================
    # 카메라
    # =====================
    target_x = player.centerx - WIDTH // 2
    target_y = player.centery - HEIGHT // 2

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
    pygame.draw.rect(
        screen,
        PLAYER_COLOR,
        (
            player.x - camera_x,
            player.y - camera_y,
            player.width,
            player.height
        )
    )

    pygame.draw.rect(
        screen,
        (0, 255, 0),
        (
            player.x - camera_x,
            player.y - camera_y,
            player.width,
            player.height
        ),
        2
    )

    shadow_rect = pygame.Rect(
        player.x - camera_x + 5,
        player.bottom - camera_y - 8,
        player.width - 10,
        8
    )

    pygame.draw.ellipse(
        screen,
        (30, 30, 30),
        shadow_rect
    )

    # =====================
    # 체력바 배경
    #=====================

    pygame.draw.rect(
        screen,
        (50, 50, 50),
        (30, 30, 300, 30)
    )

    # =====================
    # 현재 체력
    # =====================

    health_width = int(
        (player_health / player_max_health)
        *300
    )

    health_width = max(
        0,
        min(300, health_width)
    )

    pygame.draw.rect(
        screen,
        (220, 40, 40),
        (
            30,
            30,
            health_width,
            30
        )
    )

    # 테두리
    pygame.draw.rect(
        screen,
        (255, 255, 255),
        (30, 30, 300, 30),
        2
    )

    pygame.display.flip()

pygame.quit()
sys.exit()