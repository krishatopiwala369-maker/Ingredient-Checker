import streamlit as st
import requests
from PIL import Image
import io
import time
from datetime import datetime
from pyzxing import BarCodeReader

# 🌿 Page setup
st.set_page_config(
    page_title="Ingredient Checker",
    page_icon="🌿",
    layout="centered"
)

# 🧠 Session state
if "history" not in st.session_state:
    st.session_state.history = []

if "selected" not in st.session_state:
    st.session_state.selected = None

# 🎨 Theme
theme = st.radio("🎨 Choose Theme", ["Light", "Dark"])

if theme == "Light":
    bg = "linear-gradient(135deg, #e8f5e9, #ffffff)"
    text_color = "#2e7d32"
else:
    bg = "linear-gradient(135deg, #111111, #2c2c2c)"
    text_color = "#ffffff"

# ✨ Styling
st.markdown(f"""
<style>

[data-testid="stAppViewContainer"] {{
    background: {bg};
    color: {text_color};
}}

[data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
}}

[data-testid="stToolbar"] {{
    right: 2rem;
}}

h1, h2, h3, h4, h5, h6, p, label, div, span {{
    color: {text_color} !important;
}}

.title {{
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    margin-bottom: 5px;
}}

.subtitle {{
    text-align: center;
    font-size: 16px;
    opacity: 0.8;
    margin-bottom: 25px;
}}

.stButton > button {{
    border-radius: 12px;
    transition: 0.3s;
    font-weight: bold;
}}

.stButton > button:hover {{
    transform: scale(1.03);
}}

</style>
""", unsafe_allow_html=True)

# 🌿 Title
st.markdown(
    '<div class="title">🌿 Ingredient Checker</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Scan smarter. Eat safer.</div>',
    unsafe_allow_html=True
)

# ⚙️ Preferences
st.markdown("### ⚙️ What do you want to avoid?")

avoid_palm = st.checkbox("🌴 Palm Oil")
avoid_maida = st.checkbox("🌾 Maida")
avoid_milk = st.checkbox("🥛 Milk")
avoid_nuts = st.checkbox("🥜 Nuts")

# 📦 Ingredient lists
palm_oil_names = [

    "palm oil",
    "palmolein",
    "palm kernel oil",
    "palm kernel",
    "palm fruit oil",
    "palm stearin",
    "palm olein",
    "vegetable oil",
    "vegetable fat",
    "hydrogenated vegetable oil",
    "hydrogenated palm oil",
    "fractionated palm oil",
    "modified palm oil",
    "palm shortening",
    "shortening",

    "e471",
    "e472",
    "e481",
    "e482",

    "sodium laureth sulfate",
    "glyceryl stearate",
    "stearic acid",
    "palmitic acid",
    "cetyl alcohol",
    "lauryl alcohol",
    "lauric acid",

    "mono and diglycerides",
    "mono-diglycerides",

    "emulsifier 471",
    "emulsifier 472"
]
maida_names = [

    "maida",
    "refined wheat flour",
    "refined flour",
    "all-purpose flour",
    "bleached flour",
    "white flour",
    "enriched flour",

    "refined cereal flour"
]
milk_names = [

    "milk",
    "milk solids",
    "milk powder",
    "skimmed milk powder",
    "whole milk powder",

    "whey",
    "casein",
    "caseinate",

    "butter",
    "butterfat",
    "cream",
    "cheese",

    "lactose",
    "curd",
    "ghee",
    "yogurt",
    "paneer",

    "milk protein",
    "milk fat"
]

nut_names = [

    "peanut",
    "groundnut",

    "cashew",
    "almond",
    "walnut",
    "hazelnut",
    "pecan",
    "pistachio",
    "macadamia",

    "brazil nut",
    "pine nut",

    "nut paste",
    "mixed nuts",

    "tree nuts"
]

# 💡 Explanations
explanations = {
    "palm oil": "Highly processed and may trigger allergies.",
    "maida": "Refined flour with low nutrients.",
    "milk": "May cause issues for lactose intolerance.",
    "peanut": "Common allergen causing reactions.",
    "cashew": "Tree nut allergen."
}

# 🌿 Alternatives
alternatives = {
    "palm oil": "ghee or coconut oil 🌿",
    "maida": "whole wheat flour 🌾",
    "milk": "almond or oat milk 🥛",
    "peanut": "sunflower or pumpkin seeds 🌻",
    "cashew": "roasted chana 🌰"
}

# ⏳ Time formatter
def time_ago(t):

    diff = datetime.now() - t

    if diff.seconds < 60:
        return f"{diff.seconds}s ago"

    elif diff.seconds < 3600:
        return f"{diff.seconds // 60}m ago"

    else:
        return f"{diff.seconds // 3600}h ago"

# 📝 Manual ingredient input
user_input = st.text_area("📝 Enter ingredients")

# 📸 Ingredient image upload
uploaded_file = st.file_uploader(
    "📸 Upload ingredient image",
    type=["png", "jpg", "jpeg"]
)

# 📦 Barcode image upload
barcode_file = st.file_uploader(
    "📦 Upload barcode image",
    type=["png", "jpg", "jpeg"],
    key="barcode"
)

image_text = ""
barcode_data = ""
reader = BarCodeReader()

# 📦 Barcode scanner
if barcode_file:

    with open("temp_barcode.png", "wb") as f:
        f.write(barcode_file.getbuffer())

    result = reader.decode("temp_barcode.png")

    if result and result[0]["parsed"]:

        barcode_data = result[0]["parsed"]

        st.success(f"📦 Barcode Detected: {barcode_data}")

    else:
        st.error("❌ No barcode detected")


# 📸 Show uploaded ingredient image
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, use_column_width=True)

# 🔍 Main button
if st.button("🔍 Check Ingredients"):

    st.markdown("### 🔍 Scanning ingredients...")

    progress = st.progress(0)

    for i in range(100):
        time.sleep(0.01)
        progress.progress(i + 1)

    progress.empty()

    # 📸 OCR
    if uploaded_file:

        gray = image.convert("L")

        img_bytes = io.BytesIO()

        gray.save(img_bytes, format="PNG")

        response = requests.post(
            "https://api.ocr.space/parse/image",
            files={
                "file": (
                    "img.png",
                    img_bytes.getvalue()
                )
            },
            data={
                "apikey": "helloworld"
            }
        )

        result = response.json()

        if not result.get("IsErroredOnProcessing"):

            image_text = result["ParsedResults"][0]["ParsedText"]

            st.markdown("### 🧾 Extracted Text")
            st.write(image_text)

        else:
            st.error("⚠️ OCR failed")

    # 🧠 Combine text
    final_text = (
        user_input + " " + image_text
    ).lower()

    # 🎯 Detection
    found = []

    if avoid_palm:
        found += [
            i for i in palm_oil_names
            if i in final_text
        ]

    if avoid_maida:
        found += [
            i for i in maida_names
            if i in final_text
        ]

    if avoid_milk:
        found += [
            i for i in milk_names
            if i in final_text
        ]

    if avoid_nuts:
        found += [
            i for i in nut_names
            if i in final_text
        ]

    found = list(set(found))

    # 📊 Risk Meter
    risk_score = len(found)

    st.markdown("### 📊 Risk Level")

    st.progress(min(risk_score * 25, 100))

    if risk_score == 0:
        st.success("🟢 Low Risk")

    elif risk_score <= 2:
        st.warning("🟡 Medium Risk")

    else:
        st.error("🔴 High Risk")

    # 🧾 Save history
    st.session_state.history.insert(0, {
        "text": final_text,
        "found": found,
        "time": datetime.now()
    })

    # 💡 Results
    if found:

        st.markdown("### 💡 Insights")

        for item in found:

            for key in explanations:

                if key in item:

                    st.info(f"""
❌ {item}

👉 {explanations.get(key,"")}

💡 Use {alternatives.get(key,"")} instead
""")

    else:
        st.success("✅ Safe to Use")

# 🧾 History
st.markdown("### 🧾 Scan History")

for i, item in enumerate(st.session_state.history[:5]):

    label = (
        f"{time_ago(item['time'])} • "
        f"{'Not Safe' if item['found'] else 'Safe'}"
    )

    if st.button(label, key=i):

        st.session_state.selected = item

# 🔍 Previous details
if st.session_state.selected:

    data = st.session_state.selected

    st.markdown("### 🔍 Previous Scan Details")

    if data["found"]:

        for item in data["found"]:

            for key in explanations:

                if key in item:

                    st.info(f"""
❌ {item}

👉 {explanations.get(key,"")}

💡 Use {alternatives.get(key,"")} instead
""")

    else:
        st.success("✅ Safe")

# 🗑️ Clear history
if st.button("🗑️ Clear History"):
    st.session_state.history = []

# 🌿 Footer
st.markdown(
    "<center>🌿 Made for safer choices</center>",
    unsafe_allow_html=True
)