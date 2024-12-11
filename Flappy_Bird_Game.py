import pygame
import random

# Khởi tạo Pygame
pygame.init()

# Đặt tên cửa sổ
pygame.display.set_caption("Flappy Bird Game 1024x768")
# Thêm background
bg = pygame.image.load(r'assets/background.png')
pygame.display.set_icon(bg)

# Kích thước cửa sổ
WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Chim
bird_x, bird_y = 100, HEIGHT // 2
bird_velocity = 0
bird_size = 20
bird_img = pygame.image.load(r'assets/bird.png')  # Tải ảnh chim
bird_img = pygame.transform.scale(bird_img, (40, 40))  # Thay đổi kích thước ảnh chim

# Đạn
bullets = []
bullet_size = 10  # Tăng kích thước đạn
bullet_speed = 5
max_bullets = 23  # Giới hạn số đạn ban đầu
current_bullets = max_bullets  # Đạn bắt đầu

# Chướng ngại vật
pipe_width = 100  # Chiều rộng ảnh ống đã điều chỉnh
pipe_img = pygame.image.load('assets/pipe.png')  # Tải ảnh ống

# Điều chỉnh kích thước ảnh ống
original_pipe_width, original_pipe_height = pipe_img.get_size()
pipe_height = HEIGHT // 5  # Chiều cao của ống (có thể thay đổi theo ý muốn)
pipe_ratio = pipe_height / original_pipe_height  # Tính tỷ lệ chiều cao ảnh
pipe_width = int(original_pipe_width * pipe_ratio)  # Tính lại chiều rộng sao cho giữ tỷ lệ

pipe_img = pygame.transform.scale(pipe_img, (pipe_width, pipe_height))  # Thay đổi kích thước ảnh ống

gap_size = 200  # Kích thước khoảng cách giữa các chướng ngại vật
obstacles = []
obstacle_speed = 3

# Điểm
score = 0
points = []
point_size = 10  # Kích thước điểm
point_speed = 3  # Tốc độ điểm di chuyển
font = pygame.font.SysFont(None, 36)

# Vòng lặp chính của game
running = True
while running:
    screen.fill(WHITE)
    # Hiển thị background
    screen.blit(bg, (0, 0))

    # Xử lý các sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Chim nhảy
                bird_velocity = -10
            if event.key == pygame.K_s and current_bullets > 0:  # Bắn đạn
                bullets.append([bird_x + 40, bird_y])
                current_bullets -= 1  # Giảm số đạn khi bắn

    # Cập nhật vị trí chim
    bird_velocity += 0.5  # Tăng tốc độ rơi
    bird_y += bird_velocity

    # Vẽ chim
    screen.blit(bird_img, (bird_x, bird_y))  # Vẽ chim từ ảnh

    # Kiểm tra va chạm với biên
    if bird_y > HEIGHT or bird_y < 0:
        running = False

    # Cập nhật đạn
    for bullet in bullets[:]:
        bullet[0] += bullet_speed
        pygame.draw.circle(screen, RED, bullet, bullet_size)
        if bullet[0] > WIDTH:
            bullets.remove(bullet)

    # Sinh chướng ngại vật ngẫu nhiên
    if random.randint(1, 60) == 1:
        obstacle_height_top = random.randint(50, 300)  # Chiều cao chướng ngại vật phía trên
        obstacle_height_bottom = HEIGHT - obstacle_height_top - gap_size  # Chiều cao chướng ngại vật phía dưới
        obstacles.append([WIDTH, obstacle_height_top, obstacle_height_bottom])

    # Cập nhật chướng ngại vật
    for obstacle in obstacles[:]:
        obstacle[0] -= obstacle_speed  # Di chuyển chướng ngại vật sang trái
        # Vẽ chướng ngại vật phía trên và phía dưới với ảnh ống
        screen.blit(pipe_img, (obstacle[0], 0))  # Vẽ ống phía trên
        screen.blit(pygame.transform.flip(pipe_img, False, True), (obstacle[0], HEIGHT - obstacle[2]))  # Vẽ ống phía dưới

        # Kiểm tra va chạm giữa chim và chướng ngại vật
        if (bird_x + bird_size > obstacle[0] and bird_x - bird_size < obstacle[0] + pipe_width and
            (bird_y - bird_size < obstacle[1] or bird_y + bird_size > HEIGHT - obstacle[2])):
            running = False

        # Xóa chướng ngại vật khi ra ngoài màn hình
        if obstacle[0] < -pipe_width:
            obstacles.remove(obstacle)

    # Kiểm tra va chạm giữa đạn và chướng ngại vật
    for bullet in bullets[:]:
        for obstacle in obstacles[:]:
            if (bullet[0] > obstacle[0] and bullet[0] < obstacle[0] + pipe_width and
                (bullet[1] < obstacle[1] or bullet[1] > HEIGHT - obstacle[2])):
                bullets.remove(bullet)

                # Giảm kích thước chướng ngại vật sau khi bị bắn trúng
                obstacle[1] = max(obstacle[1] * 3/4, 10)  # Giảm chiều cao chướng ngại vật phía trên
                obstacle[2] = max(obstacle[2] * 3/4, 10)  # Giảm chiều cao chướng ngại vật phía dưới

                # Kiểm tra nếu kích thước chướng ngại vật còn lại quá nhỏ, xóa nó
                if obstacle[1] < 10 or obstacle[2] < 10:
                    obstacles.remove(obstacle)

                score += 1  # Cộng điểm khi bắn trúng chướng ngại vật

    # Sinh điểm ngẫu nhiên
    if random.randint(1, 60) == 1:
        points.append([WIDTH, random.randint(50, HEIGHT - 50)])

    # Cập nhật điểm
    for point in points[:]:
        point[0] -= point_speed
        pygame.draw.circle(screen, GREEN, point, point_size)

        # Kiểm tra va chạm giữa đạn và điểm
        for bullet in bullets[:]:
            if abs(bullet[0] - point[0]) < bullet_size + point_size and abs(bullet[1] - point[1]) < bullet_size + point_size:
                bullets.remove(bullet)
                points.remove(point)
                current_bullets += 2  # Cộng 2 viên đạn khi bắn trúng điểm
                if current_bullets > max_bullets:
                    current_bullets = max_bullets  # Đảm bảo số đạn không vượt quá giới hạn

        # Xóa điểm khi ra ngoài màn hình
        if point[0] < 0:
            points.remove(point)

    # Hiển thị điểm và số đạn còn lại
    score_text = font.render(f"Score: {score}", True, BLACK)
    bullets_text = font.render(f"Bullets: {current_bullets}/{max_bullets}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(bullets_text, (10, 50))

    # Cập nhật màn hình
    pygame.display.update()

    # FPS
    pygame.time.Clock().tick(60)

pygame.quit()