# diagnose_ai.py
from tic_tac_toe import TicTacToe
import random

def diagnose_ai_understanding(ai):
    """诊断AI的理解深度"""
    
    print("=== AI理解深度诊断 ===")
    
    game = TicTacToe()
    
    # 测试1：规则理解
    print("\n1. 规则理解测试:")
    game.reset()
    
    # 尝试非法走法
    game.step(4)  # X下中心
    game.step(4)  # O尝试下同一个位置（应该无效）
    
    # 但AI应该不会选择非法走法，因为它从经验中学到了
    
    # 测试2：策略一致性
    print("\n2. 策略一致性测试:")
    consistency_tests = 10
    same_choices = 0
    
    for _ in range(consistency_tests):
        game.reset()
        state = game._get_state()
        valid_moves = game.get_valid_moves()
        
        # AI选择开局
        choice1 = ai.choose_action(state, valid_moves, greedy=True)
        
        # 重置再选一次
        choice2 = ai.choose_action(state, valid_moves, greedy=True)
        
        if choice1 == choice2:
            same_choices += 1
    
    print(f"  相同选择率: {same_choices/consistency_tests*100:.1f}%")
    
    # 测试3：反事实思考能力
    print("\n3. 反事实思考测试:")
    
    # 创建一个特定局面
    test_state = "120210000"  # X差一步赢
    if test_state in ai.q_table:
        # AI会怎么选？
        actions = ai.q_table[test_state]
        if actions:
            ai_choice = max(actions.items(), key=lambda x: x[1])[0]
            correct_choice = 8  # 应该下在8完成三连
            
            print(f"  局面: X差一步赢")
            print(f"  AI选择: 位置{ai_choice}")
            print(f"  正确选择: 位置{correct_choice}")
            
            if ai_choice == correct_choice:
                print("  ✅ AI能识别必胜机会")
            else:
                print(f"  ❌ AI错过了必胜机会")
    
    # 测试4：创新性测试
    print("\n4. 创新性测试:")
    
    # 创建一个不常见的局面
    unusual_state = "100002010"
    if unusual_state in ai.q_table:
        # AI见过这个局面吗？
        print(f"  AI见过这个不常见局面")
        actions = ai.q_table[unusual_state]
        if len(actions) > 1:
            print(f"  AI有{len(actions)}种应对策略")
        else:
            print(f"  AI只有1种固定应对")
    else:
        print(f"  AI没见过这个局面，将随机应对")
    
    # 测试5：解释能力模拟
    print("\n5. 解释能力模拟:")
    
    # 让AI"解释"它的选择
    game.reset()
    state = game._get_state()
    valid_moves = game.get_valid_moves()
    choice = ai.choose_action(state, valid_moves, greedy=True)
    
    print(f"  初始局面，AI选择位置{choice}")
    
    if state in ai.q_table and choice in ai.q_table[state]:
        value = ai.q_table[state][choice]
        
        # 模拟"解释"
        if value > 0.5:
            print(f"  AI的'理由': 这个位置有高胜率({value:.3f})")
        elif value > 0:
            print(f"  AI的'理由': 这个位置还行({value:.3f})")
        else:
            print(f"  AI的'理由': 其他位置更差({value:.3f})")
    
    # 测试6：学习速度测试
    print("\n6. 学习速度分析:")
    print(f"  AI记忆了 {len(ai.q_table)} 个状态")
    print(f"  经过 {ai.stats['games']} 局训练")
    
    efficiency = len(ai.q_table) / ai.stats['games'] if ai.stats['games'] > 0 else 0
    print(f"  学习效率: {efficiency:.3f} 状态/局")
    
    # 评估理解深度
    print("\n=== 理解深度评估 ===")
    
    depth_score = 0
    max_score = 6
    
    # 评分标准
    if same_choices/consistency_tests > 0.8:
        depth_score += 1
        print("✅ 策略一致性强")
    
    if 'test_state' in locals() and 'ai_choice' in locals() and ai_choice == correct_choice:
        depth_score += 1
        print("✅ 能识别必胜机会")
    
    if efficiency > 0.3:
        depth_score += 1
        print("✅ 学习效率高")
    
    if len(ai.q_table) > 1500:
        depth_score += 1
        print("✅ 知识覆盖面广")
    
    # 最终评估
    print(f"\n理解深度评分: {depth_score}/{max_score}")
    
    if depth_score >= 5:
        print("理解深度: 高级 (接近人类水平)")
    elif depth_score >= 3:
        print("理解深度: 中级 (有系统策略)")
    else:
        print("理解深度: 初级 (基本规则掌握)")

def explore_ai_subjectivity(ai):
    """探索AI的'主观性'"""
    
    print("\n" + "="*60)
    print("=== 探索AI的主观性 ===")
    
    # 检查AI是否有独特的"风格"
    game = TicTacToe()
    
    # 统计AI的开局偏好
    opening_counts = {i: 0 for i in range(9)}
    tests = 100
    
    for _ in range(tests):
        game.reset()
        state = game._get_state()
        valid_moves = game.get_valid_moves()
        choice = ai.choose_action(state, valid_moves, greedy=True)
        opening_counts[choice] += 1
    
    print("AI的开局偏好分布:")
    for position in range(9):
        if opening_counts[position] > 0:
            percentage = opening_counts[position] / tests * 100
            row, col = divmod(position, 3)
            print(f"  位置{position}({row},{col}): {percentage:.1f}%")
    
    # 检查是否形成了固定模式
    top_position = max(opening_counts.items(), key=lambda x: x[1])[0]
    top_percentage = opening_counts[top_position] / tests * 100
    
    if top_percentage > 50:
        print(f"\n✅ AI有明显的个人风格：偏好位置{top_position}")
        row, col = divmod(top_position, 3)
        print(f"   这形成了独特的'签名式开局'")
    elif top_percentage > 30:
        print(f"\n✓ AI有一定偏好：常选位置{top_position}")
    else:
        print(f"\n⚠ AI没有明显偏好，策略多样")
    
    # 检查AI的"价值观"
    print("\nAI的'价值观'分析:")
    
    # 统计不同动作的价值分布
    all_values = []
    for state in ai.q_table:
        for action in ai.q_table[state]:
            all_values.append(ai.q_table[state][action])
    
    if all_values:
        avg_value = sum(all_values) / len(all_values)
        max_value = max(all_values)
        min_value = min(all_values)
        
        print(f"  平均动作价值: {avg_value:.3f}")
        print(f"  最高价值动作: {max_value:.3f}")
        print(f"  最低价值动作: {min_value:.3f}")
        
        # 计算"风险偏好"
        positive_values = [v for v in all_values if v > 0]
        risk_ratio = len(positive_values) / len(all_values) if all_values else 0
        
        print(f"  积极动作比例: {risk_ratio*100:.1f}%")
        
        if risk_ratio > 0.7:
            print("  AI倾向保守策略")
        elif risk_ratio > 0.3:
            print("  AI策略平衡")
        else:
            print("  AI倾向冒险策略")

if __name__ == "__main__":
    # 这里需要您的AI实例
    # 暂时用模拟的
    print("注意：需要传入训练好的AI实例")
    print("请先训练AI，然后将实例传入此函数")