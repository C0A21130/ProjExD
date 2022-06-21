# tkinterのモジュールをインポートする
import tkinter as tk

def main():
    # tkクラスからアプリの基本となるインスタンスを作成
    root = tk.Tk()
    root.title("計算機")
    root.geometry("300x500")
    root.mainloop()

if __name__ == "__main__":
    main()