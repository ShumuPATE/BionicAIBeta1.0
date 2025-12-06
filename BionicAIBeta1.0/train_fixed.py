# train_fixed.py - 修复学习机制的版本
import time
import random
from tic_tac_toe import TicTacToe

class FixedAI:
    """修复学习机制的AI"""
    
    def __init__(self, player_id=1, exploration=0.3, learning=0.1):
        self.player_id = player_id
        self.exploration_rate = exploration
        self.learning_rate = learning
        
        # 正确的Q表结构
        self.q_table = {}  # state -> {action: value}
        
        # 统计
        self.stats = {
            "games": 0,
            "wins": 0,
            "losses": 0,
            "draws": 0,
            "states_explored": 0
        }
        
        # 当前对局记忆
        self.current_game_memory = []
    
    def choose_action(self, state, valid_moves, greedy=False):
        """选择动作"""
        # 探索：随机尝试
        if not greedy and random.random() < self.exploration_rate:
            return random.choice(valid_moves)
        
        # 利用：用学到的知识
        if state not in self.q_table:
            return random.choice(valid_moves)
        
        # 选择价值最高的合法动作
        state_values = self.q_table[state]
        best_action = None
        best_value = -9999
        
        for action in valid_moves:
            if action in state_values:
                if state_values[action] > best_value:
                    best_value = state_values[action]
                    best_action = action
        
        return best_action if best_action else random.choice(valid_moves)
    
    def remember(self, state, action, reward, next_state, done):
        """记住一步棋"""
        self.current_game_memory.append({
            "state": state,
            "action": action,
            "reward": reward,
            "next_state": next_state,
            "done": done
        })
    
    def learn_from_game(self):
        """从一整局游戏中学习"""
        if not self.current_game_memory:
            return
        
        # 从最后一步开始学习（蒙特卡洛方法）
        memory_reversed = list(reversed(self.current_game_memory))
        future_reward = 0
        
        for experience in memory_reversed:
            state = experience["state"]
            action = experience["action"]
            reward = experience["reward"]
            
            # 累积未来奖励
            future_reward = reward + 0.9 * future_reward
            
            # 确保状态在Q表中
            if state not in self.q_table:
                self.q_table[state] = {}
                self.stats["states_explored"] += 1
            
            # 当前价值
            current_value = self.q_table[state].get(action, 0)
            
            # 更新：新值 = 旧值 + 学习率 * (目标 - 旧值)
            # 这里使用简单的蒙特卡洛更新
            new_value = current_value + self.learning_rate * (future_reward - current_value)
            self.q_table[state][action] = new_value
        
        # 清空记忆
        self.current_game_memory = []
    
    def update_stats(self, result):
        """更新统计"""
        self.stats["games"] += 1
        if result == "win":
            self.stats["wins"] += 1
        elif result == "loss":
            self.stats["losses"] += 1
        else:
            self.stats["draws"] += 1
    
    def print_stats(self):
        """打印统计"""
        total = self.stats["games"]
        if total == 0:
            return
        
        print(f"\n=== AI统计 (玩家{self.player_id}) ===")
        print(f"对局数: {total}")
        print(f"胜: {self.stats['wins']} ({self.stats['wins']/total*100:.1f}%)")
        print(f"负: {self.stats['losses']} ({self.stats['losses']/total*100:.1f}%)")
        print(f"平: {self.stats['draws']} ({self.stats['draws']/total*100:.1f}%)")
        print(f"记忆的状态数: {self.stats['states_explored']}")
        
        if self.stats["states_explored"] > 0:
            print(f"平均每个状态的动作数: {sum(len(v) for v in self.q_table.values())/self.stats['states_explored']:.1f}")

def train_ai_understanding():
    """训练并观察AI的理解过程"""
    print("=== 观察AI的理解发展过程 ===")
    print("这次我们会记录AI的学习里程碑")
    
    game = TicTacToe()
    ai = FixedAI(player_id=1, exploration=0.4, learning=0.2)
    
    total_games = 5000
    milestone_interval = 500
    
    print(f"训练 {total_games} 局，每 {milestone_interval} 局记录一次")
    print("=" * 60)
    
    milestones = []
    
    for game_num in range(1, total_games + 1):
        # 重置游戏
        state = game.reset()
        
        # 一局游戏
        while not game.done:
            # AI的回合
            if game.current_player == 1:
                valid_moves = game.get_valid_moves()
                action = ai.choose_action(state, valid_moves)
                next_state, reward, done, info = game.step(action)
                ai.remember(state, action, reward, next_state, done)
                state = next_state
            # 随机对手的回合
            else:
                valid_moves = game.get_valid_moves()
                action = random.choice(valid_moves)
                next_state, reward, done, info = game.step(action)
                state = next_state
        
        # 学习
        ai.learn_from_game()
        
        # 更新统计
        if game.winner == 1:
            ai.update_stats("win")
        elif game.winner == 2:
            ai.update_stats("loss")
        else:
            ai.update_stats("draw")
        
        # 记录里程碑
        if game_num % milestone_interval == 0:
            # 测试当前AI的水平
            test_wins = 0
            for _ in range(100):
                test_state = game.reset()
                test_done = False
                
                while not test_done:
                    if game.current_player == 1:
                        valid_moves = game.get_valid_moves()
                        action = ai.choose_action(test_state, valid_moves, greedy=True)
                        test_state, _, test_done, _ = game.step(action)
                    else:
                        valid_moves = game.get_valid_moves()
                        action = random.choice(valid_moves)
                        test_state, _, test_done, _ = game.step(action)
                
                if game.winner == 1:
                    test_wins += 1
            
            win_rate = test_wins
            milestones.append((game_num, win_rate, ai.stats["states_explored"]))
            
            print(f"第 {game_num:4d} 局 | 胜率: {win_rate:3d}% | 记忆状态: {ai.stats['states_explored']:4d}")
            
            # 如果这是第一次突破50%胜率，特别标记
            if win_rate >= 50 and len([m for m in milestones if m[1] >= 50]) == 1:
                print(f"  🎉 里程碑！AI在第{game_num}局首次突破50%胜率")
    
    # 训练完成
    print("=" * 60)
    print(f"训练完成！")
    
    # 显示里程碑
    print("\n=== 理解发展里程碑 ===")
    for game_num, win_rate, states in milestones:
        print(f"第{game_num:4d}局: 胜率{win_rate:3d}%，记忆{states:4d}个状态")
    
    # 分析理解程度
    print("\n=== AI的理解程度分析 ===")
    print(f"1. 记忆容量: {ai.stats['states_explored']}个状态")
    print(f"2. 总对局经验: {ai.stats['games']}局")
    print(f"3. 最终胜率: {milestones[-1][1]}%")
    
    # 评估理解深度
    if milestones[-1][1] >= 80:
        print("4. 理解深度: 高级 (掌握了游戏策略)")
    elif milestones[-1][1] >= 60:
        print("4. 理解深度: 中级 (理解了基本规则)")
    elif milestones[-1][1] >= 40:
        print("4. 理解深度: 初级 (开始发现模式)")
    else:
        print("4. 理解深度: 入门 (还在随机探索)")
    
    return ai

def analyze_ai_knowledge(ai):
    """深入分析AI学到的知识"""
    print("\n" + "="*60)
    print("=== 深入分析AI的知识结构 ===")
    
    if not ai.q_table:
        print("AI没有学到任何知识！")
        return
    
    print(f"AI记忆了 {len(ai.q_table)} 个不同的游戏局面")
    
    # 分析几个关键局面
    print("\n--- 关键局面分析 ---")
    
    # 1. 初始局面
    initial_state = "0" * 9
    if initial_state in ai.q_table:
        print("1. 初始局面 (空棋盘):")
        actions = ai.q_table[initial_state]
        if actions:
            best_action = max(actions.items(), key=lambda x: x[1])[0]
            row, col = divmod(best_action, 3)
            print(f"   最佳动作: 位置{best_action} (行{row},列{col})")
            print(f"   动作价值: {actions[best_action]:.3f}")
            
            # 显示所有动作的价值排序
            print("   所有动作价值排名:")
            sorted_actions = sorted(actions.items(), key=lambda x: x[1], reverse=True)
            for i, (action, value) in enumerate(sorted_actions[:3]):  # 只显示前三
                r, c = divmod(action, 3)
                print(f"     {i+1}. 位置{action}({r},{c}): {value:.3f}")
    
    # 2. 中心已被占据的局面
    center_state = "000010000"
    if center_state in ai.q_table:
        print(f"\n2. 中心已被X占据:")
        game = TicTacToe()
        # 设置棋盘状态
        for i in range(3):
            for j in range(3):
                game.board[i][j] = int(center_state[i*3+j])
        game.current_player = 2  # O的回合
        game.render()
        
        actions = ai.q_table[center_state]
        if actions:
            best_action = max(actions.items(), key=lambda x: x[1])[0]
            print(f"   AI(O)会选择: 位置{best_action}")
    
    # 3. 必胜局面
    win_state = "110200000"  # X差一步赢
    if win_state in ai.q_table:
        print(f"\n3. X差一步获胜的局面:")
        actions = ai.q_table[win_state]
        if actions:
            best_action = max(actions.items(), key=lambda x: x[1])[0]
            expected_action = 2  # 应该下在位置2完成三连
            if best_action == expected_action:
                print(f"   ✅ AI正确选择了获胜位置 {best_action}")
            else:
                print(f"   ❌ AI选择了位置 {best_action}，但获胜位置应该是 {expected_action}")
    
    # 4. 需要防守的局面
    defense_state = "202001000"  # O差一步赢
    if defense_state in ai.q_table:
        print(f"\n4. 需要防守的局面 (O差一步赢):")
        actions = ai.q_table[defense_state]
        if actions:
            best_action = max(actions.items(), key=lambda x: x[1])[0]
            defense_action = 1  # 应该下在位置1阻止O
            if best_action == defense_action:
                print(f"   ✅ AI正确选择了防守位置 {best_action}")
            else:
                print(f"   ❌ AI选择了位置 {best_action}，但防守位置应该是 {defense_action}")
    
    # 统计AI的知识质量
    print("\n--- 知识质量分析 ---")
    total_states = len(ai.q_table)
    
    # 计算平均每个状态的决策信心
    confidences = []
    for state, actions in ai.q_table.items():
        if actions:
            values = list(actions.values())
            if values:
                # 信心 = 最佳值 - 次佳值
                sorted_values = sorted(values, reverse=True)
                if len(sorted_values) > 1:
                    confidence = sorted_values[0] - sorted_values[1]
                    confidences.append(confidence)
    
    if confidences:
        avg_confidence = sum(confidences) / len(confidences)
        print(f"平均决策信心: {avg_confidence:.3f}")
        print(f"最高决策信心: {max(confidences):.3f}")
        print(f"最低决策信心: {min(confidences):.3f}")
        
        if avg_confidence > 0.5:
            print("✅ AI有明确的决策偏好（理解较深）")
        elif avg_confidence > 0.1:
            print("✓ AI有一定决策偏好")
        else:
            print("⚠ AI决策犹豫（理解较浅）")

def play_with_ai(ai):
    """与AI对战"""
    print("\n" + "="*60)
    print("=== 与AI对战 ===")
    
    game = TicTacToe()
    print("你执X，AI执O")
    print("输入位置编号 0-8")
    game.print_help()
    
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
            action = ai.choose_action(state, valid_moves, greedy=True)
            row, col = divmod(action, 3)
            print(f"AI下在位置 {action} (行{row},列{col})")
            state, _, done, _ = game.step(action)
    
    game.render()
    if game.winner == 0:
        print("平局！")
    elif game.winner == 1:
        print("你赢了！")
    else:
        print("AI赢了！")

if __name__ == "__main__":
    print("井字棋AI理解发展实验")
    print("=" * 60)
    print("目标：观察AI如何从无知到理解")
    print("=" * 60)
    
    # 训练并观察
    trained_ai = train_ai_understanding()
    
    # 分析知识
    analyze_ai_knowledge(trained_ai)
    
    # 询问是否对战
    response = input("\n是否与AI对战？(y/n): ")
    if response.lower() == 'y':
        play_with_ai(trained_ai)
    
    print("\n实验完成！")