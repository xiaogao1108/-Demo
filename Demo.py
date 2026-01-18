import streamlit as st
import os
from zhipuai import ZhipuAI
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


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
你是一名专业的职业发展顾问，请基于以下大学生信息进行分析。

【学生背景】
- 专业：{major}
- 技能：{skills}
- 兴趣：{interests}
- 城市偏好：{city_preference}
- 理想职业（如有）：{career_goal}

【任务】
1. 推荐 2-3 个适合的职业方向，并说明理由
2. 分析当前能力差距
3. 给出 3 个月行动建议
4. 请对以下 5 个能力维度进行 0-100 分评分：
   - 专业基础
   - 技能匹配
   - 学习能力
   - 实践经验
   - 职业认知

【输出格式要求】
请严格按照以下 JSON 格式输出（不要多余说明）：

{{
  "career_advice": "文字分析内容",
  "ability_scores": {{
    "专业基础": 0,
    "技能匹配": 0,
    "学习能力": 0,
    "实践经验": 0,
    "职业认知": 0
  }}
}}
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

# ========== 能力雷达图函数 ==========
def draw_radar_chart(scores_dict):
    labels = list(scores_dict.keys())  # 英文标签
    values = list(scores_dict.values())

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)
    values = values + values[:1]
    angles = np.concatenate([angles, [angles[0]]])

    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
    ax.plot(angles, values, linewidth=2)
    ax.fill(angles, values, alpha=0.25)

    ax.set_thetagrids(angles[:-1] * 180 / np.pi, labels)  # 英文标签
    ax.set_ylim(0, 100)
    ax.set_title("Personal Ability Radar Chart")          # 英文标题

    return fig


# ========== 从 AI 输出中提取 JSON ==========
def extract_json(text):
    """
    从 AI 输出中提取第一个合法 JSON 对象
    """
    try:
        start = text.index("{")
        end = text.rindex("}") + 1
        return text[start:end]
    except ValueError:
        return None


# ========== 生成结果 ==========
import json

if st.button("🚀 生成职业发展建议"):
    if not major or not skills or not interests:
        st.warning("请至少填写专业、技能和兴趣信息")
        st.stop()

    if not API_KEY:
        st.error("❌ 未检测到 ZHIPUAI_API_KEY，请先设置环境变量")
        st.stop()

    with st.spinner("AI 正在分析你的职业发展方向..."):
        raw_result = get_ai_response(build_prompt())

    # ========== 解析 AI 返回 ==========
    try:
        json_text = extract_json(raw_result)
        if not json_text:
            st.error("❌ 未能从 AI 输出中提取 JSON")
            st.code(raw_result)
            st.stop()

        try:
            result_json = json.loads(json_text)
            career_text = result_json["career_advice"]
            scores = result_json["ability_scores"]
        except Exception:
            st.error("❌ JSON 解析失败")
            st.code(json_text)
            st.stop()

    except Exception as e:
        st.error("❌ AI 输出解析失败，请重试")
        st.code(raw_result)
        st.stop()

    # ========== 展示文本结果 ==========
    st.success("分析完成 ✅")
    st.markdown("### 🧠 AI 职业分析结果")
    st.markdown(career_text)

    # ========== 雷达图 ==========

    st.markdown("### 📈 个人能力雷达图")
    fig = draw_radar_chart(scores)
    st.pyplot(fig)

# ========== 说明 ==========
st.markdown("---")
st.caption("本 Demo 用于课程展示与原型验证，结果仅供参考。")

