import streamlit as st
from datetime import datetime
import plotly.express as px

from app.models.text_emotion import TextEmotionModel
from app.services.wellbeing import get_wellbeing_response
from app.utils.safety import check_safety


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="MindEase | AI Wellbeing Assistant",
    page_icon="💙",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# =========================================================
# EMOTION → COLOR / EMOJI MAP
# =========================================================

EMOTION_STYLES = {
    "joy":       {"emoji": "😊", "color": "#F5A623", "bg": "#FFF6E9"},
    "happy":     {"emoji": "😊", "color": "#F5A623", "bg": "#FFF6E9"},
    "sadness":   {"emoji": "😔", "color": "#4B6FDB", "bg": "#EEF2FD"},
    "sad":       {"emoji": "😔", "color": "#4B6FDB", "bg": "#EEF2FD"},
    "anger":     {"emoji": "😠", "color": "#E1543D", "bg": "#FDEEEC"},
    "fear":      {"emoji": "😟", "color": "#8B5CF6", "bg": "#F3EEFD"},
    "surprise":  {"emoji": "😲", "color": "#10B981", "bg": "#E9FBF4"},
    "neutral":   {"emoji": "😐", "color": "#667085", "bg": "#F2F4F7"},
    "disgust":   {"emoji": "🤢", "color": "#65A30D", "bg": "#F2FBE9"},
    "love":      {"emoji": "🥰", "color": "#EC4899", "bg": "#FDEEF6"},
}

DEFAULT_STYLE = {"emoji": "🌱", "color": "#5B7FDE", "bg": "#EEF2FD"}

# Confidence below this shows an "I'm not fully sure" note instead of a
# confident-sounding result.
LOW_CONFIDENCE_THRESHOLD = 0.40


def get_emotion_style(emotion: str) -> dict:
    return EMOTION_STYLES.get(emotion.lower(), DEFAULT_STYLE)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    @import url(
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
    );

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: linear-gradient(
            180deg,
            #F7FAFF 0%,
            #FFFFFF 45%,
            #F8FBFF 100%
        );
    }

    .block-container {
        max-width: 880px;
        padding-top: 2.5rem;
        padding-bottom: 3rem;
    }

    #MainMenu, footer {visibility: hidden;}

    /* ---------------- Header ---------------- */

    .hero-badge {
        display: flex;
        justify-content: center;
        margin-bottom: 0.75rem;
    }

    .hero-badge span {
        background: #EEF2FD;
        color: #4B6FDB;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.03em;
        text-transform: uppercase;
        padding: 0.3rem 0.9rem;
        border-radius: 999px;
    }

    .hero-title {
        text-align: center;
        font-size: 2.6rem;
        font-weight: 800;
        letter-spacing: -1.2px;
        color: #172033;
        margin-bottom: 0.4rem;
    }

    .hero-subtitle {
        text-align: center;
        color: #667085;
        font-size: 1.02rem;
        line-height: 1.7;
        max-width: 620px;
        margin: 0 auto 2.2rem auto;
    }

    /* ---------------- Cards (native st.container(border=True)) ---------------- */

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #FFFFFF;
        border: 1px solid #EAECF0 !important;
        border-radius: 18px !important;
        box-shadow: 0 1px 3px rgba(16, 24, 40, 0.04);
        margin-bottom: 1.4rem;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] > div {
        gap: 0.6rem;
    }

    .section-title {
        color: #172033;
        font-size: 1.05rem;
        font-weight: 700;
        margin-bottom: 0.9rem;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }

    /* ---------------- Text input ---------------- */

    .stTextInput input {
        border-radius: 14px !important;
        border: 1.5px solid #EAECF0 !important;
        font-size: 0.98rem !important;
        padding: 0.7rem 1rem !important;
    }

    .stTextInput input:focus {
        border-color: #4B6FDB !important;
        box-shadow: 0 0 0 3px rgba(75, 111, 219, 0.12) !important;
    }

    .input-hint {
        color: #98A2B3;
        font-size: 0.78rem;
        margin-top: -0.3rem;
        margin-bottom: 0.6rem;
    }

    /* ---------------- Buttons ---------------- */

    .stButton > button,
    .stFormSubmitButton > button {
        width: 100%;
        min-height: 2.9rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.98rem;
        border: none;
        background: linear-gradient(135deg, #4B6FDB 0%, #6E8CF0 100%);
        color: white;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
        box-shadow: 0 2px 8px rgba(75, 111, 219, 0.25);
    }

    .stButton > button:hover,
    .stFormSubmitButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 14px rgba(75, 111, 219, 0.32);
        color: white;
    }

    .stButton > button:disabled,
    .stFormSubmitButton > button:disabled {
        opacity: 0.6;
        box-shadow: none;
        transform: none;
    }

    /* ---------------- Emotion result badge ---------------- */

    .emotion-badge {
        display: flex;
        align-items: center;
        gap: 0.9rem;
        border-radius: 14px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.4rem;
    }

    .emotion-badge .emoji {
        font-size: 2rem;
    }

    .emotion-badge .label {
        font-size: 1.15rem;
        font-weight: 700;
        color: #172033;
    }

    .emotion-badge .confidence {
        font-size: 0.85rem;
        color: #667085;
        font-weight: 500;
    }

    .low-confidence-note {
        background: #FFFAEB;
        border-left: 3px solid #F5A623;
        border-radius: 10px;
        padding: 0.7rem 1rem;
        color: #93670A;
        font-size: 0.86rem;
        margin-bottom: 0.6rem;
    }

    .support-box {
        background: #F9FAFB;
        border-left: 3px solid #4B6FDB;
        border-radius: 10px;
        padding: 0.95rem 1.1rem;
        color: #344054;
        font-size: 0.96rem;
        line-height: 1.55;
        margin-bottom: 0.4rem;
    }

    .suggestion-box {
        background: #F0FDF6;
        border-left: 3px solid #12B76A;
        border-radius: 10px;
        padding: 0.95rem 1.1rem;
        color: #175C3A;
        font-size: 0.96rem;
        line-height: 1.55;
    }

    .crisis-box {
        background: #FEF3F2;
        border: 1px solid #FDA29B;
        border-radius: 14px;
        padding: 1.1rem 1.3rem;
        color: #7A271A;
        margin-top: 0.5rem;
    }

    .crisis-box strong {
        color: #B42318;
    }

    .crisis-box ul {
        margin: 0.6rem 0 0 0;
        padding-left: 1.2rem;
    }

    .crisis-box li {
        margin-bottom: 0.3rem;
        font-size: 0.92rem;
    }

    .error-box {
        background: #FFFAEB;
        border: 1px solid #FEC84B;
        border-radius: 14px;
        padding: 1rem 1.2rem;
        color: #7A4A0A;
        font-size: 0.92rem;
    }

    /* ---------------- History ---------------- */

    .history-item {
        border-bottom: 1px solid #F2F4F7;
        padding: 0.9rem 0;
    }

    .history-item:last-child {
        border-bottom: none;
        padding-bottom: 0;
    }

    .history-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.35rem;
    }

    .history-time {
        color: #98A2B3;
        font-size: 0.78rem;
        font-weight: 500;
    }

    .history-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
        font-size: 0.8rem;
        font-weight: 600;
        padding: 0.15rem 0.65rem;
        border-radius: 999px;
    }

    .history-text {
        color: #475467;
        font-size: 0.92rem;
        font-style: italic;
        line-height: 1.5;
    }

    .empty-state {
        text-align: center;
        color: #98A2B3;
        font-size: 0.92rem;
        padding: 1rem 0;
    }

    /* ---------------- Metrics ---------------- */

    [data-testid="stMetric"] {
        background: #F9FAFB;
        border: 1px solid #EAECF0;
        border-radius: 14px;
        padding: 0.9rem 1rem;
    }

    [data-testid="stMetricValue"] {
        font-size: 1.35rem !important;
        font-weight: 700 !important;
        color: #172033 !important;
    }

    [data-testid="stMetricLabel"] {
        color: #667085 !important;
        font-weight: 500 !important;
    }

    /* ---------------- Footer ---------------- */

    .footer-text {
        text-align: center;
        color: #98A2B3;
        font-size: 0.78rem;
        line-height: 1.6;
        margin-top: 2.5rem;
        padding: 1rem;
        border-top: 1px solid #EAECF0;
    }

    /* ---------------- Dark mode ---------------- */

    @media (prefers-color-scheme: dark) {

        .stApp {
            background: linear-gradient(180deg, #0B0F19 0%, #10151F 100%);
        }

        .hero-title { color: #F2F4F7; }
        .hero-subtitle { color: #98A2B3; }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: #131826;
            border-color: #1F2937 !important;
        }

        .section-title { color: #F2F4F7; }

        .support-box { background: #1A2030; color: #D0D5DD; }
        .history-text { color: #98A2B3; }
        .history-time { color: #667085; }

        [data-testid="stMetric"] {
            background: #1A2030;
            border-color: #1F2937;
        }

        [data-testid="stMetricValue"] { color: #F2F4F7 !important; }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# LOAD MODEL (with error handling so the app doesn't crash)
# =========================================================

@st.cache_resource
def load_emotion_model():
    return TextEmotionModel()


try:
    emotion_model = load_emotion_model()
    model_load_error = None
except Exception as e:
    emotion_model = None
    model_load_error = str(e)


# =========================================================
# SESSION STATE
# =========================================================

if "mood_history" not in st.session_state:
    st.session_state.mood_history = []


# =========================================================
# HERO SECTION
# =========================================================

st.markdown(
    """
    <div class="hero-badge"><span>AI-Powered Wellbeing</span></div>
    <div class="hero-title">MindEase 💙</div>
    <div class="hero-subtitle">
        A gentle AI companion that helps you understand
        your emotions and reflect on how you're feeling.
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# MODEL LOAD FAILURE — stop early with a friendly message
# =========================================================

if model_load_error:

    st.markdown(
        f"""
        <div class="error-box">
            <strong>The emotion model couldn't be loaded.</strong><br>
            Please try again in a moment, or contact support if this keeps happening.
            <br><br>
            <code style="font-size:0.78rem;">{model_load_error}</code>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.stop()


# =========================================================
# INPUT SECTION (Enter or button submits, input clears after)
# =========================================================

with st.container(border=True):

    st.markdown(
        '<div class="section-title">✍️ How are you feeling today?</div>',
        unsafe_allow_html=True
    )

    with st.form(key="mood_form", clear_on_submit=True):

        user_text = st.text_input(
            "Your thoughts",
            placeholder="Write what's on your mind and press Enter...",
            label_visibility="collapsed"
        )

        st.markdown(
            '<div class="input-hint">Press Enter or click below to analyze</div>',
            unsafe_allow_html=True
        )

        analyze_clicked = st.form_submit_button(
            "✨ Analyze My Feelings",
            type="primary"
        )


# =========================================================
# ANALYZE
# =========================================================

if analyze_clicked:

    # -----------------------------------------------------
    # EMPTY / WHITESPACE-ONLY INPUT
    # -----------------------------------------------------

    if not user_text or not user_text.strip():

        st.warning("Please write something first.")

    else:

        clean_text = user_text.strip()

        # -------------------------------------------------
        # SKIP EXACT REPEAT OF LAST ENTRY
        # -------------------------------------------------

        is_duplicate = (
            st.session_state.mood_history
            and st.session_state.mood_history[-1]["text"] == clean_text
        )

        if is_duplicate:

            st.info("You already analyzed this exact entry — showing it below in your history.")

        else:

            try:
                is_unsafe = check_safety(clean_text)
            except Exception:
                is_unsafe = False  # fail safe: don't block on a broken safety check

            # ---------------------------------------------
            # SAFETY CHECK — India-specific crisis resources
            # ---------------------------------------------

            if is_unsafe:

                st.markdown(
                    """
                    <div class="crisis-box">
                        <strong>It sounds like you may be going through a very difficult moment.</strong>
                        <br><br>
                        If you may be in immediate danger or might hurt yourself, please reach out
                        right now — you don't have to go through this alone.
                        <ul>
                            <li><strong>iCall (India):</strong> +91 9152987821</li>
                            <li><strong>AASRA:</strong> +91 9820466726</li>
                            <li><strong>Vandrevala Foundation:</strong> 1860 2662 345 / 1800 2333 330</li>
                            <li><strong>Emergency services:</strong> 112</li>
                        </ul>
                        You can also reach out to a qualified mental-health professional.
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:

                # -------------------------------------------------
                # NORMAL ANALYSIS (with error handling)
                # -------------------------------------------------

                try:

                    with st.spinner("Understanding your emotions..."):

                        result = emotion_model.predict(clean_text)

                        emotion = result["emotion"]
                        confidence = result["confidence"]

                        response = get_wellbeing_response(emotion)

                        st.session_state.mood_history.append(
                            {
                                "time": datetime.now().strftime("%d %b %Y, %I:%M %p"),
                                "emotion": emotion.capitalize(),
                                "confidence": confidence,
                                "text": clean_text
                            }
                        )

                    style = get_emotion_style(emotion)

                    with st.container(border=True):

                        low_confidence_html = ""
                        if confidence < LOW_CONFIDENCE_THRESHOLD:
                            low_confidence_html = (
                                '<div class="low-confidence-note">'
                                "I'm not fully sure about this one — the result below is my best guess."
                                "</div>"
                            )

                        st.markdown(
                            f"""
                            <div class="emotion-badge" style="background:{style['bg']};">
                                <div class="emoji">{style['emoji']}</div>
                                <div>
                                    <div class="label">{emotion.capitalize()}</div>
                                    <div class="confidence">Confidence: {confidence:.1%}</div>
                                </div>
                            </div>
                            {low_confidence_html}
                            <div class="section-title">💬 A little support</div>
                            <div class="support-box">{response["message"]}</div>
                            <div class="section-title">🌿 You could try</div>
                            <div class="suggestion-box">{response["suggestion"]}</div>
                            """,
                            unsafe_allow_html=True
                        )

                except Exception as e:

                    st.markdown(
                        f"""
                        <div class="error-box">
                            <strong>Something went wrong while analyzing your message.</strong><br>
                            Please try again — if it keeps happening, try rephrasing your entry.
                            <br><br>
                            <code style="font-size:0.78rem;">{e}</code>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )


# =========================================================
# MOOD HISTORY
# =========================================================

with st.container(border=True):

    st.markdown(
        '<div class="section-title">🕒 Mood History</div>',
        unsafe_allow_html=True
    )

    if st.session_state.mood_history:

        history_html = ""

        for entry in reversed(st.session_state.mood_history):

            style = get_emotion_style(entry["emotion"])

            history_html += f"""
            <div class="history-item">
                <div class="history-top">
                    <span class="history-time">{entry['time']}</span>
                    <span class="history-pill" style="background:{style['bg']}; color:{style['color']};">
                        {style['emoji']} {entry['emotion']} · {entry['confidence']:.0%}
                    </span>
                </div>
                <div class="history-text">"{entry['text']}"</div>
            </div>
            """

        st.markdown(history_html, unsafe_allow_html=True)

    else:

        st.markdown(
            '<div class="empty-state">Your mood history will appear here after you analyze a feeling.</div>',
            unsafe_allow_html=True
        )


# =========================================================
# MOOD DASHBOARD
# =========================================================

if st.session_state.mood_history:

    with st.container(border=True):

        st.markdown(
            '<div class="section-title">📊 Mood Dashboard</div>',
            unsafe_allow_html=True
        )

        # -----------------------------------------------------
        # EMOTION COUNTS
        # -----------------------------------------------------

        emotions = [entry["emotion"] for entry in st.session_state.mood_history]

        emotion_counts = {}
        for emotion_name in emotions:
            emotion_counts[emotion_name] = emotion_counts.get(emotion_name, 0) + 1

        total_analyses = len(emotions)
        most_common_emotion = max(emotion_counts, key=emotion_counts.get)

        # -----------------------------------------------------
        # DASHBOARD STATS
        # -----------------------------------------------------

        col1, col2 = st.columns(2)

        with col1:
            st.metric(label="Total Analyses", value=total_analyses)

        with col2:
            top_style = get_emotion_style(most_common_emotion)
            st.metric(
                label="Most Detected",
                value=f"{top_style['emoji']} {most_common_emotion}"
            )

        # -----------------------------------------------------
        # EMOTION DISTRIBUTION
        # -----------------------------------------------------

        st.markdown(
            '<div class="section-title" style="margin-top:1.2rem;">🌱 Emotion Distribution</div>',
            unsafe_allow_html=True
        )

        chart_data = {
            "Emotion": list(emotion_counts.keys()),
            "Count": list(emotion_counts.values())
        }

        bar_colors = [
            get_emotion_style(e)["color"] for e in chart_data["Emotion"]
        ]

        fig = px.bar(
            chart_data,
            x="Emotion",
            y="Count",
            text="Count"
        )

        fig.update_traces(
            marker_color=bar_colors,
            width=0.45,
            textposition="outside",
            textfont=dict(size=13, color="#344054")
        )

        fig.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis_title=None,
            yaxis_title="Count",
            showlegend=False,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, sans-serif", color="#475467"),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="#F2F4F7")
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer-text">
        MindEase provides general emotional support and reflection.
        <br>
        It is not a substitute for professional mental health care.
    </div>
    """,
    unsafe_allow_html=True
)