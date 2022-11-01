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
        self.rct.centery = randint(30, scr.rct.height-30)
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

    def __init__(self, colour, radius,  speed, enemy):
        self.sfc = pg.Surface((radius*2, radius*2)) # 空のSurface
        self.sfc.set_colorkey((0, 0, 0)) # 四隅の黒い部分を透過させる
        pg.draw.circle(self.sfc, colour, (radius, radius), radius) # 爆弾用の円を描く
        self.rct = self.sfc.get_rect()
        self.rct.center = enemy.rct.center
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


class Time:
    #ゲーム内タイマーを管理するクラス
    def __init__(self, tmr):
        self.tmr = tmr

    def update(self): #タイマーを進めるイニシャライザ
        self.tmr += 1
        

class Game_over():
    #Game_overを表示するクラス

    def __init__(self):
        self.font = pg.font.Font(None, 110)
        self.text = self.font.render("GAME_OVER", True, (255, 0, 0))
    

    def blit(self, scr):
        scr.sfc.blit(self.text, [scr.rct.centerx/2, scr.rct.centery/2]) 




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

    bom = Bomb((255, 0, 0), 10, (+1, +1), enemy)

    bom2 = Bomb((255, 0, 0), 10, (+1, +1), enemy)

    bom3 = Bomb((255, 0, 0), 10, (+1, +1), enemy)

    #タイマーを設定する
    game = Time(0)

    game_over = Time(0)

    end = Game_over()


    #ゲームが続いていることを表す
    G_done = True

    clock = pg.time.Clock()

    while True:
        scr.blit()
        for event in pg.event.get(): # 練習2
            if event.type == pg.QUIT:
                return

        if G_done:
            player.update(scr)

            enemy.update(scr)

            bom.update(scr)

            game.update()

            if game.tmr > 2000:
                bom2.update(scr)

            if game.tmr > 4500:
                bom3.update(scr)

        if (player.rct.colliderect(bom.rct) 
            or player.rct.colliderect(bom2.rct)
            or player.rct.colliderect(bom3.rct)
            or player.rct.colliderect(enemy.rct)
            ): 
            # こうかとんrctが爆弾rctと重なったら
            G_done = False#ゲームを終わらせる

        if not G_done:
            bom2 = Bomb((255, 0, 0), 10, (+1, +1), player)
            player.blit(scr)
            bom2.blit(scr)
            end.blit(scr) #Gameoverを表示する
            game_over.update()

        if game_over.tmr > 1000:
            return


        pg.display.update() #練習2
        clock.tick(1000)


if __name__ == "__main__":
    pg.init() # 初期化
    main()    # ゲームの本体
    pg.quit() # 初期化の解除
    sys.exit()
