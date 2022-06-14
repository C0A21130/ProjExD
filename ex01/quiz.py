from random import randint
import datetime

def main():
    start = datetime.datetime.now() # 始まる時間を記録
    question, anser = shutudai()    # 問題とそれに対する答えを返す
    kaito(question, anser)          # 帰ってきた問題と答えを出力する
    end = datetime.datetime.now()   # 終わる時間を記録  
    print(end - start)
    

def shutudai():
    question_number = randint(0, 2) # 問題番号

    questions = ["サザエの旦那の名前は?", "カツオの妹の名前は?", "タラオはカツオから見てどんな関係?"]
    ansers = [["マスオ", "ますお"], ["ワカメ", "ワカメ"], ["甥", "おい", "甥っ子", "おいっこ"]]

    # 問題と答えをタプルで返却する
    return questions[question_number], ansers[question_number]

def kaito(question, anser):
    inp = input(question)
    hit = 0               # 答えがあっていれば間違っていれば0、合っていれば1になる
    for i in anser:
        if i == inp:
            hit = 1

    if (hit==1):
        print("正解")
    else:
        print("不正解")

if __name__ == "__main__":
    main()
