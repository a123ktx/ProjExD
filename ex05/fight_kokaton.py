import pygame as pg
import sys
from random import randint

key_delta = {
    pg.K_UP:    [0, -1],
    pg.K_DOWN:  [0, +1],
    pg.K_LEFT:  [-1, 0],
    pg.K_RIGHT: [+1, 0],
}

class Screen:
#スクリーンを表示するクラス

    def __init__(self, title, tup, BS):
        
        pg.display.set_caption(title)
        self.sfc = pg.display.set_mode(tup)
        self.rct = self.sfc.get_rect()
        self.bgi_sfc = pg.image.load(BS)
        self.bgi_rct = self.bgi_sfc.get_rect()

    def blit(self):
        self.sfc.blit(self.bgi_sfc, self.bgi_rct)


class Player:
#こうかとんを描写するクラス

    key_delta = {
        pg.K_UP:    [0, -1],
        pg.K_DOWN:  [0, +1],
        pg.K_LEFT:  [-1, 0],
        pg.K_RIGHT: [+1, 0],
        }

    def __init__(self, file, zoom, tup):
        sfc = pg.image.load(file)
        self.sfc = pg.transform.rotozoom(sfc, 0, zoom)
        self.rct = self.sfc.get_rect()
        self.rct.center = tup

    #こうかとんを貼り付けるblitメソッド
    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    #座標の計算、更新を行う
    def update(self, scr):
        #key_statesがキーを押している時に、押されているキーをリストで受け取る
        key_states = pg.key.get_pressed()
        #key_deltaで移動方向を内包したリストをkeyとdeltaに送る
        for key, delta in Player.key_delta.items():
            if key_states[key]:
                self.rct.centerx += delta[0]
                self.rct.centery += delta[1]
                if check_bound(self.rct, scr.rct) != (+1, +1):
                    self.rct.centerx -= delta[0]
                    self.rct.centery -= delta[1]
        self.blit(scr) # = scr.sfc.blit(self.sfc, self.rct)


class Enemy:
#敵に関するクラス

    def __init__(self, file, zoom, speed, scr):
        sfc = pg.image.load(file)
        self.sfc = pg.transform.rotozoom(sfc, 0, zoom)
        self.rct = self.sfc.get_rect()
        self.rct.centerx = 1500
        self.rct.centery = randint(0, scr.rct.height)
        self.vy = speed

    #敵を貼り付けるインスタンスメソッド
    def blit(self, scr):
        scr.sfc.blit(self.sfc, self.rct)

    #敵の位置を更新するインスタンスメソッド
    def update(self, scr):
        self.rct.move_ip(0, self.vy) # 練習6
        _, tate = check_bound(self.rct, scr.rct)
        self.vy *= tate
        self.blit(scr)


class Bomb:
#ボムに関するクラス

    def __init__(self, colour, radius,  speed, scr):
        self.sfc = pg.Surface((radius*2, radius*2)) # 空のSurface
        self.sfc.set_colorkey((0, 0, 0)) # 四隅の黒い部分を透過させる
        pg.draw.circle(self.sfc, colour, (radius, radius), radius) # 爆弾用の円を描く
        self.rct = self.sfc.get_rect()
        self.rct.centerx = randint(0, scr.rct.width)
        self.rct.centery = randint(0, scr.rct.height)
        self.vx, self.vy = speed

    #ボムを貼り付けるインスタンスメソッド
    def blit(self, scr):
        scr.sfc.blit(self.sfc, self.rct)

    #ボムの位置を更新するインスタンスメソッド
    def update(self, scr):
        self.rct.move_ip(self.vx, self.vy) # 練習6
        yoko, tate = check_bound(self.rct, scr.rct)
        self.vx *= yoko
        self.vy *= tate
        self.blit(scr)




def check_bound(obj_rct, scr_rct):
    """
    obj_rct：こうかとんrct，または，爆弾rct
    scr_rct：スクリーンrct
    領域内：+1／領域外：-1
    """
    yoko, tate = +1, +1
    if obj_rct.left < scr_rct.left or scr_rct.right < obj_rct.right: 
        yoko = -1
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom: 
        tate = -1
    return yoko, tate




def main():
    #スクリーンを作る
    scr = Screen("負けるな！こうかとん", (1600, 900), "ex04/haikei.jpg")
    #プレイヤーのこうかとんを設置する
    player = Player("fig/2.png", 2.0 , (300, scr.rct.height/2))
    #敵のこうかとんを設置する
    enemy = Enemy("fig/6.png", 2.0, +1, scr)
    bom = Bomb((255, 0, 0), 10, (+1, +1), scr)

    clock = pg.time.Clock()

    while True:
        scr.blit()
        for event in pg.event.get(): # 練習2
            if event.type == pg.QUIT:
                return

        player.update(scr)

        enemy.update(scr)

        bom.update(scr)

        if player.rct.colliderect(bom.rct): # こうかとんrctが爆弾rctと重なったら
            return

        pg.display.update() #練習2
        clock.tick(1000)


if __name__ == "__main__":
    pg.init() # 初期化
    main()    # ゲームの本体
    pg.quit() # 初期化の解除
    sys.exit()
