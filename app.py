import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="How the World Measures Vehicle Recycling",
                   layout="wide")

# ================= Design system =================
INK, SLATE, MIST, BAND = "#1E2430", "#3F4A5A", "#E7EBF0", "#F5F8FA"
BLUE, TEAL, AMBER, CORAL, GREY = "#1F6FB2", "#159A8C", "#E0A93E", "#C0392B", "#9AA5B1"

st.markdown("""
<style>
html, body, [class*="css"] { font-family: "Segoe UI","Helvetica Neue",Arial,sans-serif; }
.block-container { max-width: 1180px; padding-top: 2.2rem; }
h1 { font-size: 2.05rem !important; font-weight: 700; letter-spacing: -.01em;
     color: #1E2430; border-bottom: 3px solid #1F6FB2; padding-bottom: .55rem; }
h2 { font-size: 1.35rem !important; font-weight: 650; color: #1F6FB2;
     margin-top: .6rem; letter-spacing: .01em; }
h3 { font-size: 1.05rem !important; font-weight: 650; color: #3F4A5A; }
p, li { color: #3F4A5A; font-size: .95rem; line-height: 1.55; }
[data-testid="stTable"] td, [data-testid="stTable"] th { font-size: .88rem; color: #1E2430; }
[data-testid="stTable"] th { background: #EFF5FA; font-weight: 650; }
[data-testid="stMetricLabel"] { color: #3F4A5A !important; font-size: .82rem !important;
     text-transform: uppercase; letter-spacing: .06em; }
[data-testid="stMetricValue"] { color: #1E2430 !important; font-weight: 700; }
.claim { border-left: 3px solid #1F6FB2; background: #EFF5FA;
     padding: .8rem 1.1rem; margin: .4rem 0 1.2rem 0;
     font-size: .92rem; line-height: 1.55; color: #1E2430; }
.claim b { color: #1F6FB2; }
.finding { border: 1px solid #1F6FB2; border-left: 6px solid #C0392B;
     padding: .9rem 1.2rem; margin: .8rem 0 1.1rem 0;
     font-size: .95rem; line-height: 1.6; color: #1E2430; background: #FFFFFF; }
.badge { font-size: .74rem; font-weight: 700; letter-spacing: .07em;
     text-transform: uppercase; padding: .1rem .45rem; border-radius: 2px; }
.b-meas { background:#E1EEF8; color:#1F6FB2; }
.b-der  { background:#FAF1DC; color:#8A6414; }
.b-lit  { background:#ECECEC; color:#3F4A5A; }
.b-est  { background:#F9E5E2; color:#C0392B; }
.b-abs  { background:#C0392B; color:#FFFFFF; }
[data-testid="stSidebar"] { background: #EFF5FA; }
[data-testid="stSidebar"] a { color: #1F6FB2; text-decoration: none;
     font-size: .9rem; line-height: 2; }
</style>""", unsafe_allow_html=True)

def claim(html):
    st.markdown(f'<div class="claim"><b>Claim.</b> {html}</div>',
                unsafe_allow_html=True)

PLOT = dict(
    font=dict(family='"Segoe UI","Helvetica Neue",Arial,sans-serif',
              color=INK, size=13),
    paper_bgcolor="white", plot_bgcolor="white",
    xaxis=dict(gridcolor=MIST, linecolor=SLATE, tickcolor=SLATE),
    yaxis=dict(gridcolor=MIST, linecolor=SLATE, tickcolor=SLATE),
    legend=dict(orientation="h", y=1.12, font=dict(size=12)),
    margin=dict(t=30, b=10, l=10, r=10),
)

# ================= Data
