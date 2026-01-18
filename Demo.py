import streamlit as st
import os
from zhipuai import ZhipuAI
import matplotlib.pyplot as plt
import numpy as np
import json
import traceback

# ========== 字体配置 ==========
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans', 'Arial Unicode MS', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 10
plt.rcParams['figure.autolayout'] = True  # 自动调整布局

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
    try:
        response = client.chat.completions.create(
            model="glm-4",
            messages=[
                {"role": "system", "content": "你是一名专业的职业发展顾问，请严格按要求的JSON格式输出。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"❌ API调用失败: {str(e)}")
        return None

# ========== 能力雷达图函数 ==========
def draw_radar_chart(scores_dict):
    """
    根据你的图片描述生成雷达图：
    1. 中文标签
    2. 英文标题
    3. 浅蓝色填充
    """
    labels = list(scores_dict.keys())  # 中文标签
    values = list(scores_dict.values())
    
    # 确保是5个维度
    if len(labels) != 5:
        raise ValueError(f"需要5个维度，但得到{len(labels)}个")
    
    # 转换为雷达图坐标
    num_vars = len(labels)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    
    # 闭合图形
    values += values[:1]
    angles += angles[:1]
    
    # 创建图形
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    
    # 设置背景
    ax.set_facecolor('white')
    fig.patch.set_facecolor('white')
    
    # 绘制雷达图 - 使用浅蓝色填充
    ax.plot(angles, values, 'o-', linewidth=2, color='#1f77b4')  # 蓝色线条
    ax.fill(angles, values, alpha=0.25, color='#a6cee3')  # 浅蓝色填充
    
    # 设置标签 - 使用中文标签
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=12)
    
    # 设置径向网格和标签
    ax.set_yticks([0, 20, 40, 60, 80, 100])
    ax.set_yticklabels(['0', '20', '40', '60', '80', '100'], fontsize=9)
    ax.set_ylim(0, 100)
    
    # 网格样式
    ax.grid(True, alpha=0.3)
    
    # 标题 - 使用英文标题
    ax.set_title("Personal Ability Radar Chart", 
                 fontsize=16, fontweight='bold', pad=20)
    
    # 添加签名（可选）
    fig.text(0.5, 0.02, "陈翰熙", ha='center', fontsize=10, style='italic', alpha=0.7)
    
    # 调整布局防止标签被截断
    plt.tight_layout()
    
    return fig

# ========== 从 AI 输出中提取 JSON ==========
def extract_json(text):
    """
    从 AI 输出中提取第一个合法 JSON 对象
    """
    if not text:
        return None
    
    try:
        # 查找第一个 { 和最后一个 }
        start = text.find('{')
        end = text.rfind('}') + 1
        
        if start >= 0 and end > start:
            json_str = text[start:end]
            # 验证是否能解析
            json.loads(json_str)
            return json_str
    except:
        pass
    
    return None

# ========== 生成结果 ==========
if st.button("🚀 生成职业发展建议", type="primary"):
    if not major or not skills or not interests:
        st.warning("⚠️ 请至少填写专业、技能和兴趣信息")
        st.stop()
    
    with st.spinner("🔍 AI 正在分析你的职业发展方向..."):
        raw_result = get_ai_response(build_prompt())
    
    if not raw_result:
        st.error("❌ AI 返回为空，请检查 API Key 或网络连接")
        st.stop()
    
    # ========== 解析 AI 返回 ==========
    with st.spinner("📊 解析分析结果..."):
        json_text = extract_json(raw_result)
        
        if not json_text:
            st.error("❌ 未能从 AI 输出中提取 JSON 格式数据")
            with st.expander("查看原始输出"):
                st.code(raw_result)
            st.stop()
        
        try:
            result_json = json.loads(json_text)
            
            # 验证数据结构
            if "career_advice" not in result_json or "ability_scores" not in result_json:
                st.error("❌ JSON 格式不正确，缺少必要字段")
                st.code(json_text)
                st.stop()
            
            career_text = result_json["career_advice"]
            scores = result_json["ability_scores"]
            
            # 验证评分数据
            required_keys = ["专业基础", "技能匹配", "学习能力", "实践经验", "职业认知"]
            for key in required_keys:
                if key not in scores:
                    st.error(f"❌ 缺少能力维度: {key}")
                    st.stop()
                if not isinstance(scores[key], (int, float)):
                    st.error(f"❌ 维度 {key} 的值必须是数字")
                    st.stop()
                if scores[key] < 0 or scores[key] > 100:
                    st.warning(f"⚠️ 维度 {key} 的评分 {scores[key]} 超出 0-100 范围，已自动调整")
                    scores[key] = max(0, min(100, scores[key]))
            
        except json.JSONDecodeError as e:
            st.error(f"❌ JSON 解析失败: {str(e)}")
            with st.expander("查看原始 JSON"):
                st.code(json_text)
            st.stop()
        except Exception as e:
            st.error(f"❌ 数据处理出错: {str(e)}")
            st.code(traceback.format_exc())
            st.stop()
    
    # ========== 展示文本结果 ==========
    st.success("✅ 分析完成")
    
    st.markdown("---")
    st.markdown("### 🧠 AI 职业分析结果")
    st.markdown(career_text)
    
    st.markdown("---")
    st.markdown("### 📈 个人能力雷达图")
    
    # 显示评分表格
    st.markdown("#### 📊 能力评分详情")
    cols = st.columns(5)
    for idx, (key, value) in enumerate(scores.items()):
        cols[idx].metric(key, f"{value:.1f}")
    
    # 生成雷达图
    try:
        fig = draw_radar_chart(scores)
        st.pyplot(fig)
        st.caption("📋 雷达图显示了你在5个关键维度的能力评估")
    except Exception as e:
        st.error(f"❌ 生成雷达图失败: {str(e)}")
        st.code(traceback.format_exc())

# ========== 说明 ==========
st.markdown("---")
st.caption("本 Demo 用于课程展示与原型验证，结果仅供参考。")

# 调试信息（可折叠）
with st.expander("🔧 调试信息"):
    st.write("**API状态:** 已连接" if API_KEY else "未连接")
    st.write(f"**字体配置:** {plt.rcParams['font.sans-serif']}")
