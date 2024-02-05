import sys
import pygame

from components.tilemap import Tilemap

from config.utils import load_images
from config.constants import SCREEN_HEIGHT, SCREEN_WIDTH, FPS, RENDER_SCALE

class Editor:
  def __init__(self) -> None:
    pygame.init()

    pygame.display.set_caption("Editor: Smash Ninja")
    self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    self.display = pygame.Surface((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)) # SCALING UP

    self.clock = pygame.time.Clock()
    
    self.assets = {
      'decor': load_images('tiles/decor'),
      'grass': load_images('tiles/grass'),
      'large_decor': load_images('tiles/large_decor'),
      'stone': load_images('tiles/stone'),
    }
    
    self.movement = [False, False, False, False]
    
    self.tilemap = Tilemap(self, tile_size=16)

    #CAMERA
    self.scroll = [0, 0]
    
    self.tile_list = list(self.assets)
    self.tile_group = 0
    self.tile_variant = 0
    
    self.clicking = False
    self.right_clicking = False
    self.shift = False
    self.position = (0, 0)

  def run(self) -> None:
    while True:
      self.display.fill((0, 0, 0))
      render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
      
      self.tilemap.render(self.display, offset=render_scroll)

      current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
      current_tile_img.set_alpha(150)
      
      mpos = pygame.mouse.get_pos()
      mpos = (mpos[0] / RENDER_SCALE, mpos[1] / RENDER_SCALE)
      tile_pos = ((int(mpos[0] + self.scroll[0]) // self.tilemap.tile_size),
                  (int(mpos[1] + self.scroll[1]) // self.tilemap.tile_size))
      
      tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
      
      self.display.blit(current_tile_img, (
        tile_pos[0] * self.tilemap.tile_size - self.scroll[0], 
        tile_pos[1] * self.tilemap.tile_size - self.scroll[1]))
      
      if self.clicking:
        self.tilemap.tilemap[tile_loc] = {
          'type': self.tile_list[self.tile_group],
          'variant': self.tile_variant,
          'pos': tile_pos
        }
      if self.right_clicking:
        if tile_loc in self.tilemap.tilemap:
          del self.tilemap.tilemap[tile_loc]
      
      self.display.blit(current_tile_img, self.position)

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
          if event.button == 1:
            self.clicking = True
          if event.button == 3:
            self.right_clicking = True
          if self.shift:
            if event.button == 4:
              self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]])
            if event.button == 5:
              self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]])
          else:
            if event.button == 4:
              self.tile_group = (self.tile_group - 1) % len(self.tile_list)
              self.tile_variant = 0
            if event.button == 5:
              self.tile_group = (self.tile_group + 1) % len(self.tile_list)
              self.tile_variant = 0
        if event.type == pygame.MOUSEBUTTONUP:
          if event.button == 1:
            self.clicking = False
          if event.button == 3:
            self.right_clicking = False
        
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_LSHIFT:
            self.shift = True
          if event.key == pygame.K_LEFT:
            self.movement[0] = True
          if event.key == pygame.K_RIGHT:
            self.movement[1] = True
          if event.key == pygame.K_UP:
            self.movement[2] = True
          if event.key == pygame.K_DOWN:
            self.movement[3] = True
        if event.type == pygame.KEYUP:
          if event.key == pygame.K_LSHIFT:
            self.shift = False
          if event.key == pygame.K_LEFT:
            self.movement[0] = False
          if event.key == pygame.K_RIGHT:
            self.movement[1] = False
          if event.key == pygame.K_UP:
            self.movement[2] = False
          if event.key == pygame.K_DOWN:
            self.movement[3] = False
      
      self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)) # BLIT FOR SCALING UP
      pygame.display.update()
      self.clock.tick(FPS)
      
Editor().run()