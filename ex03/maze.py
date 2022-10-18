import tkinter as tk
import maze_maker as mm

#key_down関数を定義する
def key_down(event):
    global key
    key = event.keysym

#key_up関数を定義する
def key_up(event):
    global key
    key = ""

#リアルタイム処理関数main_proc関数を定義する
def main_proc():
    global mx, my
    global cx, cy
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
    root.after(100, main_proc)

if __name__ == "__main__":
    #ウィンドウを生成する
    root = tk.Tk()
    root.title("迷えるこうかとん")#練習1

    #Canvasを生成する
    canv = tk.Canvas(root, width=1500, height=900, bg="black")
    canv.pack()

    #mmモジュールの関数を呼び出す
    maze_list = mm.make_maze(15, 9)
    maze_show = mm.show_maze(canv, maze_list)

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