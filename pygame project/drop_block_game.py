import pygame
import sys

WIDTH, HEIGHT = 400, 600
FPS = 60
BLOCK_W, BLOCK_H = 60, 30

class Block:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, BLOCK_W, BLOCK_H)
        self.color = color
        self.is_falling = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.crane_x = 0
        self.crane_dir = 1
        self.base = pygame.Rect(0, HEIGHT - 40, WIDTH, 40)
        self.stack = []
        self.current_block = Block(0, 60, (255, 100, 0))

    def spawn_new_block(self):
        self.current_block = Block(self.crane_x, 60, (255, 100, 0))

    def run(self):
        while True:
            self.screen.fill((200, 230, 255))
            pygame.draw.rect(self.screen, (139, 69, 19), self.base)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not self.current_block.is_falling:
                        self.current_block.is_falling = True

            if not self.current_block.is_falling:
                self.crane_x += 5 * self.crane_dir
                if self.crane_x <= 0 or self.crane_x >= WIDTH - BLOCK_W:
                    self.crane_dir *= -1
                self.current_block.rect.x = self.crane_x

            if self.current_block.is_falling:
                self.current_block.rect.y += 8
                
                if not self.stack:
                    if self.current_block.rect.colliderect(self.base):
                        self.current_block.rect.bottom = self.base.top
                        self.stack.append(self.current_block)
                        self.spawn_new_block()
                else:
                    last_block = self.stack[-1]
                    if self.current_block.rect.colliderect(last_block.rect):
                        self.current_block.rect.bottom = last_block.rect.top
                        self.stack.append(self.current_block)
                        self.spawn_new_block()

                if self.current_block.rect.top > HEIGHT:
                    self.stack = []
                    self.spawn_new_block()

            self.current_block.draw(self.screen)
            for b in self.stack:
                b.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()