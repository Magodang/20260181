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

PLAYER_W, PLAYER_H = 30, 30
ENEMY_W,  ENEMY_H  = 30, 30

MIN_SPEED = 5
MAX_SPEED = 8

def get_spawn_delay(score):
    if score >= 300:
        return 10
    elif score >= 120:
        return 15
    else:
        return 20


def spawn_enemy(score):
    rand = random.random()

    # ===== 확률 설정 =====
    if score >= 200:
        fast_prob = 0.10
        big_prob = 0.06
    else:
        fast_prob = 0.05
        big_prob = 0.03

    # ===== 좌우 등장 (300점 이상, 5%) =====
    if score >= 300 and rand < 0.05:
        side = random.choice(["left", "right"])
        y = random.randint(0, HEIGHT - ENEMY_H)

        if side == "left":
            rect = pygame.Rect(-ENEMY_W, y, ENEMY_W, ENEMY_H)
            speed = random.randint(MIN_SPEED, MAX_SPEED)
            direction = "horizontal_right"
        else:
            rect = pygame.Rect(WIDTH, y, ENEMY_W, ENEMY_H)
            speed = random.randint(MIN_SPEED, MAX_SPEED)
            direction = "horizontal_left"

        return rect, speed, "side", direction

    # ===== 회복 박스 =====
    elif score >= 120 and rand < 0.08:
        w, h = ENEMY_W, ENEMY_H
        speed = random.randint(MIN_SPEED, MAX_SPEED)
        return pygame.Rect(random.randint(0, WIDTH - w), -h, w, h), speed, "heal", "down"

    # ===== 가로 긴 박스 =====
    elif score >= 200 and rand < 0.13:
        w = ENEMY_W * 4
        h = ENEMY_H
        speed = int(random.randint(MIN_SPEED, MAX_SPEED) * 0.5)
        return pygame.Rect(random.randint(0, WIDTH - w), -h, w, h), speed, "wide", "down"

    # ===== 빠른 작은 박스 =====
    elif score >= 120 and rand < 0.13 + fast_prob:
        w = int(ENEMY_W * 0.7)
        h = int(ENEMY_H * 0.7)
        speed = int(random.randint(MIN_SPEED, MAX_SPEED) * 1.5)
        return pygame.Rect(random.randint(0, WIDTH - w), -h, w, h), speed, "fast", "down"

    # ===== 큰 박스 =====
    elif score >= 50 and rand < 0.13 + fast_prob + big_prob:
        w = ENEMY_W * 4
        h = ENEMY_H * 4
        speed = int(random.randint(MIN_SPEED, MAX_SPEED) * 0.5)
        return pygame.Rect(random.randint(0, WIDTH - w), -h, w, h), speed, "big", "down"

    # ===== 기본 =====
    else:
        w, h = ENEMY_W, ENEMY_H
        speed = random.randint(MIN_SPEED, MAX_SPEED)
        return pygame.Rect(random.randint(0, WIDTH - w), -h, w, h), speed, "normal", "down"


# ===== HUD (원래 형태 복구) =====
def draw_hud(score, lives):
    screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
    screen.blit(font.render(f"Lives: {'♥ ' * lives}", True, RED), (10, 50))


def game_over_screen(score):
    screen.fill(GRAY)
    screen.blit(font_big.render("GAME OVER", True, RED), (220, 220))
    screen.blit(font.render(f"Score: {score}", True, WHITE), (350, 310))
    screen.blit(font.render("R: Restart   Q: Quit", True, WHITE), (270, 360))
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
            enemies.append(list(spawn_enemy(score)))

        survived = []
        for rect, speed, etype, direction in enemies:

            # ===== 이동 처리 =====
            if direction == "down":
                rect.y += speed
            elif direction == "horizontal_right":
                rect.x += speed
            elif direction == "horizontal_left":
                rect.x -= speed

            # ===== 화면 밖 처리 =====
            if rect.top < HEIGHT and rect.right > 0 and rect.left < WIDTH:
                survived.append([rect, speed, etype, direction])
            else:
                if etype == "big":
                    score += 5
                elif etype == "fast":
                    score += 3
                else:
                    score += 1

        enemies = survived

        if invincible > 0:
            invincible -= 1
        else:
            for rect, speed, etype, direction in enemies:
                if player.colliderect(rect):

                    if etype == "heal":
                        lives = min(3, lives + 1)
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
            pygame.draw.rect(screen, BLUE, player)

        for rect, speed, etype, direction in enemies:
            if etype == "heal":
                pygame.draw.rect(screen, GREEN, rect)
            else:
                pygame.draw.rect(screen, RED, rect)

        draw_hud(score, lives)
        pygame.display.flip()

main()