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

# 经典饮食模式列表
DIET_PATTERNS = [
    "抗炎饮食", "地中海饮食", "DASH", "低升糖饮食", "低碳水化合物饮食",
    "TLC饮食", "MIND饮食", "低FODMAP饮食", "全素/植物性饮食", "古饮食(Paleo)", "肾脏保护饮食"
]

# 用餐时间配置
MEAL_TIMES = {"早餐": "07:00", "午餐": "12:00", "晚餐": "18:00"}


def generate_plan():
    """生成 7 天三餐计划，每餐含 3 道菜、1 主食、1 饮料"""
    plan = []
    for day in range(1, 8):
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
    """Onboarding：收集用户信息和偏好"""
    st.header("欢迎使用备孕食谱制作软件")
    with st.form("onboarding_form"):
        name = st.text_input("姓名")
        age = st.number_input("年龄", min_value=18, max_value=60, value=30)
        height_cm = st.number_input("身高 (cm)", min_value=100.0, max_value=220.0, value=170.0)
        weight_kg = st.number_input("体重 (kg)", min_value=30.0, max_value=200.0, value=60.0)
        body_fat = st.number_input("体脂率 (%)", min_value=0.0, max_value=60.0, value=20.0)
        diet_modes = st.multiselect("选择饮食模式", DIET_PATTERNS)
        tags = st.multiselect(
            "健康标签",
            [
                "超重/肥胖", "肌少症", "认知减退", "桥本氏甲状腺炎", "甲亢", "甲减",
                "血脂异常", "胰岛素抵抗", "肝功能异常", "肾功能不全", "慢性炎症",
                "自身免疫病", "贫血", "血液高凝", "线粒体功能障碍", "糖尿病",
                "糖前期", "内异症", "腺肌症", "多囊", "雌孕激素失衡", "更年期"
            ]
        )
        intolerances = st.multiselect(
            "食物不耐受（中度/重度需剔除）", ["乳糖", "麸质", "坚果", "海鲜"]
        )
        template = st.selectbox("选择餐盘模板", list(TEMPLATE_DEFAULTS.keys()))
        custom = st.checkbox("自定义餐盘配比")
        template_cfg = {}
        if custom:
            st.subheader("自定义餐盘配比(%)")
            for comp, default in TEMPLATE_DEFAULTS[template].items():
                template_cfg[comp] = st.slider(comp, 0, 100, default)
        submitted = st.form_submit_button("生成 7 天食谱")

    if submitted:
        # 计算 BMI
        bmi = round(weight_kg / ((height_cm / 100) ** 2), 1)
        st.session_state.update({
            "onboarded": True,
            "user": {"name": name, "age": age},
            "height_cm": height_cm,
            "weight_kg": weight_kg,
            "body_fat": body_fat,
            "bmi": bmi,
            "diet_modes": diet_modes,
            "tags": tags,
            "intolerances": intolerances,
            "template": template,
            "template_cfg": template_cfg or TEMPLATE_DEFAULTS[template],
            "plan": generate_plan(),
            "day_idx": 0
        })
        st.success("✅ 设置完成！请刷新页面查看食谱。")
        st.stop()


def dashboard():
    """Dashboard：展示基础信息、方案信息及三餐，加餐和左右切换"""
    # 基础信息卡片
    st.subheader("基础信息")
    st.markdown(f"""
- **姓名**: {st.session_state.user['name']}
- **身高**: {st.session_state.height_cm} cm
- **体重**: {st.session_state.weight_kg} kg
- **BMI**: {st.session_state.bmi}
- **体脂率**: {st.session_state.body_fat}%
""")
    st.markdown("---")

    # 方案信息卡片
    st.subheader("方案制定信息")
    st.markdown(f"""
- **饮食模式**: {', '.join(st.session_state.diet_modes) or '无'}
- **健康标签**: {', '.join(st.session_state.tags) or '无'}
- **食物不耐受**: {', '.join(st.session_state.intolerances) or '无'}
- **餐盘模板**: {st.session_state.template}
""")
    st.markdown("---")

    # 重置按钮
    if st.sidebar.button("重置 & 重新设置"):
        for k in [
            "onboarded", "user", "height_cm", "weight_kg", "body_fat",
            "bmi", "diet_modes", "tags", "intolerances", "template",
            "template_cfg", "plan", "day_idx"
        ]:
            st.session_state.pop(k, None)
        st.stop()

    # 左右箭头切换天数
    if 'day_idx' not in st.session_state:
        st.session_state.day_idx = 0
    col_prev, col_title, col_next = st.columns([1, 6, 1])
    with col_prev:
        if st.button("←"):
            st.session_state.day_idx = (st.session_state.day_idx - 1) % 7
            st.stop()
    with col_title:
        st.markdown(f"### 第 {st.session_state.day_idx + 1} 天")
    with col_next:
        if st.button("→"):
            st.session_state.day_idx = (st.session_state.day_idx + 1) % 7
            st.stop()

    # 展示三餐及加餐
    daily = st.session_state.plan[st.session_state.day_idx]
    for meal in ["早餐", "午餐", "晚餐"]:
        m = daily[meal]
        st.subheader(f"{meal} | {m['time']}")
        st.write("**主食**:", m["staple"])
        st.write("**菜品**:")
        for d in m["dishes"]:
            st.write(f"- {d}")
        st.write("**饮料**:", m["beverage"])
        if st.button(f"为{meal} 添加加餐", key=f"snack_{meal}_{st.session_state.day_idx}"):
            snack = choice([s["name"] for s in SNACK_MODULES])
            m["snacks"].append(snack)
            st.stop()
        if m["snacks"]:
            st.write("**加餐**:")
            for s in m["snacks"]:
                st.write(f"- {s}")
        st.markdown("---")


if __name__ == "__main__":
    if "onboarded" not in st.session_state:
        st.session_state.onboarded = False
    if not st.session_state.onboarded:
        onboarding()
    else:
        dashboard()
