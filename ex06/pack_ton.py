import pygame as pg
import sys
from random import randint


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
        self.goal = False
        self.score = 0

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
        self.rct.centerx = randint(500, 1200)
        self.rct.centery = randint(400, 600)
        self.vx, self.vy = speed

    #敵を貼り付けるインスタンスメソッド
    def blit(self, scr):
        scr.sfc.blit(self.sfc, self.rct)

    #敵の位置を更新するインスタンスメソッド
    def update(self, scr):
        self.rct.move_ip(self.vx, self.vy) # 練習6
        yoko, tate = check_bound(self.rct, scr.rct)
        self.vx *= yoko
        self.vy *= tate
        self.blit(scr)


class Item:
#ボムに関するクラス

    def __init__(self, colour, radius,  scr):
        self.sfc = pg.Surface((radius*2, radius*2)) # 空のSurface
        self.sfc.set_colorkey((0, 0, 0)) # 四隅の黒い部分を透過させる
        pg.draw.circle(self.sfc, colour, (radius, radius), radius) # アイテム用の円を描く
        self.rct = self.sfc.get_rect()
        self.rct.centerx = randint(200, scr.rct.width-200)
        self.rct.centery = randint(200, scr.rct.height-200)
        self.on = True

    #ボムを貼り付けるインスタンスメソッド
    def blit(self, scr):
        scr.sfc.blit(self.sfc, self.rct)



# class Wall:
#     def __init__(self, scr, y):
#         self.sfc = pg.Surface((1000, 80))
#         self.rct = self.sfc.get_rect()
#         self.rct.centerx = scr.rct.centerx
#         self.rct.centery = y


class Time:
    #ゲーム内タイマーを管理するクラス
    def __init__(self, tmr):
        self.tmr = tmr

    def update(self): #タイマーを進めるイニシャライザ
        self.tmr += 1
        

class Game_over:
    #Game_overを表示するクラス

    def __init__(self):
        self.font = pg.font.Font(None, 110)
        self.text = self.font.render("GAME_OVER", True, (255, 0, 0))

    def blit(self, scr):
        scr.sfc.blit(self.text, [scr.rct.centerx/2, scr.rct.centery/2])


class Game_clear:
    #Game_clearを表示するクラス

    def __init__(self):
        self.font = pg.font.Font(None, 110)
        self.text = self.font.render("GAME_CLEAR", True, (255, 255, 0))

    def blit(self, scr):
        scr.sfc.blit(self.text, [scr.rct.centerx/2, scr.rct.centery/2]) 


def check_bound(obj_rct, scr_rct):
    yoko, tate = +1, +1
    if obj_rct.left < scr_rct.left+100 or scr_rct.right-100 < obj_rct.right: 
        yoko = -1
    if obj_rct.top < scr_rct.top+100 or scr_rct.bottom-100 < obj_rct.bottom: 
        tate = -1
    return yoko, tate


def check_wall(obj_rct, wall_rct):
    yoko, tate = +1, +1
    if obj_rct.left < wall_rct.left or wall_rct.right < obj_rct.right: 
        yoko = -1
    if obj_rct.top < wall_rct.top or wall_rct.bottom < obj_rct.bottom: 
        tate = -1
    return yoko, tate

def main():
    #スクリーンを作る
    scr = Screen("負けるな！こうかとん", (1600, 900), "ex04/haikei.jpg")

    #プレイヤーのこうかとんを設置する
    player = Player("fig/2.png", 2.0 , (300, scr.rct.height/2))

    #敵のこうかとんを設置する
    enemy = Enemy("fig/6.png", 2.0, (+1, +1), scr)

    item = Item((255, 255, 0), 10, scr)

    #タイマーを設定する
    game = Time(0)

    game_over = Time(0)

    clear_time = Time(0)

    #ゲーム終了を設定する
    end = Game_over()

    clear = Game_clear()


    #ゲームが続いていることを表す
    G_done = True

    clock = pg.time.Clock()

    while True:
        scr.blit()
        for event in pg.event.get(): 
            if event.type == pg.QUIT:
                return

        if item.on:#アイテムが回収されていないなら描画する
            item.blit(scr)

        if G_done and not player.goal:#ゲームが続いているなら更新する
            player.update(scr)

            #壁を作る
            pg.draw.rect(scr.sfc, (121,121,121), (0,0,1600,100))
            pg.draw.rect(scr.sfc, (121,121,121), (0,800,1600,900))
            pg.draw.rect(scr.sfc, (121,121,121), (0,0,100,900))
            pg.draw.rect(scr.sfc, (121,121,121), (1500,0,1600,900))
            #プレイヤーが通れない壁を作る
            # pg.draw.rect(scr.sfc, (0,0,121), (300,280,1000,80))
            # pg.draw.rect(scr.sfc, (0,0,121), (300,550,1000,80))

            enemy.update(scr)

            game.update()

        if player.rct.colliderect(enemy.rct): 
            # こうかとんrctが敵rctと重なったら
            G_done = False#ゲームを終わらせる

        if player.rct.colliderect(item.rct):
            #アイテムを回収する昨日
            player.score += 1
            item = Item((255, 255, 0), 10, scr)
            if player.score > 8:
                #一定数回収すると終わる機能
                player.goal = True
                item.on =False
        
        if player.goal:
                player.blit(scr)
                clear.blit(scr) #Gameclearを表示する
                clear_time.update()

        if not G_done:
            player.blit(scr)
            end.blit(scr) #Gameoverを表示する
            game_over.update()

        if game_over.tmr > 1000 or clear_time.tmr > 1000:
            return


        pg.display.update() 
        clock.tick(1000)


if __name__ == "__main__":
    pg.init() # 初期化
    main()    # ゲームの本体
    pg.quit() # 初期化の解除
    sys.exit()