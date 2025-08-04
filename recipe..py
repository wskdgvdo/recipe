# app.py
import streamlit as st
from random import seed

seed(42)

# 样例餐品模块
MEAL_MODULES = [
    {"id": "meal1", "name": "三文鱼藜麦沙拉", "ingredients": ["三文鱼", "藜麦", "菠菜", "橄榄油"], "recipe": "将三文鱼煎熟，与煮熟的藜麦和菠菜拌匀，淋上橄榄油", "nutrition": {"热量": 350, "蛋白": 25, "碳水": 30, "脂肪": 15}},
    {"id": "meal2", "name": "鸡胸肉西兰花", "ingredients": ["鸡胸肉", "西兰花", "蒜", "少许橄榄油"], "recipe": "鸡胸肉清蒸后切片，与焯水西兰花和蒜炒匀", "nutrition": {"热量": 300, "蛋白": 30, "碳水": 10, "脂肪": 12}},
    {"id": "meal3", "name": "牛油果全麦三明治", "ingredients": ["全麦面包", "牛油果", "番茄", "生菜"], "recipe": "将牛油果捣碎，涂抹于全麦面包，夹入番茄和生菜", "nutrition": {"热量": 400, "蛋白": 15, "碳水": 45, "脂肪": 18}},
    {"id": "meal4", "name": "扁豆南瓜汤", "ingredients": ["扁豆", "南瓜", "洋葱", "橄榄油"], "recipe": "所有材料煮熟后搅拌成浓汤", "nutrition": {"热量": 250, "蛋白": 12, "碳水": 35, "脂肪": 8}},
    {"id": "meal5", "name": "牛肉藜麦碗", "ingredients": ["瘦牛肉", "藜麦", "彩椒", "洋葱"], "recipe": "牛肉炒熟与藜麦和彩椒洋葱同碗", "nutrition": {"热量": 380, "蛋白": 28, "碳水": 32, "脂肪": 14}},
    {"id": "meal6", "name": "豆腐鸡腿菇煲", "ingredients": ["豆腐", "鸡腿菇", "胡萝卜", "生抽"], "recipe": "所有材料炖煮20分钟", "nutrition": {"热量": 270, "蛋白": 18, "碳水": 25, "脂肪": 10}}
]

SNACK_MODULES = [
    {"id": "snack1", "name": "希腊酸奶坚果杯", "energy": 150},
    {"id": "snack2", "name": "燕麦香蕉能量球", "energy": 120},
    {"id": "snack3", "name": "水果沙拉杯", "energy": 100}
]

# 生成默认 7 天食谱计划
def generate_plan():
    plan = []
    for day in range(1, 8):
        idx = (day - 1) * 3
        meals = [
            MEAL_MODULES[idx % len(MEAL_MODULES)],
            MEAL_MODULES[(idx+1) % len(MEAL_MODULES)],
            MEAL_MODULES[(idx+2) % len(MEAL_MODULES)]
        ]
        plan.append({"day": day, "meals": meals, "snacks": []})
    return plan

# Onboarding 表单
def onboarding():
    st.header("欢迎使用备孕食谱制作软件")
    with st.form("onboarding_form"):
        name = st.text_input("姓名")
        age = st.number_input("年龄", min_value=18, max_value=60, value=30)
        tags = st.multiselect(
            "健康标签",
            ["超重/肥胖", "肌少症", "认知减退", "桥本氏甲状腺炎", "甲亢", "甲减",
             "血脂异常", "胰岛素抵抗", "肝功能异常", "肾功能不全", "慢性炎症",
             "自身免疫病", "贫血", "血液高凝", "线粒体功能障碍", "糖尿病",
             "糖前期", "内异症", "腺肌症", "多囊", "雌孕激素失衡", "更年期"]
        )
        intolerances = st.multiselect(
            "食物不耐受（中度/重度将被剔除）", ["乳糖", "麸质", "坚果", "海鲜"]
        )
        template = st.selectbox(
            "选择餐盘模板", ["4:3:3 餐盘", "2:1:1 餐盘", "地中海餐盘", "四分餐盘"]
        )
        submitted = st.form_submit_button("提交并生成食谱")
    if submitted:
        st.session_state.onboarded = True
        st.session_state.user = {"name": name, "age": age}
        st.session_state.tags = tags
        st.session_state.intolerances = intolerances
        st.session_state.template = template
        st.session_state.plan = generate_plan()
        st.experimental_rerun()

# Dashboard 页面
def dashboard():
    st.sidebar.title("设置")
    st.sidebar.write(f"用户：{st.session_state.user['name']}，年龄：{st.session_state.user['age']}")
    if st.sidebar.button("重置 & 重新设置"):
        for key in ['onboarded', 'user', 'tags', 'intolerances', 'template', 'plan']:
            if key in st.session_state:
                del st.session_state[key]
        st.experimental_rerun()

    day = st.sidebar.slider("选择天数", 1, 7, 1)
    st.sidebar.write("已选模板：", st.session_state.template)

    st.title(f"第 {day} 天 食谱计划")
    cols = st.columns(3)
    meal_labels = ["早餐", "午餐", "晚餐"]
    for i, col in enumerate(cols):
        meal = st.session_state.plan[day-1]['meals'][i]
        with col:
            st.subheader(meal_labels[i])
            with st.expander(meal['name']):
                st.write("**食材**")
                for ing in meal['ingredients']:
                    if ing in st.session_state.intolerances:
                        st.markdown(f"- **<span style='color:red'>{ing}</span>**", unsafe_allow_html=True)
                    else:
                        st.write(f"- {ing}")
                st.write("**做法：**", meal['recipe'])
                st.write("**营养（kcal / g）：**", meal['nutrition'])

    st.markdown("---")
    st.subheader("加餐")
    if st.button("添加加餐"):
        snack = st.selectbox("选择零食", SNACK_MODULES, format_func=lambda x: x['name'])
        st.session_state.plan[day-1]['snacks'].append(snack)
        st.experimental_rerun()
    if st.session_state.plan[day-1]['snacks']:
        for s in st.session_state.plan[day-1]['snacks']:
            st.write(f"- {s['name']}，{s['energy']} kcal")

# 主入口
if __name__ == '__main__':
    if 'onboarded' not in st.session_state:
        st.session_state.onboarded = False
    if not st.session_state.onboarded:
        onboarding()
    else:
        dashboard()
