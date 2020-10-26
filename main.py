import numpy as np

class Game():
    def __init__(self):


        self.currentPlayer=1
        try:
            self.size=int(input("please input size of chessboard.(default=10)"))
        except:
            self.size = 10
            print("invalid size, cheesboard size has been set in default")
        if type(self.size) != int:
            self.size = 10
            print("invalid size, cheesboard size has been set in default")
        self.board=np.zeros([self.size,self.size,2])

    def printBoard(self):
        print("  ",end='')
        for i in range(self.size):
            print(i, end=' ')
        print("")
        for i in range(self.size):
            print(i, end=' ')
            for j in range(self.size):
                if self.board[i, j,0] == 1:
                    print("X", end=' ')
                elif self.board[i, j,1] == 1:
                    print("O", end=' ')
                elif self.board[i, j,0] == 2 or self.board[i, j,1] == 2:
                    print("□", end=' ')
                else:
                    print("-", end=' ')

            print()
            
    def SetObstacle(self):
        blockcount = np.random.randint(1,6)
        i = 0
        blockspos = []
        while(i < blockcount):
            a = np.random.randint(0, self.size)
            b = np.random.randint(0, self.size)
            if (a,b) in blockspos:
                i = i
            else:
                blockspos.append((a,b))
                i += 1   
        for (a,b) in blockspos:
            self.board[a, b, 0] = 2
            self.board[a, b, 1] = 2

    def player1(self):
        validPosition=False
        r = 0
        c = 0
        while(validPosition==False):
            try:
                row, col = map(int, input("Round: player1 ").split())
            except:
                print("please input two number as row and column")
                continue
            if row>=self.size or col>=self.size:
                print("row or column out of index!")
                continue
            if self.board[row,col,1]==0 and self.board[row,col,0]==0:
                self.board[row, col, 0] = 1
                r = row
                c = col
                validPosition=True

            else:
                print("invalid position, please make a choice again")

        self.currentPlayer=2
        return (r, c)


    def player2(self):
        r = 0
        c = 0
        validPosition = False
        while (validPosition == False):
            try:
                row, col = map(int, input("Round: player2 ").split())
            except:
                print("please input two number as row and column")
                continue
            if row>=self.size or col>=self.size:
                print("row or column out of index!")
                continue
            if self.board[row, col, 0] == 0 and self.board[row, col, 1] == 0:
                self.board[row, col, 1] = 1
                r = row
                c = col
                validPosition = True

            else:
                print("invalid position, please make a choice again")
        self.currentPlayer = 1
        return (r,c)

    def playGame(self):
        gameOver=False
        self.SetObstacle()
        while(gameOver==False):
            self.printBoard()
            
            if self.currentPlayer==1:
                pos = self.player1()
            else:
                pos = self.player2()

            winner = self.IsGameOver(pos)
            if winner==1:
                print("Player1 win!!")
                gameOver=True
            elif winner==2:
                print("Player2 win!!")
                gameOver = True
            elif winner == -1:
                print("Tie, nowhere to put")
                self.printBoard()
                gameOver = True

    def test_tie(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j][0] == 0 and  self.board[i][j][1] == 0:
                    return False
        return True

    def IsGameOver(self,pos):
        #return 0 for not over, return 1 for player1 win, return 2 for player2 win.
        row = pos[0]
        col = pos[1]
        id = -1
        if self.currentPlayer == 2:
            id = 0
        else:
            id = 1
        # search vertically
        count21 = 0
        for r in range(row+1,self.size):
            if self.board[r,col,id] ==1:
                count21 += 1
            else:
                break
            if count21 == 4:
                if id == 0:
                    return 1
                elif id == 1:
                    return 2
                else:
                    print("wrong id")

        count22 = 0
        for r in range(row - 1, -1, -1):
            if self.board[r, col, id] == 1:
                count22 += 1
            else:
                break
            if count22 == 4:
                if id ==0:
                    return 1
                elif id == 1:
                    return 2
                else:
                    print("wrong id")
        if count21+count22 >= 4:
            if id == 0:
                return 1
            elif id == 1:
                return 2
            else:
                print("wrong id")
        # search horizontally
        count11 = 0
        for c in range(col + 1, self.size):
            if self.board[row, c, id] == 1:
                count11 += 1
            else:
                break
            if count11 == 4:
                if id == 0:
                    return 1
                elif id == 1:
                    return 2
                else:
                    print("wrong id")

        count12 = 0
        for c in range(col - 1, -1, -1):
            if self.board[row, c, id] == 1:
                count12 += 1
            else:
                break
            if count12 == 4:
                if id == 0:
                    return 1
                elif id == 1:
                    return 2
                else:
                    print("wrong id")
        if count11 + count12 >= 4:
            if id == 0:
                return 1
            elif id == 1:
                return 2
            else:
                print("wrong id")
        # search diagonally
        count31 = 0
        for c in range(col + 1, self.size):
            if self.board[c, c, id] == 1:
                count31 += 1
            else:
                break
            if count31 == 4:
                if id == 0:
                    return 1
                elif id == 1:
                    return 2
                else:
                    print("wrong id")

        count32 = 0
        for c in range(col - 1, -1, -1):
            if self.board[c, c, id] == 1:
                count32 += 1
            else:
                break
            if count32 == 4:
                if id == 0:
                    return 1
                elif id == 1:
                    return 2
                else:
                    print("wrong id")
        if count31 + count32 >= 4:
            if id == 0:
                return 1
            elif id == 1:
                return 2
            else:
                print("wrong id")

        # search anti-diagonally
        count41 = 0
        r = row
        c = col
        while r-1 > -1 and c +1 <self.size:
            r -= 1
            c += 1
            if self.board[r, c, id] == 1:
                count41 += 1
            else:
                break
            if count41 == 4:
                if id == 0:
                    return 1
                elif id == 1:
                    return 2
                else:
                    print("wrong id")

        count42 = 0
        r = row
        c = col
        while r + 1 < self.size and c - 1 > -1:
            r += 1
            c -= 1
            if self.board[r, c, id] == 1:
                count42 += 1
            else:
                break
            if count42 == 4:
                if id == 0:
                    return 1
                elif id == 1:
                    return 2
                else:
                    print("wrong id")
        if count41 + count42 >= 4:
            if id == 0:
                return 1
            elif id == 1:
                return 2
            else:
                print("wrong id")

        if self.test_tie():
            return -1
        return 0



if __name__ == '__main__':
    my_game=Game()
    my_game.playGame()


