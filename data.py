import numpy as np
import tree
import torch as torch



class Genetrate_data():
    def __init__(self):
        self.currentPlayer = 1
        self.AIflag = 0
        self.size=9
        self.depth=2
        self.num_games=30
        self.state=[]
        self.state_score=[]
        self.board = np.zeros([self.size, self.size, 2])
        self.ai = tree.TreeAI(self.size)

    def reset(self):
        self.board = np.zeros([self.size, self.size, 2])
        self.ai = tree.TreeAI(self.size)

    def player2(self):
        r = 0
        c = 0
        s=0
        validPosition = False
        while (validPosition == False):
            score, row, col,state,state_score = self.ai.search(self.board, self.depth-1,hand=1)

            if row >= self.size or col >= self.size:
                continue
            if self.board[row, col, 0] == 0 and self.board[row, col, 1] == 0:
                self.board[row, col, 1] = 1
                r = row
                c = col
                s=score
                validPosition = True
                for i in range(len(state)):
                    self.state.append(state[i])
                    self.state_score.append(state_score[i])
        self.currentPlayer = 1
        return (r, c),s

    def player1(self):
        r = 0
        c = 0
        s=0
        validPosition = False
        while (validPosition == False):
            score, row, col ,state,state_score= self.ai.search(self.board, self.depth,hand=0)
            if row >= self.size or col >= self.size:
                continue
            if self.board[row, col, 0] == 0 and self.board[row, col, 1] == 0:
                self.board[row, col, 0] = 1
                r = row
                c = col
                s=score
                validPosition = True
                for i in range(len(state)):
                    self.state.append(state[i])
                    self.state_score.append(state_score[i])

        self.currentPlayer = 2
        return (r, c),s

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

    def generate(self):
        for game in range(self.num_games):
            print(game)
            self.reset()
            self.AIflag = 1
            gameOver = False
            while (gameOver == False):
                if self.currentPlayer == 1:
                    pos ,s= self.player1()
                else:
                    pos,s = self.player2()

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


        return

    def get_batch(self):
        self.generate()
        batchSize = len(self.state)
        trainState = []
        trainScore = []

        for i in range(batchSize):
            state  = self.state[i]
            score=self.state_score[i]
            temp = self.encode(state)
            trainState.append(temp)
            trainScore.append(torch.tensor(score))

        trainState = torch.stack(trainState, 0)
        trainScore = torch.stack(trainScore, 0)
        trainScore = trainScore.reshape(trainScore.shape[0], 1)
        return (trainState, trainScore)

    def encode(self,state):

        onehot = torch.zeros((3, self.size, self.size))
        onehot[1] = torch.tensor(state[:, :, 0])
        onehot[2] = torch.tensor(state[:, :, 1])
        temp= torch.tensor(state[:, :, 0]+state[:, :, 1])
        temp[temp==0]=8
        temp[temp<8]=0
        temp[temp==8]=1
        onehot[0]=temp
        return onehot

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

    def test_tie(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j][0] == 0 and self.board[i][j][1] == 0:
                    return False
        return True



if __name__ == '__main__':
    my_data = Genetrate_data()

    inputs, outputs =my_data.get_batch()

    import pickle as pk

    with open("data%d.pkl" % my_data.size, "wb") as f: pk.dump((inputs, outputs), f)

