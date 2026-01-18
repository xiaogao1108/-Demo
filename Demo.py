# career_app.py
# Python≥3.7
# pip install streamlit zhipuai matplotlib numpy

import streamlit as st
import os
from zhipuai import ZhipuAI
import matplotlib.pyplot as plt
import numpy as np
import json
import traceback
import warnings
warnings.filterwarnings("ignore")

# ---------- 字体与中文字符支持 ----------
plt.rcParams["font.sans-serif"] = [
    "SimHei", "Microsoft YaHei", "DejaVu Sans", "Arial Unicode MS", "sans-serif"
]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["figure.autolayout"] = True

# ---------- 智谱 AI 客户端 ----------
API_KEY = "cfc7dad8acc1428a9013b7a0d186ee36.6GBWBrFXUTi0L210"
client = ZhipuAI(api_key=API_KEY)

# ---------- Streamlit 页面 ----------
st.set_page_config(page_title="AI 职业发展助手", layout="centered")
st.title("🎯 AI 职业发展助手")
st.write("基于大语言模型的大学生职业发展支持 Demo")

# ---------- 用户输入 ----------
st.header("📌 基本信息填写")

major = st.text_input("你的专业")
skills = st.text_area("你掌握的技能（用逗号分隔）", placeholder="如：Python, 数据分析, 写作")
interests = st.text_area("兴趣方向", placeholder="如：技术、产品、金融、教育")
city_preference = st.selectbox(
    "城市偏好", ["不限", "一线城市", "新一线城市", "二三线城市"]
)
career_goal = st.text_input("理想职业方向（可选）", placeholder="如：数据分析师 / 产品经理")

# ---------- Prompt 构造 ----------
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

# ---------- 智谱 AI 调用 ----------
def get_ai_response(prompt: str):
    try:
        resp = client.chat.completions.create(
            model="glm-4",
            messages=[
                {"role": "system", "content": "你是一名专业的职业发展顾问，请严格按要求的JSON格式输出。"},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )
        return resp.choices[0].message.content
    except Exception as e:
        st.error(f"❌ API 调用失败: {e}")
        return None

# ---------- 雷达图绘制 ----------
def draw_radar_chart(scores: dict):
    labels = list(scores.keys())
    values = list(scores.values())
    num_vars = 5
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.set_facecolor("white")
    fig.patch.set_facecolor("white")

    # 绘图
    ax.plot(angles, values, "o-", linewidth=2, color="#1E90FF",
            markersize=8, markerfacecolor="white",
            markeredgewidth=1.5, markeredgecolor="#1E90FF")
    ax.fill(angles, values, alpha=0.2, color="#87CEEB")

    # 标签
    ax.set_xticks(angles[:-1])
    try:
        ax.set_xticklabels(labels, fontsize=12, fontweight="bold")
    except Exception:
        english_labels = ["Knowledge", "Skills", "Learning", "Experience", "Awareness"]
        ax.set_xticklabels(english_labels, fontsize=11, fontweight="bold")

    # 网格
    ax.set_yticks([0, 20, 40, 60, 80, 100])
    ax.set_yticklabels(["0", "20", "40", "60", "80", "100"], fontsize=9, color="gray")
    ax.set_ylim(0, 100)
    ax.grid(True, alpha=0.3, color="gray", linestyle="-", linewidth=0.8)

    ax.set_title("个人能力雷达图", fontsize=14, fontweight="bold", pad=20, color="#333")
    plt.tight_layout()
    return fig

# ---------- 评分卡片 HTML ----------
def create_score_cards(scores: dict):
    html = """
    <div style="background-color: white; padding: 20px; border-radius: 8px; margin: 20px 0;">
        <h4 style="margin-bottom: 15px; color: #333;">能力评分详情</h4>
        <div style="display: flex; justify-content: space-between; flex-wrap: wrap;">
    """
    for k, v in scores.items():
        html += f"""
        <div style="flex: 1; min-width: 100px; margin: 5px; padding: 12px;
                    background-color: #FFF9C4; border-radius: 6px;
                    text-align: center; border: 1px solid #FFEB3B;">
            <div style="font-size: 12px; color: #666; margin-bottom: 5px;">{k}</div>
            <div style="font-size: 18px; font-weight: bold; color: #333;">{v:.1f}</div>
        </div>
        """
    html += "</div></div>"
    return html

# ---------- JSON 提取 ----------
def extract_json(text: str):
    if not text:
        return None
    try:
        start, end = text.find("{"), text.rfind("}") + 1
        if start >= 0 and end > start:
            return text[start:end]
    except Exception:
        pass
    return None

# ---------- 主流程 ----------
if st.button("🚀 生成职业发展建议", type="primary"):
    if not major or not skills or not interests:
        st.warning("⚠️ 请至少填写专业、技能和兴趣信息")
        st.stop()

    with st.spinner("🔍 AI 正在分析你的职业发展方向..."):
        raw = get_ai_response(build_prompt())
    if not raw:
        st.error("❌ AI 返回为空，请检查 API Key 或网络连接")
        st.stop()

    json_str = extract_json(raw)
    if not json_str:
        st.error("❌ 未能从 AI 输出中提取 JSON 格式数据")
        with st.expander("查看原始输出"):
            st.code(raw)
        st.stop()

    try:
        data = json.loads(json_str)
        advice = data["career_advice"]
        scores = data["ability_scores"]
        required = ["专业基础", "技能匹配", "学习能力", "实践经验", "职业认知"]
        for k in required:
            if k not in scores:
                raise KeyError(k)
            scores[k] = float(scores[k])
            scores[k] = max(0, min(100, scores[k]))
    except Exception as e:
        st.error(f"❌ 数据解析出错: {e}")
        with st.expander("查看原始 JSON"):
            st.code(json_str)
        st.stop()

    # ---------- 结果展示 ----------
    st.success("✅ 分析完成")
    st.markdown("---")
    st.markdown("### 🧠 AI 职业分析结果")
    st.markdown(advice)
    st.markdown("---")
    st.markdown("### 📈 个人能力雷达图")
    try:
        fig = draw_radar_chart(scores)
        st.pyplot(fig)
    except Exception as e:
        st.error(f"❌ 生成雷达图失败: {e}")
    # 重点修复：加上 unsafe_allow_html=True
    st.markdown(create_score_cards(scores), unsafe_allow_html=True)
    st.caption("※ 雷达图显示了你在 5 个关键维度的能力评估")

# ---------- 页脚 ----------
st.markdown("---")
st.caption("本 Demo 用于课程展示与原型验证，结果仅供参考。")
