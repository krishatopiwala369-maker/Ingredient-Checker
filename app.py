import streamlit as st
import requests
from PIL import Image
import io
import time
from datetime import datetime

# Page setup
st.set_page_config(page_title="Ingredient Checker", page_icon="🌿", layout="centered")

# Session state
if "history" not in st.session_state:
    st.session_state.history = []
if "selected" not in st.session_state:
    st.session_state.selected = None

# 🎨 Theme
theme = st.radio("🎨 Choose Theme", ["Light", "Dark"])

if theme == "Light":
    bg = "linear-gradient(135deg, #e8f5e9, #ffffff)"
    text_color = "#2e7d32"
    card_bg = "rgba(255,255,255,0.9)"
else:
    bg = "linear-gradient(135deg, #1b1b1b, #2c2c2c)"
    text_color = "#ffffff"
    card_bg = "rgba(40,40,40,0.9)"

# Styling
st.markdown(f"""
<style>
[data-testid="stAppViewContainer"] {{
    background: {bg};
    color: {text_color};
}}

.title {{
    text-align: center;
    font-size: 40px;
    font-weight: bold;
}}

.card {{
    padding: 15px;
    border-radius: 16px;
    margin-top: 15px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    background: {card_bg};
}}

</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="title">🌿 Ingredient Checker</div>', unsafe_allow_html=True)

# Profile
st.markdown("### ⚙️ Select what you want to avoid")
avoid_palm = st.checkbox("🌴 Palm Oil")
avoid_maida = st.checkbox("🌾 Maida")
avoid_milk = st.checkbox("🥛 Milk")
avoid_nuts = st.checkbox("🥜 Nuts")

# Ingredient lists
palm_oil_names = ["palm oil", "palmolein", "palm kernel oil", "e471"]
maida_names = ["maida", "refined wheat flour"]
milk_names = ["milk", "whey", "casein"]
nut_names = ["peanut", "cashew", "almond"]

# Info
explanations = {
    "palm oil": "Highly processed and may trigger allergies.",
    "maida": "Refined flour with low nutrients.",
    "milk": "May cause lactose issues.",
    "peanut": "Common allergen.",
    "cashew": "Tree nut allergen."
}

alternatives = {
    "palm oil": "ghee or coconut oil",
    "maida": "whole wheat flour",
    "milk": "almond or oat milk",
    "peanut": "sunflower or pumpkin seeds",
    "cashew": "roasted chana"
}

# Time function
def time_ago(t):
    diff = datetime.now() - t
    if diff.seconds < 60:
        return f"{diff.seconds}s ago"
    elif diff.seconds < 3600:
        return f"{diff.seconds//60}m ago"
    else:
        return f"{diff.seconds//3600}h ago"

# Input
user_input = st.text_area("📝 Enter ingredients:")
uploaded_file = st.file_uploader("📸 Upload image", type=["png","jpg","jpeg"])

image_text = ""

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image)

# Button
if st.button("🔍 Check Ingredients"):

    # Progress animation
    progress = st.progress(0)
    for i in range(100):
        time.sleep(0.01)
        progress.progress(i+1)
    progress.empty()

    # OCR
    if uploaded_file:
        gray = image.convert("L")
        img_bytes = io.BytesIO()
        gray.save(img_bytes, format="PNG")

        res = requests.post(
            "https://api.ocr.space/parse/image",
            files={"file": ("img.png", img_bytes.getvalue())},
            data={"apikey": "helloworld"}
        ).json()

        if not res.get("IsErroredOnProcessing"):
            image_text = res["ParsedResults"][0]["ParsedText"]

    final_text = (user_input + " " + image_text).lower()

    # Detection
    found = []
    if avoid_palm:
        found += [i for i in palm_oil_names if i in final_text]
    if avoid_maida:
        found += [i for i in maida_names if i in final_text]
    if avoid_milk:
        found += [i for i in milk_names if i in final_text]
    if avoid_nuts:
        found += [i for i in nut_names if i in final_text]

    found = list(set(found))

    # 📊 RISK METER
    risk_score = len(found)

    st.markdown("### 📊 Risk Level")
    st.progress(min(risk_score * 25, 100))

    if risk_score == 0:
        st.success("🟢 Low Risk")
    elif risk_score <= 2:
        st.warning("🟡 Medium Risk")
    else:
        st.error("🔴 High Risk")

    # Save history
    st.session_state.history.insert(0, {
        "text": final_text,
        "found": found,
        "time": datetime.now()
    })

    # Results
    if found:
        st.markdown("### 💡 Insights")

        for item in found:
            for key in explanations:
                if key in item:
                    st.markdown(f"""
                    <div class="card">
                        <b>❌ {item}</b><br>
                        👉 {explanations.get(key,"")}<br>
                        💡 Use <b>{alternatives.get(key,"")}</b> instead
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.success("✅ Safe to Use")

# HISTORY
st.markdown("### 🧾 History")

for i, item in enumerate(st.session_state.history[:5]):
    if st.button(f"{time_ago(item['time'])} • {'Not Safe' if item['found'] else 'Safe'}", key=i):
        st.session_state.selected = item

# Details view
if st.session_state.selected:
    data = st.session_state.selected
    st.markdown("### 🔍 Details")

    if data["found"]:
        for item in data["found"]:
            for key in explanations:
                if key in item:
                    st.markdown(f"""
                    <div class="card">
                        <b>❌ {item}</b><br>
                        👉 {explanations.get(key,"")}<br>
                        💡 Use <b>{alternatives.get(key,"")}</b> instead
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.success("✅ Safe")

# Clear
if st.button("🗑️ Clear History"):
    st.session_state.history = []