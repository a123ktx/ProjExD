import random
def shutudai(num):
    mon = ["パンはパンでも食べられないパンは？", "扇子を持ち込んではいけない乗り物は？", "小銭を無視する生き物は？"]
    print(mon[num])

def kaito(num):
    ans = input("答えをどうぞ")
    kotae = [["フライパン", "ふらいぱん"], ["潜水艦","センスイカン", "せんすいかん"], ["黄金虫","コガネムシ","こがねむし"]]
    if ans == kotae[num]:
        print("正解です")
    else:
        print("違います")

if __name__ == "__main__":
    rand = random.randint(0,2)
    shutudai(rand)
    kaito(rand)