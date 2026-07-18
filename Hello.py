import streamlit as st
import time
import random
import json
import os
from datetime import datetime

st.set_page_config(
    page_title="幸福人生大富翁记录表",
    page_icon="🎉",
    layout="wide"
)

# ============= 数据持久化工具 =============
def get_data_file_path():
    """获取数据文件路径"""
    return "game_data.json"

def load_game_data():
    """从文件加载游戏数据"""
    file_path = get_data_file_path()
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return None
    return None

def save_game_data(data):
    """保存游戏数据到文件"""
    file_path = get_data_file_path()
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except:
        return False

def init_session_from_file():
    """从文件初始化session state"""
    data = load_game_data()
    if data:
        # 恢复游戏状态
        st.session_state.players = data.get('players', {})
        st.session_state.game_started = data.get('game_started', False)
        st.session_state.game_ended = data.get('game_ended', False)
        st.session_state.winner = data.get('winner', None)
        st.session_state.game_code = data.get('game_code', None)
        st.session_state.game_master = data.get('game_master', None)
        st.session_state.all_players_ready = data.get('all_players_ready', False)
        st.session_state.created_at = data.get('created_at', None)
        st.session_state.last_updated = data.get('last_updated', None)
        return True
    return False

def sync_data_to_file():
    """同步数据到文件"""
    if 'players' in st.session_state:
        data = {
            'players': st.session_state.players,
            'game_started': st.session_state.get('game_started', False),
            'game_ended': st.session_state.get('game_ended', False),
            'winner': st.session_state.get('winner', None),
            'game_code': st.session_state.get('game_code', None),
            'game_master': st.session_state.get('game_master', None),
            'all_players_ready': st.session_state.get('all_players_ready', False),
            'created_at': st.session_state.get('created_at', datetime.now().isoformat()),
            'last_updated': datetime.now().isoformat()
        }
        return save_game_data(data)
    return False

# ============= 初始化 =============
# 初始化session state
if 'players' not in st.session_state:
    st.session_state.players = {}
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'game_ended' not in st.session_state:
    st.session_state.game_ended = False
if 'winner' not in st.session_state:
    st.session_state.winner = None
if 'player_id' not in st.session_state:
    st.session_state.player_id = None
if 'player_name' not in st.session_state:
    st.session_state.player_name = ""
if 'game_code' not in st.session_state:
    st.session_state.game_code = None
if 'current_turn' not in st.session_state:
    st.session_state.current_turn = 0
if 'all_players_ready' not in st.session_state:
    st.session_state.all_players_ready = False
if 'game_master' not in st.session_state:
    st.session_state.game_master = None
if 'target_set' not in st.session_state:
    st.session_state.target_set = False
if 'created_at' not in st.session_state:
    st.session_state.created_at = None
if 'last_updated' not in st.session_state:
    st.session_state.last_updated = None
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False

# 尝试加载已保存的数据
if not st.session_state.data_loaded:
    if init_session_from_file():
        st.session_state.data_loaded = True

# ============= 核心函数 =============
def generate_game_code():
    """生成游戏代码"""
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))

def create_game():
    """创建新游戏"""
    if not st.session_state.game_started:
        st.session_state.game_code = generate_game_code()
        st.session_state.game_master = st.session_state.player_id
        st.session_state.game_started = True
        st.session_state.created_at = datetime.now().isoformat()
        sync_data_to_file()
        st.success(f"🎮 游戏已创建！游戏代码：{st.session_state.game_code}")
        return True
    return False

def join_game(code):
    """加入已有游戏"""
    # 先尝试从文件加载最新数据
    init_session_from_file()
    
    if st.session_state.game_code is None:
        st.session_state.game_code = code.upper()
        st.session_state.game_started = True
        sync_data_to_file()
        st.success(f"✅ 成功加入游戏！游戏代码：{code}")
        return True
    elif st.session_state.game_code == code.upper():
        st.success(f"✅ 已加入游戏！游戏代码：{code}")
        return True
    else:
        st.error("❌ 游戏代码不匹配！")
        return False

def register_player():
    """注册玩家"""
    name = st.session_state.player_name_input.strip()
    if name and st.session_state.game_code:
        # 重新加载最新数据
        init_session_from_file()
        
        # 检查是否已有同名玩家
        for pid, pdata in st.session_state.players.items():
            if pdata['name'] == name:
                # 如果同名玩家已存在，让玩家重新加入，恢复所有数据
                st.session_state.player_id = pid
                st.session_state.player_name = name
                
                # 恢复玩家的目标设定状态
                if pdata.get('ready', False):
                    st.session_state.target_set = True
                    st.success(f"✅ 欢迎回来 {name}！你的目标已恢复")
                else:
                    st.session_state.target_set = False
                    st.info(f"👋 欢迎回来 {name}！请重新设定目标")
                
                sync_data_to_file()
                st.rerun()
                return
        
        # 如果是新玩家，生成唯一ID
        player_id = f"player_{int(time.time())}_{random.randint(1000, 9999)}"
        st.session_state.player_id = player_id
        st.session_state.players[player_id] = {
            'name': name,
            'target_wealth': 0,
            'target_fame': 0,
            'target_happy': 0,
            'current_wealth': 0,
            'current_fame': 0,
            'current_happy': 0,
            'pay_level': 0,
            'completed': False,
            'score': 0,
            'ready': False,
            'turn_completed': False,
            'navigation': False,
            'movie': False,
            'mining': False,
            'politics': False,
            'agriculture': False,
            'space': False,
            'enterprise': False,
            'law': False,
            'medicine': False,
            'engineer': False,
            'science': False,
            'leaner': False,
            'leanercount': 0,
            'joined_at': datetime.now().isoformat()
        }
        st.session_state.player_name = name
        st.session_state.target_set = False
        sync_data_to_file()
        st.success(f"✅ 欢迎 {name} 加入游戏！")
        st.rerun()

def set_targets():
    """保存玩家的目标设定"""
    player_id = st.session_state.player_id
    if player_id and player_id in st.session_state.players:
        # 重新加载最新数据
        init_session_from_file()
        
        player = st.session_state.players[player_id]
        wealth = st.session_state[f"target_wealth_{player_id}"]
        fame = st.session_state[f"target_fame_{player_id}"]
        happy = st.session_state[f"target_happy_{player_id}"]
        
        if wealth/1000 + fame + happy == 60:
            player['target_wealth'] = wealth
            player['target_fame'] = fame
            player['target_happy'] = happy
            player['ready'] = True
            st.session_state.target_set = True
            sync_data_to_file()
            st.success("✅ 目标设定完成！等待其他玩家...")
            return True
        else:
            st.error("❌ 目标合计必须为60分！")
            return False

def check_all_ready():
    """检查所有玩家是否已准备就绪"""
    # 重新加载最新数据
    init_session_from_file()
    
    if not st.session_state.players:
        return False
    
    # 检查是否所有玩家都已设定目标
    all_ready = all(player.get('ready', False) for player in st.session_state.players.values())
    if all_ready and len(st.session_state.players) >= 2:
        st.session_state.all_players_ready = True
        sync_data_to_file()
        return True
    return all_ready

def save_player_data():
    """保存当前玩家的游戏数据"""
    # 重新加载最新数据
    init_session_from_file()
    
    player_id = st.session_state.player_id
    if player_id and player_id in st.session_state.players:
        player = st.session_state.players[player_id]
        
        # 更新职业选择
        player['navigation'] = st.session_state.get(f"navigation_{player_id}", False)
        player['movie'] = st.session_state.get(f"movie_{player_id}", False)
        player['mining'] = st.session_state.get(f"mining_{player_id}", False)
        player['politics'] = st.session_state.get(f"politics_{player_id}", False)
        player['agriculture'] = st.session_state.get(f"agriculture_{player_id}", False)
        player['space'] = st.session_state.get(f"space_{player_id}", False)
        player['enterprise'] = st.session_state.get(f"enterprise_{player_id}", False)
        player['law'] = st.session_state.get(f"law_{player_id}", False)
        player['medicine'] = st.session_state.get(f"medicine_{player_id}", False)
        player['engineer'] = st.session_state.get(f"engineer_{player_id}", False)
        player['science'] = st.session_state.get(f"science_{player_id}", False)
        
        # 更新薪级
        pay = st.session_state.get(f"pay_{player_id}", "💵 1,000")
        player['pay_level'] = int(pay.replace("💵 ", "").replace(",", ""))
        player['current_wealth'] = player['pay_level'] * 1000
        
        # 更新名誉和快乐
        player['current_fame'] = st.session_state.get(f"nowcrown_{player_id}", 0)
        player['current_happy'] = st.session_state.get(f"nowhappy_{player_id}", 0)
        
        # 标记该玩家已更新数据
        player['turn_completed'] = True
        player['last_update'] = datetime.now().isoformat()
        
        sync_data_to_file()
        st.success(f"✅ 数据已保存！")
        return True
    return False

def end_game():
    """结束游戏并计算胜利者"""
    # 重新加载最新数据
    init_session_from_file()
    
    if not st.session_state.players:
        return
    
    # 计算每个玩家的得分
    for player in st.session_state.players.values():
        target_total = player['target_wealth']/1000 + player['target_fame'] + player['target_happy']
        current_total = player['current_wealth']/1000 + player['current_fame'] + player['current_happy']
        
        if target_total == 60:
            if (player['current_wealth']/1000 >= player['target_wealth']/1000 and
                player['current_fame'] >= player['target_fame'] and
                player['current_happy'] >= player['target_happy']):
                player['completed'] = True
                player['score'] = current_total
            else:
                # 计算完成度
                wealth_completion = min(1, player['current_wealth']/1000 / max(1, player['target_wealth']/1000))
                fame_completion = min(1, player['current_fame'] / max(1, player['target_fame']))
                happy_completion = min(1, player['current_happy'] / max(1, player['target_happy']))
                completion = (wealth_completion + fame_completion + happy_completion) / 3
                player['score'] = current_total * completion
    
    # 找出胜利者
    completed_players = [p for p in st.session_state.players.values() if p.get('completed', False)]
    if completed_players:
        completed_players.sort(key=lambda x: x['score'], reverse=True)
        st.session_state.winner = completed_players[0]
    else:
        sorted_players = sorted(st.session_state.players.values(), 
                               key=lambda x: x['score'], reverse=True)
        st.session_state.winner = sorted_players[0] if sorted_players else None
    
    st.session_state.game_ended = True
    sync_data_to_file()

def reset_game():
    """重置游戏"""
    # 删除数据文件
    file_path = get_data_file_path()
    if os.path.exists(file_path):
        os.remove(file_path)
    
    # 重置所有状态
    st.session_state.players = {}
    st.session_state.game_started = False
    st.session_state.game_ended = False
    st.session_state.winner = None
    st.session_state.player_id = None
    st.session_state.player_name = ""
    st.session_state.game_code = None
    st.session_state.current_turn = 0
    st.session_state.all_players_ready = False
    st.session_state.game_master = None
    st.session_state.target_set = False
    st.session_state.created_at = None
    st.session_state.last_updated = None
    st.session_state.data_loaded = False
    
    st.rerun()

def leave_game():
    """玩家退出游戏"""
    player_id = st.session_state.player_id
    if player_id and player_id in st.session_state.players:
        # 重新加载最新数据
        init_session_from_file()
        
        # 删除玩家
        del st.session_state.players[player_id]
        sync_data_to_file()
        
        # 重置当前玩家状态
        st.session_state.player_id = None
        st.session_state.player_name = ""
        st.session_state.target_set = False
        
        st.success("👋 已退出游戏")
        st.rerun()

# ============= 侧边栏 =============
with st.sidebar:
    st.header("🎮 游戏管理")
    
    if not st.session_state.player_id:
        # 未注册玩家
        st.subheader("📝 注册/加入游戏")
        
        st.text_input("输入你的名字", key="player_name_input", placeholder="例如：小明")
        
        # 显示当前游戏状态
        if st.session_state.game_code:
            st.info(f"🔑 当前游戏代码：{st.session_state.game_code}")
            st.write(f"👥 在线玩家：{len(st.session_state.players)} 人")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎯 创建新游戏", use_container_width=True, type="primary"):
                if st.session_state.player_name_input.strip():
                    if create_game():
                        register_player()
                        st.rerun()
                else:
                    st.warning("⚠️ 请输入你的名字！")
        
        with col2:
            game_code_input = st.text_input("游戏代码", key="game_code_input", 
                                           placeholder="输入代码", label_visibility="collapsed")
            if st.button("🔗 加入游戏", use_container_width=True):
                if st.session_state.player_name_input.strip() and game_code_input:
                    if join_game(game_code_input):
                        register_player()
                        st.rerun()
                else:
                    st.warning("⚠️ 请输入名字和游戏代码！")
        
        # 显示已有游戏信息
        if st.session_state.game_code and st.session_state.players:
            st.divider()
            st.subheader("👥 当前玩家")
            for pid, p in st.session_state.players.items():
                ready_status = "✅" if p.get('ready', False) else "⏳"
                st.write(f"   {ready_status} {p['name']} {'👑' if pid == st.session_state.game_master else ''}")
    
    else:
        # 已注册玩家
        player = st.session_state.players.get(st.session_state.player_id)
        if player:
            st.info(f"👤 当前玩家：{player['name']}")
            st.info(f"🔑 游戏代码：{st.session_state.game_code}")
            st.write(f"👥 在线玩家：{len(st.session_state.players)} 人")
            
            # 显示所有玩家状态
            st.divider()
            st.subheader("📊 玩家状态")
            for pid, p in st.session_state.players.items():
                status = "✅" if p.get('ready', False) else "⏳"
                if pid == st.session_state.player_id:
                    st.write(f"📍 **{status} {p['name']}** (你)")
                else:
                    st.write(f"   {status} {p['name']}")
            
            # 显示玩家目标状态
            if player.get('ready', False):
                st.success("🎯 目标已设定")
                st.write(f"💰 财富目标：{player.get('target_wealth', 0):,}")
                st.write(f"👑 名誉目标：{player.get('target_fame', 0)}")
                st.write(f"😊 快乐目标：{player.get('target_happy', 0)}")
            
            # 显示游戏创建时间
            if st.session_state.created_at:
                st.caption(f"📅 创建于：{st.session_state.created_at[:10]}")
            
            # 管理员功能
            if st.session_state.game_master == st.session_state.player_id:
                st.divider()
                st.subheader("⚙️ 管理员功能")
                
                if not st.session_state.game_ended:
                    if st.button("🏆 结束游戏", use_container_width=True, type="primary"):
                        end_game()
                        st.rerun()
                
                if st.button("🔄 重置游戏", use_container_width=True):
                    reset_game()
            
            # 退出游戏
            st.divider()
            if st.button("🚪 退出游戏", use_container_width=True):
                leave_game()

# ============= 主页面 =============
# 自动同步数据
if st.session_state.player_id and not st.session_state.game_ended:
    # 检查是否有新玩家加入
    old_players_count = len(st.session_state.players)
    init_session_from_file()
    new_players_count = len(st.session_state.players)
    
    # 如果有新玩家加入，刷新显示
    if new_players_count > old_players_count:
        st.rerun()
    
    # 检查所有玩家是否准备就绪
    check_all_ready()

if not st.session_state.player_id:
    # 未登录状态
    st.header("🎯 欢迎来到幸福人生大富翁！")
    
    # 显示已有游戏信息
    if st.session_state.game_code and st.session_state.players:
        st.info(f"🔑 当前游戏进行中！游戏代码：{st.session_state.game_code}")
        st.write(f"👥 已有 {len(st.session_state.players)} 名玩家参与")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("👥 玩家数量", len(st.session_state.players))
        with col2:
            ready_count = sum(1 for p in st.session_state.players.values() if p.get('ready', False))
            st.metric("✅ 已准备", ready_count)
        with col3:
            st.metric("🎯 状态", "进行中" if st.session_state.game_started else "等待中")
        
        # 显示已设定目标的玩家
        if ready_count > 0:
            st.subheader("📋 已设定目标的玩家")
            for pid, p in st.session_state.players.items():
                if p.get('ready', False):
                    st.write(f"   ✅ {p['name']}")
    
    st.markdown("""
    ### 📱 多人联机游戏说明
    
    1. **创建游戏**：点击「创建新游戏」成为房主
    2. **加入游戏**：输入房主的6位游戏代码加入
    3. **设定目标**：每位玩家设定60分的个人目标
    4. **游戏进行**：所有玩家各自记录自己的数值
    5. **决出胜负**：房主可结束游戏查看谁赢了
    
    ### 🎯 目标设定规则
    - 💰 财富：0-60,000（除以1000计分）
    - 👑 名誉：0-60分  
    - 😊 快乐：0-60分
    - **三项总和必须等于60**
    
    ### 🏆 胜利条件
    - 完成个人60分目标
    - 得分最高的玩家获胜
    """)

elif st.session_state.game_ended:
    # 游戏结束
    st.balloons()
    st.header("🏆 游戏结束！")
    
    if st.session_state.winner:
        st.success(f"### 🎉 恭喜 {st.session_state.winner['name']} 获得胜利！")
        
        # 显示排行榜
        st.subheader("📊 最终排行榜")
        
        sorted_players = sorted(st.session_state.players.values(), 
                               key=lambda x: x.get('score', 0), reverse=True)
        for i, player in enumerate(sorted_players, 1):
            col1, col2, col3, col4 = st.columns([1, 3, 2, 2])
            with col1:
                medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
                st.write(medal)
            with col2:
                st.write(f"**{player['name']}**")
            with col3:
                st.write(f"得分：{player.get('score', 0):.1f}")
            with col4:
                st.write("✅ 完成目标" if player.get('completed', False) else "⏳ 未完成")
        
        # 显示详细数据
        st.divider()
        st.subheader("📋 详细数据")
        for player in sorted_players:
            with st.expander(f"👤 {player['name']}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("💰 财富", f"{player.get('current_wealth', 0):,}", 
                             f"目标：{player.get('target_wealth', 0):,}")
                with col2:
                    st.metric("👑 名誉", player.get('current_fame', 0), 
                             f"目标：{player.get('target_fame', 0)}")
                with col3:
                    st.metric("😊 快乐", player.get('current_happy', 0), 
                             f"目标：{player.get('target_happy', 0)}")
    
    if st.button("🔄 重新开始游戏", use_container_width=True):
        reset_game()

elif not st.session_state.target_set:
    # 目标设定阶段
    st.header(f"🎯 设定你的目标 - {st.session_state.player_name}")
    
    # 检查是否已有目标（重新进入的情况）
    player = st.session_state.players.get(st.session_state.player_id, {})
    if player.get('ready', False):
        st.info("📋 你已设定目标，正在等待其他玩家...")
        if st.button("查看我的目标", use_container_width=True):
            st.write(f"💰 财富目标：{player.get('target_wealth', 0):,}")
            st.write(f"👑 名誉目标：{player.get('target_fame', 0)}")
            st.write(f"😊 快乐目标：{player.get('target_happy', 0)}")
        
        # 如果所有玩家都已准备，自动进入游戏
        check_all_ready()
        if st.session_state.all_players_ready:
            st.rerun()
    else:
        st.info("请设定你的60分目标（财富/1000 + 名誉 + 快乐 = 60）")
        
        player_id = st.session_state.player_id
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            wealth = st.number_input("💰 财富", 0, 60_000, step=1000, 
                                    key=f"target_wealth_{player_id}")
        with col2:
            fame = st.number_input("👑 名誉", 0, 60, step=1,
                                  key=f"target_fame_{player_id}")
        with col3:
            happy = st.number_input("😊 快乐", 0, 60, step=1,
                                   key=f"target_happy_{player_id}")
        with col4:
            total = wealth/1000 + fame + happy
            st.text_input("合计", f"{total:.0f}/60", disabled=True)
            if total == 60:
                st.success("✅ 完美！")
            else:
                st.error(f"需要 {60 - total:.0f} 分")
        
        if st.button("✅ 确认目标", use_container_width=True, type="primary"):
            if set_targets():
                st.rerun()
    
    # 显示等待状态
    if st.session_state.players:
        st.divider()
        st.subheader("👥 玩家进度")
        ready_count = sum(1 for p in st.session_state.players.values() if p.get('ready', False))
        total_count = len(st.session_state.players)
        st.progress(ready_count / total_count if total_count > 0 else 0)
        st.write(f"已准备：{ready_count}/{total_count} 人")
        
        # 显示已准备的玩家列表
        if ready_count > 0:
            st.write("✅ 已准备的玩家：")
            for pid, p in st.session_state.players.items():
                if p.get('ready', False):
                    st.write(f"   • {p['name']}")
        
        if ready_count >= 2 and ready_count == total_count:
            st.info("🎮 所有玩家已准备就绪！即将开始游戏...")
            time.sleep(2)
            st.session_state.all_players_ready = True
            sync_data_to_file()
            st.rerun()

elif st.session_state.all_players_ready:
    # 游戏进行中
    player_id = st.session_state.player_id
    player = st.session_state.players.get(player_id)
    
    if not player:
        st.warning("⚠️ 玩家数据丢失，请重新加入游戏")
        if st.button("重新加入"):
            leave_game()
        st.stop()
    
    st.header(f"🎮 游戏进行中 - {player['name']}")
    
    # 显示所有玩家的简要状态
    st.subheader("📊 所有玩家进度")
    cols = st.columns(min(len(st.session_state.players), 4))
    for i, (pid, p) in enumerate(st.session_state.players.items()):
        with cols[i % len(cols)]:
            current_total = p.get('current_wealth', 0)/1000 + p.get('current_fame', 0) + p.get('current_happy', 0)
            target_total = p.get('target_wealth', 0)/1000 + p.get('target_fame', 0) + p.get('target_happy', 0)
            st.metric(
                p['name'],
                f"🏆 {current_total:.0f}/{target_total:.0f}",
                delta="✅ 完成" if p.get('completed', False) else "⏳ 进行中"
            )
    
    st.divider()
    
    # 当前玩家的游戏面板
    with st.expander("📝 记录你的数据", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("#### 🎮 职业记录")
            st.toggle("⛵ 航海", key=f"navigation_{player_id}", 
                     value=player.get('navigation', False))
            st.toggle("🎬 电影", key=f"movie_{player_id}",
                     value=player.get('movie', False))
            st.toggle("⛏️ 采矿", key=f"mining_{player_id}",
                     value=player.get('mining', False))
            st.toggle("🏛️ 政治", key=f"politics_{player_id}",
                     value=player.get('politics', False))
            st.toggle("🌾 农业", key=f"agriculture_{player_id}",
                     value=player.get('agriculture', False))
            st.toggle("🚀 太空", key=f"space_{player_id}",
                     value=player.get('space', False))
            st.toggle("💼 企业", key=f"enterprise_{player_id}",
                     value=player.get('enterprise', False))
            
            st.write("#### 📚 教育记录")
            st.toggle("⚖️ 法律", key=f"law_{player_id}",
                     value=player.get('law', False))
            st.toggle("🏥 医学", key=f"medicine_{player_id}",
                     value=player.get('medicine', False))
            st.toggle("🔧 工程", key=f"engineer_{player_id}",
                     value=player.get('engineer', False))
            st.toggle("🔬 科学", key=f"science_{player_id}",
                     value=player.get('science', False))
            
            # 教育计数
            if 'leaner_count' not in st.session_state:
                st.session_state.leaner_count = player.get('leanercount', 0)
            st.toggle(f"👩‍🎓 普通 {st.session_state.leaner_count}", 
                     key=f"leaner_{player_id}",
                     value=player.get('leaner', False))
        
        with col2:
            st.write("#### 💰 薪级记录")
            # 获取当前薪级索引
            current_pay = player.get('pay_level', 0)
            pay_options = ["💵 1,000", "💵 2,000", "💵 3,000", "💵 4,000", "💵 5,000",
                          "💵 6,000", "💵 7,000", "💵 8,000", "💵 9,000", "💵 10,000",
                          "💵 11,000", "💵 12,000", "💵 13,000", "💵 14,000", "💵 15,000",
                          "💵 16,000", "💵 17,000", "💵 18,000", "💵 19,000", "💵 20,000",
                          "💵 21,000"]
            pay_index = min(current_pay // 1000 - 1, len(pay_options) - 1)
            pay_index = max(0, pay_index)
            
            pay_level = st.radio(
                "薪级",
                pay_options,
                index=pay_index,
                label_visibility="collapsed",
                key=f"pay_{player_id}"
            )
        
        with col3:
            st.write("#### 🎯 当前数值")
            current_fame = st.number_input("👑 名誉", 0, step=1,
                                         key=f"nowcrown_{player_id}",
                                         value=player.get('current_fame', 0))
            current_happy = st.number_input("😊 快乐", 0, step=1,
                                          key=f"nowhappy_{player_id}",
                                          value=player.get('current_happy', 0))
            
            # 显示目标
            st.write("---")
            st.write("#### 🎯 你的目标")
            st.write(f"💰 财富：{player.get('target_wealth', 0):,}")
            st.write(f"👑 名誉：{player.get('target_fame', 0)}")
            st.write(f"😊 快乐：{player.get('target_happy', 0)}")
            
            # 显示当前完成度
            current_total = player.get('current_wealth', 0)/1000 + player.get('current_fame', 0) + player.get('current_happy', 0)
            target_total = player.get('target_wealth', 0)/1000 + player.get('target_fame', 0) + player.get('target_happy', 0)
            if target_total > 0:
                completion = min(100, (current_total / target_total) * 100)
                st.progress(completion / 100)
                st.caption(f"完成度：{completion:.1f}%")
    
    # 保存按钮
    if st.button("💾 保存我的数据", use_container_width=True, type="primary"):
        if save_player_data():
            st.rerun()
    
    # 显示当前状态
    current_total = player.get('current_wealth', 0)/1000 + player.get('current_fame', 0) + player.get('current_happy', 0)
    target_total = player.get('target_wealth', 0)/1000 + player.get('target_fame', 0) + player.get('target_happy', 0)
    st.info(f"📊 当前总分：{current_total:.0f}/{target_total:.0f}")
    
    # 检查是否完成目标
    if current_total >= target_total and not player.get('completed', False):
        st.success("🎉 恭喜你完成目标！继续努力争取更高分数！")
    
    # 显示游戏信息
    st.divider()
    st.caption(f"📅 游戏创建：{st.session_state.created_at[:16] if st.session_state.created_at else '未知'}")

# 自动刷新数据（每10秒检查一次）
if st.session_state.player_id and not st.session_state.game_ended:
    # 使用st.empty来创建自动刷新效果
    refresh_placeholder = st.empty()
    with refresh_placeholder:
        st.caption("🔄 数据自动同步中...")