from random import randint

TARGET_STRING_NUM = 10 # 表示文字数
LOST_STRING_NUM = 4   # 欠損文字数

HIT = 1   # ヒットした
NOHIT = 0 # ヒットしなかった

def main():
    while(True):
        lost_strings = put()
        n = int(input("欠損文字はいくつあるでしょう?："))
        if n == len(lost_strings):
            print("正解")
            result = string_ans(lost_strings)
            if (result):
                break
        else:
            print("不正解です。またチャレンジしてください")
            for i in range(30):
                print("-", end="")
            print("")

# 文字を表示する
def put():
    taget_strings = [] # 対象文字を保存するリスト
    for i in range(TARGET_STRING_NUM):
        rand = randint(65,90) # 65(A)~90(Z)の乱数を作成
        taget_strings.append(rand)

    lost_strings = [] # 欠損文字を保存するリスト
    for i in range(LOST_STRING_NUM):
        rand = 0 # 乱数を保存する変数
        while (True):
            rand = randint(65, 90) # 65(A)~90(Z)
            if (rand not in taget_strings):
                break 
        lost_strings.append(rand)

    print("対象文字")
    output_string(taget_strings + lost_strings)

    print("欠損文字")
    output_string(lost_strings)

    print("表示文字")
    output_string(taget_strings)

    return lost_strings

    
def output_string(l):
    for i in l:
        print("{:3s}".format(chr(i)), end="")
    print("")

# 欠損文字の入力を求めて実際の文字と適合しているか確認する関数
def string_ans(lost_strings):
    ansers = []
    # 実際の欠損文字数の分の文字数の入力を求める
    for i in range(LOST_STRING_NUM):
        i = input(f"{i+1}文字を入力してください：")
        ansers.append(ord(i))

    # 欠損文字にヒットする度に1足していく
    status = NOHIT
    for a in ansers:
        if (a in lost_strings):
            status += HIT
        else:
            continue

    # 実際に欠損した文字数と入力してヒットした文字数が一致したときに正解を返す
    if (status == LOST_STRING_NUM):
        print("正解!!")
        return 1
    else:
        print("不正解です。またチャレンジしてください")
        for i in range(30):
            print("-", end="")
        print("")   
        return 0


if __name__ == "__main__":
    main()
