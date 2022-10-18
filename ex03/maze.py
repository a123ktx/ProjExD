import tkinter as tk

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
    global cx, cy
    if key == "Up":
        cy -=20
    elif key == "Down":
        cy += 20
    elif key == "Right":
        cx += 20
    elif key == "Left":
        cx -= 20
    canv.coords("tori", cx, cy)
    root.after(10, main_proc)

if __name__ == "__main__":
    #ウィンドウを生成する
    root = tk.Tk()
    root.title("迷えるこうかとん")#練習1

    #Canvasを生成する
    canv = tk.Canvas(root, width=1500, height=900, bg="black")
    canv.pack()

    #こうかとんを表示する
    tori = tk.PhotoImage(file="ex03/fig/4.png")
    cx, cy = 300,400
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