import tkinter as tk
import tkinter.messagebox as tkm

def key_down(event):
    global jid
    if jid != None:
        root.after_cancel(jid)
        jid = None
        return #mainに戻る
    #key = event.keysym  #keysymで押されたキーを判別できる
    #tkm.showinfo("キー押下", f"{key}キーが押されました")
    jid = root.after(100, count_up)#押された処理が終わったらcount_upが発動するようにする

def count_up():
    global tmr, jid #tmrは関数の外で定義されているためグローバル変数
    tmr = tmr+1
    label["text"] = tmr
    jid = root.after(100, count_up)#再起呼び出し、遅延時間を操作することで好きな間隔でカウントを進められる

if __name__ == "__main__":
    root = tk.Tk()
    label = tk.Label(root, font=("", 80))
    label.pack()    #rootにくっつく
    #リアルタイム処理できるようにする
    tmr = 0
    jid = None
    #root.after(1000, count_up)#1000ミリ秒遅延させてcount_up関数を呼び出す
    root.bind("<KeyPress>", key_down)#keyが押されるとkey_down関数が呼び出される


    root.mainloop()