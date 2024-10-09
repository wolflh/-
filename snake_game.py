import pygame
import random
import sys
import config  # 导入配置文件

# 初始化pygame
pygame.init()

# 设置显示窗口
screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
pygame.display.set_caption('Snake Game')

# 设置时钟
clock = pygame.time.Clock()

def reset_game():
    global snake, direction, food, waiting, game_over_flag, length, game_speed
    snake = [{'x': random.randint(0, config.WINDOW_WIDTH // config.CELL_SIZE - 1),
              'y': random.randint(0, config.WINDOW_HEIGHT // config.CELL_SIZE - 1)}]
    direction = config.INITIAL_DIRECTION
    food = {'x': random.randint(0, config.WINDOW_WIDTH // config.CELL_SIZE - 1),
            'y': random.randint(0, config.WINDOW_HEIGHT // config.CELL_SIZE - 1)}
    waiting = False
    game_over_flag = False
    length = 1
    game_speed = config.GAME_SPEED

reset_game()

def game_over():
    global game_over_flag, waiting
    game_over_flag = True
    font = pygame.font.SysFont(None, 55)
    game_over_surface = font.render('Game Over', True, config.RED)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 4)
    screen.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == config.RESTART_KEY:
                    reset_game()
                    waiting = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                direction = 'UP'
            elif event.key == pygame.K_DOWN and direction != 'UP':
                direction = 'DOWN'
            elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                direction = 'LEFT'
            elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                direction = 'RIGHT'

    if waiting:
        continue

    new_head = snake[0].copy()  # Copy the head to create a new head
    if direction == 'UP':
        new_head['y'] -= 1
    elif direction == 'DOWN':
        new_head['y'] += 1
    elif direction == 'LEFT':
        new_head['x'] -= 1
    elif direction == 'RIGHT':
        new_head['x'] += 1

    if (new_head['x'] < 0 or new_head['x'] >= config.WINDOW_WIDTH // config.CELL_SIZE or
        new_head['y'] < 0 or new_head['y'] >= config.WINDOW_HEIGHT // config.CELL_SIZE or
        new_head in snake):
        game_over()
        continue

    snake.insert(0, new_head)
    if new_head['x'] == food['x'] and new_head['y'] == food['y']:
        food = {'x': random.randint(0, (config.WINDOW_WIDTH // config.CELL_SIZE) - 1),
                'y': random.randint(0, (config.WINDOW_HEIGHT // config.CELL_SIZE) - 1)}
        length += 1
        game_speed += config.SPEED_INCREMENT
    else:
        snake.pop()

    screen.fill(config.BLACK)
    for segment in snake:
        pygame.draw.rect(screen, config.GREEN, (segment['x'] * config.CELL_SIZE, segment['y'] * config.CELL_SIZE, config.CELL_SIZE, config.CELL_SIZE))
    pygame.draw.rect(screen, config.RED, (food['x'] * config.CELL_SIZE, food['y'] * config.CELL_SIZE, config.CELL_SIZE, config.CELL_SIZE))

    # 显示蛇的长度
    font = pygame.font.SysFont(None, 28)
    length_surface = font.render(f'Length: {length}', True, pygame.Color('white'))
    screen.blit(length_surface, (5, 5))

    pygame.display.flip()
    clock.tick(game_speed)  # 使用动态更新的速度值
