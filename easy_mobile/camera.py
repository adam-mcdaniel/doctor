# type Camera struct {
#     state Rect
# }

# func (c *Camera) Apply(Rect Rect) (int, int){
#     return Rect.x + c.state.x, Rect.y + c.state.y
# }

# func (c *Camera) Update(target Rect, w int, h int) {
#     l, t, _, _ := target.Rectangle()
#     bl, bt, wc, hc := c.state.Rectangle()
#     l, t = -l+w/2, -t+h/2

#     l = int(math.Min(0, float64(l)))
#     l = int(math.Max(-float64(c.state.w-w), float64(l)))
#     t = int(math.Max(-float64(c.state.h-h), float64(t)))
#     t = int(math.Min(0, float64(t)))

#     c.state = Rect{bl+(l-bl)/20, bt+(t-bt)/20, wc, hc}
# }
# 
# 
# class Rect:
#     def __init__(self, x, y, w=32, h=32):
#         self.x = x
#         self.y = y
#         self.w = w
#         self.h = h


class Rect():
    def __init__(self,x=0,y=0,w=32,h=32):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.width = w
        self.height = h
        self.center_x = x-w/2
        self.center_y = y-h/2

    def rect(self):
        return self.x,self.y,self.w,self.h

    def position(self,x,y):
        self.x = x
        self.y = y
        self.center_x = x+self.w/2
        self.center_y = y+self.h/2

    def move(self,x,y):
        self.x += x
        self.y += y
        self.center_x += x
        self.center_y += y

    def __str__(self):
        return "<Rect: {}, {}>".format(self.x, self.y)


class Camera(object):
    def __init__(self, camera_func, width, height, ww, wh):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)
        self.WIN_WIDTH, self.WIN_HEIGHT = ww, wh

    def setWinWidth(self, width):
        self.WIN_WIDTH = width

    def setWinHeight(self, height):
        self.WIN_HEIGHT = height

    def setWinSize(self, width, height):
        self.WIN_WIDTH = width
        self.WIN_HEIGHT = height

    def setLevelSize(self, width, height):
        self.state.w = width
        self.state.h = height

    def setLevelWidth(self, width):
        self.state.w = width

    def setLevelHeight(self, height):
        self.state.h = height

    def getLevelWidth(self):
        return self.state.w

    def getLevelHeight(self):
        return self.state.h

    def getLevelSize(self):
        return self.getLevelWidth(), self.getLevelHeight()

    def collide(self, sprite):
        x, y = self.apply(sprite)

        if x >= 0 and x < self.WIN_WIDTH:
            if y >= 0 and y < self.WIN_HEIGHT:
                return True

        if (x > 0 and x < self.WIN_WIDTH) or (x + sprite.getWidth() > 0 and x + sprite.getWidth() < (0 + self.WIN_WIDTH)):
            if (y > 0 and y < self.WIN_HEIGHT) or (y + sprite.getHeight() > 0 and y + sprite.getHeight() < (0 + self.WIN_HEIGHT)):
                return True

        if (y > 0 and y < self.WIN_HEIGHT) or (y + sprite.getHeight() > 0 and y + sprite.getHeight() < (0 + self.WIN_HEIGHT)):
            if (x == 0):
                return True

        if (x > 0 and x < self.WIN_WIDTH) or (x + sprite.getWidth() > 0 and x + sprite.getWidth() < (0 + self.WIN_WIDTH)):
            if (y == 0):
                return True
 
        return False

    def apply(self, target):
        return target.rect.x + self.state.x, target.rect.y + self.state.y

    def update(self, target_rect):
        self.state = self.camera_func(self, self.state, target_rect.rect)



def simple_camera(self, camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    return pygame.Rect(-l+self.WIN_WIDTH/2, -t+self.WIN_HEIGHT/2, w, h)


def complex_camera(self, camera, target_rect):
    l, t, _, _ = target_rect.rect()
    _, _, w, h = camera.rect()
    l, t, _, _ = -l+(self.WIN_WIDTH/2), -t+(self.WIN_HEIGHT/2), w, h

    l = min(0, l)                      # stop scrolling at the left edge
    l = max(-(camera.width-self.WIN_WIDTH), l)   # stop scrolling at the right edge
    t = max(-(camera.height-self.WIN_HEIGHT), t) # stop scrolling at the bottom
    t = min(0, t)                      # stop scrolling at the top

    # globals.view_object[0].rect.left, globals.view_object[0].rect.top, _, _ = pygame.Rect(l, t, w, h)
    # globals.view_object[0].rect.left = -globals.view_object[0].rect.left
    # globals.view_object[0].rect.top = -globals.view_object[0].rect.top
    return Rect(l, t, w, h)
