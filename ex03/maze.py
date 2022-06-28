from sympy import im


import tkinter as tk

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
    cx,cy = 300, 400
    canvas.create_image(cx, cy, imag=tori, tag="tori")

    root.mainloop()