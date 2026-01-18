import streamlit as st
import os
from zhipuai import ZhipuAI

# ========== API Key ==========
API_KEY = "cfc7dad8acc1428a9013b7a0d186ee36.6GBWBrFXUTi0L210"
client = ZhipuAI(api_key=API_KEY)

# ========== 页面配置 ==========
st.set_page_config(page_title="AI 职业发展助手", layout="centered")

st.title("🎯 AI 职业发展助手")
st.write("基于大语言模型的大学生职业发展支持 Demo")

# ========== 用户输入 ==========
st.header("📌 基本信息填写")

major = st.text_input("你的专业")
skills = st.text_area("你掌握的技能（用逗号分隔）", placeholder="如：Python, 数据分析, 写作")
interests = st.text_area("你的兴趣方向", placeholder="如：技术、产品、金融、教育")
city_preference = st.selectbox(
    "城市偏好",
    ["不限", "一线城市", "新一线城市", "二三线城市"]
)
career_goal = st.text_input(
    "理想职业方向（可选）",
    placeholder="如：数据分析师 / 产品经理"
)

# ========== Prompt 构造 ==========
def build_prompt():
    return f"""
你是一名严谨、理性的职业规划顾问，请基于以下大学生信息进行分析：

【学生背景】
- 专业：{major}
- 技能：{skills}
- 兴趣：{interests}
- 城市偏好：{city_preference}
- 理想职业（如有）：{career_goal}

【任务要求】
1. 给出 2-3 个适合的职业方向，并说明匹配理由
2. 分析当前能力与目标岗位之间的主要差距
3. 给出一份可执行的 3 个月行动建议（学习 + 实践）

【输出要求】
- 使用清晰的小标题
- 内容务实，避免空泛
"""

# ========== AI 调用 ==========
def get_ai_response(prompt):
    response = client.chat.completions.create(
        model="glm-4",
        messages=[
            {"role": "system", "content": "你是一名专业的职业发展顾问"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content

# ========== 生成结果 ==========
if st.button("🚀 生成职业发展建议"):
    if not major or not skills or not interests:
        st.warning("请至少填写专业、技能和兴趣信息")
    else:
        with st.spinner("AI 正在分析你的职业发展方向..."):
            result = get_ai_response(build_prompt())

        st.success("分析完成 ✅")
        st.markdown("### 📊 AI 职业分析结果")
        st.markdown(result)

# ========== 说明 ==========
st.markdown("---")
st.caption("本 Demo 用于课程展示与原型验证，结果仅供参考。")
