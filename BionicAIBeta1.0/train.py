# train.py - 训练AI
import time
import random
from tic_tac_toe import TicTacToe
from ai_learner import TryLearnerAI

def train_simple():
    """简单训练：AI对战随机玩家"""
    print("=== 开始训练AI ===")
    print("AI将自我对战学习")
    
    # 创建游戏
    game = TicTacToe()
    
    # 创建两个AI（互相对战学习）
    ai_x = TryLearnerAI(player_id=1, exploration=0.4, learning=0.2)
    ai_o = TryLearnerAI(player_id=2, exploration=0.4, learning=0.2)
    
    total_games = 3000
    start_time = time.time()
    
    print(f"计划训练 {total_games} 局")
    print("=" * 40)
    
    for game_num in range(1, total_games + 1):
        # 重置游戏
        state = game.reset()
        
        # 一局游戏
        while not game.done:
            # 当前玩家选择动作
            current_ai = ai_x if game.current_player == 1 else ai_o
            valid_moves = game.get_valid_moves()
            action = current_ai.choose_action(state, valid_moves)
            
            # 执行动作
            next_state, reward, done, info = game.step(action)
            
            # 记录经验（只记录当前玩家的）
            current_ai.record_experience(state, action, reward, next_state, done)
            
            state = next_state
        
        # 双方都从这局游戏中学习
        ai_x.learn_from_episode()
        ai_o.learn_from_episode()
        
        # 更新统计
        if game.winner == 1:
            ai_x.update_stats("win")
            ai_o.update_stats("loss")
        elif game.winner == 2:
            ai_x.update_stats("loss")
            ai_o.update_stats("win")
        else:
            ai_x.update_stats("draw")
            ai_o.update_stats("draw")
        
        # 显示进度
        if game_num % 500 == 0:
            elapsed = time.time() - start_time
            speed = game_num / elapsed
            print(f"第 {game_num}/{total_games} 局 | "
                  f"时间: {elapsed:.1f}s | "
                  f"速度: {speed:.1f}局/秒")
    
    # 训练完成
    total_time = time.time() - start_time
    print("=" * 40)
    print(f"训练完成！总时间: {total_time:.1f}秒")
    print(f"平均速度: {total_games/total_time:.1f}局/秒")
    
    # 显示AI统计
    print("\nAI X 统计:")
    ai_x.print_stats()
    
    print("\nAI O 统计:")
    ai_o.print_stats()
    
    return ai_x, ai_o

def test_ai(ai, test_games=100):
    """测试AI性能"""
    print("\n=== 测试AI性能 ===")
    
    game = TicTacToe()
    wins = 0
    
    for _ in range(test_games):
        state = game.reset()
        
        while not game.done:
            # AI回合
            if game.current_player == 1:
                valid_moves = game.get_valid_moves()
                action = ai.choose_action(state, valid_moves, greedy=True)
                state, _, done, _ = game.step(action)
            # 随机玩家回合
            else:
                valid_moves = game.get_valid_moves()
                action = random.choice(valid_moves)
                state, _, done, _ = game.step(action)
        
        if game.winner == 1:
            wins += 1
    
    win_rate = wins / test_games * 100
    print(f"测试 {test_games} 局，AI胜率: {win_rate:.1f}%")
    
    if win_rate > 70:
        print("✅ AI表现优秀！")
    elif win_rate > 50:
        print("✓ AI表现良好")
    else:
        print("⚠ AI需要更多训练")

if __name__ == "__main__":
    print("井字棋AI训练程序")
    print("=" * 50)
    
    # 训练AI
    ai_x, ai_o = train_simple()
    
    # 测试AI
    test_ai(ai_x)
    
    # 询问是否要玩游戏
    print("\n=== 游戏选项 ===")
    print("1. 观看AI自我对战")
    print("2. 与AI对战")
    print("3. 退出")
    
    choice = input("请选择 (1/2/3): ")
    
    if choice == "1":
        print("\n=== AI自我对战演示 ===")
        game = TicTacToe()
        state = game.reset()
        
        while not game.done:
            game.render()
            current_ai = ai_x if game.current_player == 1 else ai_o
            valid_moves = game.get_valid_moves()
            action = current_ai.choose_action(state, valid_moves, greedy=True)
            state, _, done, _ = game.step(action)
            time.sleep(0.5)  # 暂停一下方便观看
        
        game.render()
        if game.winner == 0:
            print("平局！")
        else:
            print(f"{'X' if game.winner == 1 else 'O'} 获胜！")
    
    elif choice == "2":
        print("\n=== 与AI对战 ===")
        print("你执X，AI执O")
        print("输入位置编号 0-8")
        print("位置对应关系:")
        print("  0 1 2")
        print("0 0 1 2")
        print("1 3 4 5")
        print("2 6 7 8")
        
        game = TicTacToe()
        state = game.reset()
        
        while not game.done:
            game.render()
            
            if game.current_player == 1:  # 人类回合
                while True:
                    try:
                        move = int(input("你的回合 (0-8): "))
                        if move in game.get_valid_moves():
                            state, _, done, _ = game.step(move)
                            break
                        else:
                            print("无效位置，请重试")
                    except:
                        print("请输入数字 0-8")
            else:  # AI回合
                print("AI思考中...")
                valid_moves = game.get_valid_moves()
                action = ai_o.choose_action(state, valid_moves, greedy=True)
                print(f"AI下在位置 {action}")
                state, _, done, _ = game.step(action)
        
        game.render()
        if game.winner == 0:
            print("平局！")
        elif game.winner == 1:
            print("你赢了！")
        else:
            print("AI赢了！")
    
    print("\n程序结束。")