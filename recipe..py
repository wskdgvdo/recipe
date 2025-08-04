# app.py
import streamlit as st
from random import seed, sample, choice

# 保证随机结果可复现
seed(42)

# 样例菜品、主食和饮料模块
DISH_MODULES = [
    "三文鱼烤蔬菜", "蒜蓉西兰花", "红烧豆腐", "清炒菠菜", "麻婆茄子",
    "香菇油菜", "土豆炖牛肉", "清蒸鸡腿", "椒盐虾", "蒜香菌菇"
]
STAPLE_MODULES = ["糙米饭", "全麦面包", "玉米粥", "红薯", "藜麦饭"]
BEVERAGE_MODULES = ["白开水", "柠檬水", "无糖豆浆", "绿茶", "淡咖啡"]
SNACK_MODULES = [
    {"name": "希腊酸奶坚果杯"},
    {"name": "燕麦香蕉能量球"},
    {"name": "水果沙拉杯"}
]

# 经典餐盘模板及默认配比
TEMPLATE_DEFAULTS = {
    "4:3:3 餐盘": {"碳水化合物": 40, "蛋白质": 30, "脂肪": 30},
    "2:1:1 餐盘": {"蔬菜": 50, "蛋白质": 25, "碳水化合物": 25},
    "地中海餐盘": {"蔬菜": 50, "全谷": 20, "鱼禽蛋白": 15, "健康脂肪": 15},
    "四分餐盘": {"蔬菜": 25, "水果": 25, "全谷": 25, "蛋白": 25}
}

# 饮食模式列表
DIET_PATTERNS = [
    "抗炎饮食", "地中海饮食", "DASH", "低升糖饮食", "低碳水化合物饮食",
    "TLC饮食", "MIND饮食", "低FODMAP饮食", "全素/植物性饮食",
    "古饮食(Paleo)", "肾脏保护饮食"
]

# 用餐时间
MEAL_TIMES = {"早餐": "07:00", "午餐": "12:00", "晚餐": "18:00"}


def generate_plan():
    """生成 7 天三餐计划，每餐含 3 道菜、1 主食、1 饮料"""
    plan = []
    for _ in range(7):
        daily = {}
        for meal in ["早餐", "午餐", "晚餐"]:
            dishes = sample(DISH_MODULES, k=3)
            staple = choice(STAPLE_MODULES)
            beverage = choice(BEVERAGE_MODULES)
            daily[meal] = {
                "time": MEAL_TIMES[meal],
                "dishes": dishes,
                "staple": staple,
                "beverage": beverage,
                "snacks": []
            }
        plan.append(daily)
    return plan


def onboarding():
    """信息录入首页：基础信息 & 方案制定"""
    st.header("欢迎使用备孕食谱制作软件")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("基础信息")
        name = st.text_input("姓名")
        height_cm = st.number_input("身高 (cm)", 100.0, 220.0, 165.0)
        weight_kg = st.number_input("体重 (kg)", 30.0, 200.0, 55.0)
        body_fat = st.number_input("体脂率 (%)", 0.0, 60.0, 22.0)
        age = st.number_input("年龄", 18, 60, 28)
        bmi = round(weight_kg / ((height_cm / 100) ** 2), 1) if height_cm > 0 else None
        st.write(f"**BMI**: {bmi}")

    with col2:
        st.subheader("方案制定")
        diet_modes = st.multiselect("饮食模式", DIET_PATTERNS)
        tags = st.multiselect("健康标签", [
            "超重/肥胖", "肌少症", "认知减退", "桥本氏甲状腺炎", "甲亢", "甲减",
            "血脂异常", "胰岛素抵抗", "肝功能异常", "肾功能不全", "慢性炎症",
            "自身免疫病", "贫血", "血液高凝", "线粒体功能障碍", "糖尿病",
            "糖前期", "内异症", "腺肌症", "多囊", "雌孕激素失衡", "更年期"
        ])
        goal = st.text_input("饮食目标 (如：控糖、增肌减脂)")
        intolerances = st.multiselect("食物不耐受（中/重度需剔除）",
                                       ["乳糖", "麸质", "坚果", "海鲜"])
        template = st.selectbox("餐盘模板", list(TEMPLATE_DEFAULTS.keys()))
        custom = st.checkbox("自定义餐盘配比")
        template_cfg = {}
        if custom:
            st.subheader("自定义餐盘配比(%)")
            for comp, default in TEMPLATE_DEFAULTS[template].items():
                template_cfg[comp] = st.slider(comp, 0, 100, default)

    if st.button("生成食谱"):
        st.session_state.update({
            "onboarded": True,
            "user": {"name": name, "age": age},
            "height_cm": height_cm,
            "weight_kg": weight_kg,
            "body_fat": body_fat,
            "bmi": bmi,
            "diet_modes": diet_modes,
            "tags": tags,
            "goal": goal,
            "intolerances": intolerances,
            "template": template,
            "template_cfg": template_cfg or TEMPLATE_DEFAULTS[template],
            "plan": generate_plan(),
            "day_idx": 0
        })
        # 自动跳转到展示页面
        st.experimental_rerun()


def dashboard():
    """食谱展示页面：左右布局显示食物与营养，箭头切换天数"""
    if "day_idx" not in st.session_state:
        st.session_state.day_idx = 0

    col_prev, col_title, col_next = st.columns([1, 6, 1])
    with col_prev:
        if st.button("←"):
            st.session_state.day_idx = (st.session_state.day_idx - 1) % 7
            st.experimental_rerun()
    with col_title:
        st.markdown(f"## 第 {st.session_state.day_idx + 1} 天")
    with col_next:
        if st.button("→"):
            st.session_state.day_idx = (st.session_state.day_idx + 1) % 7
            st.experimental_rerun()

    daily = st.session_state.plan[st.session_state.day_idx]
    for meal in ["早餐", "午餐", "晚餐"]:
        m = daily[meal]
        st.subheader(f"{meal} | {m['time']}")
        left, right = st.columns([3, 1])
        with left:
            st.write("**主食**:", m["staple"])
            st.write("**菜品**:")
            for d in m["dishes"]:
                st.write(f"- {d}")
            st.write("**饮料**:", m["beverage"])
            if st.button(f"为{meal} 添加加餐", k
