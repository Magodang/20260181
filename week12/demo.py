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
    pygame.Rect(500, HEIGHT - 200, 80, 120),
    pygame.Rect(1200, HEIGHT - 300, 120, 220),
    pygame.Rect(2100, HEIGHT - 250, 100, 170),
]

# 적
enemies = [

    {
        "rect": pygame.Rect(750, HEIGHT - 300, 125, 110),
        "animations": enemy1_animations,
        "current_animation": "idle",
        "frame_index": 0,
        "animation_speed": 0.05
    }
]

player = pygame.Rect(100, HEIGHT - 200, 40, 60)

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
    # 입력 처리
    # =====================
    keys = pygame.key.get_pressed()

    dx = 0

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
    if input_buffer == "jump":

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

    if camera_y < 0:
        camera_y = 0

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

        screen.blit(
            image,
            (
                int(enemy["rect"].x - camera_x),
                int(enemy["rect"].y - camera_y)
            )
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

    pygame.display.flip()

pygame.quit()
sys.exit()