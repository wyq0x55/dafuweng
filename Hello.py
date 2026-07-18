import streamlit as st

st.set_page_config(
    page_title="幸福人生大富翁记录表",
    page_icon="🎉",  # 使用emoji
    layout="wide"
)

def student():
    if st.session_state.leanercount < 3:
        st.session_state.leaner = False
    else:
        st.session_state.leaner = True
    st.session_state.leanercount += 1

if 'leanercount' not in st.session_state:
    st.session_state.leanercount = 0
if 'determine' not in st.session_state:
    st.session_state.determine = False

st.markdown("# 🎯 幸福人生大富翁记分表")

with st.expander("游戏人生目标"):
    riches, fame, happy, sum_col = st.columns(4)
    numrich = riches.number_input("💰 财富", 0, 60_000, step=1000, disabled=st.session_state.determine)
    numfame = fame.number_input("👑 名誉", 0, 60, step=1, disabled=st.session_state.determine)
    numhappy = happy.number_input("😊 快乐", 0, 60, step=1, disabled=st.session_state.determine)
    sum_col.text_input("财富/1000+名誉+快乐", "= 60  ", disabled=True)
    
    if numrich/1000 + numfame + numhappy != 60:
        st.error("你输入的目标合计不为60分")
    else:
        st.toggle("确定", key="determine", disabled=st.session_state.determine)

leaner, Payscale, fame_col, happy_col = st.columns(4)

with leaner:
    st.write("#### 🎮 职业记录")
    st.toggle("⛵ 航海", key="navigation")
    st.toggle("🎬 电影", key="movie")
    st.toggle("⛏️ 采矿", key="mining")
    st.toggle("🏛️ 政治", key="politics")
    st.toggle("🌾 农业", key="agriculture")
    st.toggle("🚀 太空", key="space")
    st.toggle("💼 企业", key="enterprise")
    
    st.write("#### 📚 教育记录")
    st.toggle("⚖️ 法律", key="law")
    st.toggle("🏥 医学", key="medicine")
    st.toggle("🔧 工程", key="engineer")
    st.toggle("🔬 科学", key="science")
    st.toggle(f"👩‍🎓 普通 `{st.session_state.leanercount}`", on_change=student, key="leaner")

with Payscale:
    st.write("#### 💰 薪级记录")
    st.radio(
        "mony",
        ("💵 1,000",
         "💵 2,000",
         "💵 3,000",
         "💵 4,000",
         "💵 5,000",
         "💵 6,000",
         "💵 7,000",
         "💵 8,000",
         "💵 9,000",
         "💵 10,000",
         "💵 11,000",
         "💵 12,000",
         "💵 13,000",
         "💵 14,000",
         "💵 15,000",
         "💵 16,000",
         "💵 17,000",
         "💵 18,000",
         "💵 19,000",
         "💵 20,000",
         "💵 21,000"),
        index=1,
        label_visibility="collapsed",
        key="pay"
    )

with fame_col:
    st.write("#### 👑 名誉")
    st.number_input("👑 名誉", 0, step=1, key="nowcrown")

with happy_col:
    st.write("#### 😊 快乐")
    st.number_input("😊 快乐", 0, step=1, key="nowhappy")