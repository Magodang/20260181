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
BLACK  = (0,   0,   0)
BLUE   = (50,  120, 220)
RED    = (220, 50,  50)
YELLOW = (240, 200, 0)
GRAY   = (40,  40,  40)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodger")
clock = pygame.time.Clock()
font = get_korean_font(36)
font_big = get_korean_font(72)

# 고정 난이도 설정
ENEMY_MIN_SPEED = 4
ENEMY_MAX_SPEED = 7
SPAWN_DELAY = 30  # 작을수록 많이 생성됨

PLAYER_W, PLAYER_H = 50, 30
ENEMY_W,  ENEMY_H  = 30, 30


def spawn_enemy():
    x = random.randint(0, WIDTH - ENEMY_W)
    speed = random.randint(ENEMY_MIN_SPEED, ENEMY_MAX_SPEED)
    return pygame.Rect(x, -ENEMY_H, ENEMY_W, ENEMY_H), speed


def draw_hud(score, lives):
    screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
    screen.blit(font.render(f"Lives: {'♥ ' * lives}", True, RED), (WIDTH - 180, 10))


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
        if keys[pygame.K_RIGHT] and player.right < WIDTH:  player.x += 5
        if keys[pygame.K_UP]    and player.top   > 0:     player.y -= 5
        if keys[pygame.K_DOWN]  and player.bottom < HEIGHT: player.y += 5

        # 적 생성
        spawn_timer += 1
        if spawn_timer >= SPAWN_DELAY:
            spawn_timer = 0
            rect, speed = spawn_enemy()
            enemies.append([rect, speed])

        # 적 이동
        survived = []
        for pair in enemies:
            pair[0].y += pair[1]
            if pair[0].top < HEIGHT:
                survived.append(pair)
            else:
                score += 1
        enemies = survived

        # 충돌 처리
        if invincible > 0:
            invincible -= 1
        else:
            for pair in enemies:
                if player.colliderect(pair[0]):
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

        for pair in enemies:
            pygame.draw.rect(screen, RED, pair[0])

        draw_hud(score, lives)
        pygame.display.flip()
        clock.tick(FPS)


main()
