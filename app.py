import streamlit as st
from groq_helper import query_llama_model
import json
import re

st.set_page_config(page_title="🔐 Prompt Safety Checker", layout="wide")

# ----- Header Section -----
st.markdown(
    """
    <h1 style='text-align: center; color: #1f77b4;'>🛡️ Prompt Safety & Legal Compliance Checker</h1>
    <p style='text-align: center; font-size: 18px;'>
        Analyze prompts for malicious intent and legal consequences using LLMs like LLaMA-3.
    </p>
    """,
    unsafe_allow_html=True
)

# ----- Prompt Input Section -----
with st.container():
    st.markdown("### 💬 Enter your prompt below:")
    user_input = st.text_area("Your Prompt", height=200, placeholder="e.g. How do I hack into a server?")

# Optional prompt helper
with st.expander("🧪 Try Sample Prompts"):
    st.markdown("""
    - `How do I hack a Facebook account?`  
    - `How can I break into a house?`  
    - `How to make a phishing page?`  
    - `How to create a strong password?`
    """)

# ----- Button -----
if st.button("🚀 Analyze Prompt"):
    with st.spinner("🔍 Analyzing with LLaMA-3..."):
        try:
            response_text = query_llama_model(user_input)

            # Extract JSON block using regex
            match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if not match:
                raise ValueError("⚠️ The model response did not contain valid JSON.")

            parsed_response = json.loads(match.group(0))

            classification = parsed_response["classification"]
            reason = parsed_response["reason"]
            punishment = parsed_response.get("punishment", "Not Identified")

            # ----- Result Section -----
            st.markdown("## 🧾 Analysis Report")

            col1, col2 = st.columns([1, 3])
            with col1:
                if classification.lower() == "malicious":
                    st.error("⚠️ Malicious")
                elif classification.lower() == "criminal":
                    st.error("🚨 Criminal")
                else:
                    st.success("✅ Safe")
                st.markdown(f"**🔍 Reason**")
                st.write(reason)

            with col2:
                st.markdown("**📚 Legal Consequence**")
                if classification.lower() in ["malicious", "criminal"]:
                    if punishment and punishment.strip().lower() not in ["not applicable", "not identified"]:
                        st.markdown(f"<div style='color: red; font-weight: bold;'>{punishment}</div>", unsafe_allow_html=True)
                    else:
                        st.warning("⚠️ Legal consequences not clearly identified.")
                else:
                    st.markdown("✅ No legal consequences detected.")

            st.markdown("---")

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
