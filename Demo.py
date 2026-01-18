## 一、整体路线图（先让你心里有数）

你要完成的，其实只有 **4 件事**：

1. **把“迷茫”说清楚（问题诊断）**
2. **把“AI 怎么帮忙”设计出来（方案）**
3. **选一个你能驾驭的 AI 工具，做 Demo**
4. **把全过程整理成 1000 字设计文档**

👉 **建议产品形态**：
 **「AI 职业发展助手」**（对话式 / 表单式 / 网页 Demo 都可以）

------

## 二、阶段 1：问题分析（第 1 天完成）

### 1️⃣ 明确“职业迷茫”的真实痛点（写文档用）

你不要泛泛而谈，直接拆成 **4 类核心痛点**：

| 痛点         | 具体表现                 |
| ------------ | ------------------------ |
| 自我认知不足 | 不知道自己适合什么岗位   |
| 信息不对称   | 不清楚岗位要求、发展路径 |
| 决策成本高   | 选择多，怕选错           |
| 行动困难     | 不知道下一步怎么做       |

📌 **你文档里要写的是：**

> 不是学生不努力，而是缺少**系统化、个性化、可执行的职业指导**

------

## 三、阶段 2：方案设计（第 1–2 天）

### 2️⃣ 把解决方案「产品化」

给你的方案一个**明确名字**（非常重要）：

> **产品名示例：**
>  **CareerPilot——AI 职业发展导航助手**

------

### 3️⃣ 设计核心功能（不用多，3–4 个就够）

#### 🔹 功能 1：AI 职业画像分析

- 输入：
  - 专业
  - 技能
  - 兴趣
  - 城市偏好
- 输出：
  - 3–5 个匹配职业方向
  - 匹配理由（可解释）

#### 🔹 功能 2：岗位能力差距分析

- 对比：
  - 当前能力 vs 目标岗位
- 输出：
  - 技能缺口清单
  - 学习优先级

#### 🔹 功能 3：行动路线图生成

- 输出：
  - 3 个月行动计划
  - 学习 + 实习 + 项目建议

#### 🔹（可选）功能 4：简历/自我介绍优化

------

## 四、阶段 3：选 AI 工具（这是老师最爱看的部分）

### 4️⃣ 推荐你用的工具组合（**简单、稳妥、好解释**）

> **强烈建议，不要自己训练模型**

#### ✔ AI 核心能力

- **大语言模型**（ChatGPT / 通义千问 / 文心一言 / Claude）
- 用途：分析、生成建议、规划路径

#### ✔ Demo 实现工具（任选一个）

| 工具                    | 适合你吗            |
| ----------------------- | ------------------- |
| **Streamlit（Python）** | ⭐⭐⭐⭐⭐ 非常适合      |
| Gradio                  | ⭐⭐⭐⭐                |
| Web 表单 + 接口         | ⭐⭐⭐                 |
| PPT + 录屏              | ⭐⭐⭐（最低保底方案） |

👉 **如果你会 Python：用 Streamlit**
 👉 **不会代码：用对话式 + 录屏演示**

------

## 五、阶段 4：做 Demo（第 3–4 天）

### 5️⃣ Demo 最低可行版本（MVP）

你只需要做到：

1. 用户输入信息
2. AI 返回职业建议
3. 页面/对话能跑

#### Streamlit Demo 示例结构（给你一个方向）：

```
- 输入专业
- 输入技能（多选）
- 输入兴趣
- 点击「生成职业建议」
- 展示：
  - 职业方向
  - 能力差距
  - 行动建议
```

📌 **注意**：
 老师看的是：

- 能不能跑
- AI 有没有真的参与决策
   **不是 UI 多好看**

------

## 六、阶段 5：写设计文档（第 5 天）

### 6️⃣ 1000 字文档结构（直接照抄）

#### 1️⃣ 项目背景与问题诊断（≈200字）

- 职业迷茫现象
- 四大痛点

#### 2️⃣ 解决方案设计（≈300字）

- 产品定位
- 功能模块
- 使用流程

#### 3️⃣ AI 工具选择与理由（≈200字）

- 为什么用大模型
- 相比传统咨询的优势

#### 4️⃣ 关键配置与实现（≈150字）

- Prompt 设计思路
- Demo 技术路线

#### 5️⃣ 迭代与优化记录（≈100字）

- 初版问题
- 改进点

#### 6️⃣ 效果评估（≈100字）

- 用户体验
- 实际指导价值

------

## 七、阶段 6：视频 / 演示（半天搞定）

### 7️⃣ 3 分钟视频结构

| 时间      | 内容        |
| --------- | ----------- |
| 0:00–0:30 | 背景 + 问题 |
| 0:30–1:00 | 产品介绍    |
| 1:00–2:30 | Demo 操作   |
| 2:30–3:00 | 总结价值    |

👉 **录屏工具**：OBS / 腾讯会议 / 自带录屏

------

## 八、给你一个现实建议（非常重要）

> **评分重点不是技术，而是：**

- 问题是否真实
- AI 是否合理参与
- Demo 是否可用
- 逻辑是否完整

**90% 的人会败在：想做太大**


根据以上步骤,我完成了以下demo

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
    st.pyplot(test_fig)且完成了部分设计文档
## 一、项目背景与问题诊断

当代大学生职业发展困境并非源于个体懈怠，而是一个由**信息、决策与执行**组成的“系统性问题闭环”：从“自我认知不清”出发，因“岗位信息模糊”而加剧，在“高决策压力”下陷入犹豫，最终因“缺乏行动路径”而停滞。

### 大学生职业发展迷茫的核心痛点分析

| 痛点类别     | 占比 | 具体表现                                               | 数据来源                                                     |
| ------------ | ---- | ------------------------------------------------------ | ------------------------------------------------------------ |
| 自我认知不足 | 33%  | 不清楚自身能力、兴趣与岗位要求的匹配关系，职业定位模糊 | 智联招聘《2023大学生就业力调研报告》；中国青年报《2022大学生职业规划现状调查》 |
| 信息不对称   | 28%  | 岗位要求、发展路径了解碎片化，新兴职业认知滞后         | BOSS直聘研究院《高校就业指导有效性调研》；人社部《新职业发展报告（2023）》 |
| 决策成本高   | 23%  | 面对多种就业选择难以权衡，担忧首份工作选错带来长期影响 | 麦可思研究院毕业生就业报告；智联招聘《首份工作选择焦虑调研》 |
| 行动困难     | 16%  | 能力提升路径不清，计划执行率低，实习转化效果有限       | 教育部高教评估中心；实习僧《实习价值评估报告（2023）》       |


接下来由你来补全剩余文档,文档总字数控制在1000字以内
