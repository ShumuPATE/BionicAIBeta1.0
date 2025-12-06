# quick_test.py - 快速测试
from tic_tac_toe import TicTacToe

def main():
    print("=== 井字棋快速测试 ===")
    print("测试游戏基本功能")
    
    # 创建游戏
    game = TicTacToe()
    
    print("1. 显示初始棋盘:")
    game.render()
    
    print("2. 显示合法走法:")
    print("   合法走法:", game.get_valid_moves())
    
    print("3. 测试几步棋:")
    moves = [4, 0, 5, 2, 8]  # 预定的棋步
    
    for i, move in enumerate(moves):
        player = "X" if i % 2 == 0 else "O"
        print(f"\n   {player}下在位置 {move}:")
        state, reward, done, info = game.step(move)
        game.render()
        
        if done:
            winner = info.get("winner", 0)
            if winner == 0:
                print("      游戏结束：平局")
            else:
                print(f"      游戏结束：{'X' if winner == 1 else 'O'}获胜")
            break
    
    print("\n4. 测试完成！")
    print("如果看到棋盘和棋步，说明游戏功能正常。")
    print("现在可以运行 train.py 来训练AI了。")

if __name__ == "__main__":
    main()