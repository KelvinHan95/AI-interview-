#=============
#面试模拟器
#=============
import streamlit as st
import requests

API_KEY = st.secrets["DEEPSEEK_API_KEY"]  #streamlit 加密api写法

job = st.text_input("应聘岗位", placeholder="如：后端开发、运营、销售")
years = st.text_input("工作年限", placeholder="如：3年、应届生")

SYSTEM_PROMPT = """你是一个严格的面试官。
用户要应聘的岗位是：{job}，工作年限：{years}。
请出 5 个面试问题，每个问题后面标注考察重点。
要求：问题要真实、有区分度，不要太简单，贴合这个岗位实际会问的。"""

st.title("AI面试模拟器")          #创建标题


if st.button("开始模拟面试"):            #创建按钮
    if not job or not years:
        st.warning("岗位和年限都要填")
    else:
        with st.spinner("Ai面试官准备中..."):
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"我要应聘{job},{years}经验，请开始提问"}
            ]

            response = requests.post(
                "https://api.deepseek.com/chat/completions",
                headers={
                    "Authorization": f"Bearer {st.secrets['DEEPSEEK_API_KEY']}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek-flash",
                    "messages": messages,
                    "stream": False
                }
            )
            result = response.json()
            answer = result["choices"][0]["message"]["content"]
            st.subheader("面试题")
            st.write(answer)
