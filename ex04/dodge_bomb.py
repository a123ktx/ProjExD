import pygame as py
import sys
from random import randint

def check_bound(obj_rct, scr_rct):#objはこうかとんと爆弾のrct、scrはスクリーンのrct
    yoko, tate = +1, +1
    if obj_rct.left < scr_rct.left or scr_rct.right < obj_rct.right:
        yoko = -1
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom:
        tate = -1
    return yoko, tate

def main():
    global game_C, tmr
    py.display.set_caption("逃げろ！こうかとん")
    scrn_sfc = py.display.set_mode((1600, 900))
    scrn_rct = scrn_sfc.get_rect()
    bg_sfc = py.image.load("ex04/haikei.jpg")
    bg_rct = bg_sfc.get_rect()

    #練習3
    tori_sfc = py.image.load("fig/6.png")
    tori_sfc = py.transform.rotozoom(tori_sfc, 0, 2.0)
    tori_rct = tori_sfc.get_rect()
    tori_rct.centerx = randint(50, scrn_rct.width/2)#こうかとんの出現位置を画面上の右上からランダムにする
    tori_rct.centery = randint(50, scrn_rct.height/2)

    #練習5
    bomb_sfc = py.Surface((20, 20)) #空のSurface
    bomb_sfc.set_colorkey((0, 0, 0))
    py.draw.circle(bomb_sfc, (255, 0, 0), (10, 10), 10) #円を描く
    bomb_rct = bomb_sfc.get_rect()
    bomb_rct.centerx = randint(tori_rct.right, scrn_rct.width)#ランダム変更に合わせて、こうかとんとボムが重ならないよう調整
    bomb_rct.centery = randint(tori_rct.bottom, scrn_rct.height)
    #練習6
    vx, vy = +1, +1


    clock = py.time.Clock()
    #終了後のタイマーを設定する
    tmr2 = 5
    #ゲームが進行していることを確認する
    G_done = True
    while True:
        scrn_sfc.blit(bg_sfc, bg_rct) #練習2

        for event in py.event.get():  #イベントを繰り返しで処理
            if event.type == py.QUIT: #ウィンドウの×ボタンをクリックしたら
                return #main関数を抜け出す
        if G_done == True:#ゲームが進行していたらこうかとんが動くようにする
            key_states = py.key.get_pressed()
            if key_states[py.K_UP]: tori_rct.centery -= 1  #こうかとんが縦に+1
            if key_states[py.K_DOWN]: tori_rct.centery += 1 #こうかとんが縦に-1
            if key_states[py.K_LEFT]: tori_rct.centerx -= 1 #こうかとんが横に-1
            if key_states[py.K_RIGHT]: tori_rct.centerx += 1 #こうかとんが横に-1
            yoko, tate = check_bound(tori_rct, scrn_rct)
            if yoko == -1:
                if key_states[py.K_LEFT]:
                    tori_rct.centerx += 1
                if key_states[py.K_RIGHT]:
                    tori_rct.centerx -= 1
            if tate == -1:
                if key_states[py.K_UP]:
                    tori_rct.centery += 1
                if key_states[py.K_DOWN]:
                    tori_rct.centery -= 1
        scrn_sfc.blit(tori_sfc, tori_rct)

        #跳ね返る度に爆弾が加速する機能を追加する
        yoko, tate = check_bound(bomb_rct, scrn_rct)
        if yoko == 1:
            vx *= 1 
        elif yoko == -1:
            vx *= yoko*1.1
        if tate == 1:
            vy *= 1
        elif tate == -1:
            vy *= tate*1.1
        if G_done == False: #ゲームが終わったら爆弾を止める
            vx = 0
            vy = 0
            bomb_rct.center = tori_rct.center
        bomb_rct.move_ip(vx,vy) #練習6
        scrn_sfc.blit(bomb_sfc, bomb_rct)

        if tori_rct.colliderect(bomb_rct): #こうかとんrctが爆弾rctと重なったら
            G_done = False #ゲームを終わらせる
            tmr2 -= 0.005
            py.display.update()
            clock.tick(1000) 
            if tmr2 < 0:
                return
        py.display.update()
        clock.tick(1000)              #1000fpsを刻む

                
if __name__ == "__main__":
    py.init()  #モジュールを初期化する
    main()     #ゲームの本体
    py.quit()  #モジュールの初期化の解除
    sys.exit() #プログラムを終了する