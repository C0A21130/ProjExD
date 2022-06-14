from random import randint

taget_string_num = 5
lost_string_num = 3

def main():
    taget_strings = []
    for i in range(taget_string_num):
        rand = randint(65,90) # 65(A) ~ 90(Z)の乱数を作成
        taget_strings.append(rand)

    lost_strings = []
    for i in range(lost_string_num):
        rand = 0
        while (True):
            rand = randint(65, 90)
            if (rand not in taget_strings):
                break 
        lost_strings.append(rand)

    print("対象文字")
    for i in taget_strings:
        print("{:3s}".format(chr(i)), end="")
    for i in lost_strings:
        print("{:3s}".format(chr(i)), end="")
    print("")

    print("欠損文字")
    for i in lost_strings:
        print("{:3s}".format(chr(i)), end="")
    print("")

    print("表示文字")
    for i in taget_strings:
        print("{:3s}".format(chr(i)), end="")
    print("")

    n = int(input("欠損文字はいくつあるでしょう?"))
    if n == len(lost_strings):
        print("正解")
        string_ans(lost_strings)
    else:
        print("不正解です。またチャレンジしてください")
        for i in range(30):
            print("-", end="")
        print("")

def string_ans(lost_strings):
    ansers = []
    for i in range(lost_string_num):
        i = input(f"{i+1}もじめは?")
        ansers.append(ord(i))

    status = 0
    for a in ansers:
        if (a in lost_strings):
            status += 1
        else:
            continue
    if (status == lost_string_num):
        print("正解!!")
    else:
        print("不正解です。またチャレンジしてください")
        for i in range(30):
            print("-", end="")
        print("")   


if __name__ == "__main__":
    main()
