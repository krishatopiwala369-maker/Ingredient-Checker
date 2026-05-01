import streamlit as st

# Page setup
st.set_page_config(page_title="Ingredient Checker", page_icon="🌿", layout="centered")

# CSS Styling
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #e8f5e9, #ffffff);
}

[data-testid="stHeader"] {
    background: transparent;
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

.stTextArea textarea {
    border-radius: 12px;
    border: 1px solid #c8e6c9;
    padding: 10px;
}

.stButton>button {
    background: linear-gradient(90deg, #66bb6a, #43a047);
    color: white;
    border-radius: 12px;
    padding: 10px 20px;
    border: none;
    font-size: 16px;
}

.stButton>button:hover {
    background: linear-gradient(90deg, #43a047, #2e7d32);
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
st.markdown('<div class="subtitle">Check for palm oil & maida in seconds</div>', unsafe_allow_html=True)

# 🔍 Hidden ingredient names

palm_oil_names = [
    "palm oil", "palmolein", "palm kernel oil", "palm kernel",
    "palm stearin", "palmitic acid", "palm fatty acid",
    "glyceryl stearate", "vegetable oil (palm)", "palm extract",
    "sodium lauryl sulfate", "sodium laureth sulfate",
    "cetyl alcohol", "stearic acid", "elaeis guineensis",
    "e471", "e472", "e481"
]

maida_names = [
    "maida", "refined wheat flour", "white flour",
    "bleached flour", "enriched flour",
    "wheat flour (refined)", "all-purpose flour",
    "plain flour"
]

# Highlight function
def highlight_text(text, words):
    highlighted = text
    for word in words:
        highlighted = highlighted.replace(
            word,
            f"<mark>{word}</mark>"
        )
    return highlighted

# Input
user_input = st.text_area("📝 Enter ingredients:")

# Button
if st.button("🔍 Check Ingredients"):
    text = user_input.lower()
    found = []

    for item in palm_oil_names + maida_names:
        if item in text:
            found.append(item)

    if found:
        st.markdown(
            f'<div class="not-safe-box">❌ Not Safe<br>{"<br>".join(found)}</div>',
            unsafe_allow_html=True
        )

        highlighted = highlight_text(text, found)
        st.markdown("### 🔍 Detected in your input:")
        st.markdown(highlighted, unsafe_allow_html=True)

    else:
        st.markdown(
            '<div class="safe-box">✅ Safe to Use</div>',
            unsafe_allow_html=True
        )

# Footer
st.markdown("<br><center>🌿 Made for safer choices</center>", unsafe_allow_html=True)