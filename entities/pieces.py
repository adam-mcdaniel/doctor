from easy_mobile.setup import SCREEN_WIDTH, SCREEN_HEIGHT
from easy_mobile.sprite import Sprite
from .tiles import *
from .__init__ import *

from random import randint

sign = lambda x: x and (1, -1)[x < 0]


def evalMove(screen, x, y, cx=None, cy=None, isQueen=False, deep=True):
    points = 0
    q = BlackQueen(x, y)
    for sprite in screen:
        if isinstance(sprite, WhitePiece):
            sx, sy = sprite.toBoardPos(sprite.getX(), sprite.getY())
            if sx == x and sy == y:
                if isinstance(sprite, WhiteQueen):
                    points += 1000000000000000000000000000000000000000000
                elif isinstance(sprite, WhiteCastle):
                    points += 5000
                elif isinstance(sprite, WhiteKnight):
                    points += 5000
                elif isinstance(sprite, WhiteKing):
                    points += 3000
                elif isinstance(sprite, WhitePawn):
                    points += 2500
                else:
                    points += 2500

                if cx and cy:
                    if abs(sx - cx) <= 2 and abs(sy - cy) <= 2:
                        points += 10000

            elif abs(sx - x) <= 2 and abs(sy - y) <= 2 and deep:
                points -= evalMove(screen, sx, sy, deep=False) / 2

            # elif not sprite.check(screen, sx, sy, x, y):
            #     points -= 1000
                    
            # else:
            #     if not q.check(screen, x, y, sx, sy):
            #         points += 1010000

        elif isinstance(sprite, BlackPiece):
            sx, sy = sprite.toBoardPos(sprite.getX(), sprite.getY())
            if not sprite.check(screen, sx, sy, x, y):
                points += 1000
    
    return points
   

class Piece(Sprite):
    def __init__(self, x, y, *args, **kwargs):
        self.shrink = 2.5

        self.saveX, self.saveY = x, y

        self.locked = False
        self.moved = False
        super(Piece, self).__init__(x*WIDTH+WIDTH / (self.shrink*2),
                                    y*HEIGHT+START_HEIGHT+HEIGHT / (self.shrink*2),
                                    *args, **kwargs,
                                    width=WIDTH-WIDTH / self.shrink,
                                    height=HEIGHT-HEIGHT / self.shrink)
    
    def setMoved(self):
        self.moved = True
    
    def getMoved(self):
        moved = self.moved
        self.moved = False
        return moved

    def getMoves(self, screen, cx=None, cy=None):
        if not cx or not cy:
            cx, cy = self.toBoardPos(self.getX(), self.getY())
        for y in range(0, BOARD_HEIGHT):
            for x in range(0, BOARD_WIDTH):
                if not (cx == x and cy == y) and not self.check(screen, cx, x, cy, y):
                    yield (x, y)

    def check(self, screen, x1, x2, y1, y2): return True
    
    def set(self):
        x = round(self.getX() / WIDTH)
        y = round((self.getY() - START_HEIGHT) / HEIGHT)

        x = max(min(x, BOARD_WIDTH-1), 0)
        y = max(min(y, BOARD_HEIGHT-1), 0)

        # if round((self.getY() - START_HEIGHT) / HEIGHT - 0.2, 1) != y:
        #     print((self.getY() - START_HEIGHT) / HEIGHT, y)

        self.goto(
            x*WIDTH+WIDTH / (self.shrink*2),
            y*HEIGHT+START_HEIGHT+HEIGHT / (self.shrink*2)
            )

    def toBoardPos(self, x, y):
        
        x = round(x / WIDTH)
        y = round((y - START_HEIGHT) / HEIGHT)

        x = max(min(x, BOARD_WIDTH-1), 0)
        y = max(min(y, BOARD_HEIGHT-1), 0)

        return x, y

    def update(self, screen):
        if self.getTouchDown() or self.locked:
            self.locked = True


            for sprite in screen:
                if isinstance(sprite, Piece):
                    if sprite.locked and sprite != self:
                        self.locked = False


            if screen.getTouchUp():
                self.locked = False
                
            if self.locked:
                screen.moveToFront(self)
                self.counter = 0
                x, y = screen.getTouchPos()
                x -= self.getWidth() / 2
                y -= self.getHeight() / 2
                self.goto(x, y)
        else:
            self.set()


class BlackPiece(Piece):
    def __init__(self, x, y, *args, **kwargs):
        super().__init__(x, y, *args, **kwargs)
        self.moved = False

    def movePiece(self, x, y):
        self.goto(x * WIDTH,
                  y * HEIGHT + START_HEIGHT)
        self.moved = True
        self.set()

    def update(self, screen):
        x, y = self.toBoardPos(self.getX(), self.getY())
        if self.moved:
            for sprite in screen:
                if isinstance(sprite, WhitePiece):
                    sx, sy = self.toBoardPos(sprite.getX(), sprite.getY())
                    if sx == x and sy == y or self.collide(sprite):
                        screen.remove(sprite)
            self.moved = False


class WhitePiece(Piece):
    def update(self, screen):
        if self.getDoubleTap():
            print("DOUBLE TAP!")


        if self.getTouchDown() or self.locked:
            
            if not self.locked:
                self.saveX, self.saveY = self.getX(), self.getY()
            self.locked = True


            for sprite in screen:
                if isinstance(sprite, Piece):
                    if sprite.locked and sprite != self:
                        self.locked = False


            if screen.getTouchUp():
                # self.set()
                x_1, y_1 = self.toBoardPos(self.saveX,
                                   self.saveY)
                x_2, y_2 = self.toBoardPos(self.getX(),
                                   self.getY())

                # if abs(x_1 - x_2) > 1 or abs(y_1 - y_2) > 1:
                b = self.check(screen, x_1, x_2, y_1, y_2)
                if b:
                    self.goto(self.saveX, self.saveY)


                self.locked = False
                for sprite in screen:
                    if sprite != self:
                        if isinstance(sprite, WhitePiece):
                            if self.toBoardPos(self.getX(), self.getY()) == self.toBoardPos(sprite.getX(), sprite.getY()):
                                self.goto(self.saveX, self.saveY)
                        if isinstance(sprite, BlackPiece):
                            if self.toBoardPos(self.getX(), self.getY()) == self.toBoardPos(sprite.getX(), sprite.getY()):
                                screen.remove(sprite)
                        if isinstance(sprite, EmptyTile):
                            if self.toBoardPos(self.getX(), self.getY()) == self.toBoardPos(sprite.getX(), sprite.getY()):
                                self.goto(self.saveX, self.saveY)

                cx, cy = self.toBoardPos(self.getX(),
                                   self.getY())

                if not (cx == x_1 and cy == y_1):
                    self.setMoved()
                
            if self.locked:
                screen.moveToFront(self)
                self.counter = 0
                x, y = screen.getTouchPos()
                x -= self.getWidth() / 2
                y -= self.getHeight() / 2
                self.goto(x, y)
        else:
            self.set()



class WhitePawn(WhitePiece):
    def __init__(self, x, y):
        super().__init__(x, y, image='img/WhitePawn.png')

    def update(self, screen):
        super().update(screen)
        if self.getTouchDown() or self.locked:
            pass
        else:
            x, y = self.toBoardPos(self.getX(), self.getY())
            if y == BOARD_HEIGHT - 1:
                print(x, y)
                w = WhiteKnight(x, y)
                w.setMoved()
                screen.append(w)
                screen.remove(self)

            for sprite in screen:
                if sprite == self:
                    continue

                if isinstance(sprite, EmptyTile):
                    sx, sy = self.toBoardPos(sprite.getX(), sprite.getY())
                    if sy == y + 1 and sx == x:
                        print(x, y)
                        w = WhiteKnight(x, y)
                        w.setMoved()
                        screen.append(w)
                        screen.remove(self)

    def check(self, screen, x1, x2, y1, y2):
        flag = False
        attacking = False
        if y2 == y1 + 1:
            pass
        else:
            flag = True

        for sprite in screen:
            if sprite == self:
                continue

            if isinstance(sprite, EmptyTile) or isinstance(sprite, WhitePiece):
                sx, sy = self.toBoardPos(sprite.getX(), sprite.getY())

                if x2 == sx and y2 == sy:
                    flag = True
            elif isinstance(sprite, BlackPiece):
                sx, sy = self.toBoardPos(sprite.getX(), sprite.getY())
                if x2 == sx and y2 == sy:
                    if abs(x2 - x1) == 1:
                        attacking = True
                    else:
                        flag = True
    
        if attacking:
            pass
        elif abs(x2 - x1) != 0:
            # if x2 == x1 + 1 and y1 == 2 and x1 == 0:
            #     pass
            # elif x2 == x1 - 1 and y1 == 2 and x1 == 6:
            #     pass
            # else:
            #     flag = True
            flag = True

        return flag


class WhiteCastle(WhitePiece):
    def __init__(self, x, y):
        super().__init__(x, y, image='img/WhiteCastle.png')

    def check(self, screen, x1, x2, y1, y2):
        flag = False
        if x1 == x2 or y1 == y2:
            for sprite in screen:
                if sprite == self:
                    continue

                if isinstance(sprite, EmptyTile) or isinstance(sprite, WhitePiece):
                    sx, sy = self.toBoardPos(sprite.getX(), sprite.getY())
                    if (x1 <= sx <= x2 or x1 >= sx >= x2) and (y1 <= sy <= y2 or y1 >= sy >= y2):
                        flag = True
                elif isinstance(sprite, BlackPiece):
                    sx, sy = self.toBoardPos(sprite.getX(), sprite.getY())
                    if sx == x2 and sy == y2:
                        # print(x2, y2, sx, sy)
                        # print(x2, y2, sx, sy)
                        pass
                    elif (x1 <= sx <= x2 or x1 >= sx >= x2) and (y1 <= sy <= y2 or y1 >= sy >= y2):
                        flag = True
        else:
            flag = True

        return flag


class WhiteQueen(WhitePiece):
    def __init__(self, x, y):
        super().__init__(x, y, image='img/WhiteQueen.png')

    def check(self, screen, x1, x2, y1, y2):
        flag = False
        if x1 == x2 or y1 == y2:
            for sprite in screen:
                if sprite == self:
                    continue

                if isinstance(sprite, EmptyTile) or isinstance(sprite, WhitePiece):
                    sx, sy = self.toBoardPos(sprite.getX(), sprite.getY())
                    if (x1 <= sx <= x2 or x1 >= sx >= x2) and (y1 <= sy <= y2 or y1 >= sy >= y2):
                        flag = True
                elif isinstance(sprite, BlackPiece):
                    sx, sy = self.toBoardPos(sprite.getX(), sprite.getY())
                    if sx == x2 and sy == y2:
                        # print(x2, y2, sx, sy)
                        # print(x2, y2, sx, sy)
                        pass
                    elif (x1 <= sx <= x2 or x1 >= sx >= x2) and (y1 <= sy <= y2 or y1 >= sy >= y2):
                        flag = True
        else:
            if abs(x2 - x1) == abs(y2 - y1):
                for sprite in screen:
                    if sprite == self:
                        continue

                    if isinstance(sprite, EmptyTile) or isinstance(sprite, WhitePiece):
                        sx, sy = self.toBoardPos(sprite.getX(), sprite.getY())
                        for p in range(abs(x2 - x1)):
                            if x1 + p * sign(x2 - x1) == sx and y1 + p * sign(y2 - y1) == sy:
                                flag = True

                    if isinstance(sprite, BlackPiece):
                        sx, sy = self.toBoardPos(sprite.getX(), sprite.getY())
                        for p in range(abs(x2 - x1)+1):
                            if x1 + p * sign(x2 - x1) == sx and y1 + p * sign(y2 - y1) == sy:
                                if x1 + p * sign(x2 - x1) == x2 and y1 + p * sign(y2 - y1) == y2:
                                    pass
                                else:
                                    flag = True
            else:
                flag = True
            
        return flag


class WhiteBishop(WhitePiece):
    def __init__(self, x, y):
        super().__init__(x, y, image='img/WhiteBishop.png')

    def check(self, screen, x1, x2, y1, y2):
        flag = False
        if abs(x2 - x1) == abs(y2 - y1):
            for sprite in screen:
                if sprite == self:
                    continue

                if isinstance(sprite, EmptyTile) or isinstance(sprite, WhitePiece):
                    sx, sy = self.toBoardPos(sprite.getX(), sprite.getY())
                    for p in range(abs(x2 - x1)):
                        if x1 + p * sign(x2 - x1) == sx and y1 + p * sign(y2 - y1) == sy:
                            flag = True

                if isinstance(sprite, BlackPiece):
                    sx, sy = self.toBoardPos(sprite.getX(), sprite.getY())
                    for p in range(abs(x2 - x1)+1):
                        if x1 + p * sign(x2 - x1) == sx and y1 + p * sign(y2 - y1) == sy:
                            if x1 + p * sign(x2 - x1) == x2 and y1 + p * sign(y2 - y1) == y2:
                                pass
                            else:
                                flag = True
        else:
            flag = True
            
        return flag


class WhiteKnight(WhitePiece):
    def __init__(self, x, y):
        super().__init__(x, y, image='img/WhiteKnight.png')

    def check(self, screen, x1, x2, y1, y2):
        flag = False

        if x2 == x1 - 1 and y2 == y1 - 2:
            pass
        elif x2 == x1 + 1 and y2 == y1 - 2:
            pass
        elif x2 == x1 - 1 and y2 == y1 + 2:
            pass
        elif x2 == x1 + 1 and y2 == y1 + 2:
            pass
        elif x2 == x1 - 2 and y2 == y1 - 1:
            pass
        elif x2 == x1 + 2 and y2 == y1 - 1:
            pass
        elif x2 == x1 - 2 and y2 == y1 + 1:
            pass
        elif x2 == x1 + 2 and y2 == y1 + 1:
            pass
        else:
            flag = True

        for sprite in screen:
            if sprite == self:
                continue

            if isinstance(sprite, EmptyTile) or isinstance(sprite, WhitePiece):
                sx, sy = self.toBoardPos(sprite.getX(), sprite.getY())
                if x2 == sx and y2 == sy:
                    flag = True

        return flag


class WhiteKing(WhitePiece):
    def __init__(self, x, y):
        super().__init__(x, y, image='img/WhiteKing.png')

    def check(self, screen, x1, x2, y1, y2):
        flag = False

        if x2 == x1 - 1 and y2 == y1:
            pass
        elif x2 == x1 + 1 and y2 == y1:
            pass
        elif x2 == x1 and y2 == y1 - 1:
            pass
        elif x2 == x1 and y2 == y1 + 1:
            pass
        elif x2 == x1 - 1 and y2 == y1 + 1:
            pass
        elif x2 == x1 + 1 and y2 == y1 + 1:
            pass
        elif x2 == x1 - 1 and y2 == y1 - 1:
            pass
        elif x2 == x1 + 1 and y2 == y1 - 1:
            pass
        else:
            flag = True

        for sprite in screen:
            if sprite == self:
                continue

            if isinstance(sprite, EmptyTile) or isinstance(sprite, WhitePiece):
                sx, sy = self.toBoardPos(sprite.getX(), sprite.getY())
                if x2 == sx and y2 == sy:
                    flag = True

        return flag


class BlackPawn(BlackPiece):
    def __init__(self, x, y):
        super().__init__(x, y, image='img/BlackPawn.png')

    def update(self, screen):
        super().update(screen)

        if self.getTouchDown() or self.locked:
            pass
        else:
            x, y = self.toBoardPos(self.getX(), self.getY())
            if y == 0:
                print(x, y)
                q = BlackQueen(x, y)
                q.setMoved()
                screen.append(q)
                screen.remove(self)

            for sprite in screen:
                if sprite == self:
                    continue

                if isinstance(sprite, EmptyTile):
                    sx, sy = self.toBoardPos(sprite.getX(), sprite.getY())
                    if sy == y - 1 and sx == x:
                        print(x, y)
                        q = BlackQueen(x, y)
                        q.setMoved()
                        screen.append(q)
                        screen.remove(self)

    def check(self, screen, x1, x2, y1, y2):
        flag = False
        attacking = False

        if y2 == y1 - 1:
            pass
        else:
            flag = True

        for sprite in screen:
            if sprite == self:
                continue

            if isinstance(sprite, EmptyTile) or isinstance(sprite, BlackPiece):
                sx, sy = self.toBoardPos(sprite.getX(), sprite.getY())

                if x2 == sx and y2 == sy:
                    flag = True
            elif isinstance(sprite, WhitePiece):
                sx, sy = self.toBoardPos(sprite.getX(), sprite.getY())
                if x2 == sx and y2 == sy:
                    if abs(x2 - x1) == 1:
                        attacking = True
                    else:
                        flag = True
    
        if attacking:
            pass
        elif abs(x2 - x1) != 0:
            flag = True

        return flag



class BlackCastle(BlackPiece):
    def __init__(self, x, y):
        super().__init__(x, y, image='img/BlackCastle.png')

    def check(self, screen, x1, x2, y1, y2):
        flag = False
        if x1 == x2 or y1 == y2:
            for sprite in screen:
                if sprite == self:
                    continue

                if isinstance(sprite, EmptyTile) or isinstance(sprite, BlackPiece):
                    sx, sy = self.toBoardPos(sprite.getX(), sprite.getY())
                    if (x1 <= sx <= x2 or x1 >= sx >= x2) and (y1 <= sy <= y2 or y1 >= sy >= y2):
                        flag = True
                elif isinstance(sprite, WhitePiece):
                    sx, sy = self.toBoardPos(sprite.getX(), sprite.getY())
                    if sx == x2 and sy == y2:
                        # print(x2, y2, sx, sy)
                        # print(x2, y2, sx, sy)
                        pass
                    elif (x1 <= sx <= x2 or x1 >= sx >= x2) and (y1 <= sy <= y2 or y1 >= sy >= y2):
                        flag = True
        else:
            flag = True

        return flag


class BlackKnight(BlackPiece):
    def __init__(self, x, y):
        super().__init__(x, y, image='img/BlackKnight.png')

    def check(self, screen, x1, x2, y1, y2):
        flag = False

        if x2 == x1 - 1 and y2 == y1 - 2:
            pass
        elif x2 == x1 + 1 and y2 == y1 - 2:
            pass
        elif x2 == x1 - 1 and y2 == y1 + 2:
            pass
        elif x2 == x1 + 1 and y2 == y1 + 2:
            pass
        elif x2 == x1 - 2 and y2 == y1 - 1:
            pass
        elif x2 == x1 + 2 and y2 == y1 - 1:
            pass
        elif x2 == x1 - 2 and y2 == y1 + 1:
            pass
        elif x2 == x1 + 2 and y2 == y1 + 1:
            pass
        else:
            flag = True

        for sprite in screen:
            if sprite == self:
                continue

            if isinstance(sprite, EmptyTile) or isinstance(sprite, BlackPiece):
                sx, sy = self.toBoardPos(sprite.getX(), sprite.getY())
                if x2 == sx and y2 == sy:
                    flag = True

        return flag


class GreenKnight(BlackPiece):
    def __init__(self, x, y):
        super().__init__(x, y, image='img/GreenKnight.png')
        self.save_x = x
        self.save_y = y

    def check(self, screen, x1, x2, y1, y2):
        flag = False

        if x2 == x1 - 1 and y2 == y1 - 2:
            pass
        elif x2 == x1 + 1 and y2 == y1 - 2:
            pass
        elif x2 == x1 - 1 and y2 == y1 + 2:
            pass
        elif x2 == x1 + 1 and y2 == y1 + 2:
            pass
        elif x2 == x1 - 2 and y2 == y1 - 1:
            pass
        elif x2 == x1 + 2 and y2 == y1 - 1:
            pass
        elif x2 == x1 - 2 and y2 == y1 + 1:
            pass
        elif x2 == x1 + 2 and y2 == y1 + 1:
            pass
        else:
            flag = True

        for sprite in screen:
            if sprite == self:
                continue

            if isinstance(sprite, EmptyTile) or isinstance(sprite, BlackPiece):
                sx, sy = self.toBoardPos(sprite.getX(), sprite.getY())
                if x2 == sx and y2 == sy:
                    flag = True

        return flag

    def movePiece(self, x, y):
        self.save_x, self.save_y = self.toBoardPos(self.getX(), self.getY())

        self.goto(x * WIDTH,
                  y * HEIGHT + START_HEIGHT)
        self.moved = True
        
        self.set()

    def update(self, screen):
        x, y = self.toBoardPos(self.getX(), self.getY())
        if self.moved:
            screen.append(
                BlackKing(self.save_x, self.save_y)
            )

            for sprite in screen:
                if isinstance(sprite, WhitePiece):
                    sx, sy = self.toBoardPos(sprite.getX(), sprite.getY())
                    if sx == x and sy == y or self.collide(sprite):
                        screen.remove(sprite)

            self.moved = False


class BlackQueen(BlackPiece):
    def __init__(self, x, y):
        super().__init__(x, y, image='img/BlackQueen.png')

    def check(self, screen, x1, x2, y1, y2):
        flag = False
        if x1 == x2 or y1 == y2:
            for sprite in screen:
                if sprite == self:
                    continue

                if isinstance(sprite, EmptyTile) or isinstance(sprite, BlackPiece):
                    sx, sy = self.toBoardPos(sprite.getX(), sprite.getY())
                    if (x1 <= sx <= x2 or x1 >= sx >= x2) and (y1 <= sy <= y2 or y1 >= sy >= y2):
                        flag = True
                elif isinstance(sprite, WhitePiece):
                    sx, sy = self.toBoardPos(sprite.getX(), sprite.getY())
                    if sx == x2 and sy == y2:
                        pass
                    elif (x1 <= sx <= x2 or x1 >= sx >= x2) and (y1 <= sy <= y2 or y1 >= sy >= y2):
                        flag = True
        else:
            if abs(x2 - x1) == abs(y2 - y1):
                for sprite in screen:
                    if sprite == self:
                        continue

                    if isinstance(sprite, EmptyTile) or isinstance(sprite, BlackPiece):
                        sx, sy = self.toBoardPos(sprite.getX(), sprite.getY())
                        if x2 == sx and y2 == sy:
                            flag = True
                        else:    
                            for p in range(abs(x2 - x1)):
                                if x1 + p * sign(x2 - x1) == sx and y1 + p * sign(y2 - y1) == sy:
                                    flag = True
    
                    if isinstance(sprite, WhitePiece):
                        sx, sy = self.toBoardPos(sprite.getX(), sprite.getY())
                        for p in range(abs(x2 - x1)+1):
                            if x1 + p * sign(x2 - x1) == sx and y1 + p * sign(y2 - y1) == sy:
                                if x1 + p * sign(x2 - x1) == x2 and y1 + p * sign(y2 - y1) == y2:
                                    pass
                                else:
                                    flag = True
            else:
                flag = True

        return flag



class BlackBishop(BlackPiece):
    def __init__(self, x, y):
        super().__init__(x, y, image='img/BlackBishop.png')

    def check(self, screen, x1, x2, y1, y2):
        flag = False
        if abs(x2 - x1) == abs(y2 - y1):
            for sprite in screen:
                if sprite == self:
                    continue

                if isinstance(sprite, EmptyTile) or isinstance(sprite, BlackPiece):
                    sx, sy = self.toBoardPos(sprite.getX(), sprite.getY())
                    if x2 == sx and y2 == sy:
                        flag = True
                    else:    
                        for p in range(abs(x2 - x1)):
                            if x1 + p * sign(x2 - x1) == sx and y1 + p * sign(y2 - y1) == sy:
                                flag = True

                if isinstance(sprite, WhitePiece):
                    sx, sy = self.toBoardPos(sprite.getX(), sprite.getY())
                    for p in range(abs(x2 - x1)+1):
                        if x1 + p * sign(x2 - x1) == sx and y1 + p * sign(y2 - y1) == sy:
                            if x1 + p * sign(x2 - x1) == x2 and y1 + p * sign(y2 - y1) == y2:
                                pass
                            else:
                                flag = True
        else:
            flag = True

        return flag



class BlackKing(BlackPiece):
    def __init__(self, x, y):
        super().__init__(x, y, image='img/BlackKing.png')

    def check(self, screen, x1, x2, y1, y2):
        flag = False

        if x2 == x1 - 1 and y2 == y1:
            pass
        elif x2 == x1 + 1 and y2 == y1:
            pass
        elif x2 == x1 and y2 == y1 - 1:
            pass
        elif x2 == x1 and y2 == y1 + 1:
            pass
        elif x2 == x1 - 1 and y2 == y1 + 1:
            pass
        elif x2 == x1 + 1 and y2 == y1 + 1:
            pass
        elif x2 == x1 - 1 and y2 == y1 - 1:
            pass
        elif x2 == x1 + 1 and y2 == y1 - 1:
            pass
        else:
            flag = True

        for sprite in screen:
            if sprite == self:
                continue

            if isinstance(sprite, EmptyTile) or isinstance(sprite, BlackPiece):
                sx, sy = self.toBoardPos(sprite.getX(), sprite.getY())
                if x2 == sx and y2 == sy:
                    flag = True

        return flag


class GreenKing(BlackPiece):
    def __init__(self, x, y):
        super().__init__(x, y, image='img/GreenKing.png')
        self.save_x = x
        self.save_y = y

    def check(self, screen, x1, x2, y1, y2):
        flag = False

        if x2 == x1 - 1 and y2 == y1:
            pass
        elif x2 == x1 + 1 and y2 == y1:
            pass
        elif x2 == x1 and y2 == y1 - 1:
            pass
        elif x2 == x1 and y2 == y1 + 1:
            pass
        elif x2 == x1 - 1 and y2 == y1 + 1:
            pass
        elif x2 == x1 + 1 and y2 == y1 + 1:
            pass
        elif x2 == x1 - 1 and y2 == y1 - 1:
            pass
        elif x2 == x1 + 1 and y2 == y1 - 1:
            pass
        else:
            flag = True

        for sprite in screen:
            if sprite == self:
                continue

            if isinstance(sprite, EmptyTile) or isinstance(sprite, BlackPiece):
                sx, sy = self.toBoardPos(sprite.getX(), sprite.getY())
                if x2 == sx and y2 == sy:
                    flag = True

        return flag

    def movePiece(self, x, y):
        self.save_x, self.save_y = self.toBoardPos(self.getX(), self.getY())

        self.goto(x * WIDTH,
                  y * HEIGHT + START_HEIGHT)
        self.moved = True

        self.set()

    def update(self, screen):
        x, y = self.toBoardPos(self.getX(), self.getY())
        if self.moved:
            if not randint(0, 2):
                screen.append(
                    GreenKing(self.save_x, self.save_y)
                )
            else:
                screen.append(
                    BlackKing(self.save_x, self.save_y)
                )

            for sprite in screen:
                if isinstance(sprite, WhitePiece):
                    sx, sy = self.toBoardPos(sprite.getX(), sprite.getY())
                    if sx == x and sy == y or self.collide(sprite):
                        screen.remove(sprite)

            self.moved = False
