# ai_learner.py - AI学习器
import random
from collections import defaultdict

class TryLearnerAI:
    """通过尝试学习的AI"""
    
    def __init__(self, player_id=1, exploration=0.3, learning=0.1):
        self.player_id = player_id
        self.exploration_rate = exploration
        self.learning_rate = learning
        
        # Q表
        self.Q = defaultdict(lambda: defaultdict(float))
        self.current_episode = []
        
        # 统计
        self.stats = {
            "games": 0,
            "wins": 0,
            "losses": 0,
            "draws": 0,
            "states_explored": 0
        }
    
    def choose_action(self, state, valid_moves, greedy=False):
        """选择动作"""
        # 探索
        if not greedy and random.random() < self.exploration_rate:
            return random.choice(valid_moves)
        
        # 利用
        if state not in self.Q:
            return random.choice(valid_moves)
        
        # 选择最佳动作
        best_action = None
        best_value = -9999
        for action in valid_moves:
            if action in self.Q[state]:
                if self.Q[state][action] > best_value:
                    best_value = self.Q[state][action]
                    best_action = action
        
        return best_action if best_action is not None else random.choice(valid_moves)
    
    def record_experience(self, state, action, reward, next_state, done):
        """记录经验"""
        self.current_episode.append({
            "state": state,
            "action": action,
            "reward": reward,
            "next_state": next_state,
            "done": done
        })
    
    def learn_from_episode(self):
        """从一局游戏中学习"""
        if not self.current_episode:
            return
        
        # 从最后一步开始学习
        reversed_episode = list(reversed(self.current_episode))
        cumulative_reward = 0
        
        for exp in reversed_episode:
            state = exp["state"]
            action = exp["action"]
            reward = exp["reward"]
            
            cumulative_reward = reward + 0.9 * cumulative_reward
            
            # 更新Q值
            old_value = self.Q[state][action]
            
            if state not in self.Q:
                self.stats["states_explored"] += 1
            
            self.Q[state][action] = old_value + self.learning_rate * (cumulative_reward - old_value)
        
        self.current_episode = []
    
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
        
        print(f"=== AI统计 ===")
        print(f"对局数: {total}")
        print(f"胜: {self.stats['wins']} ({self.stats['wins']/total*100:.1f}%)")
        print(f"负: {self.stats['losses']} ({self.stats['losses']/total*100:.1f}%)")
        print(f"平: {self.stats['draws']} ({self.stats['draws']/total*100:.1f}%)")
        print(f"探索状态数: {self.stats['states_explored']}")