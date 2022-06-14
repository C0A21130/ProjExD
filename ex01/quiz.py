from random import randint
import datetime

HIT = 1
NOHIT = 0

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
    i = input(question)
    status = NOHIT   # 答えがあっていれば間違っていればNOHIT、合っていればHITになる
    if i in anser:
        status = HIT

    if (status==HIT):
        print("正解")
    else:
        print("出直してこい")

if __name__ == "__main__":
    main()
