import pygame
import random
screen_width=600
screen_hight=700
player_in_center=(300,350)
player_color=(0,255,245)
ball_color=(255,0,95)
text=(200,200,200)
screen_color=(13,17,23)
player_size=(50,50)
ball_size=(30,30)
class player:
      def __init__(self):
          self.image=pygame.Surface(player_size)
          self.image.fill(player_color)
          self.rect=(self.image.get_rect(center=player_in_center))
          self.speed=8
      def move(self):
          kays=pygame.key.get_pressed()
          if kays[pygame.K_LEFT] and self.rect.left>0:
             self.rect.x-=self.speed
          if kays[pygame.K_RIGHT] and self.rect.right<screen_width:
             self.rect.x+=self.speed
      def draw(self,screen):
          screen.blit(self.image,self.rect)
class ball:
      def __init__(self):
          self.image=pygame.Surface(ball_size)
          self.image.fill(ball_color)
          self.rect=self.image.get_rect()
          self.reset()

      def fall(self):
          self.rect.y+=self.speed
      def reset(self):
          self.rect.x=random.randint(0,screen_width-30)
          self.rect.y=random.randint(-150,-50)
          self.speed=random.randint(4,9)
      def draw(self,screen):
          screen.blit(self.image,self.rect)
class game:
    def __init__(self):
        pygame.init() 
        self.screen=pygame.display.set_mode((screen_width,screen_hight))
        pygame.display.set_caption("avoid ball game")
        self.player=player()
        self.clock=pygame.time.Clock()
        self.balls=[ball() for i in range(3)]
        self.score=0
        self.font=pygame.font.SysFont("Arial",30)
        self.running=True
    def run(self):
        while self.running:
              self.screen.fill(screen_color)
              for event in pygame.event.get():
                  if event.type == pygame.QUIT:
                     self.running=False
              self.player.move()
              for b in self.balls:
                  b.fall()
                  if b.rect.top > screen_hight:
                     b.reset()
                     self.score+=1
                  if self.player.rect.colliderect(b.rect):
                     print("game over!!!!!!! score: ",self.score)
                     self.running=False
              self.player.draw(self.screen)
              for b in self.balls:
                  b.draw(self.screen)
              score_surf = self.font.render(f"Score: {self.score}", True, text)
              self.screen.blit(score_surf, (10, 10))
              pygame.display.flip() 
              self.clock.tick(60) 

        pygame.quit()
if __name__ == "__main__":
    my_game = game()
    my_game.run()
