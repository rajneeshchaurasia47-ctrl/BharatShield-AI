import streamlit as st
import re

st.set_page_config(
    page_title="BharatShield AI",
    page_icon="🛡️",
    layout="wide"
)

st.markdown("""
<style>
.hero{padding:18px 22px;border-radius:18px;background:linear-gradient(135deg,#0b3d91,#1677ff);color:white}
.card{padding:16px;border-radius:14px;background:white;border:1px solid #e6eaf0;margin-bottom:12px}
.risk{font-size:28px;font-weight:800}.small{color:#667085}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="hero"><h1>🛡️ BharatShield AI</h1>'
    '<p>Explainable financial scam & misinformation resilience assistant</p></div>',
    unsafe_allow_html=True
)
st.caption(
    "Public-good prototype • Educational safety analysis • "
    "No stock tips, buy/sell signals or price predictions"
)

examples = {
    "Suspicious tip-group message": """URGENT! Guaranteed 40% profit in 7 days.
Join our SEBI approved premium Telegram group now. Pay ₹2,999 to unlock today's secret stock.
Limited seats! DM the admin and send payment screenshot.""",

    "Fake registration claim": """Our platform is officially registered with SEBI. Registration No: SEBI123456.
Deposit today and our expert will double your money. Visit https://example-investment.com""",

    "Educational content": """Volatility means the price of an investment can move up or down over time.
Diversification can reduce concentration risk, but it cannot remove all investment risk."""
}

if "analysis" not in st.session_state:
    st.session_state.analysis = None
if "last_text" not in st.session_state:
    st.session_state.last_text = ""

left, right = st.columns([1.1, .9])

with left:
    st.subheader("Check a message or financial claim")
    choice = st.selectbox(
        "Try a demo case",
        ["Custom input"] + list(examples.keys())
    )
    text = st.text_area(
        "Paste message / claim / URL",
        value="" if choice == "Custom input" else examples[choice],
        height=220
    )
    lang = st.selectbox("Output language", ["English", "Hindi"])
    analyze = st.button(
        "🔎 Analyze Safely",
        type="primary",
        use_container_width=True
    )

def analyze_text(t):
    tl = t.lower()
    flags = []
    score = 8

    pats = [
        (r"guaranteed|guarantee|100%|sure profit|double your money|fixed return",
         "Guaranteed/assured return language", 28),
        (r"urgent|limited seats|act now|today only|last chance",
         "Urgency / scarcity pressure", 16),
        (r"telegram|whatsapp|dm the admin|premium group|tip group",
         "Private tip-group / messaging-channel solicitation", 16),
        (r"pay|payment|deposit|₹|rs\.?|registration fee|unlock",
         "Payment/deposit request", 18),
        (r"sebi\s*(approved|registered)|registration\s*(no|number)",
         "Regulatory registration claim requires independent verification", 18),
        (r"expert|insider|secret stock|sure shot|target price",
         "Authority/insider-style persuasion", 15),
        (r"http://|https://|\.com|\.in|\.org",
         "External link present; verify destination independently", 8)
    ]

    for pat, label, pts in pats:
        if re.search(pat, tl):
            flags.append(label)
            score += pts

    if (
        sum(x in tl for x in [
            "volatility", "diversification", "risk",
            "cannot remove all", "educational", "uncertainty"
        ]) >= 2 and not flags
    ):
        score = 10

    score = min(score, 98)

    if score >= 70:
        level = "HIGH RISK"
        action = (
            "Pause. Do not transfer money or share credentials. "
            "Verify the claim independently through official sources."
        )
    elif score >= 40:
        level = "CAUTION"
        action = (
            "Pause and verify the sender, registration claim, "
            "link and evidence before taking any financial action."
        )
    else:
        level = "LOW SIGNALS"
        action = (
            "No strong scam pattern was detected. This is not proof "
            "that the content is safe; verify important claims."
        )

    return score, level, flags, action

def hindi_level(level):
    return {
        "HIGH RISK": "उच्च जोखिम",
        "CAUTION": "सावधानी",
        "LOW SIGNALS": "कम जोखिम संकेत"
    }[level]

def hindi_flag(flag):
    translations = {
        "Guaranteed/assured return language":
            "गारंटीड/निश्चित रिटर्न का दावा",
        "Urgency / scarcity pressure":
            "जल्दी करने या सीमित अवसर का दबाव",
        "Private tip-group / messaging-channel solicitation":
            "प्राइवेट टिप-ग्रुप / मैसेजिंग चैनल में शामिल होने का आग्रह",
        "Payment/deposit request":
            "पैसे जमा करने या भुगतान करने का अनुरोध",
        "Regulatory registration claim requires independent verification":
            "रेगुलेटरी रजिस्ट्रेशन के दावे की स्वतंत्र पुष्टि जरूरी है",
        "Authority/insider-style persuasion":
            "एक्सपर्ट/इनसाइडर जैसी भाषा से भरोसा बनाने का प्रयास",
        "External link present; verify destination independently":
            "बाहरी लिंक मौजूद है; गंतव्य की स्वतंत्र रूप से पुष्टि करें"
    }
    return translations.get(flag, flag)

def hindi_action(action):
    if action.startswith("Pause. Do not transfer"):
        return (
            "रुकें। पैसे ट्रांसफर न करें और पासवर्ड/OTP जैसी जानकारी साझा न करें। "
            "दावे की आधिकारिक स्रोतों से स्वतंत्र रूप से पुष्टि करें।"
        )
    if action.startswith("Pause and verify"):
        return (
            "रुकें और कोई वित्तीय कार्रवाई करने से पहले भेजने वाले, "
            "रजिस्ट्रेशन दावे, लिंक और सबूत की पुष्टि करें।"
        )
    return (
        "कोई मजबूत स्कैम पैटर्न नहीं मिला। इसका मतलब यह नहीं है कि "
        "कंटेंट सुरक्षित है; महत्वपूर्ण दावों की पुष्टि जरूर करें।"
    )

with right:
    st.subheader("Risk analysis")

    if analyze and text.strip():
        st.session_state.analysis = analyze_text(text)
        st.session_state.last_text = text

    if st.session_state.analysis:
        score, level, flags, action = st.session_state.analysis

        if lang == "Hindi":
            display_level = hindi_level(level)
            display_flags = [hindi_flag(f) for f in flags]
            display_action = hindi_action(action)
            signal_text = f"समझने योग्य जोखिम संकेत: {score}/100"
            red_flags_title = "🚩 खतरे के संकेत"
            reasoning_title = "🧾 कारण"
            reasoning_text = (
                "यह संकेत दिखाई देने वाले भाषा-पैटर्न पर आधारित है; "
                "यह दावा नहीं करता कि भेजने वाला व्यक्ति/संस्था धोखाधड़ी कर रही है।"
            )
            safer_title = "🛡️ सुरक्षित अगला कदम"
            no_flags = "सबमिट किए गए टेक्स्ट में कोई मजबूत पैटर्न नहीं मिला।"
            footer_note = (
                "महत्वपूर्ण दावों की स्वतंत्र पुष्टि करें। यह रेगुलेटरी "
                "वेरिफिकेशन सेवा या निवेश सलाह का टूल नहीं है।"
            )
        else:
            display_level = level
            display_flags = flags
            signal_text = f"Explainable risk signal: {score}/100"
            red_flags_title = "🚩 Red flags detected"
            reasoning_title = "🧾 Reasoning"
            reasoning_text = (
                "The signal is based on observable language patterns, "
                "not a claim that the sender is fraudulent."
            )
            safer_title = "🛡️ Safer next step"
            no_flags = "No strong pattern detected in the submitted text."
            display_action = action
            footer_note = (
                "Verify important claims independently. This is not a "
                "regulatory verification service or investment-advice tool."
            )

        st.markdown(
            f'<div class="card"><div class="risk">{display_level}</div>'
            f'<div class="small">{signal_text}</div></div>',
            unsafe_allow_html=True
        )

        st.markdown(f"**{red_flags_title}**")
        for f in display_flags or [no_flags]:
            st.write("• " + f)

        st.markdown(f"**{reasoning_title}**")
        st.write("• " + reasoning_text)

        st.markdown(f"**{safer_title}**")
        st.info(display_action)

        st.caption(footer_note)
    else:
        if lang == "Hindi":
            st.info("एक संदेश डालें और “Analyze Safely” पर क्लिक करें।")
        else:
            st.info("Paste a message and click Analyze Safely.")

st.divider()

if lang == "Hindi":
    st.subheader("यह क्यों उपयोगी है")
    c1, c2, c3 = st.columns(3)
    c1.metric("फोकस", "फ्रॉड + गलत सूचना")
    c2.metric("डिज़ाइन", "Bharat-first")
    c3.metric("सिद्धांत", "समझाएं, टिप न दें")
else:
    st.subheader("Why this is useful")
    c1, c2, c3 = st.columns(3)
    c1.metric("Focus", "Fraud + misinformation")
    c2.metric("Design", "Bharat-first")
    c3.metric("Principle", "Explain, don't tip")

st.caption(
    "Hackathon prototype: not a regulatory verification service "
    "or investment-advice tool."
)
