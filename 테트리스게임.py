import pygame
import random

# 초기화
pygame.init()

# 화면 크기
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)

# 테트리스 블록 모양
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]],  # J
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]]   # Z
]

# 게임 보드 크기
BOARD_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
BOARD_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE

# 블록 클래스
class Block:
    def __init__(self, shape):
        self.shape = shape
        self.color = random.choice([RED, GREEN, BLUE, CYAN, MAGENTA, YELLOW])
        self.x = BOARD_WIDTH // 2 - len(shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

# 게임 보드 클래스
class Board:
    def __init__(self):
        self.grid = [[BLACK for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

    def can_move(self, block, dx, dy):
        for y, row in enumerate(block.shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = block.x + x + dx
                    new_y = block.y + y + dy
                    if new_x < 0 or new_x >= BOARD_WIDTH or new_y >= BOARD_HEIGHT:
                        return False
                    if new_y >= 0 and self.grid[new_y][new_x] != BLACK:
                        return False
        return True

    def place_block(self, block):
        for y, row in enumerate(block.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[block.y + y][block.x + x] = block.color

    def clear_lines(self):
        self.grid = [row for row in self.grid if any(cell == BLACK for cell in row)]
        while len(self.grid) < BOARD_HEIGHT:
            self.grid.insert(0, [BLACK for _ in range(BOARD_WIDTH)])

# 게임 루프
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("테트리스")
    clock = pygame.time.Clock()

    board = Board()
    current_block = Block(random.choice(SHAPES))
    running = True

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and board.can_move(current_block, -1, 0):
                    current_block.x -= 1
                elif event.key == pygame.K_RIGHT and board.can_move(current_block, 1, 0):
                    current_block.x += 1
                elif event.key == pygame.K_DOWN and board.can_move(current_block, 0, 1):
                    current_block.y += 1
                elif event.key == pygame.K_UP:
                    current_block.rotate()
                    if not board.can_move(current_block, 0, 0):  # 회전 불가능하면 되돌림
                        current_block.rotate()
                        current_block.rotate()
                        current_block.rotate()

        if board.can_move(current_block, 0, 1):
            current_block.y += 1
        else:
            board.place_block(current_block)
            board.clear_lines()
            current_block = Block(random.choice(SHAPES))
            if not board.can_move(current_block, 0, 0):  # 새 블록이 움직일 수 없으면 게임 종료
                running = False

        # 보드 그리기
        for y, row in enumerate(board.grid):
            for x, cell in enumerate(row):
                if cell != BLACK:
                    pygame.draw.rect(screen, cell, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        # 현재 블록 그리기
        for y, row in enumerate(current_block.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, current_block.color, ((current_block.x + x) * BLOCK_SIZE, (current_block.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        pygame.display.flip()
        clock.tick(5)  # FPS를 5로 설정하여 게임 속도를 느리게 조정

    pygame.quit()

if __name__ == "__main__":
    main()