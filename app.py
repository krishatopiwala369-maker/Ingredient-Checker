import streamlit as st
st.caption("Quickly check if your food contains palm oil or maida")

# Page config
st.set_page_config(page_title="Ingredient Checker", page_icon="🌿", layout="centered")

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f6;
    }
    .title {
        font-size: 40px;
        font-weight: bold;
        color: #2e7d32;
        text-align: center;
    }
    .subtitle {
        text-align: center;
        color: #555;
        margin-bottom: 20px;
    }
    .stTextArea textarea {
        border-radius: 10px;
        border: 1px solid #ccc;
        padding: 10px;
    }
    .stButton>button {
        background-color: #2e7d32;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #1b5e20;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Title section
st.markdown('<div class="title">🌿 Ingredient Checker</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Check for hidden harmful ingredients like palm oil & maida</div>', unsafe_allow_html=True)

# Ingredient lists
palm_oil_names = [
    "palm oil", "palmolein", "palm kernel oil", "palm kernel",
    "palm stearin", "palmitic acid", "palm fatty acid",
    "glyceryl stearate", "vegetable oil (palm)", "palm extract"
]

maida_names = [
    "maida", "refined wheat flour", "white flour",
    "bleached flour", "enriched flour"
]

# Input box
user_input = st.text_area("📝 Enter ingredients here:")

# Button
if st.button("🔍 Check Ingredients"):
    text = user_input.lower()

    found_palm = []
    found_maida = []

    for item in palm_oil_names:
        if item in text:
            found_palm.append(item)

    for item in maida_names:
        if item in text:
            found_maida.append(item)

    st.markdown("---")

    if found_palm or found_maida:
        st.error("❌ Not Safe")

        if found_palm:
            st.markdown("### 🌴 Palm Oil Detected")
            for item in found_palm:
                st.write(f"• {item}")

        if found_maida:
            st.markdown("### 🌾 Maida Detected")
            for item in found_maida:
                st.write(f"• {item}")

    else:
        st.success("✅ Safe to Use")

# Footer
st.markdown("---")
st.markdown("<center>Made with 🌿 for safer choices</center>", unsafe_allow_html=True)