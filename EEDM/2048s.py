# 有空可以接着优化例如加个play，选择难度等

import pygame
import random
import sys
from pygame.locals import *

PIXEL = 150
SCORE_PIXEL = 100
SIZE = 4

# 地图类
class Map:
    def __init__(self,size):
        self.size = size
        self.score = 0
        self.map = [[0 for i in range(size) ]for j in range(size)]
        self.add()
        self.add()

    # 新增2或4，有1/4概率产生4
    def add(self):
        while True:
            # 随机生成直到生成成功
            p = random.randint(0, self.size * self.size - 1)
            if self.map[int(p / self.size)][p % self.size] == 0:
                x = 2 if random.randint(0,3) > 0 else 4
                self.map[int(p / self.size)][p % self.size] = x
                self.score += x
                break

    # 地图向左靠拢，其他方向的靠拢可以通过适当旋转实现，返回地图是否更新
    def adjust(self):
        changed = False
        for a in self.map:
            b = []
            last = 0
            for v in a:
                if v != 0:
                    if v ==last:
                        # 相同合并乘二
                        b.append(b.pop() << 1)
                        last = 0
                    else:
                        b.append(v)
                        last = v
            b += [0] * (self.size - len(b))
            for i in range(self.size):
                if a[i] != b[i]:
                    changed = True
            a[:] = b
        return changed

    # 逆时针旋转地图90度!
    def rotate90(self):
        self.map = [[self.map[c][r] for c in range(self.size)] for r in reversed(range(self.size))]

    # 判断GAMEOVER
    def over(self):
        for r in range(self.size):
            for c in range(self.size):
                if self.map[r][c] == 0:
                    return False
        for r in range(self.size):
            for c in range(self.size - 1):
                if self.map[r][c] == self.map[r][c + 1]:
                    return False
        for r in range(self.size - 1):
            for c in range(self.size):
                if self.map[r][c] == self.map[r + 1][c]:
                    return False
        return True

    # 各种移动
    def moveUp(self):
        self.rotate90()
        if self.adjust():
            self.add()
        self.rotate90()
        self.rotate90()
        self.rotate90()

    def moveRight(self):
        self.rotate90()
        self.rotate90()
        if self.adjust():
            self.add()
        self.rotate90()
        self.rotate90()

    def moveDown(self):
        self.rotate90()
        self.rotate90()
        self.rotate90()
        if self.adjust():
            self.add()
        self.rotate90()

    def moveLeft(self):
        if self.adjust():
            self.add()

# 屏幕更新
def show(map):
    for i in range(SIZE):
        for j in range(SIZE):
            # 背景颜色块
            screen.blit(map.map[i][j] == 0 and block[(i + j) % 2] or block[2 + (i + j) % 2], (PIXEL * j, PIXEL * i))
            # 设定数值
            if map.map[i][j] != 0:
                map_text = map_font.render(str(map.map[i][j]), True, (106, 90, 205))
                # rect返回一个矩形
                text_rect = map_text.get_rect()
                text_rect.center = (PIXEL * j + PIXEL / 2, PIXEL * i + PIXEL / 2)
                screen.blit(map_text, text_rect)
            # 分数显示
        screen.blit(score_block, (0, PIXEL * SIZE))
        score_text = score_font.render((map.over() and "Game over with score " or "Score: ") + str(map.score), True,
                                       (106, 90, 205))
        score_rect = score_text.get_rect()
        score_rect.center = (PIXEL * SIZE / 2, PIXEL * SIZE + SCORE_PIXEL / 2)
        screen.blit(score_text, score_rect)
        pygame.display.update()


map = Map(SIZE)
pygame.init()
#窗体
screen = pygame.display.set_mode((PIXEL * SIZE, PIXEL * SIZE + SCORE_PIXEL))
# 标题
pygame.display.set_caption("2048")
# https://blog.csdn.net/katyusha1/article/details/78352802
# 绘制一个矩形
block = [pygame.Surface((PIXEL, PIXEL)) for i in range(4)]
# 设置颜色块 Surface.fill表面用颜色。4种颜色类别
block[0].fill((152, 251, 152))
block[1].fill((240, 255, 255))
block[2].fill((0, 255, 127))
block[3].fill((225, 255, 255))
# 分数区颜色
score_block = pygame.Surface((PIXEL * SIZE, SCORE_PIXEL))
score_block.fill((245, 245, 245))
# 设置字体
map_font = pygame.font.Font(None, int(PIXEL * 2 / 3))
score_font = pygame.font.Font(None, int(SCORE_PIXEL * 2 / 3))
clock = pygame.time.Clock()
show(map)

while not map.over():
	# 12为实验参数
	clock.tick(12)
	# 接收玩家操作
	for event in pygame.event.get():
		if event.type == QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
				map.moveRight()
			elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
				map.moveLeft()
			elif event.key == pygame.K_UP or event.key == pygame.K_w:
				map.moveUp()
			elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
				map.moveDown()
			elif event.key ==pygame.K_q:
				map = Map(SIZE)
			show(map)

# 游戏结束
pygame.time.delay(3000)
