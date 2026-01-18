import streamlit as st
import os
from zhipuai import ZhipuAI
import matplotlib.pyplot as plt
import numpy as np
import json
import traceback
import matplotlib.font_manager as fm
import warnings
warnings.filterwarnings('ignore')

# ========== 字体配置 ==========
# 修复中文字体显示问题
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

# ========== 修复的雷达图函数 ==========
def draw_radar_chart_fixed(scores_dict):
    """
    绘制雷达图，确保5个角显示汉字标签
    根据图片描述：白色背景，蓝色多边形，黑色圆环
    """
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
    
    # 创建图形
    fig, ax = plt.subplots(figsize=(9, 9), subplot_kw=dict(polar=True), dpi=100)
    
    # 设置背景为白色
    ax.set_facecolor('white')
    fig.patch.set_facecolor('white')
    
    # 绘制雷达图 - 蓝色多边形
    line = ax.plot(angles_closed, values_closed, 'o-', linewidth=2.5, 
                   color='#1E90FF', markersize=8, markerfacecolor='white', 
                   markeredgewidth=2, markeredgecolor='#1E90FF')
    ax.fill(angles_closed, values_closed, alpha=0.25, color='#87CEEB')
    
    # 设置标签位置 - 在雷达图外圈显示汉字标签
    ax.set_xticks(angles)
    
    # 尝试使用中文字体
    try:
        xticklabels = ax.set_xticklabels(labels, fontsize=13, fontweight='bold')
        
        # 调整标签位置使其更清晰
        for label, angle in zip(xticklabels, angles):
            # 根据角度调整标签位置
            if 0 <= angle < np.pi/2:  # 第一象限
                label.set_horizontalalignment('left')
                label.set_verticalalignment('bottom')
            elif np.pi/2 <= angle < np.pi:  # 第二象限
                label.set_horizontalalignment('right')
                label.set_verticalalignment('bottom')
            elif np.pi <= angle < 3*np.pi/2:  # 第三象限
                label.set_horizontalalignment('right')
                label.set_verticalalignment('top')
            else:  # 第四象限
                label.set_horizontalalignment('left')
                label.set_verticalalignment('top')
                
            # 稍微向外偏移标签
            label.set_position((angle, 110))
            
    except Exception as e:
        # 如果中文字体失败，使用英文标签
        st.warning("⚠️ 中文字体可能未正确加载，使用英文标签")
        english_labels = {
            "专业基础": "Professional\nKnowledge",
            "技能匹配": "Skill\nMatch", 
            "学习能力": "Learning\nAbility",
            "实践经验": "Practical\nExperience", 
            "职业认知": "Career\nAwareness"
        }
        labels_eng = [english_labels.get(label, label) for label in labels]
        ax.set_xticklabels(labels_eng, fontsize=12, fontweight='bold')
    
    # 设置径向网格 - 黑色圆环
    ax.set_yticks([0, 20, 40, 60, 80, 100])
    ax.set_yticklabels(['0', '20', '40', '60', '80', '100'], 
                       fontsize=10, color='black')
    ax.set_ylim(0, 110)  # 为标签留出空间
    
    # 设置网格样式
    ax.grid(True, alpha=0.3, color='black', linestyle='-', linewidth=0.8)
    
    # 在主标题位置添加汉字标题
    try:
        ax.set_title("个人能力雷达图", fontsize=18, fontweight='bold', pad=25)
    except:
        ax.set_title("Ability Radar Chart", fontsize=18, fontweight='bold', pad=25)
    
    # 在雷达图内部每个数据点位置添加数值
    for i, (angle, value) in enumerate(zip(angles, values)):
        # 在数据点附近显示数值
        x = np.cos(angle) * (value + 5)  # 稍微向外偏移
        y = np.sin(angle) * (value + 5)
        
        ax.text(angle, value + 8, f'{value:.0f}', 
                ha='center', va='center', 
                fontsize=11, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', 
                         facecolor='white', 
                         edgecolor='#1E90FF',
                         alpha=0.8))
    
    # 在图形底部添加说明文字
    plt.figtext(0.5, 0.01, "雷达图显示了你在5个关键维度的能力评估", 
                ha='center', fontsize=10, style='italic', alpha=0.7)
    
    # 调整布局防止标签被截断
    plt.tight_layout(rect=[0, 0.05, 1, 0.95])
    
    return fig

# ========== 从 AI 输出中提取 JSON ==========
def extract_json(text):
    """从 AI 输出中提取 JSON 数据"""
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
    except Exception as e:
        st.warning(f"⚠️ JSON 提取警告: {str(e)}")
    
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
                    try:
                        scores[key] = float(scores[key])
                    except:
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
    
    # 显示能力评分详情（根据图片描述）
    st.markdown("### 📊 能力评分详情")
    
    # 创建5列的指标卡片
    cols = st.columns(5)
    score_items = list(scores.items())
    
    for idx in range(5):
        with cols[idx]:
            key, value = score_items[idx]
            st.metric(label=key, value=f"{value:.1f}")
    
    st.markdown("---")
    st.markdown("### 📈 个人能力雷达图")
    
    # 生成雷达图
    try:
        fig = draw_radar_chart_fixed(scores)
        if fig:
            st.pyplot(fig)
            st.caption("📋 雷达图显示了你在5个关键维度的能力评估")
        else:
            st.error("❌ 雷达图生成失败")
    except Exception as e:
        st.error(f"❌ 生成雷达图失败: {str(e)}")
        st.code(traceback.format_exc())
        
        # 显示柱状图作为替代
        st.info("💡 尝试显示柱状图作为替代...")
        fig_bar, ax_bar = plt.subplots(figsize=(10, 5))
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        bars = ax_bar.bar(scores.keys(), scores.values(), color=colors)
        ax_bar.set_ylabel('分数', fontsize=12)
        ax_bar.set_title('能力评分柱状图', fontsize=14, fontweight='bold')
        ax_bar.set_ylim(0, 100)
        
        # 在每个柱子上添加数值
        for bar in bars:
            height = bar.get_height()
            ax_bar.text(bar.get_x() + bar.get_width()/2., height + 1,
                       f'{height:.0f}', ha='center', va='bottom', fontsize=10)
        
        plt.xticks(fontsize=11)
        plt.tight_layout()
        st.pyplot(fig_bar)

# ========== 说明 ==========
st.markdown("---")
st.caption("本 Demo 用于课程展示与原型验证，结果仅供参考。")

# 添加调试信息
with st.expander("🔧 系统信息"):
    st.write(f"Python 版本: {os.sys.version}")
    st.write(f"Matplotlib 版本: {matplotlib.__version__}")
    st.write(f"当前字体配置: {plt.rcParams['font.sans-serif']}")
    
    # 测试字体显示
    st.write("**字体测试:**")
    test_fig, test_ax = plt.subplots(figsize=(6, 1))
    test_ax.text(0.5, 0.5, "中文测试: 专业基础", fontsize=12, ha='center')
    test_ax.axis('off')
    st.pyplot(test_fig)
