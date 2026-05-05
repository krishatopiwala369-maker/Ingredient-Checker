import streamlit as st
import requests
from PIL import Image
import io

# Page setup
st.set_page_config(page_title="Ingredient Checker", page_icon="🌿", layout="centered")

# Styling
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #e8f5e9, #ffffff);
}
.title {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    color: #2e7d32;
}
.subtitle {
    text-align: center;
    color: #555;
    margin-bottom: 25px;
}
.safe-box {
    padding: 15px;
    border-radius: 12px;
    background-color: #e8f5e9;
    color: #2e7d32;
    margin-top: 20px;
}
.not-safe-box {
    padding: 15px;
    border-radius: 12px;
    background-color: #ffebee;
    color: #c62828;
    margin-top: 20px;
}
mark {
    background-color: #ffcdd2;
    padding: 2px 5px;
    border-radius: 4px;
}
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="title">🌿 Ingredient Checker</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Type or scan ingredients</div>', unsafe_allow_html=True)

# 🧍‍♀️ Allergy Profile Mode
st.markdown("### ⚙️ Select what you want to avoid")

avoid_palm = st.checkbox("🌴 Palm Oil")
avoid_maida = st.checkbox("🌾 Maida (Refined Flour)")
avoid_milk = st.checkbox("🥛 Milk")
avoid_nuts = st.checkbox("🥜 Nuts")

# Ingredient lists
palm_oil_names = [
    "palm oil", "palmolein", "palm kernel oil", "palm kernel",
    "palm stearin", "palmitic acid", "glyceryl stearate",
    "vegetable oil (palm)", "e471", "e472", "e481",
    "shortening", "vegetable fat"
]

maida_names = [
    "maida", "refined wheat flour", "white flour",
    "all-purpose flour", "enriched flour"
]

milk_names = [
    "milk", "milk solids", "whey", "casein", "butter", "cheese"
]

nut_names = [
    "almond", "cashew", "peanut", "walnut", "hazelnut"
]

# Highlight function
def highlight_text(text, words):
    for word in words:
        text = text.replace(word, f"<mark>{word}</mark>")
    return text

# Text input
user_input = st.text_area("📝 Enter ingredients:")

# Image upload
uploaded_file = st.file_uploader("📸 Upload ingredient image", type=["png", "jpg", "jpeg"])

image_text = ""

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Convert to grayscale
    gray_image = image.convert("L")

    img_bytes = io.BytesIO()
    gray_image.save(img_bytes, format="PNG")
    img_bytes = img_bytes.getvalue()

    with st.spinner("🔍 Reading image..."):
        response = requests.post(
            "https://api.ocr.space/parse/image",
            files={"file": ("image.png", img_bytes)},
            data={"apikey": "helloworld", "language": "eng"}
        )

        result = response.json()

        if result.get("IsErroredOnProcessing") == False:
            parsed = result.get("ParsedResults")
            if parsed:
                image_text = parsed[0].get("ParsedText", "")
                st.markdown("### 🧾 Extracted Text:")
                st.write(image_text)
            else:
                st.error("⚠️ No text found in image")
        else:
            st.error("⚠️ OCR failed. Try a clearer image")

# Combine inputs
final_text = (user_input + " " + image_text).lower()

# Button
if st.button("🔍 Check Ingredients"):
    found = []

    if avoid_palm:
        for item in palm_oil_names:
            if item in final_text:
                found.append(item)

    if avoid_maida:
        for item in maida_names:
            if item in final_text:
                found.append(item)

    if avoid_milk:
        for item in milk_names:
            if item in final_text:
                found.append(item)

    if avoid_nuts:
        for item in nut_names:
            if item in final_text:
                found.append(item)

    found = list(set(found))  # remove duplicates

    if found:
        count = len(found)

        if count >= 3:
            risk = "🚨 High Risk"
        else:
            risk = "⚠️ Medium Risk"

        st.markdown(
            f'<div class="not-safe-box">❌ Not Safe<br>{"<br>".join(found)}</div>',
            unsafe_allow_html=True
        )

        st.markdown(f"### {risk}")

        highlighted = highlight_text(final_text, found)
        st.markdown("### 🔍 Detected in your input:")
        st.markdown(highlighted, unsafe_allow_html=True)

    else:
        st.markdown('<div class="safe-box">✅ Safe to Use</div>', unsafe_allow_html=True)
        st.markdown("### 🟢 Low Risk")

# Footer
st.markdown("<br><center>🌿 Made for safer choices</center>", unsafe_allow_html=True)