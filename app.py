# Dashboard Insight Assistant (Governance-Safe MVP)
# Streamlit-based local prototype
# ---------------------------------
# This MVP demonstrates end-to-end flow:
# Upload dashboard image -> Mask sensitive text -> OCR -> Rule-based insight generation
# Local-only, no retention, no learning

import streamlit as st
from PIL import Image
import pytesseract
import re
import io

# -----------------------------
# Configuration / Governance
# -----------------------------
st.set_page_config(page_title="Dashboard Insight Assistant", layout="centered")

st.markdown("""
### Dashboard Insight Assistant
**Generated locally · No data is stored · For internal use only**
""")

# -----------------------------
# Helper Functions
# -----------------------------

def mask_sensitive_text(text: str) -> str:
    """Mask basic sensitive patterns using regex (demo-level)."""
    patterns = {
        r"\\b\\d{12,16}\\b": "[MASKED_ACCOUNT]",
        r"\\b[A-Z]{1,2}\\d{6,8}\\b": "[MASKED_ID]",
        r"\\$\\s?\\d+(?:,\\d{3})*(?:\\.\\d{2})?": "[MASKED_AMOUNT]"
    }
    masked_text = text
    for pattern, replacement in patterns.items():
        masked_text = re.sub(pattern, replacement, masked_text)
    return masked_text


def extract_text_from_image(image: Image.Image) -> str:
    """Run OCR on uploaded image."""
    return pytesseract.image_to_string(image)


def generate_insights(text: str) -> dict:
    """Rule/template-based insight generation."""
    insights = {
        "Overview": "This dashboard provides a consolidated view of operational performance across multiple teams.",
        "Key Changes": "Several metrics show variation compared to previous periods, indicating potential shifts in workload or performance.",
        "Possible Drivers": "Observed changes may be driven by operational volume fluctuations, resource allocation, or process bottlenecks.",
        "Monitoring Recommendations": "It is recommended to continue monitoring key KPIs, particularly those approaching predefined thresholds."
    }
    return insights

# -----------------------------
# UI Flow
# -----------------------------

uploaded_file = st.file_uploader("Upload a dashboard screenshot", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Dashboard", use_column_width=True)

    if st.button("Generate Summary"):
        with st.spinner("Processing locally..."):
            raw_text = extract_text_from_image(image)
            masked_text = mask_sensitive_text(raw_text)
            insights = generate_insights(masked_text)

        st.success("Summary generated (no data stored)")

        st.markdown("---")
        st.subheader("Executive Summary")
        st.write(insights["Overview"])

        st.subheader("Key Changes")
        st.write(insights["Key Changes"])

        st.subheader("Possible Drivers")
        st.write(insights["Possible Drivers"])

        st.subheader("Monitoring Recommendations")
        st.write(insights["Monitoring Recommendations"])

        with st.expander("View masked extracted text (for audit/demo)"):
            st.text(masked_text)

# -----------------------------
# Footer / Disclaimer
# -----------------------------
st.markdown("""
---
*This tool runs entirely on-device. No inputs or outputs are stored unless explicitly saved by the user.*
""")
