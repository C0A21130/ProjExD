import tkinter as tk
import tkinter.messagebox as tkm
import maze_maker
from random import randint

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

    # 押したキーによって移動先を変更する
    if key == "Up": # キーボードの上キーを押したことを検知する
        # こうかとんの上が道かゴールかを確認する
        my = (my-1) if maze_lst[my-1][mx] == 0 or maze_lst[my-1][mx]==2 else my
    elif key == "Down": # キーボードの下キーを押したことを検知する
        # こうかとんの下が道かゴールかを確認する
        my = (my+1) if maze_lst[my+1][mx] == 0 or maze_lst[my+1][mx]==2 else my
    elif key == "Left": # キーボードの左キーを押したことを検知する
        # こうかとんの左が道かゴールかを確認する
        mx = (mx-1) if maze_lst[my][mx-1] == 0 or maze_lst[my][mx-1]==2 else mx
    elif key == "Right": # キーボードの右キーを押したことを検知する
        # こうかとんの右が道かゴールかを確認する
        mx = (mx+1) if maze_lst[my][mx+1] == 0 or maze_lst[my][mx+1]==2 else mx
    
    # こうかとんの現在位置が決まる
    cx = 50 + mx * stride
    cy = 50 + my * stride

    # 変更した数値で更新する
    canvas.coords("tori", cx, cy)
    root.after(update_time, main_proc)

    # こうかとんがゴールしたかどうかを確認する関数を実行
    check_goal()

# ゴールを作成する関数
def create_goal():
    global maze_lst, count, cx, cy
    # もともとゴールだった場所を元の道のマスにもどす
    for x in range(15):
            for y in range(9):
                if maze_lst[y][x]==2:
                    maze_lst[y][x]=0 # ゴールをもとの道のマスに戻す
                    canvas.create_rectangle(x*100, y*100, x*100+100, y*100+100,
                                            fill="white")
    
    # 壁かつスタート位置でない場所にゴールを作成する
    while(1):     
        gx = randint(0, 14)
        gy = randint(0, 8)
        if maze_lst[gy][gx] == 0 or (gx==1 and gy==1):
            maze_lst[gy][gx] = 2
            break;
    canvas.create_rectangle(gx*100, gy*100, gx*100+100, gy*100+100,
                            fill="red")

#　こうかとんがゴールにたどり着いたことを確認する関数
def check_goal():
    global count
    if maze_lst[my][mx]==2:
        create_goal()
        tkm.showinfo("クリアー", "あなたはゴールしました")


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

    # ゴールを作成する関数を実行する
    create_goal()

    # こうかとんインスタンスを生成して表示する
    tori = tk.PhotoImage(file="fig/8.png")
    mx, my = 1, 1 # こうかとんのいるマス(x, y)
    cx, cy = 0, 0 # こうかとんの座標(x, y)
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
