import numpy as np
import tree
import matplotlib.pyplot as plt

class Game():
    def __init__(self, boadrsize):
        self.currentPlayer = 1
        self.AIflag = 0
        self.finalscore = 0
        self.size = boadrsize

        self.board = np.zeros([self.size, self.size, 2])
        self.ai = tree.TreeAI(self.size)

    def printBoard(self):
        print("  ", end='')
        for i in range(self.size):
            print(i, end=' ')
        print("")
        for i in range(self.size):
            print(i, end=' ')
            for j in range(self.size):
                if self.board[i, j, 0] == 1:
                    print("X", end=' ')
                elif self.board[i, j, 1] == 1:
                    print("O", end=' ')
                elif self.board[i, j, 0] == 2 or self.board[i, j, 1] == 2:
                    print("□", end=' ')
                else:
                    print("-", end=' ')

            print()

    def SetObstacle(self):
        if self.size <= 3:
            blockcount = 1
        else:
            blockcount = np.random.randint(1, self.size / 2)
        i = 0
        blockspos = []
        while (i < blockcount):
            a = np.random.randint(0, self.size)
            b = np.random.randint(0, self.size)
            if (a, b) in blockspos:
                i = i
            else:
                blockspos.append((a, b))
                i += 1
        for (a, b) in blockspos:
            self.board[a, b, 0] = 2
            self.board[a, b, 1] = 2

    def player2(self):
        validPosition = False
        row = 0
        col = 0
        while (validPosition == False):

            print("TreeAI's Turn")
            _, row, col, _, _ = self.ai.search(self.board, 2, hand=0)
            print("TreeAI choose to put in: {x}, {y}".format(x=row, y=col))

            if row >= self.size or col >= self.size:
                print("row or column out of index!")
                continue
            if self.board[row, col, 1] == 0 and self.board[row, col, 0] == 0:
                self.board[row, col, 1] = 1
                r = row
                c = col
                validPosition = True

            else:
                print("invalid position, please make a choice again")

        self.currentPlayer = 1
        return (row, col)

    def player1(self):
        row = 0
        col = 0
        validPosition = False
        while (validPosition == False):

            print("NetworkAI's Turn")
            row, col= self.ai.network(self.board, hand=1)
            print("NetworkAI choose to put in: {x}, {y}".format(x=row, y=col))
            if row >= self.size or col >= self.size:
                print("row or column out of index!")
                continue
            if self.board[row, col, 0] == 0 and self.board[row, col, 1] == 0:
                self.board[row, col, 0] = 1
                r = row
                c = col
                validPosition = True

            else:
                print("invalid position, please make a choice again")
                continue
        self.currentPlayer = 2
        return (row, col)

    def playGame(self):
        self.AIflag = 1
        gameOver = False
        self.SetObstacle()

        while (gameOver == False):
            self.printBoard()

            if self.currentPlayer == 1:
                pos = self.player1()
            else:
                pos = self.player2()

            winner = self.IsGameOver(pos)
            if winner == 1:
                print("Player1 win!!")
                self.printBoard()
                gameOver = True
            elif winner == 2:
                print("Player2 win!!")
                self.printBoard()
                gameOver = True
            elif winner == -1:
                print("Tie, nowhere to put")
                self.printBoard()
                gameOver = True
            self.finalscore = self.ai.get_type_count(self.board)

    def test_tie(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j][0] == 0 and self.board[i][j][1] == 0:
                    return False
        return True

    def IsGameOver(self, pos):
        # return 0 for not over, return 1 for player1 win, return 2 for player2 win.
        row = pos[0]
        col = pos[1]
        id = -1
        if self.currentPlayer == 2:
            id = 0
        else:
            id = 1
        # search vertically
        count21 = 0
        for r in range(row + 1, self.size):
            if self.board[r, col, id] == 1:
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
                if id == 0:
                    return 1
                elif id == 1:
                    return 2
                else:
                    print("wrong id")
        if count21 + count22 >= 4:
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
        r = row
        c = col
        while r + 1 < self.size and c + 1 < self.size:
            r += 1
            c += 1
            a = self.board[r, c, id]
            if self.board[r, c, id] == 1:
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
        r = row
        c = col
        while r - 1 > -1 and c - 1 > -1:
            r -= 1
            c -= 1
            if self.board[r, c, id] == 1:
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
        while r - 1 > -1 and c + 1 < self.size:
            r -= 1
            c += 1
            a = self.board[r, c, id]
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
    for i in range(8, 9):
        file_score = 'file_score_{size}.jpg'.format(size=i)
        games_node = np.zeros(100)
        games_efficiency = np.zeros(100)
        final_score_P1 = np.zeros(100)
        final_score_P2 = np.zeros(100)
        for j in range(100):
            my_game = Game(i)
            my_game.playGame()
            score = my_game.finalscore.sum(axis=0)
            final_score_P1[j] = score[0]
            final_score_P2[j] = score[1]


        plt.bar(x=range(100), height=final_score_P2.tolist(), label='Tree_AI', color='steelblue', alpha=0.8)
        plt.bar(x=range(100), height=final_score_P1.tolist(), label='Network_AI', color='orange', alpha=0.8)
        for x, y in enumerate(final_score_P2.tolist()):
            plt.text(x, y + 100, '%s' % y, ha='center', va='bottom')
        for x, y in enumerate(final_score_P1.tolist()):
            plt.text(x, y + 100, '%s' % y, ha='center', va='top')
        plt.title("NetworkAI VS TreeAI")
        plt.xlabel("games")
        plt.ylabel("final scores")
        plt.legend()
        plt.savefig(file_score)
        plt.clf()

print(1)

