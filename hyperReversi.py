import numpy as np
import random

TILE = 0
POINT = 1

class Field():

    def __init__(self):
        self.field = np.zeros((10,10,2), dtype=int)
        self.field[3][3][TILE] = 1
        self.field[4][4][TILE] = 1
        self.field[5][5][TILE] = 1
        self.field[6][6][TILE] = 1
        self.field[3][5][TILE] = 2
        self.field[4][6][TILE] = 2
        self.field[5][3][TILE] = 2
        self.field[6][4][TILE] = 2
        self.field[3][4][TILE] = 3
        self.field[4][3][TILE] = 3
        self.field[5][6][TILE] = 3
        self.field[6][5][TILE] = 3
        self.field[3][6][TILE] = 4
        self.field[4][5][TILE] = 4
        self.field[5][4][TILE] = 4
        self.field[6][3][TILE] = 4

        self.field[3][3][POINT] = 1
        self.field[4][4][POINT] = 1
        self.field[5][5][POINT] = 1
        self.field[6][6][POINT] = 1
        self.field[3][5][POINT] = 1
        self.field[4][6][POINT] = 1
        self.field[5][3][POINT] = 1
        self.field[6][4][POINT] = 1
        self.field[3][4][POINT] = 1
        self.field[4][3][POINT] = 1
        self.field[5][6][POINT] = 1
        self.field[6][5][POINT] = 1
        self.field[3][6][POINT] = 1
        self.field[4][5][POINT] = 1
        self.field[5][4][POINT] = 1
        self.field[6][3][POINT] = 1
    
        #tarn == 1 or 3 -> Player1, tarn == 2 or 4 -> Player2
        self.tarn = 1
        self.remainingLocation = self.getTileBlankSum()
        self.winState = 0
        self.player1Point = 8
        self.player2Point = 8
        self.isSkiped = False

    #ターンを次の値に変更
    def tarnEnd(self):
        self.remainingLocation = self.getTileBlankSum()
        self.player1Point = self.getFieldPoint(1)
        self.player2Point = self.getFieldPoint(2)
        self.isSkiped = False
        if self.remainingLocation == 0:
            p1 = self.getFieldPoint(1)
            p2 = self.getFieldPoint(2)
            if p1 > p2:
                self.winState = 1
            elif p2 > p1:
                self.winState = 2
            elif p1 == p2:
                self.winState = 3
        else:
            self.__addTarn()
            i = 0
            while self.getPlaceablePosition() == []:
                self.isSkiped = True
                i += 1
                self.__addTarn()
                if i > 4:
                    p1 = self.getFieldPoint(1)
                    p2 = self.getFieldPoint(2)
                    if p1 > p2:
                        self.winState = 1
                    elif p2 > p1:
                        self.winState = 2
                    elif p1 == p2:
                        self.winState = 3
                    return

    def __addTarn(self):
        self.tarn = (self.tarn + 1) % 5
        if self.tarn == 0:
            self.tarn = 1

    #これは暗黒関数。これがないと探索できない
    def __getTileState(self, x, y, otherTile):
        if self.field[x][y][TILE] == 0:
            return 0
        elif self.field[x][y][TILE] != self.tarn:
            return 1
        elif self.field[x][y][TILE] == self.tarn:
            if otherTile == 1:
                return 2
            else:
                return 0
    
    #探索関数、タイルがひっくり返る方向を八方位で返す
    def __searchTile(self, x, y):
        

        validDirection = []
        #タイルがひっくり返る方角を配列に入れて返す
        #上: 0 右上: 1 右: 2 右下: 3 下: 4 左下: 5 左: 6 左上: 7

        #タイルから下方向の探索
        if x != 9:
            otherTile = 0
            i = x
            while i != 9:
                i += 1
                t = self.__getTileState(i, y, otherTile)
                if t == 0:
                    break
                elif t == 1:
                    otherTile = 1
                elif t == 2:
                    validDirection.append(4)

            #タイルから右下方向の探索
            if y != 9:
                otherTile = 0
                i = x
                j = y
                while i != 9 and j != 9:
                    i += 1
                    j += 1
                    t = self.__getTileState(i, j, otherTile)
                    if t == 0:
                        break
                    elif t == 1:
                        otherTile = 1
                    elif t == 2:
                        validDirection.append(3)
            #タイルから左下方向の探索
            if y != 0:
                otherTile = 0
                i = x
                j = y
                while i != 9 and j != 0:
                    i += 1
                    j -= 1
                    t = self.__getTileState(i, j, otherTile)
                    if t == 0:
                        break
                    elif t == 1:
                        otherTile = 1
                    elif t == 2:
                        validDirection.append(5)

        #タイルから上歩行の探索
        if x != 0:
            otherTile = 0
            i = x
            while i != 0:
                i -= 1
                t = self.__getTileState(i, y, otherTile)
                if t == 0:
                    break
                elif t == 1:
                    otherTile = 1
                elif t == 2:
                    validDirection.append(0)

            #タイルから右上方向の探索
            if y != 9:
                otherTile = 0
                i = x
                j = y
                while i != 0 and j != 9:
                    i -= 1
                    j += 1
                    t = self.__getTileState(i, j, otherTile)
                    if t == 0:
                        break
                    elif t == 1:
                        otherTile = 1
                    elif t == 2:
                        validDirection.append(1)

            #タイルから左上方向の探索
            if y != 0:
                otherTile = 0
                i = x
                j = y
                while i != 0 and j != 0:
                    i -= 1
                    j -= 1
                    t = self.__getTileState(i, j, otherTile)
                    if t == 0:
                        break
                    elif t == 1:
                        otherTile = 1
                    elif t == 2:
                        validDirection.append(7)

        #タイルから左方向の探索
        if y != 0:
            otherTile = 0
            i = y 
            while i != 0:
                i -= 1
                t = self.__getTileState(x, i, otherTile)
                if t == 0:
                    break
                elif t == 1:
                    otherTile = 1
                elif t == 2:
                    validDirection.append(6)

       #タイルから右方向の探索
        if y != 9:
            otherTile = 0
            i = y 
            while i != 9:
                i += 1
                t = self.__getTileState(x, i, otherTile)
                if t == 0:
                    break
                elif t == 1:
                    otherTile = 1
                elif t == 2:
                    validDirection.append(2)
        return validDirection

    def __changeTileColor(self, x, y):
        self.field[x][y][TILE] = self.tarn

    def __addTilePoint(self, x, y):
        self.field[x][y][POINT] += 1

    def __removeTilePoint(self, x, y):
        self.field[x][y][POINT] -= 1

    #挟まれたタイルの処理
    def __setTileState(self, x, y, state):
        #自分のタイルの色違いに対する処理(+処理)
        if state == 0:
            self.__changeTileColor(x, y)
            self.__addTilePoint(x, y)
        #相手のタイルをひっくり返す処理
        elif state == 1:
            self.__changeTileColor(x, y)
        #相手のタイルの+値を削る処理
        elif state == 2:
            self.__removeTilePoint(x, y)


    #探索関数の値をBoolに直すだけ
    def isSetTile(self, x, y):
        if self.field[x][y][TILE] != 0:
            return False

        if self.__searchTile(x, y) != []:
            return True

        return False

    def getFieldPoint(self, player):
        point = 0
        #player2
        if player % 2 == 0:
            for x in range(0, 10):
                for y in range(0, 10): 
                    if self.field[x][y][TILE] == 2 or self.field[x][y][TILE] == 4:
                        point += 1
                        point += (self.field[x][y][POINT] - 1) ** 2

        #player1
        else:
            for x in range(0, 10):
                for y in range(0, 10): 
                    if self.field[x][y][TILE] == 1 or self.field[x][y][TILE] == 3:
                        point += 1
                        point += (self.field[x][y][POINT] - 1) ** 2
        return point
    

    def setTile(self, x, y):
        if self.isSetTile(x, y) == False:
            return False
        
        t = self.__searchTile(x, y)

        for i in t:
            if i == 0:
                j = x
                while j != 0:
                    j -= 1
                    if self.field[j][y][TILE] == self.tarn:
                        break
                    elif self.field[j][y][TILE] % 2 == self.tarn % 2 and self.field[j][y][TILE] != self.tarn:
                        self.__setTileState(j, y, 0)
                    elif self.field[j][y][TILE] % 2 != self.tarn % 2:
                        if self.field[j][y][POINT] == 1:
                            self.__setTileState(j, y, 1)
                        elif self.field[j][y][POINT] > 1:
                            self.__setTileState(j, y, 2)

            elif i == 1:
                j = x
                k = y
                while j != 0 and k != 9:
                    j -= 1
                    k += 1
                    if self.field[j][k][TILE] == self.tarn:
                        break
                    elif self.field[j][k][TILE] % 2 == self.tarn % 2 and self.field[j][k][TILE] != self.tarn:
                        self.__setTileState(j, k, 0)
                    elif self.field[j][k][TILE] % 2 != self.tarn % 2:
                        if self.field[j][k][POINT] == 1:
                            self.__setTileState(j, k, 1)
                        elif self.field[j][k][POINT] > 1:
                            self.__setTileState(j, k, 2)

            elif i == 2:
                j = y
                while j != 9:
                    j += 1
                    if self.field[x][j][TILE] == self.tarn:
                        break
                    elif self.field[x][j][TILE] % 2 == self.tarn % 2 and self.field[x][j][TILE] != self.tarn:
                        self.__setTileState(x, j, 0)
                    elif self.field[x][j][TILE] % 2 != self.tarn % 2:
                        if self.field[x][j][POINT] == 1:
                            self.__setTileState(x, j, 1)
                        elif self.field[x][j][POINT] > 1:
                            self.__setTileState(x, j, 2)

            elif i == 3:
                j = x
                k = y
                while j != 9 and k != 9:
                    j += 1
                    k += 1
                    if self.field[j][k][TILE] == self.tarn:
                        break
                    elif self.field[j][k][TILE] % 2 == self.tarn % 2 and self.field[j][k][TILE] != self.tarn:
                        self.__setTileState(j, k, 0)
                    elif self.field[j][k][TILE] % 2 != self.tarn % 2:
                        if self.field[j][k][POINT] == 1:
                            self.__setTileState(j, k, 1)
                        elif self.field[j][k][POINT] > 1:
                            self.__setTileState(j, k, 2)

            elif i == 4:
                j = x
                while j != 9:
                    j += 1
                    if self.field[j][y][TILE] == self.tarn:
                        break
                    elif self.field[j][y][TILE] % 2 == self.tarn % 2 and self.field[j][y][TILE] != self.tarn:
                        self.__setTileState(j, y, 0)
                    elif self.field[j][y][TILE] % 2 != self.tarn % 2:
                        if self.field[j][y][POINT] == 1:
                            self.__setTileState(j, y, 1)
                        elif self.field[j][y][POINT] > 1:
                            self.__setTileState(j, y, 2)

            elif i == 5:
                j = x
                k = y
                while j != 9 and k != 0:
                    j += 1
                    k -= 1
                    if self.field[j][k][TILE] == self.tarn:
                        break
                    elif self.field[j][k][TILE] % 2 == self.tarn % 2 and self.field[j][k][TILE] != self.tarn:
                        self.__setTileState(j, k, 0)
                    elif self.field[j][k][TILE] % 2 != self.tarn % 2:
                        if self.field[j][k][POINT] == 1:
                            self.__setTileState(j, k, 1)
                        elif self.field[j][k][POINT] > 1:
                            self.__setTileState(j, k, 2)

            elif i == 6:
                
                j = y
                while j != 0:
                    j -= 1
                    if self.field[x][j][TILE] == self.tarn:
                        break
                    elif self.field[x][j][TILE] % 2 == self.tarn % 2 and self.field[x][j][TILE] != self.tarn:
                        self.__setTileState(x, j, 0)
                    elif self.field[x][j][TILE] % 2 != self.tarn % 2:
                        if self.field[x][j][POINT] == 1:
                            self.__setTileState(x, j, 1)
                        elif self.field[x][j][POINT] > 1:
                            self.__setTileState(x, j, 2)

            elif i == 7:
                j = x
                k = y
                while j != 0 and k != 0:
                    j -= 1
                    k -= 1
                    if self.field[j][k][TILE] == self.tarn:
                        break
                    elif self.field[j][k][TILE] % 2 == self.tarn % 2 and self.field[j][k][TILE] != self.tarn:
                        self.__setTileState(j, k, 0)
                    elif self.field[j][k][TILE] % 2 != self.tarn % 2:
                        if self.field[j][k][POINT] == 1:
                            self.__setTileState(j, k, 1)
                        elif self.field[j][k][POINT] > 1:
                            self.__setTileState(j, k, 2)

        self.__changeTileColor(x, y)
        self.__addTilePoint(x, y)
        self.tarnEnd()

    def getPlaceablePosition(self):
        positionList = []
        for i in range(0, 10):
            for j in range(0, 10):
                if self.isSetTile(i, j):
                    positionList.append([i, j])
        return positionList
        
    #盤面をわかりやすく出力
    def printField(self):
        print("\n-----------------------------------------------\n")
        if self.winState != 0:
            if self.winState == 1:
                print("Player1 Win!")
            elif self.winState == 2:
                print("Player2 Win!")
            else:
                print("Hikiwake!")
            print()
            return

        print("Player1Point: " + str(self.player1Point))
        print("Player2Point: " + str(self.player2Point))

        if self.isSkiped:
            print("TarnSkiped")

        if self.tarn % 2 == 0:
            print("Tarn: Player2, ", self.tarn)
        else:
            print("Tarn: Player1, ", self.tarn)

        print(" ", end = "|")
        for i in range(0, 10):
            print(i, end = "|")
        print("   |", end = "")
        for i in range(0, 10):
            print(i, end = "|")
        print()
        for x in range(0, 10):
            for y in range(0, 10): 
                if(y == 0):
                    print(x, end = "|")
                print(self.field[x][y][TILE], end = " ")
            print("", end = "  ")
            for y in range(0, 10): 
                if(y == 0):
                    print(x, end = "|")
                print(self.field[x][y][POINT] - 1 if self.field[x][y][POINT] - 1 >= 0 else 0, end = " ")
            print()
        




    def getTileBlankSum(self):
        sum = 0
        for i in range(0, 10):
            for j in range(0, 10):
                if self.field[i][j][TILE] == 0:
                    sum += 1
        return sum

    def debug(self):
        self.isSetTile(2, 4)
        
class Organizer():
    def __init__(self, showBoard=True, showResult=True, debug = False):
        self._showBoard = showBoard
        self._showResult = showResult
        self._debug = debug

    def start(self):
        if self._debug: 
            field = Field()
            field.printField()
            while(field.remainingLocation != 0):
                posList = field.getPlaceablePosition()
                pos = random.choice(posList)
                field.printField()
                field.setTile(pos[0], pos[1])
            field.printField()
        else:
            field = Field()
            while field.remainingLocation != 0:
                if self._showBoard:
                    field.printField()

                print("x: ", end = "")
                x = int(input())
                print("y: ", end = "")
                y = int(input())
                if  [x, y] in field.getPlaceablePosition():
                    field.setTile(x, y)
                else:
                    print("その位置は無効です")
            
            if field.winState != 0:
                if field.winState == 1:
                    print("Player1 Win!")
                elif field.winState == 2:
                    print("Player2 Win!")
                else:
                    print("Hikiwake!")
                print()
                return



def main():
    print("HyperReversi")
    game = Organizer()
    game.start()
    

if __name__ == "__main__":
    main()
