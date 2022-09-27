import random
import random
global a, b, c, alpha
syuturyoku = 9
kesson = 2
chance = 3
alpha = 26

def shutudai(alpha):
    lst = []
    prom = []
    for i in range(alpha -1):
        lst.append(chr(i+65))
    random.shuffle(lst)
    del lst[0:24-a]
    for w in lst:
        print(f"対象文字:{w}")
    delst = []
    for i in range(kesson):
        D = lst.pop()
        delst.append(D)
    print(f"欠損文字:{delst}")
    print(f"表示文字:{lst}")
    return delst

def kaitou(seikai):
    ans = int(input("欠損文字はいくつあるでしょうか？:"))
    if ans != b:
        print("不正解です")
    else:
        print("正解です、では具体的に欠損文字を1つずつ入力してください")
        for i in range(ans):
            c= 

if __name__ == "__main__":
    C = 0
    while C != chance:
        A = shutudai()
        B = kaitou(A)
        if B == 4:
            C += 1