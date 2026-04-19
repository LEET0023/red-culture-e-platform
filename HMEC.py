import os
import streamlit as st
import pandas as pd

# 导入AI模块 (请确保这些文件在你的项目根目录下的 ai_modules 文件夹中)
from ai_modules.quiz_ai import AIQuizExplainer
from ai_modules.qa_ai import AIQASystem
from ai_modules.adaptive_test import AdaptiveTestGenerator
from ai_modules.badge_system import BadgeSystem

# =========================
# 页面设置
# =========================
st.set_page_config(
    page_title="“红脉E传”——陈毅旧居红色文化英语传播平台",
    page_icon="🏛️",
    layout="wide"
)
# ===# 路径适配逻辑
# ======================
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


IMG_DIR = os.path.join(BASE_DIR, "images")

IMAGE_PATHS = {
    "museum_gate_1": os.path.join(IMG_DIR, "ecfa_museum.png"),
    "chenyi_home": os.path.join(IMG_DIR, "chenyi_oldhome.png"),
    "chenyi_courtyard": os.path.join(IMG_DIR, "chenyi_yard.png"),
    "osmanthus": os.path.join(IMG_DIR, "osmanthus.png"),
    "chenyi_bio": os.path.join(IMG_DIR, "chenyi_life.png"),
    "chenyi_family": os.path.join(IMG_DIR, "chenyi_family.png"),
    "chenhaosu_visit": os.path.join(IMG_DIR, "chenhaosu_visit.png"),
    "oxhide_bed": os.path.join(IMG_DIR, "leather_bed.png"),
}

SECTIONS = [
    "走进陈毅旧居——一座夯土房里的革命史 / Entering Chen Yi’s Former Residence — A Revolutionary Story in a Rammed-Earth House",
    "百年丹桂见证鱼水情深 / A Century-Old Osmanthus Tree Witnessing the Bond Between Soldiers and Civilians",
    "陈毅元帅生平与家庭 / Marshal Chen Yi: His Life and Family",
    "陈昊苏回访沂蒙老房东 / Chen Haosu’s Return Visit to His Old Landlord in Yimeng",
    "革命文物展示 / Display of Revolutionary Cultural Relics"
]

# 视频文件夹路径
VIDEO_FOLDERS = {
    SECTIONS[0]: os.path.join(BASE_DIR, "走进陈毅旧居——一座夯土房里的革命史"),
    SECTIONS[1]: os.path.join(BASE_DIR, "百年丹桂见证鱼水情深"),
    SECTIONS[2]: os.path.join(BASE_DIR, "陈毅元帅生平与家庭"),
    SECTIONS[3]: os.path.join(BASE_DIR, "陈昊苏回访沂蒙老房东"),
    SECTIONS[4]: os.path.join(BASE_DIR, "革命文物展示"),
}

LEVELS = ["小学层 / Primary Level"]

SECTION_IMAGES = {
    SECTIONS[0]: [IMAGE_PATHS["chenyi_courtyard"]],
    SECTIONS[1]: [IMAGE_PATHS["osmanthus"]],
    SECTIONS[2]: [IMAGE_PATHS["chenyi_bio"], IMAGE_PATHS["chenyi_family"]],
    SECTIONS[3]: [IMAGE_PATHS["chenhaosu_visit"]],
    SECTIONS[4]: [IMAGE_PATHS["oxhide_bed"]],
}

# 后续的 Streamlit UI 逻辑代码...

# =========================
# 页面样式
# =========================
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: "Microsoft YaHei", "PingFang SC", sans-serif;
}
.main-title {
    font-size: 38px;
    font-weight: 900;
    color: #8b1f1f;
    text-align: center;
    margin-bottom: 6px;
}
.sub-title {
    font-size: 18px;
    color: #4b4b4b;
    text-align: center;
    margin-bottom: 24px;
}
.page-tag {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 999px;
    background: linear-gradient(90deg, #f7e2cf, #f3d7d7);
    color: #7a1f1f;
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 12px;
}
.section-title {
    font-size: 28px;
    font-weight: 800;
    color: #922d2d;
    margin-top: 8px;
    margin-bottom: 10px;
}
.subsection-title {
    font-size: 21px;
    font-weight: 800;
    color: #7f2020;
    margin-top: 24px;
    margin-bottom: 6px;
}
.subsection-line {
    width: 100%;
    height: 3px;
    background: linear-gradient(90deg, #b33a3a, #e8b37f);
    border-radius: 999px;
    margin-bottom: 16px;
}
.cn {
    font-size: 17px;
    font-weight: 700;
    color: #222;
    margin-bottom: 6px;
}
.en {
    font-size: 16px;
    color: #444;
    margin-bottom: 12px;
    line-height: 1.85;
}
.notice-box {
    background: #fff7ef;
    border-left: 5px solid #c67b52;
    border-radius: 14px;
    padding: 14px 16px;
    margin: 12px 0;
}
.video-wrap {
    background: linear-gradient(180deg, #fff6f6, #fffaf5);
    border-radius: 18px;
    padding: 14px;
    box-shadow: 0 8px 22px rgba(139, 31, 31, 0.10);
    margin-bottom: 16px;
}
.level-tip {
    background: #fffaf6;
    border-radius: 14px;
    padding: 12px;
    text-align: center;
    margin-bottom: 10px;
}
.footer-contact-box {
    margin-top: 12px;
    padding: 16px;
    border-radius: 14px;
    background: #fff7ef;
    border-left: 5px solid #c67b52;
    color: #6b3a2e;
    font-size: 16px;
    text-align: center;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

# =========================
# Session 初始化
# =========================
defaults = {
    "current_page": "home",
    "section": None,
    "level": None,
    "show_data": False,
    "show_contact": False
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ========== 初始化AI模块 ==========
@st.cache_resource
def init_ai_modules():
    # 确保这些类已经在你的 ai_modules 文件夹对应的文件中定义好
    return {
        "quiz_explainer": AIQuizExplainer(),
        "qa_system": AIQASystem(),
        # 如果 AdaptiveTestGenerator 和 BadgeSystem 还没写好，可以先注释掉或保持原样
        "adaptive_test": AdaptiveTestGenerator(),
        "badge_system": BadgeSystem()
    }

ai_modules = init_ai_modules()

# 添加用户ID（用于徽章系统）
if "user_id" not in st.session_state:
    import uuid
    st.session_state.user_id = str(uuid.uuid4())[:8]
# ========================================

# =========================
# 示例数据（只保留小学层）
# =========================
DATA_SAMPLE = pd.DataFrame({
    "指标 / Metric": [
        "页面浏览量 / Page Views",
        "小学层点击量 / Primary Level Clicks",
        "任务完成率 / Task Completion Rate",
        "词汇点击热度 / Vocabulary Click Heat",
    ],
    "示例数据 / Sample Data": [
        1280, 320, "72%", "High"
    ]
})

# =========================
# 内容数据（只保留小学层）
# =========================
CONTENT = {
    SECTIONS[0]: {
        "小学层 / Primary Level": {
            "标题 / Title": ("一座老房子的大故事", "A Small Old House with a Big Story"),
            "导览文案 / Guide Text": [
                ("这是前河湾陈毅旧居。", "This is Marshal Chen Yi’s old home in Qian Hewan."),
                ("1946年6月至1947年2月，陈毅一家在此居住生活。", "From June 1946 to February 1947, war hero Chen Yi lived here with his family."),
                ("这是一座典型的夯土民居建筑，是由钟氏家族族长钟维坤于1927年所建。", "The house is a traditional rammed-earth vernacular architecture, built in 1927 by Zhong Weikun."),
                ("这座房子看起来很普通，但它藏着一段重要的革命故事。", "The house looks simple, but it carries an important revolutionary story.")
            ],
            "词汇卡 / Word Cards": [
                ("old home", "旧居"),
                ("family", "家人"),
                ("house", "房子"),
                ("built", "建造"),
                ("history", "历史"),
                ("story", "故事")
            ],
            "平台任务 / Platform Task": {
                "题目_cn": "陈毅一家在这里住了多长时间？",
                "题目_en": "How long did Chen Yi’s family live here?",
                "选项": [
                    "A. 两个月 / Two months",
                    "B. 八个月 / Eight months",
                    "C. 两年 / Two years"
                ],
                "答案": "B. 八个月 / Eight months"
            },
            "打卡任务 / Check-in Task": (
                "请站在门前说一句英语：This old house has a big story.",
                "Please stand in front of the gate and say: This old house has a big story."
            )
        }
    },

    SECTIONS[1]: {
        "小学层 / Primary Level": {
            "标题 / Title": ("百年桂花树的故事", "The Story of a Century-Old Osmanthus Tree"),
            "导览文案 / Guide Text": [
                ("看！在小院里，有一棵非常古老的桂花树。", "Look! In the small yard, there is a very old sweet osmanthus tree."),
                ("它已经有一百多年了。人们称它为“江北第一桂”。", "It is over 100 years old. People call it “the most famous osmanthus tree in northern China.”"),
                ("很久以前，这棵树被种在花盆里。陈毅看到后说：", "Long ago, the tree was in a flowerpot. Chen Yi saw it and said:"),
                ("“这树栽在花盆里长不大，得栽到地上。”", "This tree cannot grow big in a pot. It should be planted in the ground."),
                ("于是他亲手把树栽到了院子里。", "So he planted the tree in the yard by himself."),
                ("直到今天，这棵树仍然在这里，长得高大又茂盛。", "The tree is still here today. It grows tall and strong."),
                ("这棵树讲述了一个温暖的故事。", "This tree tells us a warm story."),
                ("在艰苦的岁月里，军民之间像一家人一样互相帮助。", "In hard times, soldiers and local people helped each other like a family.")
            ],
            "词汇卡 / Word Cards": [
                ("yard", "院子"),
                ("tree", "树"),
                ("flowerpot", "花盆"),
                ("ground", "地上"),
                ("plant", "种植"),
                ("help each other", "互相帮助")
            ],
            "平台任务 / Platform Task": {
                "题目_cn": "陈毅做了什么？",
                "题目_en": "What did Chen Yi do?",
                "选项": [
                    "A. He cut the tree. / 他把树砍了。",
                    "B. He planted the tree in the yard. / 他把树栽到了院子里。",
                    "C. He put the tree in a room. / 他把树搬进了房间。"
                ],
                "答案": "B. He planted the tree in the yard. / 他把树栽到了院子里。"
            },
            "打卡任务 / Check-in Task": (
                "请找出院子里的桂花树，并说一句英语：This tree is very old.",
                "Please find the osmanthus tree in the yard and say: This tree is very old."
            )
        }
    },

    SECTIONS[2]: {
        "小学层 / Primary Level": {
            "标题 / Title": ("陈毅是谁？这是他的家庭", "Who Was Chen Yi? This Was His Family"),
            "导览文案 / Guide Text": [
                ("陈毅来自四川乐至。", "Chen Yi came from Lezhi, Sichuan."),
                ("在很长一段时间里，他为国家和人民努力工作。", "For many years, he worked hard for the country and the people."),
                ("土地革命时期，他领导了南方三年游击战争。", "During the Land Revolution period, he led guerrilla war in the south for three years."),
                ("1955年，他被授予元帅军衔。", "In 1955, he was awarded the rank of Marshal."),
                ("这是一张陈毅一家的合影。", "This is a family photo of Chen Yi."),
                ("他有四个孩子。", "He had four children."),
                ("他们分别是陈昊苏、陈丹淮、陈小鲁和陈姗姗。", "They were Chen Haosu, Chen Danhuai, Chen Xiaolu, and Chen Shanshan."),
                ("张茜怀里抱着的是最小的女儿陈姗姗。", "The baby in Zhang Xi’s arms is their youngest daughter, Chen Shanshan.")
            ],
            "词汇卡 / Word Cards": [
                ("family photo", "全家福"),
                ("child", "孩子"),
                ("Marshal", "元帅"),
                ("hometown", "家乡"),
                ("war", "战争"),
                ("family", "家庭")
            ],
            "平台任务 / Platform Task": {
                "题目_cn": "陈毅有几个孩子？",
                "题目_en": "How many children did Chen Yi have?",
                "选项": [
                    "A. Two",
                    "B. Three",
                    "C. Four"
                ],
                "答案": "C. Four"
            },
            "打卡任务 / Check-in Task": (
                "请说一句英语：This is Chen Yi’s family photo.",
                "Please say: This is Chen Yi’s family photo."
            )
        }
    },

    SECTIONS[3]: {
        "小学层 / Primary Level": {
            "标题 / Title": ("他回来看老朋友了", "He Came Back to See Old Friends"),
            "导览文案 / Guide Text": [
                ("这一张照片，是陈昊苏1990年来看望老房东的照片。", "Look at this photo. It shows Chen Haosu visiting his old landlord in 1990."),
                ("回到北京以后，他一直没有忘记沂蒙人民的恩情。", "After returning to Beijing, he never forgot the kindness of the Yimeng people."),
                ("他还写下了一首诗。", "He also wrote a poem."),
                ("这首诗表达了他的思念和感谢。", "The poem shows his memory and gratitude.")
            ],
            "词汇卡 / Word Cards": [
                ("photo", "照片"),
                ("visit", "看望"),
                ("landlord", "房东"),
                ("kindness", "恩情 / 善意"),
                ("poem", "诗"),
                ("remember", "记得")
            ],
            "平台任务 / Platform Task": {
                "题目_cn": "陈昊苏后来写了什么？",
                "题目_en": "What did Chen Haosu write later?",
                "选项": [
                    "A. 一本书 / A book",
                    "B. 一首诗 / A poem",
                    "C. 一封信 / A letter"
                ],
                "答案": "B. 一首诗 / A poem"
            },
            "打卡任务 / Check-in Task": (
                "请说一句英语：He never forgot the village.",
                "Please say: He never forgot the village."
            )
        }
    },

    SECTIONS[4]: {
        "小学层 / Primary Level": {
            "标题 / Title": ("一张老床背后的故事", "The Story Behind an Old Bed"),
            "导览文案 / Guide Text": [
                ("这是他们一家当年居住的地方。", "This is where their family lived."),
                ("你看到的这张牛皮床，就是他们当年使用过的。", "See this tough oxhide bed? It was used by the family."),
                ("现在，它已经成为国家三级革命文物。", "It is now a National Grade III Revolutionary Cultural Relic."),
                ("它让我们想起过去的生活和那段历史。", "It helps us remember the past and that period of history.")
            ],
            "词汇卡 / Word Cards": [
                ("bed", "床"),
                ("oxhide", "牛皮"),
                ("relic", "文物"),
                ("family", "家庭"),
                ("history", "历史"),
                ("remember", "记住")
            ],
            "平台任务 / Platform Task": {
                "题目_cn": "这件文物是什么？",
                "题目_en": "What is this relic?",
                "选项": [
                    "A. A table",
                    "B. A bed",
                    "C. A chair"
                ],
                "答案": "B. A bed"
            },
            "打卡任务 / Check-in Task": (
                "请说一句英语：This old bed is part of history.",
                "Please say: This old bed is part of history."
            )
        }
    }
}

# =========================
# 工具函数
# =========================
# =========================
# 小红星 AI 助手逻辑
# =========================
def render_ai_sidebar():
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 🌟 小红星助手 / AI Assistant")
        st.caption("我是你的红色文化小讲解员，有什么想问的吗？")

        # 初始化聊天历史记录，保存在 Session 中，切换页面不会消失
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # 在侧边栏创建一个小容器，专门放对话气泡
        chat_container = st.container(height=300)
        with chat_container:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

        # 聊天输入框
        if prompt := st.chat_input("输入你的问题..."):
            # 1. 记录并显示用户问题
            st.session_state.messages.append({"role": "user", "content": prompt})
            with chat_container:
                with st.chat_message("user"):
                    st.markdown(prompt)

            # 2. 调用你已经初始化好的 qa_system (DeepSeek 本地模型)
            with chat_container:
                with st.chat_message("assistant"):
                    with st.spinner("小红星思考中..."):
                        # 这里会自动关联你当前所在的主题 (section)
                        current_section = st.session_state.section or "陈毅旧居纪念馆"
                        answer = ai_modules["qa_system"].ask(
                            question=prompt,
                            context=current_section
                        )
                        st.markdown(answer)

            # 3. 记录 AI 的回答
            st.session_state.messages.append({"role": "assistant", "content": answer})

            # 4. 触发小互动：提问质量评分
            score = ai_modules["qa_system"].get_question_quality_score(prompt)
            if score >= 15:
                st.toast(f"好提问！徽章积分 +{score} 🎖️")

        # 清空按钮
        if st.button("清空对话", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
def find_first_video_in_folder(folder_path):
    if not os.path.exists(folder_path):
        return None
    video_exts = (".mp4", ".mov", ".avi", ".m4v", ".mpeg")
    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith(video_exts):
            return os.path.join(folder_path, file_name)
    return None

def section_header(title):
    st.markdown(f'<div class="subsection-title">{title}</div>', unsafe_allow_html=True)
    st.markdown('<div class="subsection-line"></div>', unsafe_allow_html=True)

def show_centered_image(path, caption="", width=440):
    left, center, right = st.columns([1.2, 2, 1.2])
    with center:
        if os.path.exists(path):
            st.image(path, width=width, caption=caption)
        else:
            st.warning(f"图片未找到：{path}")

def show_two_centered_images(path1, path2, caption1="", caption2="", width=280):
    col1, col2 = st.columns(2)
    with col1:
        if os.path.exists(path1):
            st.image(path1, width=width, caption=caption1)
        else:
            st.warning(f"图片未找到：{path1}")
    with col2:
        if os.path.exists(path2):
            st.image(path2, width=width, caption=caption2)
        else:
            st.warning(f"图片未找到：{path2}")

def show_video_primary_level(folder_path):
    section_header("讲解视频 / Guide Video")
    st.markdown('<div class="video-wrap">', unsafe_allow_html=True)
    video_path = find_first_video_in_folder(folder_path)
    left, center, right = st.columns([1.3, 2.2, 1.3])
    with center:
        if video_path and os.path.exists(video_path):
            with open(video_path, "rb") as f:
                st.video(f.read())
        else:
            st.info(f"该栏目视频文件夹中未找到视频文件：{folder_path}")
    st.markdown('</div>', unsafe_allow_html=True)

def reset_bottom_panels():
    st.session_state.show_data = False
    st.session_state.show_contact = False

def go_home():
    st.session_state.current_page = "home"
    st.session_state.section = None
    st.session_state.level = None
    reset_bottom_panels()

def go_to_museum():
    st.session_state.current_page = "museum"
    st.session_state.section = None
    st.session_state.level = None
    reset_bottom_panels()

def go_to_residence():
    st.session_state.current_page = "residence"
    st.session_state.section = None
    st.session_state.level = None
    reset_bottom_panels()

def go_to_section(section):
    st.session_state.current_page = "section"
    st.session_state.section = section
    st.session_state.level = None
    reset_bottom_panels()

def go_to_level(level):
    st.session_state.current_page = "level"
    st.session_state.level = level
    reset_bottom_panels()
    st.rerun()

def render_title():
    st.markdown('<div class="main-title">“红脉E传”——陈毅旧居红色文化英语传播平台</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-title">以陈毅旧居为核心场景，构建面向小学层级的红色文化英语学习、讲解与传播平台</div>',
        unsafe_allow_html=True
    )

def render_contact_footer():
    st.markdown("---")
    btn_key = f"contact_btn_{st.session_state.current_page}_{st.session_state.section}_{st.session_state.level}"

    if st.button("联系我们 / Contact Us", use_container_width=True, key=btn_key):
        st.session_state.show_contact = not st.session_state.show_contact

    if st.session_state.show_contact:
        st.markdown(
            """
            <div class="footer-contact-box">
                联系电话：17669641585 张广晶
            </div>
            """,
            unsafe_allow_html=True
        )

def render_data_only_for_residence():
    if st.button("查看数据 / View Data", use_container_width=True):
        st.session_state.show_data = not st.session_state.show_data

    if st.session_state.show_data:
        section_header("查看数据 / View Data")
        st.dataframe(DATA_SAMPLE, use_container_width=True)
        chart_df = pd.DataFrame({
            "Level": ["Primary"],
            "Clicks": [320]
        }).set_index("Level")
        st.bar_chart(chart_df)

def render_guide_paragraphs(paragraphs):
    for cn, en in paragraphs:
        st.markdown(f'<div class="cn">{cn}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="en">{en}</div>', unsafe_allow_html=True)

def render_word_list(items):
    for en_text, cn_text in items:
        st.markdown(f"- **{en_text}** = {cn_text}")

def render_platform_task(task, section, level):
    section_header("平台任务 / Platform Task")
    st.markdown(f"**{task['题目_cn']}**")
    st.markdown(task["题目_en"])
    
    # 获取用户ID
    user_id = st.session_state.user_id
    
    choice = st.radio(
        "请选择答案 / Choose an answer",
        task["选项"],
        index=None,
        key=f"{section}_{level}_radio"
    )
    
    if choice is not None:
        submit_key = f"{section}_{level}_submit"
        if st.button("✅ 提交答案", key=submit_key, use_container_width=True):
            is_correct = (choice == task["答案"])
            
            # 记录答题结果（用于徽章）
            ai_modules["badge_system"].record_answer(
                user_id, is_correct, task['题目_cn'], section
            )
            
            if is_correct:
                st.balloons()
                st.success("✓ 回答正确 / Correct!")
                
                # AI生成生动解析
                explanation = ai_modules["quiz_explainer"].explain_answer(
                    question=task['题目_cn'],
                    user_answer=choice,
                    correct_answer=task['答案'],
                    context=f"这是关于{section}的学习",
                    is_correct=True
                )
                with st.expander("🎯 小红星解析 / Explanation", expanded=True):
                    st.info(explanation)
            else:
                st.error(f"✗ 回答有误 / Incorrect. 正确答案是：{task['答案']}")
                
                # AI生成错题解析
                explanation = ai_modules["quiz_explainer"].explain_answer(
                    question=task['题目_cn'],
                    user_answer=choice,
                    correct_answer=task['答案'],
                    context=f"这是关于{section}的学习",
                    is_correct=False
                )
                with st.expander("📖 小红星来帮你 / Let me help you", expanded=True):
                    st.warning(explanation)
                
                # 记录错题用于后续个性化测试
                ai_modules["adaptive_test"].record_mistake(
                    user_id, task['题目_cn'], choice, task['答案'], section
                )

def render_checkin_task(task_tuple):
    cn_text, en_text = task_tuple
    section_header("打卡任务 / Check-in Task")
    st.markdown('<div class="notice-box">', unsafe_allow_html=True)
    st.markdown(cn_text)
    st.markdown(en_text)
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# 页面
# =========================
def render_home():
    render_title()
    st.markdown('<div class="page-tag">首页 / Home</div>', unsafe_allow_html=True)

    show_centered_image(IMAGE_PATHS["museum_gate_1"], "纪念馆入口图片", width=420)

    st.markdown("## the Memorial Hall of the Former Headquarters of the East China Field Army and the Former Military Headquarters of the New Fourth Army")
    st.markdown("## 华东野战军总部旧址暨新四军军部旧址纪念馆")

    if st.button("进入纪念馆 / Enter Memorial Hall", use_container_width=True):
        go_to_museum()
        st.rerun()

    render_contact_footer()

def render_museum():
    render_title()
    st.markdown('<div class="page-tag">纪念馆页面 / Memorial Hall</div>', unsafe_allow_html=True)

    if st.button("← 返回首页 / Back to Home"):
        go_home()
        st.rerun()

    show_centered_image(IMAGE_PATHS["chenyi_home"], "陈毅旧居图片", width=430)

    st.markdown("## Chen Yi’s Former Residence / 陈毅旧居")

    if st.button("进入陈毅旧居 / Enter Chen Yi’s Former Residence", use_container_width=True):
        go_to_residence()
        st.rerun()

    render_contact_footer()

def render_residence():
    render_title()
    st.markdown('<div class="page-tag">陈毅旧居 / Chen Yi’s Former Residence</div>', unsafe_allow_html=True)

    if st.button("← 返回纪念馆 / Back to Memorial Hall"):
        go_to_museum()
        st.rerun()

    st.markdown("## 五大主题 / Five Thematic Modules")
    st.markdown("请选择一个主题进入学习。")

    for sec in SECTIONS:
        if st.button(sec, key=f"theme_{sec}", use_container_width=True):
            go_to_section(sec)
            st.rerun()

    render_data_only_for_residence()
    render_contact_footer()

def render_section():
    section = st.session_state.section

    render_title()
    st.markdown('<div class="page-tag">主题页面 / Section Page</div>', unsafe_allow_html=True)

    if st.button("← 返回五大主题 / Back to Themes"):
        go_to_residence()
        st.rerun()

    st.markdown(f'<div class="section-title">{section}</div>', unsafe_allow_html=True)

    images = SECTION_IMAGES.get(section, [])
    if len(images) == 1:
        show_centered_image(images[0], "主题图片", width=420)
    elif len(images) == 2:
        show_two_centered_images(images[0], images[1], "主题图片1", "主题图片2", width=260)


    st.markdown("---")
    st.info("当前可用层级：小学层 / Primary Level")
    
    if st.button("📖 进入学习 / Start Learning", use_container_width=True):
        go_to_level("小学层 / Primary Level")
        st.rerun()
    
    render_contact_footer()

def render_level():
    section = st.session_state.section
    level = st.session_state.level
    data = CONTENT[section][level]

    render_title()
    st.markdown('<div class="page-tag">分层学习页面 / Level Page</div>', unsafe_allow_html=True)

    if st.button("← 返回主题页 / Back to Section"):
        st.session_state.current_page = "section"
        st.session_state.level = None
        reset_bottom_panels()
        st.rerun()

    st.markdown(f'<div class="section-title">{level}</div>', unsafe_allow_html=True)

    # 小学层显示视频
    show_video_primary_level(VIDEO_FOLDERS[section])

    title_cn, title_en = data["标题 / Title"]
    section_header("标题 / Title")
    st.markdown(f"### {title_cn}")
    st.markdown(f"**{title_en}**")

    section_header("导览文案 / Guide Text")
    render_guide_paragraphs(data["导览文案 / Guide Text"])

    if "词汇卡 / Word Cards" in data:
        section_header("词汇卡 / Word Cards")
        render_word_list(data["词汇卡 / Word Cards"])

    if "平台任务 / Platform Task" in data:
        render_platform_task(data["平台任务 / Platform Task"], section, level)

    if "打卡任务 / Check-in Task" in data:
        render_checkin_task(data["打卡任务 / Check-in Task"])

    render_contact_footer()

# =========================
# 路由
# =========================
# 关键：先渲染侧边栏 AI，再渲染主页面内容
render_ai_sidebar()
if st.session_state.current_page == "home":
    render_home()
elif st.session_state.current_page == "museum":
    render_museum()
elif st.session_state.current_page == "residence":
    render_residence()
elif st.session_state.current_page == "section":
    render_section()
elif st.session_state.current_page == "level":
    render_level()