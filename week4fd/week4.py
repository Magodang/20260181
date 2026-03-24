import pygame
import sys
import math
from sprites import load_sprite

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Sprite Collision Demo")

clock = pygame.time.Clock()

RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# Rect (충돌 및 위치 계산용)
player_rect = pygame.Rect(100, 100, 50, 50)
center_rect = pygame.Rect(0, 0, 50, 50)
center_rect.center = (400, 300)

player_speed = 5

# 스프라이트 이미지 로드
player_img = load_sprite("rocket", (50, 50))
center_img = load_sprite("stone", (50, 50))

def circle_collision(r1, r2):
    x1, y1 = r1.center
    x2, y2 = r2.center
    radius1 = r1.width // 2
    radius2 = r2.width // 2
    
    distance = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    return distance <= (radius1 + radius2)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 키 입력
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_rect.x += player_speed
    if keys[pygame.K_UP]:
        player_rect.y -= player_speed
    if keys[pygame.K_DOWN]:
        player_rect.y += player_speed

    # 화면 밖 제한
    player_rect.clamp_ip(screen.get_rect())

    # 충돌 검사
    collided = circle_collision(player_rect, center_rect)

    # 배경색 변경
    if collided:
        screen.fill(YELLOW)
    else:
        screen.fill(WHITE)

    # 스프라이트 그리기
    screen.blit(player_img, player_rect)
    screen.blit(center_img, center_rect)

    # AABB 표시
    pygame.draw.rect(screen, RED, player_rect, 2)
    pygame.draw.rect(screen, RED, center_rect, 2)

    # 중심 좌표
    px, py = player_rect.center
    cx, cy = center_rect.center

    # 반지름
    pr = player_rect.width // 2
    cr = center_rect.width // 2

    # 원형 Bounding Circle
    pygame.draw.circle(screen, BLUE, (px, py), pr, 2)
    pygame.draw.circle(screen, BLUE, (cx, cy), cr, 2)

    # 중심점 표시
    pygame.draw.circle(screen, BLUE, (px, py), 4)
    pygame.draw.circle(screen, BLUE, (cx, cy), 4)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()