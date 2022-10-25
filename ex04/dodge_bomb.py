import pygame as py
import sys


def main():
    py.display.set_caption("逃げろ！こうかとん")
    scrn_sfc = py.display.set_mode((1600, 900))

    bg_sfc = py.image.load("ex04/haikei.jpg")
    bg_rct = bg_sfc.get_rect()

    #練習3
    tori_sfc = py.image.load("fig/6.png")
    tori_sfc = py.transform.rotozoom(tori_sfc, 0, 2.0)
    tori_rct = tori_sfc.get_rect()
    tori_rct.center = 900, 400

    clock = py.time.Clock()
    while True:
        scrn_sfc.blit(bg_sfc, bg_rct) #練習2

        for event in py.event.get():  #イベントを繰り返しで処理
            if event.type == py.QUIT: #ウィンドウの×ボタンをクリックしたら
                return #main関数を抜け出す

        key_states = py.key.get_pressed()
        if key_states[py.K_UP]: tori_rct.centery -= 1  #こうかとんが縦に+1
        if key_states[py.K_DOWN]: tori_rct.centery += 1 #こうかとんが縦に-1
        if key_states[py.K_LEFT]: tori_rct.centerx -= 1 #こうかとんが横に-1
        if key_states[py.K_RIGHT]: tori_rct.centerx += 1 #こうかとんが横に-1

        scrn_sfc.blit(tori_sfc, tori_rct)
        py.display.update()
        clock.tick(1000)              #1000fpsを刻む

                
if __name__ == "__main__":
    py.init()  #モジュールを初期化する
    main()     #ゲームの本体
    py.quit()  #モジュールの初期化の解除
    sys.exit() #プログラムを終了する