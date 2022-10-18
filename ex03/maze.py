import tkinter as tk
import maze_maker as mm

#key_down関数を定義する
def key_down(event):
    global key, tmr_S
    key = event.keysym
    if tmr_S == False:
        root.after(100, count_down)
        tmr_S = True

#key_up関数を定義する
def key_up(event):
    global key
    key = ""

#リアルタイム処理関数main_proc関数を定義する
def main_proc():
    global mx, my
    global cx, cy
    global game_C
    if key == "Up":
        my -=1
    elif key == "Down":
        my += 1
    elif key == "Right":
        mx += 1
    elif key == "Left":
        mx -= 1
    if maze_list[my][mx] != 1:
        cx, cy = mx*100+50, my*100+50
    else:
        if key == "Up":
            my +=1
        elif key == "Down":
            my -= 1
        elif key == "Right":
            mx -= 1
        elif key == "Left":
            mx += 1
    canv.coords("tori", cx, cy)
    if game_C == True:
        root.after(100, main_proc)

def count_down():#カウントダウンする関数を定義する
    global tmr, game_C
    tmr -= 1
    canv.create_rectangle(0, 0, 150, 100, outline ="white", fill="white")
    canv.create_text(100,50, text=tmr, font=("", 80))
    root.after(1000, count_down)
    if tmr < 0:
        canv.create_text(800, 400, text="GAME OVER", font=("",80), fill="red")
        game_C = False
        



if __name__ == "__main__":
    #タイマーの初期値を設定する
    tmr = 30
    #タイマーが動いてるかどうか設定する
    tmr_S = False

    #ゲームが続いているのか確認する
    game_C = True

    #ウィンドウを生成する
    root = tk.Tk()
    root.title("迷えるこうかとん")#練習1

    #Canvasを生成する
    canv = tk.Canvas(root, width=1500, height=900, bg="black")
    canv.pack()

    #mmモジュールの関数を呼び出す
    maze_list = mm.make_maze(15, 9)
    maze_show = mm.show_maze(canv, maze_list)

    #残り時間を表示する
    label = tk.Label(root, font=("", 80))
    label.pack()

    #こうかとんを表示する
    tori = tk.PhotoImage(file="ex03/fig/4.png")
    mx, my =1, 1
    cx, cy = mx*100+50, my*100+50
    canv.create_image(cx, cy, image=tori, tag="tori")

    #keyを初期化する
    key = ""    #現在押されているキーを表す変数

    #key_downに<KeyPress>を紐づける
    root.bind("<KeyPress>", key_down)

    #key_upに<KeyRelease>を紐づける
    root.bind("<KeyRelease>", key_up)

    #main_procを呼び出し、常時起動するようにする
    main_proc()


    root.mainloop()