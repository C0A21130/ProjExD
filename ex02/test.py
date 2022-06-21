import tkinter as tk
import tkinter.messagebox as tkm

def button_click(event):
    btn = event.widget
    txt = btn["text"]
    tkm.showwarning("警告", f"{txt}ボタンを押した！！")

def new_func(btn):
    for row in btn:
        print(row,btn[row])

# アプリの基礎となるtkクラスからrootインスタンスを作成する
root = tk.Tk()

root.title("おためしか")  # アプリのタイトルをつける
root.geometry("500x200") # アプリの画面の大きさを幅500,高さ400にする

# アプリ内に文字を出力する
label = tk.Label(root, 
                text="ラベルを書いてみた件",
                font=("Ricty Diminished",20)
                )
label.pack() # 実際に出力する

# アプリ内にボタンを作成する(アプリ名, 表示する文字, 押したときに実行する関数)
button = tk.Button(root, text="押すな", command=button_click)
button.bind("<1>", button_click)
button.pack()

# 入力欄をアプリに作成する
entry = tk.Entry(root, width=30)
entry.insert(tk.END, "fugapiyo") # 初期状態で表示する文字を決める
entry.pack()


root.mainloop()

