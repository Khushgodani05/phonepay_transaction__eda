"""
PhonePe Transaction Insights — Streamlit Dashboard
Professional EDA Presentation App
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from sqlalchemy import create_engine
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="PhonePe Transaction Insights",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# BRAND COLORS
# ─────────────────────────────────────────────
PHONEPE_PURPLE = '#5f259f'
PHONEPE_LIGHT  = '#a57bd6'
PHONEPE_DARK   = '#3a1260'
ACCENT_GOLD    = '#f7b731'
ACCENT_TEAL    = '#1abc9c'
ACCENT_CORAL   = '#e74c3c'
BG_DARK        = '#0f0a1e'
BG_CARD        = '#1a1035'
TEXT_WHITE     = '#f0ecfa'

# ─────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Nunito:wght@400;600;700&display=swap');

  /* Root overrides */
  html, body, [class*="css"] {{
    font-family: 'Nunito', sans-serif;
    background-color: {BG_DARK};
    color: {TEXT_WHITE};
  }}

  /* Main area */
  .main .block-container {{
    padding: 1.5rem 2.5rem 3rem 2.5rem;
    max-width: 1400px;
  }}

  /* Sidebar */
  section[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {PHONEPE_DARK} 0%, {BG_DARK} 100%);
    border-right: 2px solid {PHONEPE_PURPLE};
  }}
  section[data-testid="stSidebar"] * {{
    color: {TEXT_WHITE} !important;
    font-family: 'Nunito', sans-serif;
  }}
  section[data-testid="stSidebar"] .stRadio label {{
    font-size: 15px;
    font-weight: 600;
    padding: 4px 0;
  }}

  /* Hero header */
  .hero-header {{
    background: linear-gradient(135deg, {PHONEPE_DARK} 0%, {PHONEPE_PURPLE} 60%, #8b3fd4 100%);
    border-radius: 16px;
    padding: 28px 36px;
    margin-bottom: 28px;
    border: 1px solid {PHONEPE_LIGHT}44;
    box-shadow: 0 8px 40px #5f259f55;
  }}
  .hero-title {{
    font-family: 'Rajdhani', sans-serif;
    font-size: 2.8rem;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: 1px;
    margin: 0;
    line-height: 1.2;
  }}
  .hero-sub {{
    font-size: 1.05rem;
    color: #d4b8f5;
    margin-top: 6px;
    font-weight: 400;
  }}
  .hero-badge {{
    display: inline-block;
    background: {ACCENT_GOLD};
    color: {PHONEPE_DARK};
    font-weight: 700;
    font-size: 0.78rem;
    border-radius: 20px;
    padding: 3px 14px;
    margin-top: 10px;
    letter-spacing: 0.5px;
  }}

  /* Section headings */
  .section-title {{
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.75rem;
    font-weight: 700;
    color: {ACCENT_GOLD};
    border-left: 5px solid {PHONEPE_PURPLE};
    padding-left: 14px;
    margin: 28px 0 16px 0;
    letter-spacing: 0.5px;
  }}

  /* KPI cards */
  .kpi-card {{
    background: linear-gradient(135deg, {BG_CARD}, #221650);
    border: 1px solid {PHONEPE_PURPLE}88;
    border-radius: 14px;
    padding: 20px 22px;
    text-align: center;
    box-shadow: 0 4px 20px #5f259f33;
  }}
  .kpi-value {{
    font-family: 'Rajdhani', sans-serif;
    font-size: 2.1rem;
    font-weight: 700;
    color: {ACCENT_GOLD};
    line-height: 1.1;
  }}
  .kpi-label {{
    font-size: 0.88rem;
    color: #c3abf0;
    margin-top: 4px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.6px;
  }}
  .kpi-icon {{
    font-size: 1.6rem;
    margin-bottom: 6px;
  }}

  /* Insight box */
  .insight-box {{
    background: linear-gradient(135deg, #1a1035ee, #2a1a55ee);
    border-left: 4px solid {ACCENT_TEAL};
    border-radius: 10px;
    padding: 16px 20px;
    margin: 14px 0;
    font-size: 0.96rem;
    color: #ddd4f5;
    line-height: 1.7;
  }}
  .insight-box strong {{
    color: {ACCENT_TEAL};
    font-size: 1.01rem;
  }}

  /* Chart container */
  .chart-container {{
    background: {BG_CARD};
    border: 1px solid {PHONEPE_PURPLE}55;
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 18px;
  }}

  /* Divider */
  hr {{
    border: none;
    border-top: 1px solid {PHONEPE_PURPLE}55;
    margin: 24px 0;
  }}

  /* Streamlit overrides */
  .stSelectbox > div > div {{
    background: {BG_CARD};
    color: {TEXT_WHITE};
    border: 1px solid {PHONEPE_PURPLE};
    border-radius: 8px;
  }}
  .stDataFrame {{
    border-radius: 10px;
    overflow: hidden;
  }}
  h1, h2, h3, h4 {{
    color: {TEXT_WHITE} !important;
  }}
  p, li {{
    color: #ddd4f5 !important;
    font-size: 1rem;
  }}
  .stMarkdown p {{
    color: #ddd4f5 !important;
  }}
  /* Tab styling */
  .stTabs [data-baseweb="tab-list"] {{
    gap: 8px;
    background: {BG_CARD};
    border-radius: 10px;
    padding: 6px;
  }}
  .stTabs [data-baseweb="tab"] {{
    color: #c3abf0 !important;
    font-weight: 600;
    font-size: 0.95rem;
    border-radius: 8px;
    padding: 6px 18px;
  }}
  .stTabs [aria-selected="true"] {{
    background: {PHONEPE_PURPLE} !important;
    color: white !important;
  }}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# MATPLOTLIB THEME
# ─────────────────────────────────────────────
def set_plot_style():
    plt.rcParams.update({
        'figure.facecolor':  BG_CARD,
        'axes.facecolor':    BG_CARD,
        'axes.edgecolor':    '#3a2c6a',
        'axes.labelcolor':   '#c3abf0',
        'axes.titlecolor':   TEXT_WHITE,
        'xtick.color':       '#c3abf0',
        'ytick.color':       '#c3abf0',
        'text.color':        TEXT_WHITE,
        'grid.color':        '#2a1e50',
        'grid.linestyle':    '--',
        'grid.alpha':        0.5,
        'axes.titlesize':    14,
        'axes.titleweight':  'bold',
        'axes.labelsize':    11,
        'xtick.labelsize':   9,
        'ytick.labelsize':   9,
        'figure.dpi':        110,
        'legend.facecolor':  BG_CARD,
        'legend.edgecolor':  PHONEPE_PURPLE,
        'legend.labelcolor': TEXT_WHITE,
    })

set_plot_style()


# ─────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    try:
        engine = create_engine("mysql+pymysql://root:Khush%40123@127.0.0.1:3306/phonepay")
        with engine.connect() as conn:
            df_ins  = pd.read_sql("SELECT * FROM aggregate_insurance",   conn)
            df_txn  = pd.read_sql("SELECT * FROM aggregate_transaction", conn)
            df_usr  = pd.read_sql("SELECT * FROM aggregate_users",       conn)
        return df_ins, df_txn, df_usr, True
    except Exception as e:
        return None, None, None, False


df_insurance, df_transaction, df_users, db_connected = load_data()


# ─────────────────────────────────────────────
# SAMPLE DATA (fallback when DB not connected)
# ─────────────────────────────────────────────
def generate_sample_data():
    np.random.seed(42)
    states = ['Maharashtra','Karnataka','Telangana','Tamil Nadu','Uttar Pradesh',
              'Rajasthan','Gujarat','West Bengal','Delhi','Kerala',
              'Andhra Pradesh','Madhya Pradesh','Bihar','Odisha','Punjab']
    years  = [2018,2019,2020,2021,2022,2023]
    qtrs   = ['Q1','Q2','Q3','Q4']
    txn_types = ['Peer-to-peer payments','Merchant payments',
                 'Recharge & bill payments','Financial Services','Others']
    ins_types  = ['TOTAL','Renewal','New Policy']
    brands    = ['Samsung','Xiaomi','Vivo','Oppo','Realme','OnePlus','Apple','Others']

    rows_txn, rows_ins, rows_usr = [], [], []
    for s in states:
        for y in years:
            for q in qtrs:
                for t in txn_types:
                    cnt = int(np.random.lognormal(10, 1.5))
                    amt = cnt * np.random.uniform(200, 2000)
                    rows_txn.append({'level':'state','region':s,'year':y,'quater':q,
                                     'insurancetype':t,'insurancecount':cnt,'insuranceamount':amt})
            for q in qtrs:
                for t in ins_types:
                    cnt = int(np.random.lognormal(8, 1.2))
                    amt = cnt * np.random.uniform(500, 5000)
                    rows_ins.append({'level':'state','region':s,'year':y,'quater':q,
                                     'insurancetype':t,'insurancecount':cnt,'insuranceamount':amt})
            for q in qtrs:
                opens = int(np.random.lognormal(12, 1.5))
                for b in brands:
                    uc = int(np.random.lognormal(9, 1.2))
                    rows_usr.append({'level':'state','region':s,'year':y,'quater':q,
                                     'appopen':opens,'usersbydevicebrand':b,'usersbydevicecount':uc})
    df_txn = pd.DataFrame(rows_txn)
    df_ins = pd.DataFrame(rows_ins)
    df_usr = pd.DataFrame(rows_usr)
    return df_ins, df_txn, df_usr


if not db_connected:
    df_insurance, df_transaction, df_users = generate_sample_data()

# ─── Normalise quarter column ───
for df in [df_insurance, df_transaction, df_users]:
    if 'quater' in df.columns:
        df['quater'] = df['quater'].astype(str).str.strip().apply(
            lambda x: f'Q{x}' if x.isdigit() else x)

df_users_clean = df_users[df_users['usersbydevicebrand'] != 'Nan'].copy()


# ─────────────────────────────────────────────
# HELPER: fmt numbers
# ─────────────────────────────────────────────
def fmt_num(n):
    if n >= 1e9:  return f"₹{n/1e9:.2f}B"
    if n >= 1e7:  return f"₹{n/1e7:.2f}Cr"
    if n >= 1e5:  return f"₹{n/1e5:.2f}L"
    return f"{n:,.0f}"

def fmt_count(n):
    if n >= 1e9:  return f"{n/1e9:.2f}B"
    if n >= 1e6:  return f"{n/1e6:.2f}M"
    if n >= 1e3:  return f"{n/1e3:.1f}K"
    return f"{n:,.0f}"


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style='text-align:center; padding: 10px 0 20px 0;'>
        <div style='font-family:Rajdhani,sans-serif; font-size:1.6rem; font-weight:700;
                    color:#f7b731; letter-spacing:1px;'>📱 PhonePe</div>
        <div style='font-size:0.8rem; color:#a57bd6; margin-top:2px;'>Transaction Insights</div>
    </div>
    """, unsafe_allow_html=True)

    if not db_connected:
        st.warning("⚠️ DB offline — showing sample data")

    st.markdown("---")
    st.markdown("<div style='font-size:0.85rem; color:#a57bd6; font-weight:700; text-transform:uppercase; letter-spacing:1px; margin-bottom:8px;'>Navigation</div>", unsafe_allow_html=True)

    page = st.radio("", [
        "🏠  Overview",
        "💳  Transactions",
        "🛡️  Insurance",
        "👥  Users & Devices",
        "🗺️  Geo Analysis",
        "📈  Trend Analysis",
        "🔬  Correlation & Multi-var",
        "📋  Business Summary",
    ], label_visibility="collapsed")

    st.markdown("---")
    st.markdown(f"""
    <div style='font-size:0.78rem; color:#7a6aaa; text-align:center; padding-top:8px;'>
        <b>Data</b>: PhonePe Pulse GitHub<br>
        <b>Records</b>: {len(df_transaction):,} transactions<br>
        <b>Period</b>: 2018 – 2023<br>
        <b>Scope</b>: India (State-level)
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HERO BANNER
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="hero-header">
  <div class="hero-title">📊 PhonePe Transaction Insights</div>
  <div class="hero-sub">Exploratory Data Analysis · ETL Pipeline · Business Intelligence Dashboard</div>
  <span class="hero-badge">EDA PROJECT · FINANCE / PAYMENT SYSTEMS</span>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# PAGE 1: OVERVIEW
# ═══════════════════════════════════════════════════════
if "Overview" in page:
    st.markdown('<div class="section-title">Project Overview</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    total_txn_amt  = df_transaction['insuranceamount'].sum()
    total_txn_cnt  = df_transaction['insurancecount'].sum()
    total_ins_amt  = df_insurance['insuranceamount'].sum()
    total_app_open = df_users['appopen'].sum()

    for col, icon, val, label in [
        (col1, "💰", fmt_num(total_txn_amt),   "Total Txn Value"),
        (col2, "🔢", fmt_count(total_txn_cnt),  "Total Txn Count"),
        (col3, "🛡️", fmt_num(total_ins_amt),   "Insurance Value"),
        (col4, "📲", fmt_count(total_app_open), "App Opens"),
    ]:
        with col:
            st.markdown(f"""
            <div class="kpi-card">
              <div class="kpi-icon">{icon}</div>
              <div class="kpi-value">{val}</div>
              <div class="kpi-label">{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b = st.columns([1.1, 0.9])

    with col_a:
        st.markdown('<div class="section-title" style="font-size:1.3rem;">Project Summary</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="insight-box">
        <strong>ETL Pipeline:</strong> This project implements a complete Extract → Transform → Load workflow,
        processing raw JSON files from the PhonePe Pulse GitHub repository and loading them into a
        structured MySQL database for analysis.<br><br>
        <strong>Three Data Domains:</strong><br>
        • <strong>Transactions</strong> — 5,174 records across payment types, states, years & quarters<br>
        • <strong>Insurance</strong> — 701 records tracking insurance policy transactions<br>
        • <strong>Users</strong> — 7,326 records on device brands and app engagement<br><br>
        <strong>Key Analytical Goals:</strong> Customer segmentation, fraud detection, geo insights,
        payment performance benchmarking, user engagement, and insurance product analysis.
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="section-title" style="font-size:1.3rem;">Business Objectives</div>', unsafe_allow_html=True)
        objectives = [
            ("🗺️", "Geographical Insights", "State & district-level payment trend mapping"),
            ("💳", "Payment Performance",   "Evaluate popularity of payment categories"),
            ("👥", "User Engagement",       "Monitor activity for retention strategy"),
            ("🛡️", "Insurance Insights",    "Analyze transactions for product improvement"),
            ("📈", "Trend Analysis",        "Examine time-based transaction fluctuations"),
        ]
        for icon, title, desc in objectives:
            st.markdown(f"""
            <div style='display:flex; align-items:flex-start; gap:12px; padding:10px 14px;
                        background:#1a1035; border-radius:10px; margin-bottom:8px;
                        border:1px solid #3a2c6a;'>
              <span style='font-size:1.3rem;'>{icon}</span>
              <div>
                <div style='font-weight:700; color:{ACCENT_GOLD}; font-size:0.95rem;'>{title}</div>
                <div style='color:#c3abf0; font-size:0.85rem;'>{desc}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    # Dataset preview
    st.markdown('<div class="section-title" style="font-size:1.3rem;">Dataset Preview</div>', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["💳 Transactions", "🛡️ Insurance", "👥 Users"])
    with tab1:
        st.dataframe(df_transaction.head(8), use_container_width=True, height=220)
    with tab2:
        st.dataframe(df_insurance.head(8), use_container_width=True, height=220)
    with tab3:
        st.dataframe(df_users.head(8), use_container_width=True, height=220)


# ═══════════════════════════════════════════════════════
# PAGE 2: TRANSACTIONS
# ═══════════════════════════════════════════════════════
elif "Transactions" in page:
    st.markdown('<div class="section-title">Transaction Analysis</div>', unsafe_allow_html=True)

    # ── Chart 1: Distribution of Transaction Counts ──
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Distribution of Transaction Counts**")
        fig, ax = plt.subplots(figsize=(7, 4))
        sns.histplot(df_transaction['insurancecount'].dropna(), bins=40, kde=True,
                     color=PHONEPE_PURPLE, edgecolor=BG_DARK, ax=ax)
        ax.set_xlabel('Transaction Count');  ax.set_ylabel('Frequency')
        ax.set_title('Transaction Count Distribution', pad=12)
        ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f'{x/1e3:.0f}K'))
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close()

    # ── Chart 2: Transaction Types ──
    with col2:
        st.markdown("**Transaction Type Frequency**")
        type_counts = df_transaction['insurancetype'].value_counts().reset_index()
        type_counts.columns = ['Transaction Type', 'Count']
        fig, ax = plt.subplots(figsize=(7, 4))
        palette = sns.color_palette('Purples_r', len(type_counts))
        bars = ax.barh(type_counts['Transaction Type'], type_counts['Count'],
                       color=palette, edgecolor=BG_DARK)
        for bar in bars:
            ax.text(bar.get_width() + max(type_counts['Count'])*0.01,
                    bar.get_y() + bar.get_height()/2,
                    f'{bar.get_width():,.0f}', va='center', fontsize=8, color=TEXT_WHITE)
        ax.set_xlabel('Count'); ax.set_title('Transactions by Type', pad=12)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close()

    st.markdown('<div class="insight-box"><strong>Key Insight:</strong> '
                'The distribution of transaction counts is heavily right-skewed — a small number of '
                'high-volume states and transaction types drive the majority of activity. '
                'Peer-to-peer payments dominate frequency, confirming it as PhonePe\'s core use-case.</div>',
                unsafe_allow_html=True)

    # ── Chart 3: Records by Year ──
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("**Records by Year**")
        year_counts = df_transaction['year'].astype(str).value_counts().sort_index()
        fig, ax = plt.subplots(figsize=(7, 4))
        bars = ax.bar(year_counts.index, year_counts.values,
                      color=PHONEPE_PURPLE, edgecolor=BG_DARK, width=0.55)
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width()/2,
                    bar.get_height() + max(year_counts.values)*0.01,
                    f'{bar.get_height():,}', ha='center', fontsize=9, color=ACCENT_GOLD)
        ax.set_xlabel('Year'); ax.set_ylabel('Record Count')
        ax.set_title('Transaction Records per Year', pad=12)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close()

    # ── Chart 4: Yearly Transaction Value ──
    with col4:
        st.markdown("**Total Transaction Value by Year**")
        yearly_amount = df_transaction.groupby('year')['insuranceamount'].sum().reset_index().sort_values('year')
        fig, ax = plt.subplots(figsize=(7, 4))
        bars = ax.bar(yearly_amount['year'].astype(str), yearly_amount['insuranceamount'],
                      color=ACCENT_TEAL, edgecolor=BG_DARK, width=0.55)
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width()/2,
                    bar.get_height() + max(yearly_amount['insuranceamount'])*0.01,
                    fmt_num(bar.get_height()), ha='center', fontsize=8, color=TEXT_WHITE)
        ax.set_xlabel('Year')
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: fmt_num(x)))
        ax.set_title('Total Transaction Amount per Year', pad=12)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close()

    # ── Chart 5: Avg amount by type ──
    st.markdown("**Average Transaction Amount by Payment Type**")
    avg_by_type = (df_transaction.groupby('insurancetype')['insuranceamount']
                   .mean().sort_values(ascending=False).reset_index())
    fig, ax = plt.subplots(figsize=(12, 4))
    palette = sns.color_palette('viridis', len(avg_by_type))
    bars = ax.barh(avg_by_type['insurancetype'], avg_by_type['insuranceamount'],
                   color=palette, edgecolor=BG_DARK)
    for bar in bars:
        ax.text(bar.get_width() + max(avg_by_type['insuranceamount'])*0.005,
                bar.get_y() + bar.get_height()/2,
                fmt_num(bar.get_width()), va='center', fontsize=9, color=TEXT_WHITE)
    ax.set_xlabel('Avg Amount (INR)')
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: fmt_num(x)))
    ax.set_title('Average Transaction Amount per Payment Category', pad=12)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close()

    st.markdown('<div class="insight-box"><strong>Key Insight:</strong> '
                'Transaction value shows a strong upward trajectory year-over-year. '
                'Post-2020 acceleration is likely driven by COVID-19 accelerating India\'s '
                'shift to digital payments. Merchant payments carry the highest average ticket size, '
                'while recharge & bill payments are high-frequency but low-value.</div>',
                unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# PAGE 3: INSURANCE
# ═══════════════════════════════════════════════════════
elif "Insurance" in page:
    st.markdown('<div class="section-title">Insurance Analysis</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    # ── Chart: Insurance Amount Distribution (Box) ──
    with col1:
        st.markdown("**Insurance Amount Distribution**")
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.boxplot(df_insurance['insuranceamount'].dropna(), vert=False, patch_artist=True,
                   boxprops=dict(facecolor=PHONEPE_LIGHT, color=PHONEPE_PURPLE),
                   medianprops=dict(color=ACCENT_GOLD, linewidth=2.5),
                   whiskerprops=dict(color=PHONEPE_LIGHT),
                   capprops=dict(color=PHONEPE_LIGHT),
                   flierprops=dict(marker='o', color=ACCENT_CORAL, alpha=0.4, markersize=3))
        ax.set_title('Distribution of Insurance Transaction Amounts', pad=12)
        ax.set_xlabel('Insurance Amount (INR)')
        ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: fmt_num(x)))
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close()

    # ── Chart: Insurance Type Pie ──
    with col2:
        st.markdown("**Insurance Type Breakdown**")
        ins_type_sum = df_insurance.groupby('insurancetype')['insurancecount'].sum()
        fig, ax = plt.subplots(figsize=(7, 4))
        wedges, texts, autotexts = ax.pie(
            ins_type_sum.values, labels=ins_type_sum.index,
            autopct='%1.1f%%',
            colors=sns.color_palette('Purples_r', len(ins_type_sum)),
            startangle=140,
            wedgeprops={'edgecolor': BG_DARK, 'linewidth': 2},
            textprops={'color': TEXT_WHITE, 'fontsize': 10}
        )
        for at in autotexts:
            at.set(color=ACCENT_GOLD, fontsize=9, fontweight='bold')
        ax.set_title('Insurance Type Distribution', pad=12)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close()

    st.markdown('<div class="insight-box"><strong>Key Insight:</strong> '
                'Insurance amounts show significant outliers — a small segment of premium corporate '
                'policies pull the mean well above the median. The bulk of insurance transactions '
                'are low-value retail policies. One insurance type (TOTAL) dominates, suggesting '
                'limited product diversity needing expansion.</div>',
                unsafe_allow_html=True)

    # ── Chart: Insurance Count by Quarter ──
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("**Insurance Count by Quarter**")
        qtr_ins = (df_insurance.groupby('quater')['insurancecount']
                   .sum().reset_index().sort_values('quater'))
        fig, ax = plt.subplots(figsize=(7, 4))
        colors = [PHONEPE_PURPLE, PHONEPE_LIGHT, ACCENT_GOLD, ACCENT_TEAL]
        bars = ax.bar(qtr_ins['quater'], qtr_ins['insurancecount'],
                      color=colors[:len(qtr_ins)], edgecolor=BG_DARK, width=0.5)
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width()/2,
                    bar.get_height() + max(qtr_ins['insurancecount'])*0.01,
                    fmt_count(bar.get_height()), ha='center', fontsize=9, color=TEXT_WHITE)
        ax.set_xlabel('Quarter'); ax.set_ylabel('Total Count')
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: fmt_count(x)))
        ax.set_title('Insurance Transactions by Quarter', pad=12)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close()

    # ── Chart: Insurance Scatter (count vs amount) ──
    with col4:
        st.markdown("**Insurance Count vs Amount (Scatter)**")
        sample = df_insurance.dropna(subset=['insurancecount','insuranceamount']).sample(
            min(2000, len(df_insurance)), random_state=42)
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.scatter(sample['insurancecount'], sample['insuranceamount'],
                   alpha=0.35, s=18, color=PHONEPE_PURPLE, edgecolors='none')
        ax.set_xlabel('Insurance Count')
        ax.set_ylabel('Insurance Amount')
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: fmt_num(x)))
        ax.set_title('Count vs Amount Correlation (Sampled)', pad=12)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close()

    # ── Facet: Top 4 states quarterly insurance ──
    st.markdown("**Top 4 States — Quarterly Insurance Amount (Facet)**")
    top4_ins = (df_insurance[df_insurance['level']=='state']
                .groupby('region')['insuranceamount'].sum()
                .sort_values(ascending=False).head(4).index)
    facet_data = (df_insurance[(df_insurance['level']=='state') & (df_insurance['region'].isin(top4_ins))]
                  .groupby(['region','quater'])['insuranceamount'].sum().reset_index())
    fig, axes = plt.subplots(1, 4, figsize=(16, 4), sharey=True)
    c_list = [PHONEPE_PURPLE, ACCENT_TEAL, ACCENT_GOLD, ACCENT_CORAL]
    for i, (state, axs) in enumerate(zip(top4_ins, axes)):
        sdata = facet_data[facet_data['region']==state].sort_values('quater')
        axs.bar(sdata['quater'], sdata['insuranceamount'], color=c_list[i], edgecolor=BG_DARK)
        axs.set_title(state, fontsize=11, fontweight='bold')
        axs.set_xlabel('Quarter')
        if i == 0: axs.set_ylabel('Amount (INR)')
        axs.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: fmt_num(x)))
    fig.suptitle('Quarterly Insurance Amount — Top 4 States', fontsize=13, fontweight='bold', color=TEXT_WHITE, y=1.02)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close()

    st.markdown('<div class="insight-box"><strong>Key Insight:</strong> '
                'States with Q1 spikes reflect tax-saving insurance purchases before India\'s '
                'financial year-end (March 31). Maharashtra and Karnataka show the steepest growth, '
                'indicating higher financial literacy and disposable incomes in these tech-hub states.</div>',
                unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# PAGE 4: USERS & DEVICES
# ═══════════════════════════════════════════════════════
elif "Users" in page:
    st.markdown('<div class="section-title">User & Device Analysis</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    # ── Chart: Top 10 Device Brands ──
    with col1:
        st.markdown("**Top 10 Device Brands by User Count**")
        brand_counts = (df_users_clean.groupby('usersbydevicebrand')['usersbydevicecount']
                        .sum().sort_values(ascending=False).head(10))
        fig, ax = plt.subplots(figsize=(7, 5))
        palette = sns.color_palette('Purples_r', len(brand_counts))
        bars = ax.bar(brand_counts.index, brand_counts.values, color=palette, edgecolor=BG_DARK)
        ax.set_xlabel('Device Brand'); ax.set_ylabel('Total Users')
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: fmt_count(x)))
        ax.set_title('Top Device Brands (PhonePe Users)', pad=12)
        plt.xticks(rotation=40, ha='right')
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close()

    # ── Chart: App Opens Country vs State ──
    with col2:
        st.markdown("**App Opens: India vs State Level**")
        fig, ax = plt.subplots(figsize=(7, 5))
        sns.boxplot(data=df_users, x='level', y='appopen',
                    palette={'India': PHONEPE_PURPLE, 'state': ACCENT_TEAL},
                    width=0.45, ax=ax)
        ax.set_xlabel('Aggregation Level'); ax.set_ylabel('App Opens')
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f'{x/1e6:.0f}M'))
        ax.set_title('App Open Distribution by Level', pad=12)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close()

    st.markdown('<div class="insight-box"><strong>Key Insight:</strong> '
                'Samsung and Xiaomi (Redmi) dominate PhonePe\'s user base, directly reflecting '
                'India\'s mid-range smartphone market. Premium brands like OnePlus and Apple '
                'represent smaller but high-ARPU segments — valuable for premium feature targeting. '
                'The wide IQR at state level confirms that Maharashtra, Karnataka, and Telangana '
                'are the primary app engagement hubs.</div>',
                unsafe_allow_html=True)

    # ── Chart: Users vs App Opens regression ──
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("**User Count vs App Opens (Regression)**")
        df_users_num = df_users_clean.dropna(subset=['appopen','usersbydevicecount']).copy()
        df_users_num['usersbydevicecount'] = pd.to_numeric(df_users_num['usersbydevicecount'], errors='coerce')
        df_users_num['appopen'] = pd.to_numeric(df_users_num['appopen'], errors='coerce')
        df_users_num = df_users_num.dropna(subset=['appopen','usersbydevicecount']).sample(
            min(2000, len(df_users_num)), random_state=42)
        fig, ax = plt.subplots(figsize=(7, 4))
        sns.regplot(data=df_users_num, x='usersbydevicecount', y='appopen',
                    scatter_kws={'alpha': 0.3, 's': 15, 'color': PHONEPE_PURPLE},
                    line_kws={'color': ACCENT_CORAL, 'linewidth': 2}, ax=ax)
        ax.set_xlabel('Users by Device Count')
        ax.set_ylabel('App Opens')
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f'{x/1e6:.1f}M'))
        ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f'{x/1e3:.0f}K'))
        ax.set_title('Device Users vs App Engagement', pad=12)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close()

    # ── Chart: Top 5 brands year-wise ──
    with col4:
        st.markdown("**Top 5 Brands — App Opens by Year**")
        top5_brands = (df_users_clean.groupby('usersbydevicebrand')['usersbydevicecount']
                       .sum().sort_values(ascending=False).head(5).index)
        brand_year = (df_users_clean[df_users_clean['usersbydevicebrand'].isin(top5_brands)]
                      .groupby(['year','usersbydevicebrand'])['appopen'].sum().unstack(fill_value=0))
        fig, ax = plt.subplots(figsize=(7, 4))
        brand_year.plot(kind='bar', ax=ax,
                        color=sns.color_palette('tab10', len(top5_brands)),
                        edgecolor=BG_DARK, width=0.75)
        ax.set_xlabel('Year')
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f'{x/1e9:.1f}B'))
        ax.set_title('App Opens per Brand per Year', pad=12)
        ax.legend(fontsize=8, loc='upper left')
        plt.xticks(rotation=0)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close()


# ═══════════════════════════════════════════════════════
# PAGE 5: GEO ANALYSIS
# ═══════════════════════════════════════════════════════
elif "Geo" in page:
    st.markdown('<div class="section-title">Geographical Analysis</div>', unsafe_allow_html=True)

    # ── Chart: Top 10 States by Transaction Count ──
    st.markdown("**Top 10 States by Transaction Count**")
    state_txn = (df_transaction[df_transaction['level']=='state']
                 .groupby('region')['insurancecount'].sum()
                 .sort_values(ascending=False).head(10))
    fig, ax = plt.subplots(figsize=(13, 5))
    palette = sns.color_palette('Purples_r', len(state_txn))
    bars = ax.barh(state_txn.index[::-1], state_txn.values[::-1],
                   color=palette[::-1], edgecolor=BG_DARK)
    for bar in bars:
        ax.text(bar.get_width() + max(state_txn.values)*0.005,
                bar.get_y() + bar.get_height()/2,
                fmt_count(bar.get_width()), va='center', fontsize=9, color=TEXT_WHITE)
    ax.set_xlabel('Total Transaction Count')
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: fmt_count(x)))
    ax.set_title('Top 10 States — Transaction Volume', pad=12)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close()

    st.markdown('<div class="insight-box"><strong>Key Insight:</strong> '
                'Maharashtra, Karnataka, and Telangana consistently lead in transaction volume, '
                'reflecting their tech-savvy urban populations and high smartphone penetration. '
                'North-eastern states appear in the lower half despite significant growth potential — '
                'a key opportunity for PhonePe\'s expansion strategy.</div>',
                unsafe_allow_html=True)

    # ── Chart: State × Year Heatmap ──
    st.markdown("**State × Year Transaction Heatmap (Top 15 States)**")
    top15_states = (df_transaction[df_transaction['level']=='state']
                    .groupby('region')['insurancecount'].sum()
                    .sort_values(ascending=False).head(15).index)
    heat_data = (df_transaction[(df_transaction['level']=='state') &
                                (df_transaction['region'].isin(top15_states))]
                 .groupby(['region','year'])['insurancecount'].sum().unstack(fill_value=0))
    fig, ax = plt.subplots(figsize=(14, 6))
    sns.heatmap(heat_data, cmap='Purples', annot=True, fmt='.0f',
                linewidths=0.5, linecolor=BG_DARK, ax=ax,
                annot_kws={'size': 8, 'color': TEXT_WHITE},
                cbar_kws={'label': 'Transaction Count'})
    ax.set_title('Transaction Count Heatmap — State × Year', pad=14)
    ax.set_xlabel('Year'); ax.set_ylabel('State')
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close()

    # ── Chart: Bubble chart ──
    st.markdown("**State Positioning — Count vs Value (Bubble Chart)**")
    bubble_data = (df_transaction[df_transaction['level']=='state']
                   .groupby('region')
                   .agg(total_count=('insurancecount','sum'),
                        total_amount=('insuranceamount','sum'))
                   .reset_index().dropna().nlargest(20, 'total_count'))
    sizes = (bubble_data['total_count'] / bubble_data['total_count'].max()) * 1200
    fig, ax = plt.subplots(figsize=(13, 6))
    sc = ax.scatter(bubble_data['total_count'], bubble_data['total_amount'],
                    s=sizes, alpha=0.65, c=sizes, cmap='Purples', edgecolors=PHONEPE_LIGHT, linewidth=0.8)
    for _, row in bubble_data.iterrows():
        ax.annotate(row['region'], (row['total_count'], row['total_amount']),
                    fontsize=7.5, ha='center', va='bottom', color=TEXT_WHITE,
                    xytext=(0, 7), textcoords='offset points')
    ax.set_xlabel('Total Transaction Count')
    ax.set_ylabel('Total Transaction Amount (INR)')
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: fmt_count(x)))
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: fmt_num(x)))
    ax.set_title('State Positioning Matrix — Volume vs Value', pad=12)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close()

    st.markdown('<div class="insight-box"><strong>Key Insight:</strong> '
                'States in the top-right quadrant with large bubbles are "Star Markets" — '
                'high volume AND high value (Maharashtra, Karnataka). States with large bubbles '
                'but low Y-axis position are "Volume-Heavy but Low-Value" — high transaction frequency '
                'with low per-transaction amounts, suggesting different user demographics or use-cases.</div>',
                unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# PAGE 6: TREND ANALYSIS
# ═══════════════════════════════════════════════════════
elif "Trend" in page:
    st.markdown('<div class="section-title">Trend Analysis</div>', unsafe_allow_html=True)

    # ── Chart: Quarterly transaction trend multi-line ──
    st.markdown("**Quarterly Transaction Count — Year-over-Year**")
    trend = (df_transaction.groupby(['year','quater'])['insurancecount']
             .sum().reset_index().sort_values(['year','quater']))
    fig, ax = plt.subplots(figsize=(13, 5))
    palette = sns.color_palette('tab10', n_colors=trend['year'].nunique())
    for idx, (yr, grp) in enumerate(trend.groupby('year')):
        ax.plot(grp['quater'], grp['insurancecount'],
                marker='o', label=str(yr), color=palette[idx], linewidth=2.2, markersize=7)
    ax.set_xlabel('Quarter'); ax.set_ylabel('Transaction Count')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: fmt_count(x)))
    ax.set_title('Year-over-Year Quarterly Transaction Volume', pad=12)
    ax.legend(title='Year', loc='upper left', fontsize=9)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close()

    # ── Chart: Year + Quarter grouped bars ──
    st.markdown("**Transaction Amount — Year × Quarter Grouped**")
    year_qtr = (df_transaction.groupby(['year','quater'])['insuranceamount']
                .sum().unstack(fill_value=0))
    fig, ax = plt.subplots(figsize=(13, 5))
    year_qtr.plot(kind='bar', ax=ax,
                  color=[PHONEPE_PURPLE, PHONEPE_LIGHT, ACCENT_GOLD, ACCENT_TEAL],
                  edgecolor=BG_DARK, width=0.75)
    ax.set_xlabel('Year')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: fmt_num(x)))
    ax.set_title('Total Transaction Amount by Year and Quarter', pad=12)
    ax.legend(title='Quarter', fontsize=9)
    plt.xticks(rotation=0)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close()

    st.markdown('<div class="insight-box"><strong>Key Insight:</strong> '
                'Lines shifting upward with each successive year confirm sustained growth without '
                'seasonal regression. Q4 consistently shows higher amounts due to festive season '
                'purchases (Diwali, New Year). The 2020-2021 acceleration aligns with COVID-19 '
                'accelerating India\'s digital payment adoption. Q2 dips in multiple years may '
                'reflect academic-year slowdowns in consumer spending.</div>',
                unsafe_allow_html=True)

    # ── Chart: 100% stacked bar — payment mix by quarter ──
    st.markdown("**Payment Mix by Quarter (100% Stacked)**")
    pivot_qtr_type = (df_transaction.groupby(['quater','insurancetype'])['insurancecount']
                      .sum().unstack(fill_value=0))
    pivot_pct = pivot_qtr_type.div(pivot_qtr_type.sum(axis=1), axis=0) * 100
    fig, ax = plt.subplots(figsize=(10, 5))
    pivot_pct.plot(kind='bar', stacked=True, ax=ax,
                   colormap='tab10', edgecolor=BG_DARK, width=0.5)
    ax.set_xlabel('Quarter'); ax.set_ylabel('Percentage (%)')
    ax.set_title('Payment Type Composition by Quarter (100% Stacked)', pad=12)
    ax.legend(fontsize=8, bbox_to_anchor=(1.01, 1), loc='upper left')
    plt.xticks(rotation=0)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close()

    # ── Chart: Top 5 states insurance trend ──
    st.markdown("**Top 5 States — Insurance Amount Over Years**")
    top5_ins_states = (df_insurance[df_insurance['level']=='state']
                       .groupby('region')['insuranceamount'].sum()
                       .sort_values(ascending=False).head(5).index)
    ins_trend = (df_insurance[(df_insurance['level']=='state') &
                               (df_insurance['region'].isin(top5_ins_states))]
                 .groupby(['region','year'])['insuranceamount'].sum().reset_index())
    fig, ax = plt.subplots(figsize=(12, 5))
    for i, state in enumerate(top5_ins_states):
        sdata = ins_trend[ins_trend['region']==state].sort_values('year')
        ax.plot(sdata['year'], sdata['insuranceamount'],
                marker='o', label=state,
                color=sns.color_palette('tab10')[i],
                linewidth=2.2, markersize=7)
    ax.set_xlabel('Year'); ax.set_ylabel('Total Insurance Amount (INR)')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: fmt_num(x)))
    ax.set_title('Insurance Amount Growth — Top 5 States', pad=12)
    ax.legend(fontsize=9); ax.grid(True, alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close()


# ═══════════════════════════════════════════════════════
# PAGE 7: CORRELATION & MULTI-VAR
# ═══════════════════════════════════════════════════════
elif "Correlation" in page:
    st.markdown('<div class="section-title">Correlation & Multi-variable Analysis</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    # ── Correlation Heatmap ──
    with col1:
        st.markdown("**Correlation Matrix — Transaction Numerics**")
        numeric_cols = df_transaction[['insurancecount','insuranceamount']].dropna()
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.heatmap(numeric_cols.corr(), annot=True, fmt='.3f',
                    cmap='Purples', linewidths=1.5, square=True,
                    cbar_kws={'shrink': 0.7}, ax=ax,
                    annot_kws={'size': 14, 'color': TEXT_WHITE, 'fontweight': 'bold'})
        ax.set_title('Correlation Matrix', pad=12)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close()

    # ── Insurance correlation heatmap ──
    with col2:
        st.markdown("**Correlation Matrix — Insurance Numerics**")
        ins_num = df_insurance[['insurancecount','insuranceamount']].dropna()
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.heatmap(ins_num.corr(), annot=True, fmt='.3f',
                    cmap='RdPu', linewidths=1.5, square=True,
                    cbar_kws={'shrink': 0.7}, ax=ax,
                    annot_kws={'size': 14, 'color': TEXT_WHITE, 'fontweight': 'bold'})
        ax.set_title('Correlation Matrix — Insurance', pad=12)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close()

    st.markdown('<div class="insight-box"><strong>Key Insight:</strong> '
                'A high correlation (>0.7) between transaction count and amount confirms that '
                'high-volume regions are also high-value — making them doubly strategic for '
                'partnership investments and merchant acquisition campaigns.</div>',
                unsafe_allow_html=True)

    # ── Violin Plot ──
    st.markdown("**Transaction Amount Distribution by Quarter (Violin Plot)**")
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.violinplot(data=df_transaction.dropna(subset=['insuranceamount']),
                   x='quater', y='insuranceamount',
                   palette='Purples', inner='quartile', ax=ax)
    ax.set_xlabel('Quarter'); ax.set_ylabel('Transaction Amount (INR)')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: fmt_num(x)))
    ax.set_title('Quarterly Distribution of Transaction Amounts', pad=12)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close()

    # ── Users pairplot-style scatter ──
    st.markdown("**Device Count vs App Opens — Multi-segment Scatter**")
    top5b = (df_users_clean.groupby('usersbydevicebrand')['usersbydevicecount']
             .sum().sort_values(ascending=False).head(5).index)
    seg_filtered = df_users_clean[df_users_clean['usersbydevicebrand'].isin(top5b)]
    seg_data = seg_filtered.sample(
        min(3000, len(seg_filtered)), random_state=42)
    fig, ax = plt.subplots(figsize=(12, 5))
    pal5 = sns.color_palette('tab10', 5)
    for i, brand in enumerate(top5b):
        bd = seg_data[seg_data['usersbydevicebrand']==brand]
        ax.scatter(bd['usersbydevicecount'], bd['appopen'],
                   alpha=0.35, s=18, color=pal5[i], label=brand)
    ax.set_xlabel('Users by Device Count')
    ax.set_ylabel('App Opens')
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f'{x/1e3:.0f}K'))
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f'{x/1e6:.0f}M'))
    ax.set_title('Device User Count vs App Opens by Brand', pad=12)
    ax.legend(fontsize=9)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close()


# ═══════════════════════════════════════════════════════
# PAGE 8: BUSINESS SUMMARY
# ═══════════════════════════════════════════════════════
elif "Business" in page:
    st.markdown('<div class="section-title">Business Summary & Recommendations</div>', unsafe_allow_html=True)

    business_cases = [
        ("🎯", "Customer Segmentation",
         "High-volume states (Maharashtra, Karnataka, Telangana) and Samsung/Xiaomi users "
         "form the core segment. Target premium users on OnePlus/Apple for financial services upsell."),
        ("🚨", "Fraud Detection",
         "Right-skewed transaction distributions with extreme outliers warrant automated "
         "anomaly detection. High-value outliers in insurance data should trigger manual review workflows."),
        ("🗺️", "Geographical Expansion",
         "North-eastern states show low volume despite demographic potential. Tier-2 and Tier-3 city "
         "campaigns with vernacular content can unlock the next 100M users."),
        ("💳", "Payment Category Strategy",
         "Merchant payments carry the highest average ticket size — investing in merchant onboarding "
         "directly drives revenue per transaction. Recharge payments drive frequency and retention."),
        ("📲", "User Engagement",
         "Q4 festive season shows peak engagement. Pre-season campaigns (Sep-Oct) with cashback "
         "offers can maximise activation and transaction volume during Diwali cycles."),
        ("🛡️", "Insurance Diversification",
         "Insurance product diversity is limited — TOTAL type dominates. Introduce term life, "
         "health, and vehicle insurance bundles to diversify revenue and increase policy counts."),
        ("📈", "Trend Capitalisation",
         "Post-COVID (2021+) shows the steepest growth acceleration. Sustaining this requires "
         "continuous UX improvements and offline-to-online merchant integrations."),
        ("🏆", "Competitive Benchmarking",
         "Consistent YoY growth validates platform health. Focus on reducing churn in "
         "low-engagement states through personalised nudges and loyalty rewards."),
    ]

    for i in range(0, len(business_cases), 2):
        c1, c2 = st.columns(2)
        for col, (icon, title, text) in zip([c1, c2], business_cases[i:i+2]):
            with col:
                st.markdown(f"""
                <div style='background:linear-gradient(135deg,{BG_CARD},{PHONEPE_DARK}); 
                            border:1px solid {PHONEPE_PURPLE}88; border-radius:14px; 
                            padding:20px 22px; margin-bottom:14px;
                            box-shadow: 0 4px 20px #5f259f22;'>
                  <div style='font-size:1.5rem; margin-bottom:8px;'>{icon}</div>
                  <div style='font-family:Rajdhani,sans-serif; font-size:1.1rem; 
                              font-weight:700; color:{ACCENT_GOLD}; margin-bottom:8px;'>{title}</div>
                  <div style='color:#ddd4f5; font-size:0.92rem; line-height:1.65;'>{text}</div>
                </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-title" style="font-size:1.3rem; margin-top:30px;">Conclusion</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="insight-box" style="border-left-color:{ACCENT_GOLD};">
    <strong>Project Conclusion:</strong><br><br>
    This EDA successfully demonstrates a structured data engineering pipeline — from raw nested JSON files 
    to a clean, queryable relational database — forming the analytical backbone of the PhonePe Pulse dashboard.<br><br>
    
    Key findings confirm that <strong>PhonePe's transaction growth is sustained and accelerating</strong>, 
    driven primarily by urban tech-hubs (Maharashtra, Karnataka) with Samsung and Xiaomi users forming 
    the dominant demographic. The post-2020 surge validates digital payment adoption as a structural shift 
    in Indian consumer behaviour.<br><br>
    
    Strategic priorities include: expanding into under-penetrated states, diversifying insurance products, 
    optimising for festive season peaks, and leveraging device-level segmentation for targeted campaigns.
    </div>
    """, unsafe_allow_html=True)

    # Tech stack
    st.markdown('<div class="section-title" style="font-size:1.3rem;">Technical Stack</div>', unsafe_allow_html=True)
    cols = st.columns(5)
    for col, (tech, desc) in zip(cols, [
        ("🐍 Python", "Pandas · NumPy · SQLAlchemy"),
        ("🗄️ MySQL", "Relational DB · 3 tables"),
        ("📊 Seaborn", "Statistical Visualization"),
        ("📉 Matplotlib", "Custom Plot Theming"),
        ("🚀 Streamlit", "Interactive Dashboard"),
    ]):
        with col:
            st.markdown(f"""
            <div style='background:{BG_CARD}; border:1px solid {PHONEPE_PURPLE}66; 
                        border-radius:10px; padding:14px; text-align:center;'>
              <div style='font-size:1.1rem; font-weight:700; color:{ACCENT_GOLD};'>{tech}</div>
              <div style='font-size:0.78rem; color:#a57bd6; margin-top:4px;'>{desc}</div>
            </div>""", unsafe_allow_html=True)


# ─── Footer ───
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(f"""
<div style='text-align:center; color:#4a3a7a; font-size:0.82rem; padding:16px; 
            border-top:1px solid {PHONEPE_PURPLE}33;'>
  PhonePe Transaction Insights · EDA Capstone Project · Built with Streamlit
</div>""", unsafe_allow_html=True)