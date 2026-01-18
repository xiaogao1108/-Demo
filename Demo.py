import streamlit as st
import os
from zhipuai import ZhipuAI
import matplotlib.pyplot as plt
import numpy as np
import json
import traceback
import warnings
warnings.filterwarnings('ignore')

# ========== 字体配置 ==========
# 确保中文字体正确显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans', 'Arial Unicode MS', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.autolayout'] = True

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
interests = st.text_area("兴趣方向", placeholder="如：技术、产品、金融、教育")
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

# ========== 完全按照图片样式绘制雷达图 ==========
def draw_radar_chart_exact(scores_dict):
    """完全按照图片中的雷达图样式绘制"""
    # 获取标签和值
    labels = list(scores_dict.keys())
    values = list(scores_dict.values())
    
    # 确保是5个维度
    if len(labels) != 5:
        raise ValueError(f"需要5个维度，但得到{len(labels)}个")
    
    # 为雷达图准备数据
    num_vars = 5
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    
    # 闭合图形
    values_closed = values + values[:1]
    angles_closed = angles + angles[:1]
    
    # 创建图形，完全按照图片尺寸
    fig, ax = plt.subplots(figsize=(8, 6), subplot_kw=dict(polar=True))
    
    # 设置背景为纯白色
    ax.set_facecolor('white')
    fig.patch.set_facecolor('white')
    
    # 绘制雷达图 - 使用图片中的蓝色线条
    ax.plot(angles_closed, values_closed, 'o-', linewidth=2, 
            color='#1E90FF', markersize=6, markerfacecolor='white', 
            markeredgewidth=1.5, markeredgecolor='#1E90FF')
    
    # 使用图片中的浅蓝色填充
    ax.fill(angles_closed, values_closed, alpha=0.2, color='#87CEEB')
    
    # 设置5个维度的标签位置
    ax.set_xticks(angles)
    
    # 设置5个中文标签
    ax.set_xticklabels(['专业基础', '技能匹配', '学习能力', '实践经验', '职业认知'], 
                       fontsize=11, fontweight='bold')
    
    # 设置径向网格 - 与图片完全一致
    ax.set_yticks([0, 20, 40, 60, 80, 100])
    ax.set_yticklabels(['0', '20', '40', '60', '80', '100'], 
                       fontsize=8, color='gray')
    ax.set_ylim(0, 100)
    
    # 设置网格样式
    ax.grid(True, alpha=0.3, color='gray', linestyle='-', linewidth=0.5)
    
    # 设置标题 - 与图片完全一致
    ax.set_title("个人能力雷达图", fontsize=14, fontweight='bold', pad=20, color='#333333')
    
    # 调整布局
    plt.tight_layout()
    
    return fig

# ========== 创建完全按照图片样式的评分卡片 ==========
def create_score_cards_exact(scores):
    """创建完全按照图片样式的评分卡片"""
    # 按照图片中的顺序和样式创建HTML
    html = '''
    <div style="background-color: white; padding: 20px; border-radius: 8px; margin: 20px 0;">
        <h4 style="margin-bottom: 15px; color: #333;">能力评分详情</h4>
        <div style="display: flex; justify-content: space-between; flex-wrap: wrap;">
    '''
    
    # 按照图片中的五个维度顺序
    dimensions = ["专业基础", "技能匹配", "学习能力", "实践经验", "职业认知"]
    
    for dim in dimensions:
        value = scores.get(dim, 0)
        html += f'''
        <div style="flex: 1; min-width: 100px; margin: 5px; padding: 12px; 
                    background-color: #FFF9C4; border-radius: 6px; 
                    text-align: center; border: 1px solid #FFEB3B;">
            <div style="font-size: 12px; color: #666; margin-bottom: 5px;">
                {dim}
            </div>
            <div style="font-size: 18px; font-weight: bold; color: #333;">
                {value:.1f}
            </div>
        </div>
        '''
    
    html += '''
        </div>
    </div>
    '''
    return html

# ========== 从 AI 输出中提取 JSON ==========
def extract_json(text):
    """从 AI 输出中提取 JSON 数据"""
    if not text:
        return None
    
    try:
        start = text.find('{')
        end = text.rfind('}') + 1
        
        if start >= 0 and end > start:
            json_str = text[start:end]
            json.loads(json_str)  # 验证是否能解析
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
    
    # 解析 AI 返回
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
                    try:
                        scores[key] = float(scores[key])
                    except:
                        st.error(f"❌ 维度 {key} 的值必须是数字")
                        st.stop()
                if scores[key] < 0 or scores[key] > 100:
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
    
    # 展示结果
    st.success("✅ 分析完成")
    
    st.markdown("---")
    st.markdown("### 🧠 AI 职业分析结果")
    st.markdown(career_text)
    
    st.markdown("---")
    
    # 生成雷达图
    st.markdown("### 📈 个人能力雷达图")
    try:
        fig = draw_radar_chart_exact(scores)
        st.pyplot(fig)
    except Exception as e:
        st.error(f"❌ 生成雷达图失败: {str(e)}")
    
    # 显示评分详情卡片
    st.markdown(create_score_cards_exact(scores), unsafe_allow_html=True)
    
    # 添加图片中的说明文字
    st.caption("※ 雷达图显示了你在5个关键维度的能力评估")

# ========== 说明 ==========
st.markdown("---")
st.caption("本 Demo 用于课程展示与原型验证，结果仅供参考。")
