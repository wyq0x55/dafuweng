import streamlit as st
st.set_page_config(page_title="幸福人生大富翁记录表",page_icon=":tada:",layout="wide")
def student():
    if st.session_state.leanercount < 3:
        st.session_state.leaner = False
    else:
        st.session_state.leaner = True
    st.session_state.leanercount += 1

if not 'leanercount' in st.session_state:
    st.session_state.leanercount = 0
if not 'determine' in st.session_state:
    st.session_state.determine = False
""" # 幸福人生大富翁记分表"""
with st.expander("游戏人生目标"):
    riches,fame,happy,sum = st.columns(4)
    numrich=riches.number_input(":moneybag:财富",0,60_000,step =1000,disabled=st.session_state.determine)
    numfame=fame.number_input(":crown:名誉",0,60,step =1,disabled=st.session_state.determine)
    numhappy=happy.number_input(":smile:快乐",0,60,step =1,disabled=st.session_state.determine)
    sum.text_input("财富/1000+名誉+快乐","= 60  ")
    if numrich/1000+numfame+numhappy>60:
        st.error("你输入的目标合计大于60分")
    else:
        st.toggle("确定",key="determine",disabled=st.session_state.determine)

leaner,Payscale,fame,happy = st.columns(4)
with leaner:
    st.write("#### 职业记录")
    st.toggle(":rowboat:航海",key="navigation")
    st.toggle(":movie_camera:电影",key="movie")
    st.toggle(":hammer:采矿",key="mining")
    st.toggle(":movie_camera:政治",key="politics")
    st.toggle(":male-farmer:农业",key="agriculture")
    st.toggle(":rocket:太空",key="space")
    st.toggle(":male-office-worker:企业",key="enterprise")
    st.write("#### 教育记录")
    st.toggle(":male-judge:法律",key="law")
    st.toggle(":male-doctor:医学",key="medicine")
    st.toggle(":construction_worker:工程",key="engineer")
    st.toggle(":male-scientist:科学",key="science")
    st.toggle(f":female-student:普通`{st.session_state.leanercount}`",on_change=student,key="leaner")
with Payscale:
    st.write("#### 薪级记录")
    st.radio("",(":moneybag:1,000",
                 ":moneybag:2,000",
                 ":moneybag:3,000",
                 ":moneybag:4,000",
                 ":moneybag:5,000",
                 ":moneybag:6,000",
                 ":moneybag:7,000",
                 ":moneybag:8,000",
                 ":moneybag:9,000",
                 ":moneybag:10,000",
                 ":moneybag:11,000",
                 ":moneybag:12,000",
                 ":moneybag:13,000",
                 ":moneybag:14,000",
                 ":moneybag:15,000",
                 ":moneybag:16,000",
                 ":moneybag:17,000",
                 ":moneybag:18,000",
                 ":moneybag:19,000",
                 ":moneybag:20,000",
                 ":moneybag:21,000",
                    ),label_visibility="collapsed",key="pay")

with fame:
    st.write("#### :crown:名誉")
    st.number_input(":crown:名誉",0,step =1,key="nowcrown")
with happy:
    st.write("#### :smile:快乐")
    st.number_input(":smile:快乐",0,step =1,key="nowhappy")
