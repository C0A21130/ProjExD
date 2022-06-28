import tkinter as tk
import tkinter.messagebox as tkm

# 1000msに1回tmrを1増やす
def count_up():
    global tmr, jid
    tmr = tmr + 1
    label["text"] = tmr
    jid = root.after(1000, count_up)
    
# ボタンを押した後に押したボタンを表示する関数
def keydown(event):
    global jid
    if jid != None:
        root.after_cancel(jid)
        jid = None
        return
    key = event.keysym
    tkm.showinfo("キー落下", f"{key}が押されました")
    jid = root.after(1000, count_up)

if __name__ == "__main__":
    root = tk.Tk()
    label = tk.Label(root, text="hello", font=("Times New Roman", 80))
    label.pack()
    tmr = 0 # グローバル変数
    jid = None # ジョブ番号
    # root.after(1000, count_up)
    root.bind("<KeyPress>", keydown)
    root.mainloop()
