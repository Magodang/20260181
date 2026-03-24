import pygame
import sys
import random
import math

pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("My First Pygame")

WHITE = (255,255,255)
BLUE = (0,0,255)
RED = (255,0,0)
BLACK = (0,0,0)

clock = pygame.time.Clock()
running = True

# 반지름 통일
RADIUS = 20

# 플레이어
x = 400
y = 300
speed = 5

# 적 리스트
enemies = []

# 시간 시작
start_time = pygame.time.get_ticks()

# 폰트 생성
font = pygame.font.SysFont(None, 36)

class Enemy:
    def __init__(self):
        self.radius = RADIUS

        side = random.choice(["left","right","top","bottom"])

        if side == "left":
            self.x = -self.radius
            self.y = random.randint(0,600)
            self.vx = random.randint(2,5)
            self.vy = 0

        elif side == "right":
            self.x = 800 + self.radius
            self.y = random.randint(0,600)
            self.vx = -random.randint(2,5)
            self.vy = 0

        elif side == "top":
            self.x = random.randint(0,800)
            self.y = -self.radius
            self.vx = 0
            self.vy = random.randint(2,5)

        elif side == "bottom":
            self.x = random.randint(0,800)
            self.y = 600 + self.radius
            self.vx = 0
            self.vy = -random.randint(2,5)

    def update(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.radius)

    def is_off_screen(self):
        return (
            self.x < -50 or self.x > 850 or
            self.y < -50 or self.y > 650
        )


# 충돌 체크 함수
def check_collision(x1, y1, x2, y2, r):
    dist = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    return dist < r * 2


game_over = False
elapsed_time = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        # 이동
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            y -= speed
        if keys[pygame.K_DOWN]:
            y += speed
        if keys[pygame.K_LEFT]:
            x -= speed
        if keys[pygame.K_RIGHT]:
            x += speed

        # 경계 제한
        x = max(RADIUS, min(800 - RADIUS, x))
        y = max(RADIUS, min(600 - RADIUS, y))

        # 적 생성
        if random.random() < 0.03:
            enemies.append(Enemy())

        # 적 업데이트
        for e in enemies:
            e.update()

        # 충돌 체크
        for e in enemies:
            if check_collision(x, y, e.x, e.y, RADIUS):
                game_over = True
                elapsed_time = (pygame.time.get_ticks() - start_time) // 1000

        # 화면 밖 제거
        enemies = [e for e in enemies if not e.is_off_screen()]

    # 현재 시간 계산 (게임 중일 때만)
    if not game_over:
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000

    # 그리기
    screen.fill(WHITE)

    pygame.draw.circle(screen, BLUE, (x, y), RADIUS)

    for e in enemies:
        e.draw()

    # 시간 텍스트
    time_text = font.render(f"Time: {elapsed_time}s", True, BLACK)
    screen.blit(time_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
