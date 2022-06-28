import tkinter as tk
import maze_maker

# 押されたキーを読み取りグローバル変数keyに代入する関数
def key_down(event):
    global key
    key = event.keysym

# グローバル変数keyに空文字を代入する関数
def key_up(event):
    global key
    key = ""

# 常時起動する関数
def main_proc():
    global cx, cy, mx, my
    stride = 100 # こうかとんの歩幅
    if key == "Up":
        my -= 1
    elif key == "Down":
        my += 1
    elif key == "Left":
        mx -= 1
    elif key == "Right":
        mx += 1
    cx = 50 + mx * stride
    cy = 50 + my * stride

    # 変更した数値で後進する
    canvas.coords("tori", cx, cy)
    root.after(update_time, main_proc)


if __name__ == "__main__":
    # ウィンドウ(幅：1500、高さ：900)の生成
    root = tk.Tk()
    root.title("迷えるこうかとん")
    root.geometry("1500x900")

    # canvasの生成
    canvas = tk.Canvas(root, width=1500, height=900, bg="black")
    canvas.pack()

    # maze_makerモジュールのmake_maze関数を使って15x9マスの迷路の配列を生成する
    maze_lst = maze_maker.make_maze(15, 9)

    # maze_makerモジュールのshow_maze関数を使って背景の迷路を描画する
    maze_maker.show_maze(canvas, maze_lst)

    # こうかとんインスタンスを生成して表示する
    tori = tk.PhotoImage(file="fig/8.png")
    mx, my = 1, 1     # こうかとんのいるマス(x, y)
    cx, cy = 250, 350 # こうかとんの座標(x, y)
    canvas.create_image(cx, cy, imag=tori, tag="tori")

    key = ""  # グローバル変数keyを空文字で初期化する

    # キーを押されたときにkey_down関数を呼び出すようにする
    root.bind("<KeyPress>", key_down)

    # キーを話したときにkey_up関数を呼び出すようにする
    root.bind("<KeyRelease>", key_up)

    update_time = 100 #更新する秒数
    # 常時main_proc関数を呼び出す
    root.after(update_time, main_proc)

    root.mainloop()
