import streamlit as st

st.set_page_config(
    page_title="幸福人生大富翁记录表",
    page_icon="🎉",
    layout="wide"
)

# 初始化session state
if 'players' not in st.session_state:
    st.session_state.players = []  # 存储所有玩家数据
if 'current_player' not in st.session_state:
    st.session_state.current_player = None
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'game_ended' not in st.session_state:
    st.session_state.game_ended = False
if 'winner' not in st.session_state:
    st.session_state.winner = None
if 'player_count' not in st.session_state:
    st.session_state.player_count = 0

def student():
    if st.session_state.leanercount < 3:
        st.session_state.leaner = False
    else:
        st.session_state.leaner = True
    st.session_state.leanercount += 1

def add_player():
    """添加新玩家"""
    player_name = st.session_state.new_player_name.strip()
    if player_name and player_name not in [p['name'] for p in st.session_state.players]:
        st.session_state.players.append({
            'name': player_name,
            'target_wealth': 0,
            'target_fame': 0,
            'target_happy': 0,
            'current_wealth': 0,
            'current_fame': 0,
            'current_happy': 0,
            'pay_level': 0,
            'completed': False,
            'score': 0
        })
        st.session_state.new_player_name = ""
        st.success(f"✅ 玩家 {player_name} 已加入！")
    elif player_name in [p['name'] for p in st.session_state.players]:
        st.warning("⚠️ 该玩家已存在！")

def start_game():
    """开始游戏"""
    if len(st.session_state.players) >= 2:
        st.session_state.game_started = True
        st.session_state.current_player = 0
        st.success("🎮 游戏开始！")
    else:
        st.warning("⚠️ 至少需要2名玩家才能开始游戏！")

def end_game():
    """结束游戏并计算胜利者"""
    if st.session_state.game_started and not st.session_state.game_ended:
        # 计算每个玩家的得分
        for player in st.session_state.players:
            # 得分计算：目标达成度 + 当前数值
            target_total = player['target_wealth']/1000 + player['target_fame'] + player['target_happy']
            current_total = player['current_wealth']/1000 + player['current_fame'] + player['current_happy']
            
            # 如果目标总和为60，且当前数值达到目标，则完成
            if target_total == 60:
                if (player['current_wealth']/1000 >= player['target_wealth']/1000 and
                    player['current_fame'] >= player['target_fame'] and
                    player['current_happy'] >= player['target_happy']):
                    player['completed'] = True
                    player['score'] = current_total
                else:
                    # 未完成目标的得分
                    completion = min(1, (player['current_wealth']/1000 / max(1, player['target_wealth']/1000) +
                                        player['current_fame'] / max(1, player['target_fame']) +
                                        player['current_happy'] / max(1, player['target_happy'])) / 3)
                    player['score'] = current_total * completion
        
        # 找出胜利者
        completed_players = [p for p in st.session_state.players if p['completed']]
        if completed_players:
            # 按得分排序
            completed_players.sort(key=lambda x: x['score'], reverse=True)
            st.session_state.winner = completed_players[0]
        else:
            # 如果没有完成者，选择得分最高的
            st.session_state.players.sort(key=lambda x: x['score'], reverse=True)
            st.session_state.winner = st.session_state.players[0]
        
        st.session_state.game_ended = True

def reset_game():
    """重置游戏"""
    st.session_state.players = []
    st.session_state.current_player = None
    st.session_state.game_started = False
    st.session_state.game_ended = False
    st.session_state.winner = None
    st.session_state.leanercount = 0

# 侧边栏：玩家管理
with st.sidebar:
    st.header("👥 玩家管理")
    
    if not st.session_state.game_started:
        # 添加玩家
        col1, col2 = st.columns([3, 1])
        with col1:
            st.text_input("输入玩家名称", key="new_player_name", placeholder="例如：小明")
        with col2:
            st.button("➕ 添加", on_click=add_player, use_container_width=True)
        
        # 显示已添加的玩家
        if st.session_state.players:
            st.subheader(f"已加入玩家 ({len(st.session_state.players)})")
            for i, player in enumerate(st.session_state.players):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"{i+1}. {player['name']}")
                with col2:
                    if st.button("❌", key=f"remove_{i}"):
                        st.session_state.players.pop(i)
                        st.rerun()
        
        # 开始游戏按钮
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎮 开始游戏", use_container_width=True, type="primary"):
                start_game()
                st.rerun()
    else:
        # 游戏进行中的控制
        st.info(f"🎯 当前玩家: {st.session_state.players[st.session_state.current_player]['name']}")
        st.write(f"👥 总玩家数: {len(st.session_state.players)}")
        
        if not st.session_state.game_ended:
            if st.button("🏆 结束游戏并判定胜负", use_container_width=True, type="primary"):
                end_game()
                st.rerun()
        else:
            if st.button("🔄 重新开始", use_container_width=True):
                reset_game()
                st.rerun()

# 主页面
if st.session_state.game_started and not st.session_state.game_ended:
    # 游戏进行中
    st.header(f"🎯 当前玩家：{st.session_state.players[st.session_state.current_player]['name']}")
    
    # 显示所有玩家进度
    st.subheader("📊 玩家进度")
    progress_cols = st.columns(min(len(st.session_state.players), 4))
    for i, player in enumerate(st.session_state.players):
        with progress_cols[i % len(progress_cols)]:
            st.metric(
                player['name'],
                f"🏆 {player['current_wealth']/1000 + player['current_fame'] + player['current_happy']:.0f}",
                delta="✅" if player['completed'] else "⏳"
            )
    
    st.divider()
    
    # 当前玩家的游戏面板
    with st.expander("游戏人生目标", expanded=True):
        riches, fame, happy, sum_col = st.columns(4)
        numrich = riches.number_input("💰 财富目标", 0, 60_000, step=1000, 
                                    key=f"target_wealth_{st.session_state.current_player}")
        numfame = fame.number_input("👑 名誉目标", 0, 60, step=1,
                                  key=f"target_fame_{st.session_state.current_player}")
        numhappy = happy.number_input("😊 快乐目标", 0, 60, step=1,
                                    key=f"target_happy_{st.session_state.current_player}")
        sum_col.text_input("财富/1000+名誉+快乐", "= 60", disabled=True)
        
        # 保存目标
        if numrich/1000 + numfame + numhappy == 60:
            player = st.session_state.players[st.session_state.current_player]
            player['target_wealth'] = numrich
            player['target_fame'] = numfame
            player['target_happy'] = numhappy
            st.success("✅ 目标设定完成！")
            
            # 下一个玩家按钮
            if st.button("➡️ 下一位玩家", use_container_width=True):
                if st.session_state.current_player < len(st.session_state.players) - 1:
                    st.session_state.current_player += 1
                else:
                    st.info("🎯 所有玩家已设定目标，开始游戏！")
                st.rerun()
        else:
            st.error("❌ 目标合计必须为60分！")
    
    # 职业和数值记录
    st.divider()
    st.subheader("🎮 游戏记录")
    
    player = st.session_state.players[st.session_state.current_player]
    
    leaner, Payscale, fame_col, happy_col = st.columns(4)
    
    with leaner:
        st.write("#### 🎮 职业记录")
        st.toggle("⛵ 航海", key=f"navigation_{st.session_state.current_player}")
        st.toggle("🎬 电影", key=f"movie_{st.session_state.current_player}")
        st.toggle("⛏️ 采矿", key=f"mining_{st.session_state.current_player}")
        st.toggle("🏛️ 政治", key=f"politics_{st.session_state.current_player}")
        st.toggle("🌾 农业", key=f"agriculture_{st.session_state.current_player}")
        st.toggle("🚀 太空", key=f"space_{st.session_state.current_player}")
        st.toggle("💼 企业", key=f"enterprise_{st.session_state.current_player}")
        
        st.write("#### 📚 教育记录")
        st.toggle("⚖️ 法律", key=f"law_{st.session_state.current_player}")
        st.toggle("🏥 医学", key=f"medicine_{st.session_state.current_player}")
        st.toggle("🔧 工程", key=f"engineer_{st.session_state.current_player}")
        st.toggle("🔬 科学", key=f"science_{st.session_state.current_player}")
        st.toggle(f"👩‍🎓 普通 `{st.session_state.leanercount}`", on_change=student, key=f"leaner_{st.session_state.current_player}")
    
    with Payscale:
        st.write("#### 💰 薪级记录")
        pay_level = st.radio(
            "薪级",
            ("💵 1,000", "💵 2,000", "💵 3,000", "💵 4,000", "💵 5,000",
             "💵 6,000", "💵 7,000", "💵 8,000", "💵 9,000", "💵 10,000",
             "💵 11,000", "💵 12,000", "💵 13,000", "💵 14,000", "💵 15,000",
             "💵 16,000", "💵 17,000", "💵 18,000", "💵 19,000", "💵 20,000",
             "💵 21,000"),
            index=1,
            label_visibility="collapsed",
            key=f"pay_{st.session_state.current_player}"
        )
        # 提取数值
        player['pay_level'] = int(pay_level.replace("💵 ", "").replace(",", ""))
    
    with fame_col:
        st.write("#### 👑 名誉")
        current_fame = st.number_input("👑 当前名誉", 0, step=1, 
                                     key=f"nowcrown_{st.session_state.current_player}")
        player['current_fame'] = current_fame
    
    with happy_col:
        st.write("#### 😊 快乐")
        current_happy = st.number_input("😊 当前快乐", 0, step=1,
                                      key=f"nowhappy_{st.session_state.current_player}")
        player['current_happy'] = current_happy
    
    # 更新财富值（从薪级自动计算）
    player['current_wealth'] = player['pay_level'] * 1000
    
    # 保存当前玩家数据
    if st.button("💾 保存当前玩家数据", use_container_width=True):
        st.success(f"✅ {player['name']} 的数据已保存！")

elif st.session_state.game_ended:
    # 显示游戏结果
    st.balloons()
    
    st.header("🏆 游戏结束！")
    
    if st.session_state.winner:
        st.success(f"### 🎉 恭喜 {st.session_state.winner['name']} 获得胜利！")
        
        # 显示排行榜
        st.subheader("📊 最终排行榜")
        
        sorted_players = sorted(st.session_state.players, key=lambda x: x['score'], reverse=True)
        for i, player in enumerate(sorted_players, 1):
            col1, col2, col3, col4 = st.columns([2, 3, 2, 2])
            with col1:
                medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
                st.write(f"{medal}")
            with col2:
                st.write(f"**{player['name']}**")
            with col3:
                st.write(f"得分: {player['score']:.1f}")
            with col4:
                if player['completed']:
                    st.write("✅ 完成目标")
                else:
                    st.write("⏳ 未完成")
        
        # 显示详细的玩家数据
        st.divider()
        st.subheader("📋 详细数据")
        for player in st.session_state.players:
            with st.expander(f"👤 {player['name']}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("💰 财富", f"{player['current_wealth']:,}", f"目标: {player['target_wealth']:,}")
                with col2:
                    st.metric("👑 名誉", player['current_fame'], f"目标: {player['target_fame']}")
                with col3:
                    st.metric("😊 快乐", player['current_happy'], f"目标: {player['target_happy']}")
    
    if st.button("🔄 重新开始游戏", use_container_width=True):
        reset_game()
        st.rerun()

else:
    # 游戏未开始状态
    st.header("🎯 欢迎来到幸福人生大富翁！")
    st.info("👈 请在左侧添加至少2名玩家，然后点击「开始游戏」")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        #### 📝 游戏规则
        1. 添加至少2名玩家
        2. 每位玩家设定60分的目标（财富/1000+名誉+快乐）
        3. 通过职业和教育积累分数
        4. 最先完成目标且得分最高的玩家获胜！
        """)
    with col2:
        st.markdown("""
        #### 🎯 目标设定
        - 💰 财富：0-60,000（除以1000计分）
        - 👑 名誉：0-60分
        - 😊 快乐：0-60分
        - 三项总和必须等于60
        """)
    with col3:
        st.markdown("""
        #### 🏆 胜利条件
        - 完成个人设定的60分目标
        - 得分最高的玩家获胜
        - 支持多人在线记录
        - 实时查看所有玩家进度
        """)