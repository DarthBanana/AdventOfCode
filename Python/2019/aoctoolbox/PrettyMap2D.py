from Map2D import *
import pygame
IMAGES = {}
MAX_TILE_DIM = 20
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

def display_text(text_to_display, colour):
    
    text = font.render(text_to_display, True, colour)
    text_rect = text.get_rect()
    dim = max(text_rect.width, text_rect.height)
    print(dim)
    text_rect.center = (TILE_IMAGE_WIDTH/2, TILE_IMAGE_HEIGHT/2)
    image = pygame.Surface((TILE_IMAGE_WIDTH, TILE_IMAGE_HEIGHT))
    image.fill((50,50,50))
    image.blit(text, text_rect)
    #scaled = pygame.transform.scale(image, (TILE_IMAGE_WIDTH, TILE_IMAGE_HEIGHT))
    

    return image
def get_sprite_image(value):
    if (value, TILE_IMAGE_HEIGHT) in IMAGES:
        return IMAGES[(value, TILE_IMAGE_HEIGHT)]
    else:
        sprite_image = display_text(str(value), (200,200,200))        
        IMAGES[(value, TILE_IMAGE_HEIGHT)] = sprite_image
    return sprite_image

class Tile(pygame.sprite.DirtySprite):
    def __init__(self, value, x, y, map_left, map_top, minx, miny):
        super().__init__()
        
        self.value = None
        self.x = x
        self.y = y
        self.set_value(value)        
        self.update(map_left, map_top, minx, miny)
        

    def set_value(self, value):                
        if self.value != value:
            self.value = value
            self.dirty = True
            self.image = get_sprite_image(value)

    def update(self, map_left, map_top, minx, miny):
        self.image = get_sprite_image(self.value)
        self.rect = self.image.get_rect()
        self.rect.x = map_left + ((self.x - minx) * TILE_IMAGE_WIDTH)
        self.rect.y = map_top + ((self.y-miny) * TILE_IMAGE_HEIGHT)    
        self.dirty = True


class PrettyInfiniteGrid(InfiniteGrid):
    def __init__(self):
        super().__init__()
        self.characters = {}
        self.sprites = {}
        self.render_group = pygame.sprite.Group()       
        self.screen = pygame.display.set_mode((1024, 768))
        self.last_width = None
        self.last_height= None
        self.map_left = 0
        self.map_top = 0


    def __setitem__(self, k, value):  
        print("Setting ", k, " to ", value)
        super().__setitem__(k, value)                
        if k in self.sprites:
            sprite = self.sprites[k]
            sprite.set_value(value)
        else:
            sprite = Tile(value, k.x, k.y, self.map_left, self.map_top, self.minx, self.miny)
            self.sprites[k] = sprite
            self.render_group.add(sprite)
            #sprite.groups = self.render_group
        
        self.refresh()

    def rescale(self, width, height):
        print("Rescaling to ", width, height)
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        tile_width = screen_width // width
        tile_height = screen_height // height
        tile_dim = min(tile_width, tile_height, MAX_TILE_DIM)
        tile_dim = max(tile_dim, MIN_TILE_DIM)
        map_width = width * TILE_IMAGE_WIDTH
        map_height = height * TILE_IMAGE_HEIGHT
        if width < screen_width:
            self.map_left = (screen_width - map_width) // 2
        else:
            self.map_left = 0
        if height < screen_height:
            self.map_top = (screen_height - map_height) // 2
        else:
            self.map_top = 0
        print(self.map_left, self.map_top)
        upate_tile_size(tile_dim)
        self.render_group.update(self.map_left, self.map_top, self.minx, self.miny)

            

    def refresh(self):        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        new_width = self.get_width()
        new_height = self.get_height()
        if self.last_width != new_width or self.last_height != new_height:
            self.rescale(new_width, new_height)
            self.last_width = new_width
            self.last_height = new_height

        pygame.sprite.Group.draw(self.render_group, self.screen)
        pygame.display.update()
