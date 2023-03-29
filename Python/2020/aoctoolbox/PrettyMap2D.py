
from time import sleep
from Map2D import *
import pygame
IMAGES = {}
MAX_TILE_DIM = 40
MIN_TILE_DIM = 8
TILE_IMAGE_WIDTH = 20
TILE_IMAGE_HEIGHT = 20

pygame.font.init()
def upate_tile_size(dim):
    global font
    global TILE_IMAGE_WIDTH
    global TILE_IMAGE_HEIGHT
    font = pygame.font.SysFont('Courrier', dim)
    TILE_IMAGE_WIDTH = font.size("#")[0]
    TILE_IMAGE_HEIGHT = font.size("#")[1]

upate_tile_size(MAX_TILE_DIM)

def display_text(text_to_display, width, height, colour):
    
    text = font.render(text_to_display, True, colour)
    text_rect = text.get_rect()
    dim = max(text_rect.width, text_rect.height)
    #print(dim)
    text_rect.center = (width/2, height/2)
    image = pygame.Surface((width, height))
    image.fill((50,50,50))
    image.blit(text, text_rect)
    #scaled = pygame.transform.scale(image, (TILE_IMAGE_WIDTH, TILE_IMAGE_HEIGHT))
    return image


class SpriteSource():
    def __init__(self):
        self.images = {}
        self.width = TILE_IMAGE_WIDTH
        self.heigth = TILE_IMAGE_WIDTH
        self.sizes = {}
        for i in range(MIN_TILE_DIM, MAX_TILE_DIM+1):
            font = pygame.font.SysFont('Courrier', i)
            width = font.size("#")[0]
            height = font.size("#")[1]
            self.sizes[i] = (width, height)            

    def upate_tile_size(self, width, height):
        
        global font
        global TILE_IMAGE_WIDTH
        global TILE_IMAGE_HEIGHT
        tile_dim = min(width, height, MAX_TILE_DIM)
        tile_dim = max(tile_dim, MIN_TILE_DIM)   
            
        best_size = MIN_TILE_DIM        
        for dim in range(MIN_TILE_DIM, MAX_TILE_DIM + 1):
            (w, h) = self.sizes[dim]            
            if w > width or h > height:
                break
            best_size = dim

        font = pygame.font.SysFont('Courrier', best_size)
        TILE_IMAGE_WIDTH = font.size("#")[0]
        TILE_IMAGE_HEIGHT = font.size("#")[1]
        self.width = TILE_IMAGE_WIDTH
        self.height = TILE_IMAGE_HEIGHT
        

    def generate_sprite_image(self, value, width, height):
        sprite_image = display_text(str(value), width, height, (200,200,200))  
        return sprite_image

    def get_sprite_image(self, value):
        if (value, self.width, self.height) in self.images:
            return self.images[(value, self.width, self.height)]
        else:
            sprite_image = self.generate_sprite_image(value, self.width, self.height)            
            self.images[(value, self.width, self.height)] = sprite_image
        return sprite_image
    
class Tile(pygame.sprite.Sprite):
    def __init__(self, sprite_source, value, x, y, map_left, map_top, minx, miny):
        super().__init__()
        
        self.value = None
        self.x = x
        self.y = y
        self.sprite_source = sprite_source
        self.set_value(value)        
        self.update(map_left, map_top, minx, miny)
        
    def set_value(self, value):                
        if self.value != value:
            self.value = value
            self.dirty = True
            self.image = self.sprite_source.get_sprite_image(value)

    def move(self, x, y):
        self.x = x
        self.y = y
        
        self.update(self.map_left, self.map_top, self.minx, self.miny)

    def update(self, map_left, map_top, minx, miny):
        self.image = self.sprite_source.get_sprite_image(self.value)
        self.rect = self.image.get_rect()
        assert(self.rect)
        #print(map_left, self.x, minx, self.sprite_source.width)
        self.rect.x = map_left + ((self.x - minx) * self.sprite_source.width)
        self.rect.y = map_top + ((self.y-miny) * self.sprite_source.height)   
        self.source_rect = self.image.get_rect() 
        self.source_rect.x = map_left
        self.source_rect.y = map_top
        self.map_left = map_left
        self.map_top = map_top
        self.minx = minx
        self.miny = miny
        self.dirty = True

class PrettyMap2DOverlay(Map2DOverlay):
    def __init__(self, map, altitude):
        super().__init__(map, altitude)

        self.sprites = {}
        self.overlay_group = pygame.sprite.RenderPlain()        
    
    def __setitem__(self, k, value):
        super().__setitem__(k, value)
        if k in self.sprites:
            sprite = self.sprites[k]
            sprite.set_value(value)
        else:
            sprite = Tile(self.attached_map.sprite_source, value, k.x, k.y, self.attached_map.map_left, self.attached_map.map_top, self.attached_map.minx, self.attached_map.miny)
            self.sprites[k] = sprite
            sprite.groups = self.overlay_group
            self.overlay_group.add(sprite)
        self.attached_map.try_auto_refresh()    
    
    def update(self, map_left, map_top, minx, miny):
        for sprite in self.sprites.values():
            sprite.update(map_left, map_top, minx, miny)
        #self.attached_map.try_auto_refresh()
        

    def draw(self):
        self.overlay_group.draw(self.attached_map.screen)
        

class PrettyMap2D(Map2D):
    def __init__(self, default=" ", sprite_source=None, lines=None):
        
        if sprite_source is None:
            sprite_source = SpriteSource()
        self.sprite_source = sprite_source
        self.autodraw = False  
        self.sprites = {}
        self.screen = pygame.display.set_mode((1024, 768), pygame.RESIZABLE)
        super().__init__(default, lines=lines)      
        self.autodraw = True
        #self.reset()

    #def reset(self):
        
    def clear(self):
        super().clear()
        self.render_group = pygame.sprite.RenderPlain()       
        self.overlay_group = pygame.sprite.RenderPlain()        
        self.last_width = None
        self.last_height= None
        self.map_left = 0
        self.map_top = 0
        self.rescale(1,1)
        self.pointer = None


    def get_new_overlay(self, altitude):
        print("new_overlay")
        return PrettyMap2DOverlay(self, altitude)
    
    def __setitem__(self, k, value):  
        #print("Setting ", k, " to ", value)
        super().__setitem__(k, value)                
        if k in self.sprites:
            sprite = self.sprites[k]
            #sprite.remove(self.render_group)
            sprite.set_value(value)
        else:
                    
            sprite = Tile(self.sprite_source, value,  k.x, k.y, self.map_left, self.map_top, self.minx, self.miny)
            self.sprites[k] = sprite
            sprite.groups = self.render_group
            self.render_group.add(sprite)

        self.try_auto_refresh()
        

    def set_pointer(self, k, value):
        if self.pointer:
            self.pointer.move(k.x, k.y)
            self.pointer.set_value(value)
        else:
            self.pointer = Tile(self.sprite_source, value, k.x, k.y, self.map_left, self.map_top, self.minx, self.miny)
            self.pointer.groups = self.overlay_group
            self.overlay_group.add(self.pointer)
        
        self.try_auto_refresh()
        

    def rescale(self, width, height):
        #print("Rescaling to ", width, height)        
        width = max(width, 1)
        height = max(height, 1)
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        tile_width = screen_width // width
        tile_height = screen_height // height
        #print(tile_width, tile_height)
        self.sprite_source.upate_tile_size(tile_width, tile_height)
        map_width = width * self.sprite_source.width
        map_height = height * self.sprite_source.height        
        if map_width < screen_width:
            self.map_left = (screen_width - map_width) // 2
        else:
            self.map_left = 0
        if map_height < screen_height:
            self.map_top = (screen_height - map_height) // 2
        else:
            self.map_top = 0

        self.render_group.update(self.map_left, self.map_top, self.minx, self.miny)
        self.overlay_group.update(self.map_left, self.map_top, self.minx, self.miny)        
        for overlay in self.overlays:
            overlay.update(self.map_left, self.map_top, self.minx, self.miny)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                self.rescale(self.get_width(), self.get_height())
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    def try_auto_refresh(self):
        if self.autodraw:
            self.refresh()

    def refresh(self):           
        self.check_events()     
        new_width = self.get_width()
        new_height = self.get_height()
        if self.last_width != new_width or self.last_height != new_height:
            self.rescale(new_width, new_height)
            self.last_width = new_width
            self.last_height = new_height
        
        
        self.screen.fill((0, 0, 0))
        
        pygame.sprite.Group.draw(self.render_group, self.screen)
        for overlay in self.overlays:
            #print("Drawing overlay")
            overlay.draw()

        pygame.sprite.Group.draw(self.overlay_group, self.screen)
        
        pygame.display.flip()
    
class PrettyInfiniteGrid(PrettyMap2D):
    def __init__(self, default=' '):
        super().__init__(default)