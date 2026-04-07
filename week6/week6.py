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

WIDTH, HEIGHT = 1200, 800
FPS = 60

WHITE  = (255, 255, 255)
BLUE   = (50, 120, 220)
RED    = (220, 50, 50)
GREEN  = (0, 200, 0)
GRAY   = (40, 40, 40)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodger")
clock = pygame.time.Clock()
font = get_korean_font(36)
font_big = get_korean_font(72)

pygame.mixer.init()

pygame.mixer.music.load("week6/bgm.mp3")
pygame.mixer.music.set_volume(1.0)
pygame.mixer.music.play(-1)  # -1: 무한 반복

PLAYER_W, PLAYER_H = 30, 30
ENEMY_W,  ENEMY_H  = 30, 30

MIN_SPEED = 5
MAX_SPEED = 8

player_img = pygame.image.load("week6/player.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (PLAYER_W, PLAYER_H))

def get_spawn_delay(score):
    if score >= 1001:
        return 4
    elif score >= 301:
        return 6
    elif score >= 120:
        return 10
    else:
        return 15


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

    # ===== 기존 확률 =====
    if score <= 50:
        big_prob = 0
    elif score <= 120:
        big_prob = 0.04
    elif score <= 1000:
        big_prob = 0.07
    else:
        big_prob = 0.10

    if score <= 120:
        fast_prob = 0
    elif score <= 200:
        fast_prob = 0.06
    elif score <= 1000:
        fast_prob = 0.11
    else:
        fast_prob = 0.14

    if score < 120:
        heal_prob = 0
    else:
        heal_prob = 0.04

    if score <= 200:
        wide_prob = 0
    elif score <= 1000:
        wide_prob = 0.07
    else:
        wide_prob = 0.11

    if score <= 1000:
        giant_prob = 0
    else:
        giant_prob = 0.03

    cumulative = 0

    cumulative += giant_prob
    if rand < cumulative:
        w = ENEMY_W * 8
        h = ENEMY_H * 8
        speed = int(random.randint(MIN_SPEED, MAX_SPEED) * 0.3)
        return pygame.Rect(random.randint(0, WIDTH - w), -h, w, h), speed, "giant"

    cumulative += heal_prob
    if rand < cumulative:
        speed = int(random.randint(MIN_SPEED, MAX_SPEED) * 0.8)
        return pygame.Rect(random.randint(0, WIDTH - ENEMY_W), -ENEMY_H, ENEMY_W, ENEMY_H), speed, "heal"

    cumulative += wide_prob
    if rand < cumulative:
        w = ENEMY_W * 4
        h = ENEMY_H
        speed = int(random.randint(MIN_SPEED, MAX_SPEED) * 0.7)
        return pygame.Rect(random.randint(0, WIDTH - w), -h, w, h), speed, "wide"

    cumulative += fast_prob
    if rand < cumulative:
        w = int(ENEMY_W * 0.6)
        h = int(ENEMY_H * 0.6)
        speed = int(random.randint(MIN_SPEED, MAX_SPEED) * 1.8)
        return pygame.Rect(random.randint(0, WIDTH - w), -h, w, h), speed, "fast"

    cumulative += big_prob
    if rand < cumulative:
        w = ENEMY_W * 4
        h = ENEMY_H * 4
        speed = int(random.randint(MIN_SPEED, MAX_SPEED) * 0.5)
        return pygame.Rect(random.randint(0, WIDTH - w), -h, w, h), speed, "big"

    return pygame.Rect(random.randint(0, WIDTH - ENEMY_W), -ENEMY_H, ENEMY_W, ENEMY_H), random.randint(MIN_SPEED, MAX_SPEED), "normal"


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


def main():
    player = pygame.Rect(WIDTH // 2 - PLAYER_W // 2, HEIGHT - 60, PLAYER_W, PLAYER_H)
    enemies = []
    score = 0
    lives = 3
    spawn_timer = 0
    invincible = 0

    while True:
        clock.tick(FPS)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]  and player.left  > 0:     player.x -= 5
        if keys[pygame.K_RIGHT] and player.right < WIDTH: player.x += 5
        if keys[pygame.K_UP]    and player.top   > 0:     player.y -= 5
        if keys[pygame.K_DOWN]  and player.bottom < HEIGHT: player.y += 5

        spawn_timer += 1
        if spawn_timer >= get_spawn_delay(score):
            spawn_timer = 0
            rect, speed, etype = spawn_enemy(score)
            enemies.append([rect, speed, etype])

        survived = []
        for rect, speed, etype in enemies:

            # ===== 이동 처리 =====
            if etype == "side_right":
                rect.x += speed
            elif etype == "side_left":
                rect.x -= speed
            else:
                rect.y += speed

            # ===== 화면 밖 =====
            if rect.top < HEIGHT and rect.right > 0 and rect.left < WIDTH:
                survived.append([rect, speed, etype])
            else:
                if etype == "big":
                    score += 5
                elif etype == "fast":
                    score += 3
                elif etype == "wide":
                    score += 3
                elif etype == "giant":
                    score += 10
                else:
                    score += 1

        enemies = survived

        if invincible > 0:
            invincible -= 1
        else:
            for enemy in enemies[:]:
                rect, speed, etype = enemy

                if player.colliderect(rect):

                    # ===== 보스 즉사 =====
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

        screen.fill(GRAY)

        blink = (invincible // 10) % 2 == 0
        if blink:
            screen.blit(player_img, player)

        for rect, speed, etype in enemies:
            if etype == "heal":
                pygame.draw.rect(screen, GREEN, rect)
            else:
                pygame.draw.rect(screen, RED, rect)

        draw_hud(score, lives)
        pygame.display.flip()

main()