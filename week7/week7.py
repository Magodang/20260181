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

WHITE  = (255, 255, 255)
BLUE   = (50, 120, 220)
RED    = (220, 50, 50)
GREEN  = (0, 200, 0)
GRAY   = (40, 40, 40)

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
    {"time": 60,  "x": 200},
    {"time": 60,  "x": 400},
    {"time": 180,  "x": 200},
    {"time": 180,  "x": 400},
    {"time": 180, "x": 600},
    {"time": 300, "x": 800},
]


# ===============================
# ===== 패턴 상태 변수 =====
# ===============================
pattern_mode = False
pattern_timer = 0
pattern_phase = 0   # 0=대기, 1=페이드인, 2=정지, 3=페이드아웃
pattern_scale = 1.0
pattern_alpha = 0


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
def spawn_pattern(pattern, frame, speed, speed_set):
    spawned = []

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
    screen.fill(GRAY)

    title = font_big.render("GAME OVER", True, RED)
    score_text = font.render(f"Score: {score}", True, WHITE)
    guide = font.render("R: Restart   Q: Quit", True, WHITE)

    screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40)))
    screen.blit(score_text, score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20)))
    screen.blit(guide, guide.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 70)))

    pygame.display.flip()

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r: return True
                if e.key == pygame.K_q: pygame.quit(); sys.exit()


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


def main():
    global pattern_mode, pattern_timer, pattern_phase, pattern_scale, pattern_alpha
    global shake_timer, shake_intensity

    player = pygame.Rect(WIDTH // 2 - PLAYER_W // 2, HEIGHT - 60, PLAYER_W, PLAYER_H)
    enemies = []
    score = 100
    lives = 3
    spawn_timer = 0
    invincible = 0

    triggered_100 = False  # 최초 100점 체크

    while True:
        clock.tick(FPS)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a])  and player.left  > 0: player.x -= 4
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player.right < WIDTH: player.x += 4
        if (keys[pygame.K_UP] or keys[pygame.K_w])    and player.top   > 0: player.y -= 4
        if (keys[pygame.K_DOWN] or keys[pygame.K_s])  and player.bottom < HEIGHT: player.y += 4


        # ===============================
        # ===== 패턴 트리거 =====
        # ===============================
        if score >= 100 and not triggered_100:
            triggered_100 = True
            pattern_mode = True
            pattern_timer = 0
            pattern_phase = 0

        # ===============================
        # ===== 일반 스폰 (패턴 아닐 때만) =====
        # ===============================
        if not pattern_mode:
            spawn_timer += 1
            if spawn_timer >= get_spawn_delay(score):
                spawn_timer = 0
                rect, speed, etype = spawn_enemy(score)
                enemies.append([rect, speed, etype])


        # ===============================
        # ===== 패턴 진행 =====
        # ===============================
        if pattern_mode:
            pattern_timer += 1

            # ===== 패턴 박스 생성 =====
            if pattern_phase == 4:
                pattern_speed = 4 if score < 2000 else 10
                new_blocks = spawn_pattern(pattern1, pattern_timer, pattern_speed)
                enemies.extend(new_blocks)

            # 0~3초 대기
            if pattern_phase == 0:
                if pattern_timer > FPS * 3:
                    pattern_phase = 1
                    pattern_timer = 0

                    shake_timer = 999999
                    shake_intensity = 8

            # 페이드 인
            elif pattern_phase == 1:
                pattern_scale += 0.02
                pattern_alpha += 5
                if pattern_alpha >= 255:
                    pattern_alpha = 255
                    pattern_phase = 2
                    pattern_timer = 0

            # 유지 1초
            elif pattern_phase == 2:
                if pattern_timer > FPS:
                    pattern_phase = 3

            # 페이드 아웃
            elif pattern_phase == 3:
                pattern_scale -= 0.02
                pattern_alpha -= 5
                if pattern_alpha <= 0:
                    pattern_alpha = 0

                    pattern_phase = 4
                    pattern_timer = 0
                    shake_timer = 0

        # ===============================
        # ===== 적 이동 =====
        # ===============================
        survived = []
        for rect, speed, etype in enemies:

            if etype == "side_right":
                rect.x += speed
            elif etype == "side_left":
                rect.x -= speed
            else:
                rect.y += speed

            if rect.top < HEIGHT and rect.right > 0 and rect.left < WIDTH:
                survived.append([rect, speed, etype])
            else:
                score += 1

        enemies = survived


        # ===============================
        # ===== 충돌 =====
        # ===============================
        if invincible > 0:
            invincible -= 1
        else:
            for enemy in enemies[:]:
                rect, speed, etype = enemy

                if player.colliderect(rect):

                    if pattern_phase == 4:
                        if game_over_screen(score):
                            main()
                        return

                    if etype == "giant":
                        if game_over_screen(score):
                            main()
                        return

                    elif etype == "heal":
                        if lives < 3:
                            lives += 1
                        else:
                            score += 10
                        enemies.remove(enemy)

                    else:
                        lives -= 1
                        invincible = 90
                        enemies.clear()

                    if lives <= 0:
                        if game_over_screen(score):
                            main()
                        return
                    break

        # ===============================
        # ===== 렌더링 =====
        # ===============================
        offset_x, offset_y = apply_shake()

        screen.fill(GRAY)

        blink = (invincible // 10) % 2 == 0
        if blink:
            pygame.draw.rect(screen, BLUE, player.move(offset_x, offset_y))

        for rect, speed, etype in enemies:
            if etype == "heal":
                pygame.draw.rect(screen, GREEN, rect.move(offset_x, offset_y))
            else:
                pygame.draw.rect(screen, RED, rect.move(offset_x, offset_y))

        draw_hud(score, lives)

        # 패턴 타이틀 표시
        if pattern_mode:
            draw_pattern_title()

        pygame.display.flip()


main()