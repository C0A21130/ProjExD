import tkinter as tk
from turtle import goto

# 押されたキーを読み取り表示する関数
def key_down(event):
    global key
    key = event.keysym
    print(key)

def key_up(event):
    global key
    key = ""

if __name__ == "__main__":
    # ウィンドウの生成
    root = tk.Tk()
    root.title("迷えるこうかとん")
    root.geometry("1500x900")

    # canvasの生成
    canvas = tk.Canvas(root, width=1500, height=900, bg="black")
    canvas.pack()

    # こうかとんインスタンスを生成して表示する
    tori = tk.PhotoImage(file="fig/8.png")
    cx,cy = 300, 400 # こうかとんの座標(x, y)
    canvas.create_image(cx, cy, imag=tori, tag="tori")

    key = ""  # グローバル変数keyを空文字で初期化する

    # キーを押されたときにkey_down関数を呼び出すようにする
    root.bind("<KeyPress>", key_down)

    # キーを話したときにkey_up関数を呼び出すようにする
    root.bind("<KeyRelease>", key_up)

    root.mainloop()
