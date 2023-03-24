
from Map2D import *
import pyglet
IMAGES = {}
MAX_TILE_DIM = 40
MIN_TILE_DIM = 8
TILE_IMAGE_WIDTH = 20
TILE_IMAGE_HEIGHT = 20


def upate_tile_size(dim):
    pass
    #global font
    #global TILE_IMAGE_WIDTH 
    #global TILE_IMAGE_HEIGHT 
    #font = pyglet.font.load('Courrier New', dim)
    #TILE_IMAGE_HEIGHT = font.ascent + font.descent
    #TILE_IMAGE_WIDTH = font.advance("#")

    #TILE_IMAGE_WIDTH = font.size("#")[0]
    #TILE_IMAGE_HEIGHT = font.size("#")[1]

#upate_tile_size(MAX_TILE_DIM)

def display_text(text_to_display, colour):
    text= pyglet.text.Label(text_to_display, font_name='Times New Roman', font_size=20, x=0, y=0, anchor_x='left', anchor_y='top')
    return text

def get_sprite_image(value):
    if (value, TILE_IMAGE_HEIGHT) in IMAGES:
        return IMAGES[(value, TILE_IMAGE_HEIGHT)]
    else:
        sprite_image = display_text(str(value), (200,200,200))        
        IMAGES[(value, TILE_IMAGE_HEIGHT)] = sprite_image
    return sprite_image

class Tile():
    def __init__(self, value, x, y, map_left, map_top, minx, miny):
        
        
        self.value = None
        self.myx = x
        self.myy = y
        self.set_value(value)        
        self.update(map_left, map_top, minx, miny)
        

    def set_value(self, value):                
        if self.value != value:
            self.value = value            
            self.image = get_sprite_image(value)

    def update(self, map_left, map_top, minx, miny):
        self.image = get_sprite_image(self.value)        
        self.x = map_left + ((self.myx - minx) * TILE_IMAGE_WIDTH)
        self.y = map_top + ((self.myy-miny) * TILE_IMAGE_HEIGHT)   
        self.image.x = self.x
        self.image.y = self.y

        self.dirty = True
    def on_draw(self):
        self.image.draw()

class PrettyInfiniteGrid(InfiniteGrid):
    def __init__(self):
        super().__init__()
        self.characters = {}
        self.sprites = {}  
        self.render_group = pyglet.graphics.Batch()
        
        
        self.screen = pyglet.window.Window(1280, 720)
        self.last_width = None
        self.last_height= None
        self.map_left = 0
        self.map_top = 0
        self.rescale(1,1)



    def __setitem__(self, k, value):  
        #print("Setting ", k, " to ", value)
        super().__setitem__(k, value)                
        if k in self.sprites:
            sprite = self.sprites[k]
            #sprite.remove(self.render_group)
            sprite.set_value(value)
        else:
                    
            sprite = Tile(value, k.x, k.y, self.map_left, self.map_top, self.minx, self.miny)
            self.sprites[k] = sprite
            #sprite.groups = self.render_group
            #self.render_group.add(sprite)
        
        
        self.refresh()

    def rescale(self, width, height):
        #print("Rescaling to ", width, height)
        print(self.render_group)
        screen_width = self.screen._width
        screen_height = self.screen._height
        #self.background = pygame.Surface(self.screen.get_size())
        #self.background = self.background.convert()
        #self.background.fill((0, 0, 50))        

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
        #print(self.map_left, self.map_top)
        upate_tile_size(tile_dim)
        for sprite in self.sprites.values():
            sprite.update(self.map_left, self.map_top, self.minx, self.miny)
        #self.render_group.update(self.map_left, self.map_top, self.minx, self.miny)
        #self.render_group.clear(self.screen, self.background)

    def check_events(self):
        pass

    def refresh(self):           
        self.check_events()     
        new_width = self.get_width()
        new_height = self.get_height()
        if self.last_width != new_width or self.last_height != new_height:
            self.rescale(new_width, new_height)
            self.last_width = new_width
            self.last_height = new_height
        
        
        #self.render_group.clear(self.screen, self.background)
        #rects = self.render_group.draw(self.screen)
        for sprite in self.sprites.values():
            sprite.on_draw()
        #self.render_group.draw()
    


