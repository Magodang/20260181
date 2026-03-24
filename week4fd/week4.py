import pygame
import sys
import math
from sprites import load_sprite

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Collision Comparison Demo (Fixed Bounds)")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)

RED   = (255, 0, 0)
BLUE  = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# ================= 플레이어 =================
player_speed = 5

player_img_orig = load_sprite("rocket")
player_img = pygame.transform.smoothscale(player_img_orig, (60, 160))  # 크기 확대
player_rect = player_img.get_rect(topleft=(100, 100))

# ================= 중앙 오브젝트 =================
center_pos = (400, 300)

center_img_orig = load_sprite("stone", (80, 80))  # 약간 확대
center_rect = center_img_orig.get_rect(center=center_pos)  # 충돌 기준 고정 Rect

angle = 0
rot_speed = 1

# ================= OBB 계산 =================
def get_obb_points(rect, angle):
    cx, cy = rect.center
    w, h = rect.width, rect.height
    rad = math.radians(angle)
    corners = [(-w/2,-h/2),(w/2,-h/2),(w/2,h/2),(-w/2,h/2)]
    pts = []
    for x,y in corners:
        rx = x*math.cos(rad) - y*math.sin(rad)
        ry = x*math.sin(rad) + y*math.cos(rad)
        pts.append((cx+rx, cy+ry))
    return pts

# ================= SAT =================
def dot(v1,v2): return v1[0]*v2[0] + v1[1]*v2[1]

def get_axes(points):
    axes=[]
    for i in range(len(points)):
        p1=points[i]
        p2=points[(i+1)%len(points)]
        edge=(p2[0]-p1[0], p2[1]-p1[1])
        normal=(-edge[1], edge[0])
        l=math.hypot(*normal)
        axes.append((normal[0]/l, normal[1]/l))
    return axes

def project(points, axis):
    d=[dot(p,axis) for p in points]
    return min(d), max(d)

def sat_collision(p1,p2):
    axes = get_axes(p1) + get_axes(p2)
    for a in axes:
        min1,max1 = project(p1,a)
        min2,max2 = project(p2,a)
        if max1 < min2 or max2 < min1:
            return False
    return True

# ================= 충돌 =================
def circle_collision(r1,r2):
    x1,y1=r1.center; x2,y2=r2.center
    r1r=min(r1.width,r1.height)//2
    r2r=min(r2.width,r2.height)//2
    return math.hypot(x1-x2,y1-y2) <= r1r+r2r

def aabb_collision(r1,r2):
    return r1.colliderect(r2)

# ================= 메인 루프 =================
running=True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running=False

    k = pygame.key.get_pressed()
    if k[pygame.K_LEFT]:  player_rect.x -= player_speed
    if k[pygame.K_RIGHT]: player_rect.x += player_speed
    if k[pygame.K_UP]:    player_rect.y -= player_speed
    if k[pygame.K_DOWN]:  player_rect.y += player_speed
    if k[pygame.K_z]:     rot_speed += 0.05

    player_rect.clamp_ip(screen.get_rect())
    angle += rot_speed

    # 회전 이미지는 화면 표시용
    rot_img  = pygame.transform.rotate(center_img_orig, angle)
    rot_rect = rot_img.get_rect(center=center_rect.center)

    # OBB 좌표 (고정 Rect 기준)
    player_pts = get_obb_points(player_rect, 0)
    enemy_pts  = get_obb_points(center_rect, angle)

    # 충돌 판정 (고정 Rect 기준)
    hit_circle = circle_collision(player_rect, center_rect)
    hit_aabb   = aabb_collision(player_rect, center_rect)
    hit_obb    = sat_collision(player_pts, enemy_pts)

    screen.fill(WHITE)

    # 스프라이트
    screen.blit(player_img, player_rect)
    screen.blit(rot_img, rot_rect)

    # ===== Circle =====
    pygame.draw.circle(screen, BLUE, player_rect.center, min(player_rect.width,player_rect.height)//2, 2)
    pygame.draw.circle(screen, BLUE, center_rect.center, min(center_rect.width,center_rect.height)//2, 2)

    # ===== AABB =====
    pygame.draw.rect(screen, RED, player_rect, 2)
    pygame.draw.rect(screen, RED, center_rect, 2)

    # ===== OBB =====
    pygame.draw.lines(screen, GREEN, True, player_pts, 2)
    pygame.draw.lines(screen, GREEN, True, enemy_pts, 2)

    # ===== 텍스트 =====
    t1 = font.render(f"Circle: {'HIT' if hit_circle else 'SAFE'}", True, BLUE)
    t2 = font.render(f"AABB: {'HIT' if hit_aabb else 'SAFE'}", True, RED)
    t3 = font.render(f"OBB: {'HIT' if hit_obb else 'SAFE'}", True, GREEN)

    screen.blit(t1, (10,10))
    screen.blit(t2, (10,35))
    screen.blit(t3, (10,60))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()