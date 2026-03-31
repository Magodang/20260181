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

WIDTH, HEIGHT = 800, 600
FPS = 60

WHITE  = (255, 255, 255)
BLUE   = (50, 120, 220)
RED    = (220, 50, 50)
GRAY   = (40, 40, 40)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodger")
clock = pygame.time.Clock()
font = get_korean_font(36)
font_big = get_korean_font(72)

PLAYER_W, PLAYER_H = 50, 30
ENEMY_W,  ENEMY_H  = 30, 30

SPAWN_DELAY = 20
MIN_SPEED = 5
MAX_SPEED = 8

def spawn_enemy(score):
    rand = random.random()

    # ===== 빠른 소형 적 (최우선 조건) =====
    if score >= 120 and rand < 0.05:
        w = int(ENEMY_W * 0.7)
        h = int(ENEMY_H * 0.7)
        speed = int(random.randint(MIN_SPEED, MAX_SPEED) * 1.5)
        enemy_type = "fast"

    # ===== 거대 적 =====
    elif score >= 50 and rand < 0.03:
        w = ENEMY_W * 4
        h = ENEMY_H * 4
        speed = int(random.randint(MIN_SPEED, MAX_SPEED) * 0.5)
        enemy_type = "big"

    # ===== 기본 적 =====
    else:
        w = ENEMY_W
        h = ENEMY_H
        speed = random.randint(MIN_SPEED, MAX_SPEED)
        enemy_type = "normal"

    x = random.randint(0, WIDTH - w)
    return pygame.Rect(x, -h, w, h), speed, enemy_type


def draw_hud(score, lives):
    screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))

    life_text = font.render(f"Lives: {'♥ ' * lives}", True, RED)
    screen.blit(life_text, (WIDTH - life_text.get_width() - 10, 10))


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
        if spawn_timer >= SPAWN_DELAY:
            spawn_timer = 0
            rect, speed, etype = spawn_enemy(score)
            enemies.append([rect, speed, etype])

        survived = []
        for rect, speed, etype in enemies:
            rect.y += speed

            if rect.top < HEIGHT:
                survived.append([rect, speed, etype])
            else:
                # ===== 점수 처리 =====
                if etype == "big":
                    score += 5
                else:
                    score += 1

        enemies = survived

        if invincible > 0:
            invincible -= 1
        else:
            for rect, speed, etype in enemies:
                if player.colliderect(rect):
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

        # ===== 적 색상 구분 =====
        for rect, speed, etype in enemies:
            if etype == "big":
                pygame.draw.rect(screen, (255, 120, 120), rect)  # 연한 빨강
            elif etype == "fast":
                pygame.draw.rect(screen, (255, 255, 0), rect)    # 노랑
            else:
                pygame.draw.rect(screen, RED, rect)

        draw_hud(score, lives)
        pygame.display.flip()

main()