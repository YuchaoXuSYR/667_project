import numpy as np
from enum import IntEnum
import random
import torch as tr
from neural_network import ChessNet
class CHESS_TYPE(IntEnum):
    NONE = 0,
    SLEEP_TWO = 1,
    LIVE_TWO = 2
    SLEEP_THREE = 3
    LIVE_THREE = 4,
    SLEEP_FOUR = 5,
    LIVE_FOUR = 6,
    LIVE_FIVE = 7


SCORE_MAX = 0x7fffffff
SCORE_MIN = -1 * SCORE_MAX


class TreeAI():
    def __init__(self, size):
        self.size = size
        self.state=[]
        self.state_score=[]
        self.firstorsecond=0
        # four direction
        self.record = np.zeros([size, size, 4])
        TYPE_NUM = 8
        self.type_count = np.zeros([TYPE_NUM, 2])
        # A more central position will have a higher position score
        self.net = ChessNet(self.size)
        self.net.load_state_dict(tr.load("model%d.pth" % self.size))
        self.net.eval()

    def reset(self):
        for y in range(self.size):
            for x in range(self.size):
                for i in range(4):
                    self.record[y][x][i] = 0

        for i in range(len(self.type_count)):
            for j in range(len(self.type_count[0])):
                self.type_count[i][j] = 0

    def getScore(self,board):

        # for i in range(1, 8, 1):
        #    self.type_count[i] = (i * 2) * (self.type_count[i] ** 2)
        if self.firstorsecond==1:
            stander = np.array(
                [[1, 1], [4, 4], [4, 4], [10, 10], [400, 100], [5000, 2000], [10000, 9000], [9999999, 9999999]])
        else:
            stander = np.array(
                [[1, 1], [4, 4], [4, 4], [10, 10], [400, 400], [5000, 5000], [10000, 10000], [9999999, 9999999]])


        sum= self.type_count * stander

        scores = sum.sum(axis=0)

        AIscore = scores[1] - scores[0]
        return AIscore

    def get_type_count(self, board):
        Player = 0
        AI = 1
        self.reset()
        for y in range(self.size):
            for x in range(self.size):
                if board[x][y][AI] == 1:
                    self.evaluatePoint(board, x, y, AI, Player)
                elif board[x][y][Player] == 1:
                    self.evaluatePoint(board, x, y, Player, AI)
        stander = np.array(
            [[0, 0], [1,1],[2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7]])
        sum = self.type_count * stander
        return sum


    def get_move(self, board):
        pos_board = np.zeros([self.size + 2, self.size + 2])
        for i in range(self.size):
            for j in range(self.size):
                if board[i, j, 0] == 1 or board[i, j, 1] == 1:
                    pos_board[i + 1, j + 1] = -999
                    pos_board[i + 2, j + 1] += 1
                    pos_board[i, j + 1] += 1
                    pos_board[i + 1, j + 2] += 1
                    pos_board[i + 1, j] += 1
                    pos_board[i + 2, j + 2] += 1
                    pos_board[i + 2, j] += 1
                    pos_board[i, j + 2] += 1
                    pos_board[i, j] += 1
                elif board[i, j, 0] == 2 or board[i, j, 1] == 2:
                    pos_board[i + 1, j + 1] = -999

        pos_board = np.delete(pos_board, -1, axis=1)
        pos_board = np.delete(pos_board, 0, axis=1)
        pos_board = np.delete(pos_board, -1, axis=0)
        pos_board = np.delete(pos_board, 0, axis=0)

        ava_pos = pos_board > 0
        pos_list = []
        for i in range(self.size):
            for j in range(self.size):
                if ava_pos[i, j]:
                    pos_list.append((i, j))
        return pos_list

    def network(self,board,hand=1):

        moves = self.get_move(board)


        max=SCORE_MIN
        min=SCORE_MAX
        best_move=None

        for x, y in moves:
            board[x][y][hand] = 1
            onehot=self.encode(board)
            onehot=onehot.unsqueeze(dim=0)
            score = self.net(onehot)
            board[x][y][hand] = 0

            if hand==1 and score>max:
                max=score
                best_move=(x,y)
            if hand==0 and score<min:
                min = score
                best_move = (x, y)

        if best_move==None:
            return (random.randint(0, self.size - 1), random.randint(0, self.size - 1))

        return best_move


    def encode(self,state):
        onehot = tr.zeros((3, self.size, self.size))
        onehot[1] = tr.tensor(state[:, :, 0])
        onehot[2] = tr.tensor(state[:, :, 1])
        temp= tr.tensor(state[:, :, 0]+state[:, :, 1])
        temp[temp==0]=8
        temp[temp<8]=0
        temp[temp==8]=1
        onehot[0]=temp
        return onehot


    def uniform(self, board):
        move = self.get_move(board)
        if move == []:
            if board[0][0][1] == 1 or board[0][0][0] == 1:
                print("error")
            else:
                return (random.randint(0, self.size - 1), random.randint(0, self.size - 1))

        return move[random.randint(0, len(move)) - 1]

    def __search(self, board, depth,hand, alpha=SCORE_MIN, beta=SCORE_MAX):

        if depth <= 0:
            score = self.evaluate(board)
            self.numOfNode += 1
            return score
        moves = self.get_move(board)
        bestmove = None


        # if there are no moves, just return the score
        if len(moves) == 0:
            return self.evaluate(board)

        for x, y in moves:

            board[x][y][hand] = 1
            score = self.__search(board, depth - 1,abs(hand-1), alpha,beta)
            if depth == self.maxdepth:
                self.state.append(board.copy())
                self.state_score.append(score)
            board[x][y][hand] = 0
            if hand == 1:
                if score > alpha:
                    alpha = score
                    bestmove = (x, y)
                    if alpha >= beta:
                        break
            elif hand == 0:
                if score < beta:
                    beta = score
                    bestmove = (x, y)
                    if alpha >= beta:
                        break

            # a = ((x,y), score)
            # print(a)


        if depth == self.maxdepth and bestmove:
            self.bestmove = bestmove
        if hand == 1:
            return alpha
        else:
            return beta


    def search(self, board, depth=2,hand=0):
        self.maxdepth = depth
        self.bestmove = None
        self.numOfNode = 0
        self.firstorsecond=hand
        score = self.__search(board, depth,hand)
        if self.bestmove==None:
            print("None")
            x,y=(random.randint(0, self.size - 1), random.randint(0, self.size - 1))
        else:
            x, y = self.bestmove
        nodes = self.numOfNode
        #print("AI process {} nodes".format(nodes))
        return nodes, x, y,self.state,self.state_score

    def evaluate(self, board):
        # human priority
        Player = 0
        AI = 1
        self.reset()
        for y in range(self.size):
            for x in range(self.size):
                if board[x][y][AI] == 1:
                    self.evaluatePoint(board, x, y, AI, Player)
                elif board[x][y][Player] == 1:
                    self.evaluatePoint(board, x, y, Player, AI)
        score = self.getScore(board)
        return score

    def evaluatePoint(self, board, x, y, mine, opponent):
        direction = [(1, 0), (0, 1), (1, 1), (1, -1)]

        for i in range(4):  # analyze four direction. horizontal,vertical,diagonal
            if self.record[x][y][i] == 0:
                self.analysisLine(board, x, y, direction[i], i, mine, opponent)

    def getLine(self, board, x, y, dir, mine, opponent):
        line = np.zeros([9])
        tmp_x = x + (-5 * dir[0])
        tmp_y = y + (-5 * dir[1])
        for i in range(9):
            tmp_x += dir[0]
            tmp_y += dir[1]
            if (tmp_x < 0 or tmp_x >= self.size or tmp_y < 0 or tmp_y >= self.size):
                line[i] = 1  # set out of range as player chess
            elif (board[tmp_x, tmp_y, opponent] == 1):
                line[i] = 1
            elif (board[tmp_x, tmp_y, 1] == 2 or board[tmp_x, tmp_y, 0] == 2):
                line[i] = 1
            elif (board[tmp_x, tmp_y, mine] == 1):
                line[i] = 2
        return line

    def analysisLine(self, board, x, y, direction, dir_index, mine, opponent):
        def setRecord(self, x, y, left, right, index, dir):
            tmp_x = x + (-5 + left) * dir[0]
            tmp_y = y + (-5 + left) * dir[1]
            for i in range(left, right + 1):
                tmp_x += dir[0]
                tmp_y += dir[1]
                if tmp_x >= self.size or tmp_y >= self.size or tmp_y < 0 or tmp_x < 0:
                    break
                self.record[tmp_x][tmp_y][index] = 1

        line = self.getLine(board, x, y, direction, mine, opponent)


        left_idx, right_idx = 4, 4
        while right_idx < 8:
            if line[right_idx + 1] != 2:
                break
            right_idx += 1
        while left_idx > 0:
            if line[left_idx - 1] != 2:
                break
            left_idx -= 1
        left_range, right_range = left_idx, right_idx
        while right_range < 8:
            if line[right_range + 1] == 1:
                break
            right_range += 1
        while left_range > 0:
            if line[left_range - 1] == 1:
                break
            left_range -= 1

        m_range = right_idx - left_idx + 1
        chess_range = right_range - left_range + 1
        if chess_range < 5:
            setRecord(self, x, y, left_range, right_range, dir_index, direction)
            return 0

        setRecord(self, x, y, left_idx, right_idx, dir_index, direction)

        if m_range == 5:
            self.type_count[CHESS_TYPE.LIVE_FIVE, mine] += 1

        if m_range == 4:
            left_empty = right_empty = False
            if line[left_idx - 1] == 0 and line[right_idx + 1] == 0:
                self.type_count[CHESS_TYPE.LIVE_FOUR, mine] += 1
            else:
                self.type_count[CHESS_TYPE.SLEEP_FOUR, mine] += 1

        if m_range == 3:
            left_empty = right_empty = False
            left_four = right_four = False
            if line[left_idx - 1] == 0:
                if line[left_idx - 2] == 2:  # MXMMM
                    setRecord(self, x, y, left_idx - 2, left_idx - 1, dir_index, direction)
                    self.type_count[CHESS_TYPE.SLEEP_FOUR, mine] += 1
                    left_four = True
                left_empty = True

            if line[right_idx + 1] == 0:
                if line[right_idx + 2] == 2:  # MMMXM
                    setRecord(self, x, y, right_idx + 1, right_idx + 2, dir_index, direction)
                    self.type_count[CHESS_TYPE.SLEEP_FOUR, mine] += 1
                    right_four = True
                right_empty = True

            if left_four or right_four:
                pass
            elif left_empty and right_empty:
                if chess_range > 5:  # XMMMXX, XXMMMX
                    self.type_count[CHESS_TYPE.LIVE_THREE, mine] += 1
                else:  # PXMMMXP
                    self.type_count[CHESS_TYPE.SLEEP_THREE, mine] += 1
            elif left_empty or right_empty:  # PMMMX, XMMMP
                self.type_count[CHESS_TYPE.SLEEP_THREE, mine] += 1

        if m_range == 2:
            left_empty = right_empty = False
            left_three = right_three = False
            if line[left_idx - 1] == 0:
                if line[left_idx - 2] == 2:
                    setRecord(self, x, y, left_idx - 2, left_idx - 1, dir_index, direction)
                    if line[left_idx - 3] == 0:
                        if line[right_idx + 1] == 0:  # XMXMMX
                            self.type_count[CHESS_TYPE.LIVE_THREE, mine] += 1
                        else:  # XMXMMP
                            self.type_count[CHESS_TYPE.SLEEP_THREE, mine] += 1
                        left_three = True
                    elif line[left_idx - 3] == 1:  # PMXMMX
                        if line[right_idx + 1] == 0:
                            self.type_count[CHESS_TYPE.SLEEP_THREE, mine] += 1
                            left_three = True

                left_empty = True

            if line[right_idx + 1] == 0:
                if line[right_idx + 2] == 2:
                    if line[right_idx + 3] == 2:  # MMXMM
                        setRecord(self, x, y, right_idx + 1, right_idx + 2, dir_index, direction)
                        self.type_count[CHESS_TYPE.SLEEP_FOUR, mine] += 1
                        right_three = True
                    elif line[right_idx + 3] == 0:
                        # setRecord(self, x, y, right_idx+1, right_idx+2, dir_index, dir)
                        if left_empty:  # XMMXMX
                            self.type_count[CHESS_TYPE.LIVE_THREE, mine] += 1
                        else:  # PMMXMX
                            self.type_count[CHESS_TYPE.SLEEP_THREE, mine] += 1
                        right_three = True
                    elif left_empty:  # XMMXMP
                        self.type_count[CHESS_TYPE.SLEEP_THREE, mine] += 1
                        right_three = True

                right_empty = True

            if left_three or right_three:
                pass
            elif left_empty and right_empty:  # XMMX
                self.type_count[CHESS_TYPE.LIVE_TWO, mine] += 1
            elif left_empty or right_empty:  # PMMX, XMMP
                self.type_count[CHESS_TYPE.SLEEP_TWO, mine] += 1

        if m_range == 1:
            left_empty = right_empty = False
            if line[left_idx - 1] == 0:
                if line[left_idx - 2] == 2:
                    if line[left_idx - 3] == 0:
                        if line[right_idx + 1] == 1:  # XMXMP
                            self.type_count[CHESS_TYPE.SLEEP_TWO, mine] += 1
                left_empty = True

            if line[right_idx + 1] == 0:
                if line[right_idx + 2] == 2:
                    if line[right_idx + 3] == 0:
                        if left_empty:  # XMXMX
                            # setRecord(self, x, y, left_idx, right_idx+2, dir_index, dir)
                            self.type_count[CHESS_TYPE.LIVE_TWO, mine] += 1
                        else:  # PMXMX
                            self.type_count[CHESS_TYPE.SLEEP_TWO, mine] += 1
                elif line[right_idx + 2] == 0:
                    if line[right_idx + 3] == 2 and line[right_idx + 4] == 0:  # XMXXMX
                        self.type_count[CHESS_TYPE.LIVE_TWO, mine] += 1

        return


