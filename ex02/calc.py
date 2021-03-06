# tkinterのモジュールをインポートする
import tkinter as tk
import tkinter.messagebox as tkm
from random import randint
import datetime

def main():
    key = randint(1000, 10000)
    d = datetime.datetime.now() # 現在の日時を取得する
    # ボタンを入力したときの動作
    def button_click(event):
        btn = event.widget
        txt = btn["text"]
        if txt == "+":
            entry.insert(tk.END, "+")
        elif txt == "=":
            formula = entry.get()
            result = eval(formula)
            entry.delete(0, tk.END)
            entry.insert(tk.END, int(result))
            dt = f"{d.month}+{d.day}" # 現在の日時を足し算の式で表す
            if str(formula) == dt:
                tkm.showwarning("おめでとう", f"お誕生日おめでとう")
        else:
            entry.insert(tk.END, int(txt))
            formula = int(entry.get())  
            if formula == key:
                entry.delete(0, tk.END)
                entry.insert(tk.END, "なぜ( ﾟДﾟ)")
            elif formula == 999:
                entry.delete(0, tk.END)
                tkm.showwarning("脱出", f"あなたは開発者と認めましょう鍵は{key}")
        
    def expo(event):
        btn = event.widget
        txt = btn["text"]
        formula = int(entry.get())
        result = formula ** 2
        entry.delete(0, tk.END)
        entry.insert(tk.END, int(result))

    def ro(event):
        btn = event.widget
        txt = btn["text"]
        formula = int(entry.get())
        result = formula ** (1/2)
        entry.delete(0, tk.END)
        entry.insert(tk.END, int(result))


    # tkクラスからアプリの基本となるインスタンスを作成
    root = tk.Tk()
    root.title("計算機")
    root.geometry("400x600")

    # 数字を表示する画面を作成する
    entry = tk.Entry(justify="right",
                    width=10,
                    font=("Times New Roman",40)
                    )
    entry.grid(row=0, column=0, columnspan=3)
    
    # 数字のボタンを9~0まで作成する
    r = 1
    c = 0
    for i in range(9, -1, -1):
        button = tk.Button(root,
                        width=4,
                        height=2,
                        text=i,
                        font=("Times New Roman", 30)
                        )
        if (i%3==0):
            r += 1
            c = 0
        else:
            c += 1
        button.grid(row=r, column=c)
        button.bind("<1>", button_click)
    
    # プラスボタンを作成する
    plus_button = tk.Button(root,
                        width=4,
                        height=2,
                        text="+",
                        font=("Times New Roman", 30)
                        )
    plus_button.grid(row=5, column=1)
    plus_button.bind("<1>", button_click)

    # イコールボタンを作成する
    equal_button = tk.Button(root,
                        width=4,
                        height=2,
                        text="=",
                        font=("Times New Roman", 30)
                        )
    equal_button.grid(row=5, column=2)
    equal_button.bind("<1>", button_click)

    # 二乗のボタンを作成する
    square_button = tk.Button(root,
                            width=4,
                            height=2,
                            text="^2",
                            font=("Times New Roman", 30)
                            )
    square_button.grid(row=2, column=4)
    square_button.bind("<1>", expo)

    # 平方根のボタンを作成する
    square_button = tk.Button(root,
                            width=4,
                            height=2,
                            text="√",
                            font=("Times New Roman", 30)
                            )
    square_button.grid(row=3, column=4)
    square_button.bind("<1>", ro)

    root.mainloop()


if __name__ == "__main__":
    main()
