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
pygame.display.set_caption("Avoid Doodles")
clock = pygame.time.Clock()
font = get_korean_font(36)
font_big = get_korean_font(72)

pygame.mixer.init()
pygame.mixer.music.load("week7/bgm.mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

prob_img = pygame.image.load("week7\prob.png").convert_alpha()
prob_img = pygame.transform.scale(prob_img, (30, 30))

prob_big_img = pygame.image.load("week7\prob_big.png").convert_alpha()
prob_big_img = pygame.transform.scale(prob_big_img, (120, 120))

prob_fast_img = pygame.image.load("week7\prob_fast.png").convert_alpha()
prob_fast_img = pygame.transform.scale(prob_fast_img, (18, 18))

prob_heal_img = pygame.image.load("week7\prob_heal.png").convert_alpha()
prob_heal_img = pygame.transform.scale(prob_heal_img, (30, 30))

PLAYER_W, PLAYER_H = 30, 30
ENEMY_W,  ENEMY_H  = 30, 30

MIN_SPEED = 8
MAX_SPEED = 11
FAST_SPEED = 25

# ===============================
# ===== 패턴 데이터 =====
# ===============================
pattern1 = [
    {"time": 60,   "x": 0},
    {"time": 60,  "x": 225},
    {"time": 60,  "x": 450},
    {"time": 180,  "x": 170},
    {"time": 180,  "x": 395},
    {"time": 180, "x": 620},
    {"time": 300, "x": -50},
    {"time": 300, "x": 200},
    {"time": 300, "x": 450},
    {"time": 300, "x": 700},
]

pattern2 = [
    {"time": 60,   "x": 0},
    {"time": 70,  "x": 225},
    {"time": 80,  "x": 450},
    {"time": 90,  "x": 170},
    {"time": 100,  "x": 395},
    {"time": 180, "x": 620},
    {"time": 300, "x": -50},
    {"time": 300, "x": 200},
    {"time": 300, "x": 450},
    {"time": 300, "x": 700},
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
        return 6
    elif score >= 701:
        return 8
    elif score >= 401:
        return 10
    elif score >= 201:
        return 12
    elif score >= 51:
        return 14
    else:
        return 16

# ===============================
# ===== 패턴 스폰 =====
# ===============================
def spawn_pattern_big(pattern, frame, speed):
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

def spawn_pattern_warning(pattern, frame, speed, player):
    spawned = []
    global spawned_set

    for i, p in enumerate(pattern):
        if i in spawned_set:
            continue

        if p["time"] <= frame:
            w = int(ENEMY_W * 0.6)
            x = player.centerx - w // 2
            rect = pygame.Rect(x, 0, w, HEIGHT)

            spawned.append([rect, speed, "fast_warning"])
            spawned_set.add(i)

    return spawned

def spawn_enemy(score):
    rand = random.random()

    # ===== 확률 설정 =====
    if score <= 51:
        big_prob = 0
    elif score <= 1000:
        big_prob = 0.06
    else:
        big_prob = 0.07

    if score <= 200:
        fast_prob = 0
    elif score <= 1000:
        fast_prob = 0.08
    else:
        fast_prob = 0.10

    heal_prob = 0 if score < 400 else 0.03

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
        x = random.randint(0, WIDTH - w)
        rect = pygame.Rect(x, 0, w, HEIGHT)
        return rect, 60, "fast_warning"

    # ===== 큰 =====
    cumulative += big_prob
    if rand < cumulative:
        w = ENEMY_W * 4
        h = ENEMY_H * 4
        speed = int(random.randint(MIN_SPEED, MAX_SPEED) * 0.6)
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
    pass

def draw_pattern_title(pattern_type):
    global pattern_scale, pattern_alpha

    if pattern_type == 1:
        text = "Big Big Big"
    elif pattern_type == 2:
        text = "WARNING!!"

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
    global selected_pattern
    global force_pattern

    spawned_set = set()
    completed_patterns = set()

    player = pygame.Rect(WIDTH // 2 - PLAYER_W // 2, HEIGHT - 30, PLAYER_W, PLAYER_H)
    enemies = []
    score = 0
    lives = 3
    spawn_timer = 0
    invincible = 0
    selected_pattern = None
    force_pattern = False

    while True:
        clock.tick(FPS)

        if not force_pattern and not pattern_mode:
            if score >= 50 and 1 not in completed_patterns:
                pattern_mode = True
                pattern_timer = 0
                pattern_phase = 0
                pattern_type = 1

            elif score >= 200 and 2 not in completed_patterns:
                pattern_mode = True
                pattern_timer = 0
                pattern_phase = 0
                pattern_type = 2

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_1:
                    score = 50
                    selected_pattern = 1
                    force_pattern = True
                if e.key == pygame.K_2:
                    score = 200
                    selected_pattern = 2
                    force_pattern = True
                if e.key == pygame.K_3:
                    score = 400   
                    selected_pattern = 3
                    force_pattern = True
                if e.key == pygame.K_4:
                    score = 700
                    selected_pattern = 4
                    force_pattern = True
                if e.key == pygame.K_5:
                    score = 1000        
                    selected_pattern = 5 
                    force_pattern = True 

        if force_pattern and not pattern_mode:
            pattern_mode = True
            pattern_timer = 0
            pattern_phase = 0
            pattern_type = selected_pattern

            spawned_set.clear()

            for i in range(1, pattern_type + 1):
                completed_patterns.add(i)

            force_pattern = False
            selected_pattern = None                                              

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player.left > 0: player.x -= 6
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player.right < WIDTH: player.x += 6

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

            elif pattern_phase == 4:

                if pattern_type == 1:
                    pattern_speed = 8 if score < 2000 else 10
                    new_blocks = spawn_pattern_big(pattern1, pattern_timer, pattern_speed)

                elif pattern_type == 2:
                    new_blocks = spawn_pattern_warning(pattern2, pattern_timer, 40, player)

                enemies.extend(new_blocks)

                if pattern_timer > 500:
                    pattern_phase = 5
                    pattern_timer = 0

            elif pattern_phase == 5:
                pattern_mode = False
                spawned_set.clear()
                pattern_timer = 0
                pattern_scale = 1.0
                pattern_alpha = 0
                completed_patterns.add(pattern_type)

                pattern_mode = False
                spawned_set.clear()
                force_pattern = False

        # ===== 이동 =====
        survived = []
        for rect, speed, etype in enemies:

            # ===== fast 예고 =====
            if etype == "fast_warning":
                speed -= 1

                if speed <= 0:
                    w = int(ENEMY_W * 0.6)
                    h = int(ENEMY_H * 0.6)

                    new_rect = pygame.Rect(rect.x, -h, w, h)
                    new_speed = FAST_SPEED

                    survived.append([new_rect, new_speed, "fast"])
                else:
                    survived.append([rect, speed, etype])
                continue

            # ===== 일반 이동 =====
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

                if etype == "fast_warning":
                    continue

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
            draw_rect = rect.move(offset_x, offset_y)

            if etype == "normal":
                screen.blit(prob_img, draw_rect)

            elif etype == "big":
                screen.blit(prob_big_img, draw_rect)
            
            elif etype == "fast":
                screen.blit(prob_fast_img, draw_rect)

            elif etype == "heal":
                screen.blit(prob_heal_img, draw_rect)

            elif etype == "fast_warning":
                warning = pygame.Surface((rect.width, HEIGHT), pygame.SRCALPHA)
                warning.fill((255, 0, 0, 100))
                screen.blit(warning, (draw_rect.x, 0))

            else:
                pygame.draw.rect(screen, RED, draw_rect)

        draw_hud(score, lives)

        if pattern_mode:
            draw_pattern_title(pattern_type)

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