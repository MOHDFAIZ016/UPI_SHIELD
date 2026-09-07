import os
import json
import re
import streamlit as st
from google import genai
from google.genai import types

# Page Setup
st.set_page_config(
    page_title="UPI-Shield | Cognitive Fraud Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom High-Impact Cyber/FinTech Design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Background and Layout Cleanups */
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgba(14, 165, 233, 0.08) 0%, transparent 40%),
                    radial-gradient(circle at 90% 80%, rgba(99, 102, 241, 0.08) 0%, transparent 40%),
                    #0b0f19;
        color: #f1f5f9;
    }

    /* Hero Header Card */
    .hero-container {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 32px;
        margin-bottom: 24px;
        backdrop-filter: blur(12px);
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(14, 165, 233, 0.15);
        color: #38bdf8;
        border: 1px solid rgba(56, 189, 248, 0.3);
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin-bottom: 16px;
    }

    .hero-title {
        font-size: 38px;
        font-weight: 800;
        background: linear-gradient(120deg, #ffffff 30%, #94a3b8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
        line-height: 1.2;
    }

    .hero-desc {
        color: #94a3b8;
        font-size: 16px;
        max-width: 700px;
        line-height: 1.6;
        margin: 0;
    }

    /* Glass Panels */
    .glass-card {
        background: rgba(17, 24, 39, 0.75);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 16px;
        padding: 22px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(10px);
        margin-bottom: 18px;
    }

    /* Artifact Pills */
    .entity-tag {
        display: inline-block;
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.12);
        color: #e2e8f0;
        padding: 6px 12px;
        border-radius: 8px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 12px;
        margin: 4px;
    }

    /* Metric Redesign */
    div[data-testid="stMetric"] {
        background: rgba(17, 24, 39, 0.75);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 16px 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }

    /* Neon Primary Button */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%);
        color: #ffffff;
        font-weight: 700;
        font-size: 16px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 12px;
        padding: 14px 28px;
        box-shadow: 0 10px 25px -5px rgba(2, 132, 199, 0.45);
        transition: all 0.25s ease;
    }

    div.stButton > button:first-child:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 30px -5px rgba(2, 132, 199, 0.65);
        border-color: rgba(255, 255, 255, 0.4);
    }

    /* Tabs Customization */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 8px 18px;
        background: rgba(30, 41, 59, 0.5);
        color: #94a3b8;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .stTabs [aria-selected="true"] {
        background: rgba(14, 165, 233, 0.2) !important;
        color: #38bdf8 !important;
        border-color: rgba(56, 189, 248, 0.4) !important;
    }
</style>
""", unsafe_allow_html=True)
api_key = "AQ.Ab8RN6Idqz5_hkNmHOUDGmbeDua91T6fRbDiGKhg8x8FRGkGJg"

# Hero Banner
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">
        <span style="height: 8px; width: 8px; background-color: #38bdf8; border-radius: 50%; display: inline-block;"></span>
        NPCI / UPI Threat Intelligence Node
    </div>
    <div class="hero-title">UPI-Shield Sentinel</div>
    <p class="hero-desc">
        AI-driven behavioral coercion and social-engineering fraud detection. Evaluates cognitive manipulation vectors, synthetic urgency, and spoofed authority signatures in real time.
    </p>
</div>
""", unsafe_allow_html=True)

# Preset Attack Scenarios
PRESETS = {
    "⚡ Utility Emergency: Electricity Disconnection Scam (High Risk)": (
        "URGENT: Your electricity connection will be disconnected tonight at 9:30 PM "
        "due to pending payment. Immediately pay Rs. 15 to executive via UPI at "
        "ebill-verify@upi to avoid penalty and power cut."
    ),
    "📦 Parcel Delivery: Customs & Logistics Spoof (High Risk)": (
        "SpeedPost Alert: Your parcel #IN8921 is held at regional hub due to invalid address. "
        "Pay Rs. 25 redelivery fee at indiapost-desk@upi within 2 hours or parcel will be returned."
    ),
    "☕ Benign Payment: Shared Dining Expense (Low Risk)": (
        "Hey! Split for last night's dinner came out to Rs. 450 per person. "
        "Send it over GPay or PhonePe whenever you get a chance."
    ),
    "✍️ Custom Transaction Ingestion": ""
}

# Layout Columns
col_main, col_stats = st.columns([2.1, 1], gap="medium")

# Metadata Extractor
def extract_meta_signals(text: str) -> dict:
    upi_ids = re.findall(r'[\w\.\-]+@[\w\-]+', text)
    phone_numbers = re.findall(r'(?:\+91|0)?[6-9]\d{9}', text)
    urgency_words = re.findall(r'\b(urgent|immediate|immediately|penalty|blocked|disconnected|tonight|hours?)\b', text, re.IGNORECASE)
    return {
        "upi_ids": list(set(upi_ids)),
        "phone_numbers": list(set(phone_numbers)),
        "urgency_cues": list(set(urgency_words))
    }

with col_main:
    selected_preset_key = st.selectbox("📂 Ingest Known Attack Vector / Scenario:", list(PRESETS.keys()))
    default_text = PRESETS[selected_preset_key]

    input_message = st.text_area(
        "Payload / Inbound Message Stream:",
        value=default_text,
        height=140,
        placeholder="Paste raw SMS, WhatsApp transcript, or payment request message..."
    )

    analyze_clicked = st.button("⚡ Inspect Threat Signatures", use_container_width=True)

meta = extract_meta_signals(input_message)

with col_stats:
    st.markdown("""
    <div class="glass-card">
        <h4 style="margin: 0 0 12px 0; color: #f8fafc; font-size: 16px;">Telemetry Pre-Scan</h4>
        <div style="color: #64748b; font-size: 13px; margin-bottom: 12px;">Local heuristic metadata parser</div>
    """, unsafe_allow_html=True)
    
    st.markdown("**UPI VPA Targets**")
    if meta["upi_ids"]:
        for upi in meta["upi_ids"]:
            st.markdown(f'<span class="entity-tag">💳 {upi}</span>', unsafe_allow_html=True)
    else:
        st.caption("No explicit VPA patterns identified")

    st.markdown("<br>**Contact Hooks**", unsafe_allow_html=True)
    if meta["phone_numbers"]:
        for phone in meta["phone_numbers"]:
            st.markdown(f'<span class="entity-tag">📞 {phone}</span>', unsafe_allow_html=True)
    else:
        st.caption("No direct phone indicators found")

    st.markdown("<br>**Urgency Keywords Flagged**", unsafe_allow_html=True)
    if meta["urgency_cues"]:
        st.markdown(" ".join([f'<span class="entity-tag" style="border-color: rgba(239,68,68,0.4); color: #f87171;">⚠️ {word}</span>' for word in meta["urgency_cues"]]), unsafe_allow_html=True)
    else:
        st.caption("No temporal pressure keywords detected")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Cognitive Semantic Engine
def analyze_payment_message(text: str) -> dict:
    if not api_key:
        return {"error": "API Key not found. Please verify GEMINI_API_KEY environment variable."}

    client = genai.Client(api_key=api_key)

    prompt = f"""
Analyze the following payment request, SMS, or chat text for coercion, urgency markers, 
and social-engineering scam tactics commonly seen in UPI/digital payment fraud:

"{text}"

Evaluate the psychological pressure, authority claims, and risk level.
Return your evaluation strictly in the following JSON format:
{{
  "threat_level": "High" | "Medium" | "Low",
  "threat_score": 92,
  "urgency_detected": true,
  "authority_impersonation": true,
  "scam_vector": "Urgent Utility Disconnection Scam",
  "identified_triggers": ["Artificial 9:30 PM deadline", "Rs. 15 micro-transaction bait", "DISCOM officer impersonation"],
  "explanation_en": "Clear, concise risk breakdown in English.",
  "explanation_hi": "सरल और स्पष्ट हिंदी व्याख्या।",
  "actionable_guidance_en": "Direct preventive steps in English.",
  "actionable_guidance_hi": "त्वरित सुरक्षा निर्देश हिंदी में।"
}}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.1
        )
    )

    cleaned = response.text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    try:
        return json.loads(cleaned)
    except Exception as e:
        return {"error": f"JSON Decode Error: {str(e)}"}

# Display Forensic Output
if analyze_clicked:
    if not input_message.strip():
        st.error("Please provide valid message content or select a preset.")
    else:
        with st.spinner("Executing multi-dimensional cognitive risk scan..."):
            result = analyze_payment_message(input_message)

        if "error" in result:
            st.error(result["error"])
        else:
            threat = result.get("threat_level", "Low").capitalize()
            score = result.get("threat_score", 15 if threat == "Low" else (55 if threat == "Medium" else 92))
            
            # Dynamic Banner Themes
            if threat == "High":
                bg_color = "rgba(239, 68, 68, 0.12)"
                border_color = "rgba(239, 68, 68, 0.4)"
                accent_color = "#f87171"
                status_icon = "🚨 CRITICAL THREAT DETECTED"
            elif threat == "Medium":
                bg_color = "rgba(245, 158, 11, 0.12)"
                border_color = "rgba(245, 158, 11, 0.4)"
                accent_color = "#fbbf24"
                status_icon = "⚠️ ELEVATED COERCION RISK"
            else:
                bg_color = "rgba(34, 197, 94, 0.12)"
                border_color = "rgba(34, 197, 94, 0.4)"
                accent_color = "#4ade80"
                status_icon = "✅ BENIGN TRANSACTION VERIFIED"

            st.markdown(f"""
            <div style="background: {bg_color}; border: 1px solid {border_color}; border-radius: 16px; padding: 20px 24px; margin: 24px 0 16px 0;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: {accent_color}; font-weight: 800; font-size: 18px; letter-spacing: 0.5px;">{status_icon}</span>
                    <span style="color: #94a3b8; font-size: 14px; font-weight: 600;">VECTOR: <strong style="color: #ffffff;">{result.get('scam_vector', 'N/A')}</strong></span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Visual Confidence Progress
            st.progress(score / 100, text=f"Calculated Threat Confidence: {score}% Risk Probability")

            # 4 KPI Cards
            kpi1, kpi2, kpi3, kpi4 = st.columns(4)
            with kpi1:
                st.metric("Threat Tier", threat)
            with kpi2:
                st.metric("Urgency Markers", "Identified" if result.get("urgency_detected") else "None")
            with kpi3:
                st.metric("Authority Spoof", "Identified" if result.get("authority_impersonation") else "None")
            with kpi4:
                st.metric("Risk Index", f"{score}/100")

            st.markdown("<br>", unsafe_allow_html=True)

            # Details Grid
            col_findings, col_bilingual = st.columns([1, 1], gap="large")

            with col_findings:
                st.markdown("""
                <div class="glass-card">
                    <h4 style="margin: 0 0 14px 0; color: #f8fafc;">Behavioral Red Flags</h4>
                """, unsafe_allow_html=True)
                
                triggers = result.get("identified_triggers", [])
                if triggers:
                    for t in triggers:
                        st.markdown(f"""
                        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px; background: rgba(0,0,0,0.25); padding: 10px 14px; border-radius: 8px; border-left: 3px solid {accent_color};">
                            <span style="font-size: 14px; color: #f1f5f9;">{t}</span>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.success("No behavioral red flags or manipulation indicators detected.")
                
                st.markdown("</div>", unsafe_allow_html=True)

            with col_bilingual:
                st.markdown("""
                <div class="glass-card">
                    <h4 style="margin: 0 0 14px 0; color: #f8fafc;">Multilingual Action Directive</h4>
                """, unsafe_allow_html=True)

                tab_en, tab_hi = st.tabs(["🇬🇧 English Directive", "🇮🇳 हिंदी सुरक्षा निर्देश"])

                with tab_en:
                    st.markdown(f"**Diagnostic Summary:**<br>{result.get('explanation_en')}", unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.info(f"🛡️ **Action Required:** {result.get('actionable_guidance_en')}")

                with tab_hi:
                    st.markdown(f"**विश्लेषण सारांश:**<br>{result.get('explanation_hi')}", unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.warning(f"🛡️ **आवश्यक कार्रवाई:** {result.get('actionable_guidance_hi')}")

                st.markdown("</div>", unsafe_allow_html=True)

            # Security Telemetry
            with st.expander("🔬 View Raw JSON Telemetry & Forensic Audit Log"):
                st.json(result)
