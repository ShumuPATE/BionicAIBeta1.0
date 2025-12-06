# tic_tac_toe.py - 井字棋游戏（纯Python版）
class TicTacToe:
    """井字棋游戏环境"""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        """重置游戏"""
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]  # 0:空, 1:X, 2:O
        self.current_player = 1  # X先手
        self.done = False
        self.winner = None
        return self._get_state()
    
    def _get_state(self):
        """获取当前状态（字符串）"""
        return ''.join(str(cell) for row in self.board for cell in row)
    
    def get_valid_moves(self):
        """获取合法走法"""
        moves = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    moves.append(i * 3 + j)
        return moves
    
    def step(self, action):
        """执行一步"""
        if self.done:
            return self._get_state(), 0, self.done, {}
        
        row, col = divmod(action, 3)
        
        # 检查合法性
        if self.board[row][col] != 0:
            return self._get_state(), -10, True, {}
        
        # 执行
        self.board[row][col] = self.current_player
        
        # 检查胜负
        reward, self.done, self.winner = self._check_game_over()
        
        # 切换玩家
        self.current_player = 3 - self.current_player
        
        return self._get_state(), reward, self.done, {"winner": self.winner}
    
    def _check_game_over(self):
        """检查游戏是否结束"""
        board = self.board
        
        # 检查行
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] != 0:
                return 1, True, board[i][0]
        
        # 检查列
        for j in range(3):
            if board[0][j] == board[1][j] == board[2][j] != 0:
                return 1, True, board[0][j]
        
        # 检查对角线
        if board[0][0] == board[1][1] == board[2][2] != 0:
            return 1, True, board[0][0]
        if board[0][2] == board[1][1] == board[2][0] != 0:
            return 1, True, board[0][2]
        
        # 检查平局
        for row in board:
            if 0 in row:
                return 0, False, None
        
        return 0, True, 0
    
    def render(self):
        """显示棋盘"""
        symbols = {0: '.', 1: 'X', 2: 'O'}
        print("  0 1 2")
        for i in range(3):
            row_str = f"{i} "
            for j in range(3):
                row_str += symbols[self.board[i][j]] + " "
            print(row_str)
        print()
    
    def print_help(self):
        """打印帮助信息"""
        print("\n=== 井字棋帮助 ===")
        print("棋盘位置编号（0-8）:")
        print("  0 1 2")
        print("0 0 1 2")
        print("1 3 4 5") 
        print("2 6 7 8")
        print("输入位置编号下棋，如输入4下在中心")
        print("===============\n")