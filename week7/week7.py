import pygame
import random
import sys

pygame.init()

def get_korean_font(size):
    candidates = ["malgungothic", "applegothic", "nanumgothic", "notosanscjk"]
    for name in candidates:
        font = pygame.font.SysFont(name, size)
        if font.get_ascent() > 0:
            return font
    return pygame.font.SysFont(None, size)

WIDTH, HEIGHT = 800, 800
FPS = 60

last_score = 0

WHITE  = (255, 255, 255)
BLUE   = (50, 120, 220)
RED    = (220, 50, 50)
GREEN  = (0, 200, 0)
GRAY   = (40, 40, 40)

# ===== 게임 상태 =====
STATE_MENU = 0
STATE_GAME = 1
STATE_GAMEOVER = 2
game_state = STATE_MENU

# ===== 화면 흔들림 =====
shake_timer = 0
shake_intensity = 0

# ===== 패턴 실행 =====
pattern_frame = 0
pattern_index = 0

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodger")
clock = pygame.time.Clock()
font = get_korean_font(36)
font_big = get_korean_font(72)

pygame.mixer.init()
pygame.mixer.music.load("week6/bgm.mp3")
pygame.mixer.music.set_volume(1.0)
pygame.mixer.music.play(-1)

PLAYER_W, PLAYER_H = 30, 30
ENEMY_W,  ENEMY_H  = 30, 30

MIN_SPEED = 5
MAX_SPEED = 8

# ===============================
# ===== 패턴 데이터 =====
# ===============================
pattern1 = [
    {"time": 60,   "x": 0},
    {"time": 60,  "x": 225},
    {"time": 60,  "x": 450},
    {"time": 220,  "x": 170},
    {"time": 220,  "x": 395},
    {"time": 220, "x": 620},
    {"time": 400, "x": -50},
    {"time": 400, "x": 200},
    {"time": 400, "x": 450},
    {"time": 400, "x": 700},
]


# ===============================
# ===== 패턴 상태 변수 =====
# ===============================
pattern_mode = False
pattern_timer = 0
pattern_phase = 0   # 0=대기, 1=페이드인, 2=정지, 3=페이드아웃
pattern_scale = 1.0
pattern_alpha = 0

spawned_set = set()


def get_spawn_delay(score):
    if score >= 2001:
        return 5
    elif score >= 1001:
        return 8
    elif score >= 701:
        return 10
    elif score >= 501:
        return 12
    elif score >= 301:
        return 14
    elif score >= 101:
        return 16
    else:
        return 18

# ===============================
# ===== 패턴 스폰 =====
# ===============================
def spawn_pattern(pattern, frame, speed):
    spawned = []
    global spawned_set

    for i, p in enumerate(pattern):

        if i in spawned_set:
            continue

        if p["time"] <= frame:
            w = ENEMY_W * 6
            h = ENEMY_H * 6
            rect = pygame.Rect(p["x"], -h, w, h)

            spawned.append([rect, speed, "pattern_big"])
            spawned_set.add(i)

    return spawned

def spawn_enemy(score):
    rand = random.random()

    

    # ===== 좌우 등장 (300점 이상 5%) =====
    if score >= 300 and rand < 0.05:
        side = random.choice(["left", "right"])
        y = random.randint(0, HEIGHT - ENEMY_H)
        speed = random.randint(MIN_SPEED, MAX_SPEED)

        if side == "left":
            return pygame.Rect(-ENEMY_W, y, ENEMY_W, ENEMY_H), speed, "side_right"
        else:
            return pygame.Rect(WIDTH, y, ENEMY_W, ENEMY_H), speed, "side_left"

    # ===== 확률 설정 =====
    if score <= 100:
        big_prob = 0
    elif score <= 1000:
        big_prob = 0.05
    else:
        big_prob = 0.07

    if score <= 300:
        fast_prob = 0
    elif score <= 1000:
        fast_prob = 0.07
    else:
        fast_prob = 0.10

    heal_prob = 0 if score < 300 else 0.04

    if score <= 500:
        wide_prob = 0
    elif score <= 1000:
        wide_prob = 0.06
    else:
        wide_prob = 0.07

    giant_prob = 0 if score <= 1000 else 0.02

    cumulative = 0

    # ===== 보스 =====
    cumulative += giant_prob
    if rand < cumulative:
        w = ENEMY_W * 8
        h = ENEMY_H * 8
        speed = int(random.randint(MIN_SPEED, MAX_SPEED) * 0.3)
        return pygame.Rect(random.randint(0, WIDTH - w), -h, w, h), speed, "giant"

    # ===== 회복 =====
    cumulative += heal_prob
    if rand < cumulative:
        speed = int(random.randint(MIN_SPEED, MAX_SPEED) * 0.8)
        return pygame.Rect(random.randint(0, WIDTH - ENEMY_W), -ENEMY_H, ENEMY_W, ENEMY_H), speed, "heal"

    # ===== 와이드 =====
    cumulative += wide_prob
    if rand < cumulative:
        w = ENEMY_W * 4
        h = ENEMY_H
        speed = int(random.randint(MIN_SPEED, MAX_SPEED) * 0.7)
        return pygame.Rect(random.randint(0, WIDTH - w), -h, w, h), speed, "wide"

    # ===== 빠른 =====
    cumulative += fast_prob
    if rand < cumulative:
        w = int(ENEMY_W * 0.6)
        h = int(ENEMY_H * 0.6)
        speed = int(random.randint(MIN_SPEED, MAX_SPEED) * 1.8)
        return pygame.Rect(random.randint(0, WIDTH - w), -h, w, h), speed, "fast"

    # ===== 큰 =====
    cumulative += big_prob
    if rand < cumulative:
        w = ENEMY_W * 8
        h = ENEMY_H * 8
        speed = int(random.randint(MIN_SPEED, MAX_SPEED) * 0.4)
        return pygame.Rect(random.randint(0, WIDTH - w), -h, w, h), speed, "big"

    # ===== 기본 =====
    return pygame.Rect(random.randint(0, WIDTH - ENEMY_W), -ENEMY_H, ENEMY_W, ENEMY_H), random.randint(MIN_SPEED, MAX_SPEED), "normal"

def apply_shake():
    global shake_timer, shake_intensity
    if shake_timer > 0:
        return random.randint(-shake_intensity, shake_intensity), random.randint(-shake_intensity, shake_intensity)
    return 0, 0

def draw_hud(score, lives):
    screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
    screen.blit(font.render(f"Lives: {'♥ ' * lives}", True, RED), (10, 50))


def game_over_screen(score):
    global start_rect, quit_rect
    global retry_rect, menu_rect

    while True:
        clock.tick(FPS)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                if retry_rect.collidepoint(mx, my):
                    return "retry"
                if menu_rect.collidepoint(mx, my):
                    return "menu"

        screen.fill(GRAY)

        title = font_big.render("GAME OVER", True, RED)
        score_text = font.render(f"Score: {score}", True, WHITE)

        retry_text = font.render("Retry", True, WHITE)
        menu_text = font.render("Main Menu", True, WHITE)

        screen.blit(title, title.get_rect(center=(WIDTH//2, HEIGHT//2 - 80)))
        screen.blit(score_text, score_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 20)))

        retry_rect = retry_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 40))
        menu_rect = menu_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 90))

        screen.blit(retry_text, retry_rect)
        screen.blit(menu_text, menu_rect)

        pygame.display.flip()

def menu_screen():
    title_scale = 1.0
    scale_dir = 1

    while True:
        clock.tick(FPS)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                if start_rect.collidepoint(mx, my):
                    return "start"
                if quit_rect.collidepoint(mx, my):
                    pygame.quit(); sys.exit()

        # ===== 제목 애니메이션 =====
        title_scale += 0.01 * scale_dir
        if title_scale > 1.1:
            scale_dir = -1
        elif title_scale < 0.9:
            scale_dir = 1

        screen.fill(GRAY)

        # ===== 제목 =====
        size = int(72 * title_scale)
        temp_font = get_korean_font(size)
        title = temp_font.render("Avoid Doodles!", True, WHITE)
        title_rect = title.get_rect(center=(WIDTH//2, HEIGHT//2 - 100))
        screen.blit(title, title_rect)

        # ===== 버튼 =====
        start_text = font.render("START", True, WHITE)
        quit_text = font.render("QUIT", True, WHITE)

        start_rect = start_text.get_rect(center=(WIDTH//2, HEIGHT//2))
        quit_rect = quit_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 60))

        screen.blit(start_text, start_rect)
        screen.blit(quit_text, quit_rect)

        pygame.display.flip()

# ===============================
# ===== 패턴1 (Big Big Big) =====
# ===============================
def pattern1_update():
    # 아직 패턴 내용 없음 (연출만)
    pass


def draw_pattern_title():
    global pattern_scale, pattern_alpha

    text = "Big Big Big"
    size = int(72 * pattern_scale)
    temp_font = get_korean_font(size)

    surf = temp_font.render(text, True, WHITE)
    surf.set_alpha(pattern_alpha)

    offset_x, offset_y = apply_shake()
    rect = surf.get_rect(center=(WIDTH//2 + offset_x, HEIGHT//2 + offset_y))
    screen.blit(surf, rect)

def run_game():
    global pattern_mode, pattern_timer, pattern_phase
    global pattern_scale, pattern_alpha
    global shake_timer, shake_intensity
    global last_score
    global spawned_set

    spawned_set = set()

    player = pygame.Rect(WIDTH // 2 - PLAYER_W // 2, HEIGHT - 60, PLAYER_W, PLAYER_H)
    enemies = []
    score = 100
    lives = 3
    spawn_timer = 0
    invincible = 0

    triggered_100 = False

    while True:
        clock.tick(FPS)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player.left > 0: player.x -= 5
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player.right < WIDTH: player.x += 5
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and player.top > 0: player.y -= 5
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player.bottom < HEIGHT: player.y += 5

        # ===== 패턴 트리거 =====
        if score >= 100 and not triggered_100:
            triggered_100 = True
            pattern_mode = True
            pattern_timer = 0
            pattern_phase = 0

        # ===== 일반 스폰 =====
        if not pattern_mode:
            spawn_timer += 1
            if spawn_timer >= get_spawn_delay(score):
                spawn_timer = 0
                rect, speed, etype = spawn_enemy(score)
                enemies.append([rect, speed, etype])

        # ===== 패턴 =====
        if pattern_mode:
            pattern_timer += 1

            if pattern_phase == 4:
                pattern_speed = 4 if score < 2000 else 10
                new_blocks = spawn_pattern(pattern1, pattern_timer, pattern_speed)
                enemies.extend(new_blocks)

            if pattern_phase == 0:
                if pattern_timer > FPS * 3:
                    pattern_phase = 1
                    pattern_timer = 0
                    shake_timer = 999999
                    shake_intensity = 8

            elif pattern_phase == 1:
                pattern_scale += 0.02
                pattern_alpha += 5
                if pattern_alpha >= 255:
                    pattern_phase = 2
                    pattern_timer = 0

            elif pattern_phase == 2:
                if pattern_timer > FPS:
                    pattern_phase = 3

            elif pattern_phase == 3:
                pattern_scale -= 0.02
                pattern_alpha -= 5
                if pattern_alpha <= 0:
                    pattern_phase = 4
                    pattern_timer = 0
                    shake_timer = 0

        # ===== 이동 =====
        survived = []
        for rect, speed, etype in enemies:
            rect.y += speed
            if rect.top < HEIGHT:
                survived.append([rect, speed, etype])
            else:
                score += 1
        enemies = survived

        # ===== 충돌 =====
        if invincible > 0:
            invincible -= 1
        else:
            for enemy in enemies[:]:
                rect, speed, etype = enemy

                if player.colliderect(rect):

                    # ===== 패턴 박스 =====
                    if etype == "pattern_big":
                        last_score = score
                        return "gameover"

                    # ===== 보스 =====
                    elif etype == "giant":
                        last_score = score
                        return "gameover"

                    # ===== 회복 =====
                    elif etype == "heal":
                        if lives < 3:
                            lives += 1
                        else:
                            score += 10
                        enemies.remove(enemy)

                    # ===== 일반 적 =====
                    else:
                        lives -= 1
                        invincible = 90   # ← 예전처럼 깜빡 시간

                        enemies.clear()   # ← 충돌 시 전부 제거

                    if lives <= 0:
                        last_score = score
                        return "gameover"

                    break

        # ===== 렌더링 =====
        offset_x, offset_y = apply_shake()
        screen.fill(GRAY)

        blink = (invincible // 10) % 2 == 0

        if blink:
            pygame.draw.rect(screen, BLUE, player.move(offset_x, offset_y))

        for rect, speed, etype in enemies:
            pygame.draw.rect(screen, RED, rect.move(offset_x, offset_y))

        draw_hud(score, lives)

        if pattern_mode:
            draw_pattern_title()

        pygame.display.flip()

def main():
    global game_state

    while True:

        # ===== 메뉴 =====
        if game_state == STATE_MENU:
            result = menu_screen()
            if result == "start":
                game_state = STATE_GAME

        # ===== 게임 =====
        elif game_state == STATE_GAME:
            result = run_game()
            if result == "gameover":
                game_state = STATE_GAMEOVER

        # ===== 게임오버 =====
        elif game_state == STATE_GAMEOVER:
            result = game_over_screen(last_score)

            if result == "retry":
                game_state = STATE_GAME
            elif result == "menu":
                game_state = STATE_MENU


main()