import pygame as py
import sys


def main():
    py.display.set_caption("逃げろ！こうかとん")
    scrn_sfc = py.display.set_mode((1600, 900))

    bg_sfc = py.image.load("ex04/haikei.jpg")
    bg_rct = bg_sfc.get_rect()

    clock = py.time.Clock()
    while True:
        scrn_sfc.blit(bg_sfc, bg_rct) #練習2
        py.display.update()
        clock.tick(1000)              #1000fpsを刻む

        for event in py.event.get():  #イベントを繰り返しで処理
            if event.type == py.QUIT: #ウィンドウの×ボタンをクリックしたら
                return #main関数を抜け出す


if __name__ == "__main__":
    py.init()  #モジュールを初期化する
    main()     #ゲームの本体
    py.quit()  #モジュールの初期化の解除
    sys.exit() #プログラムを終了する