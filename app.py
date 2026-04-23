import streamlit as st
import pandas as pd
import ast
import sys
import os
import base64
import requests
from datetime import datetime

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Club Finder",
    layout="centered",
)


def log_to_sheets(query, selected_labels, results_names):
    try:
        APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbznsKd97g3CIGFY5NdUUU2V0muH-Q1mYVjiLsQp6-m3gSwZVsdPD1c9yx_QeMrp9dz6vQ/exec"
        payload = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "query": query,
            "interests": ", ".join(selected_labels),
            "recommendations": ", ".join(results_names)
        }
        response = requests.post(APPS_SCRIPT_URL, json=payload, timeout=10)
        st.write(f"Status: {response.status_code}")
        st.write(f"Response: {response.text}")
    except Exception as e:
        st.error(f"Error logging data: {e}")

# ── Background Image Helper ──────────────────────────────────────────────────
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


# Ensure the path to your image is correct
try:
    img_base64 = get_base64_of_bin_file("data/2_optimized.png")
    bg_img_style = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{img_base64}");
        background-attachment: fixed;
        background-size: cover;
        background-position: center;
    }}
    </style>
    """
except FileNotFoundError:
    # Fallback if the image isn't found
    bg_img_style = """<style>.stApp { background-color: #f7f8fc; }</style>"""


# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_clubs():
    # Make sure this path matches your structure
    df = pd.read_csv("data/clubs_with_interest_areas.csv")
    if "interest_areas_ids" in df.columns:
        df["interest_areas_ids"] = df["interest_areas_ids"].apply(
            lambda x: ast.literal_eval(x) if isinstance(x, str) else x
        )
    return df


clubs_df = load_clubs()

# ── Import recommendation logic ───────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(__file__))
import recomandation_model as rec_model

# ── Interest area mapping ─────────────────────────────────────────────────────
INTEREST_OPTIONS = {
    " Sports & Fitness": 1,
    " Culture & Languages": 2,
    " Science & Research": 3,
    " Debate & Public Speaking": 4,
    " Business & Finance": 5,
    " Technology & Computing": 6,
    " Music & Performance": 7,
    " Arts & Creativity": 8,
    " Social Impact & Volunteering": 9,
    " Gaming & Esports": 10,
    " Dance": 11,
    " Film & Media": 12,
}

# ── Styling ───────────────────────────────────────────────────────────────────
st.markdown(bg_img_style, unsafe_allow_html=True)
st.markdown("""
<style>
    .section-title { font-size: 1.15rem; font-weight: 700; color: #1a1a2e; margin-bottom: 0.4rem; }

    /* Semi-transparent overlay for the main container to ensure readability */
    .block-container {
        background-color: rgba(255, 255, 255, 0.85);
        padding: 2rem !important;
        border-radius: 20px;
        margin-top: 2rem;
    }

    /* Modern Club Card with Flexbox */
    .club-card {
        background: #ffffff;
        border-radius: 14px;
        padding: 0;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        display: flex;
        overflow: hidden;
        border: 1px solid #eee;
    }

    /* Left Side: Identity */
    .card-left {
        flex: 0 0 200px;
        padding: 1.2rem;
        background: #fafaff;
        border-right: 1px solid #f0f0f0;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
    }
    .club-name { font-size: 1.1rem; font-weight: 700; color: #333; margin-bottom: 0.8rem; }

    /* Right Side: Why Join */
    .card-right {
        flex: 1;
        padding: 1.2rem;
    }
    .why-title { font-size: 0.85rem; font-weight: 800; color: #888; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.5rem; }
    .why-text { font-size: 0.95rem; color: #333; line-height: 1.6; }
    /* Social Links */
    .club-links { display: flex; gap: 8px; flex-wrap: wrap; justify-content: center; }
    .club-links a {
        font-size: 0.75rem;
        font-weight: 600;
        text-decoration: none;
        padding: 4px 10px;
        border-radius: 8px;
    }
    .tg-link  { background: #e8f4fd; color: #0088cc; }
    .ig-link  { background: #fde8f4; color: #c13584; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.title("Student club recommendation")
st.caption("Discover the student clubs that match your passion and goals in Nazarbayev University")
st.divider()

# ── Section 1 – Interest areas ────────────────────────────────────────────────
st.markdown('<p class="section-title">What are you interested in?</p>', unsafe_allow_html=True)

selected_labels = st.pills(
    label="Select Interests",
    options=list(INTEREST_OPTIONS.keys()),
    selection_mode="multi",
    label_visibility="collapsed"
)

selected_ids = [INTEREST_OPTIONS[l] for l in selected_labels] if selected_labels else []

st.divider()

# ── Section 2 + 3 – Search ───────────────────────────────────────────────────
st.markdown('<p class="section-title">Describe your ideal club experience</p>', unsafe_allow_html=True)
input_col, btn_col = st.columns([4, 1], vertical_alignment="bottom")

with input_col:
    user_text = st.text_area(
        label="club_query",
        label_visibility="collapsed",
        placeholder="e.g., I want to practice public speaking and meet international students",
        height=80,
    )

with btn_col:
    search_clicked = st.button("🔍 Search", use_container_width=True, type="primary")

st.divider()

# ── Section 4 – Results ───────────────────────────────────────────────────────
if search_clicked:
    query = user_text.strip()
    if not query and not selected_ids:
        st.warning("Please select an interest or type a query.")
    else:
        with st.spinner("Analyzing clubs..."):
            results = rec_model.top_5(query, selected_ids)

            recommended_names = []
            for item in results:
                c_name = clubs_df[clubs_df["id"] == item["id"]]["name"].values[0]
                recommended_names.append(c_name)

            log_to_sheets(query, selected_labels, recommended_names)

        st.markdown(f"### Recommended for You")

        for item in results:
            club_row = clubs_df[clubs_df["id"] == item["id"]]
            if club_row.empty:
                continue

            club = club_row.iloc[0]
            name = club.get("name", "Unknown Club")
            why_join = club.get("why_join", "This club is a great match for your interests!")
            tg_url = club.get("telegram_url", "")
            ig_url = club.get("instagram_url", "")

            links_html = ""
            if pd.notna(tg_url) and str(tg_url).startswith("http"):
                links_html += f'<a class="tg-link" href="{tg_url}" target="_blank">Telegram</a>'
            if pd.notna(ig_url) and str(ig_url).startswith("http"):
                links_html += f'<a class="ig-link" href="{ig_url}" target="_blank">Instagram</a>'

            st.markdown(
                f"""
                <div class="club-card">
                    <div class="card-left">
                        <div class="club-name">{name}</div>
                        <div class="club-links">{links_html}</div>
                    </div>
                    <div class="card-right">
                        <div class="why-title">Why this club?</div>
                        <div class="why-text">{why_join}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
