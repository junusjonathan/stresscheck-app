"""
StresCheck — app.py
Modern SaaS Stress Prediction System for Students
Fully redesigned: Medical SaaS aesthetic, Teal brand, Glassmorphism + Glow effects
"""

import streamlit as st
import pandas as pd
import joblib
import json
from streamlit_lottie import st_lottie
import streamlit.components.v1 as components

# ══════════════════════════════════════════════════════════════════
# ⚙️  BOOTSTRAP — Must be the very first Streamlit call
# ══════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="StresCheck — Deteksi Dini Stres Mahasiswa",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── INJECT FONT GLOBAL SECARA BRUTAL (OUTFIT & DM SANS) ─────────────────
st.markdown("""
    <style>
        /* 1. Import Font Google */
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600;9..40,700&family=Outfit:wght@500;600;700;800&display=swap');
        
        /* 2. Target Body & Elemen Umum Streamlit (DM Sans) */
        html, body, [class*="css"], *, 
        .stMarkdown, p, span, div, label, 
        .stButton button, .stNumberInput input, .stSlider div, 
        .stRadio div {
            font-family: "DM Sans", sans-serif !important;
        }
        
        /* 3. Target Heading & Judul Spesifik (Outfit) */
        h1, h2, h3, h4, h5, h6, 
        .sc-title, .akhir-title, .sc-nav-wordmark, 
        .sc-metric-val, .akhir-stat-val, 
        .sc-rekom-title, .sc-result-level {
            font-family: "Outfit", sans-serif !important;
        }
        
        /* 4. Fix Font Tombol Streamlit biar proporsional */
        .stButton button p {
            font-family: "DM Sans", sans-serif !important;
            font-weight: 600 !important;
        }
    </style>
""", unsafe_allow_html=True)


# ── Load external CSS ──────────────────────────────────────────────
def load_css(path: str):
    with open(path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("style.css")


# ── Load model ────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    return joblib.load("model_rf_final.pkl")

try:
    model = load_model()
except Exception:
    model = None  # Graceful degradation during development

# ── Session state ─────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "Beranda"

def goto(page: str):
    st.session_state.page = page

def scroll_top():
    components.html(
        "<script>window.parent.scrollTo(0,0);"
        "var m=window.parent.document.querySelector('.main');"
        "if(m)m.scrollTo(0,0);</script>",
        height=0,
    )

# ── Lottie helper ─────────────────────────────────────────────────
def load_lottie(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)
    

# ══════════════════════════════════════════════════════════════════
# 🧩 SHARED COMPONENTS
# ══════════════════════════════════════════════════════════════════

# Top "glass" navbar — injects a fixed header above Streamlit content
NAVBAR_HTML = """
<style>
.sc-nav {
  position: sticky;
  top: 0;
  z-index: 999;
  width: 100%;
  padding: 14px 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: rgba(248,250,252,0.78);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-bottom: 1px solid rgba(148,163,184,0.18);
  margin-bottom: 12px;
}
.sc-nav-logo {
  display: flex;
  align-items: center;
  gap: 10px;
}
.sc-nav-logo-icon {
  width: 34px; height: 34px;
  border-radius: 10px;
  background: linear-gradient(135deg, #0d9488 0%, #14b8a6 100%);
  display: flex; align-items: center; justify-content: center;
  font-size: 1.1rem;
  box-shadow: 0 4px 14px rgba(13,148,136,.30);
}
.sc-nav-wordmark {
  font-family: 'Syne', sans-serif;
  font-size: 1.15rem;
  font-weight: 800;
  color: #0f172a;
  letter-spacing: -0.04em;
}
.sc-nav-wordmark span { color: #0d9488; }
.sc-nav-badge {
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: 4px 12px;
  border-radius: 999px;
  background: #f0fdfa;
  border: 1px solid #99f6e4;
  color: #0f766e;
}
</style>
<div class="sc-nav">
  <div class="sc-nav-logo">
    <div class="sc-nav-logo-icon">🧠</div>
    <span class="sc-nav-wordmark">Stres<span>Check</span></span>
  </div>
  <span class="sc-nav-badge">Beta v1.0</span>
</div>
"""

def render_navbar():
    st.markdown(NAVBAR_HTML, unsafe_allow_html=True)

def render_steps(active: int):
    """Progress step indicator. active: 1=Beranda, 2=Form, 3=Hasil"""
    steps = [
        ("🏠", "Beranda"),
        ("📝", "Isi Data"),
        ("📊", "Hasil"),
    ]
    items = ""
    for i, (icon, label) in enumerate(steps, 1):
        if i < active:
            cls = "done"
        elif i == active:
            cls = "active"
        else:
            cls = ""
        sep = "<span class='sc-step-sep'>—</span>" if i < len(steps) else ""
        
        # FIX: HTML dirapatkan jadi satu baris biar Streamlit gak ngira ini code block
        items += f"<div class='sc-step {cls}'><div class='sc-step-circle'>{icon if i >= active else '✓'}</div><span>{label}</span></div>{sep}"

    # FIX: CSS dan Div pembungkus juga dirapatkan ke kiri
    html_code = f"""<style>
.sc-steps {{ display: flex; align-items: center; justify-content: center; gap: 8px; margin: 28px 0 36px; }}
.sc-step {{ display: flex; align-items: center; gap: 7px; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.82rem; font-weight: 600; color: #94a3b8; }}
.sc-step.done {{ color: #0d9488; }}
.sc-step.active {{ color: #0f172a; font-weight: 700; }}
.sc-step-circle {{ width: 28px; height: 28px; border-radius: 50%; background: #e2e8f0; color: #94a3b8; display: flex; align-items: center; justify-content: center; font-size: 0.78rem; transition: all .2s; }}
.sc-step.done .sc-step-circle {{ background: #0d9488; color: #fff; font-size: 0.68rem; }}
.sc-step.active .sc-step-circle {{ background: #0f172a; color: #fff; box-shadow: 0 0 0 4px rgba(13,148,136,.2); }}
.sc-step-sep {{ color: #e2e8f0; font-size: 0.75rem; margin: 0 4px; }}
</style>
<div class="sc-steps">{items}</div>
"""
    st.markdown(html_code, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# 🏠  PAGE 1 — BERANDA (FIXED LOGO & TEXT ALIGNMENT)
# ══════════════════════════════════════════════════════════════════
if st.session_state.page == "Beranda":
    scroll_top()
    render_navbar()

    # ── Hero Section ──────────────────────────────────────────────
    st.markdown("""
    <style>
    /* FIX 2: Paksa semua elemen di dalam hero ke tengah pakai Flexbox */
    .sc-hero {
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      padding: 40px 20px 10px;
    }
    .sc-hero-eyebrow {
      display: inline-flex; align-items: center; gap: 6px;
      padding: 5px 14px;
      background: #f0fdfa;
      border: 1px solid #99f6e4;
      border-radius: 999px;
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 0.75rem; font-weight: 700;
      letter-spacing: 0.1em; text-transform: uppercase;
      color: #0f766e;
      margin-bottom: 20px;
    }
    .sc-hero h1 {
      font-family: 'Syne', sans-serif !important;
      font-size: clamp(2.2rem, 5vw, 3.2rem) !important;
      font-weight: 900 !important;
      color: #0f172a !important;
      line-height: 1.1 !important;
      letter-spacing: -0.04em !important;
      margin: 0 0 16px !important;
    }
    .sc-hero h1 span { color: #0d9488; }
    
    /* FIX 2: Margin dan lebar disesuaikan agar rapi di tengah */
    .sc-hero-sub {
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 1.1rem; line-height: 1.6;
      color: #475569;
      width: 100%;
      max-width: 600px;
      margin: 10px auto 25px auto;
    }
    </style>
    <div class="sc-hero">
      <div class="sc-hero-eyebrow">🔬 Berbasis Machine Learning · Random Forest</div>
      <h1>Kenali Tingkat Stres<br>Digitalmu <span>Hari Ini</span></h1>
      <p class="sc-hero-sub">
        Sistem prediksi cerdas yang menganalisis pola aktivitas digital harian
        Anda untuk mendeteksi dini risiko stres mahasiswa.
      </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Logo + Lottie ─────────────────────────────────────────────
    # FIX 1: Kolom tengah dibikin sangat sempit [4, 1.2, 4] biar logonya otomatis kecil & nengah
    c_logo1, c_logo2, c_logo3 = st.columns([4, 1.2, 4])
    with c_logo2:
        try:
            st.image("logo_kampus.png", use_container_width=True)
        except Exception:
            pass


# ── About Section: Card Container (STABLE VERSION + SHIMMER LINE) ──
    
    about_container = st.container(border=True) 
    
    with about_container:
        st.markdown("""
        <style>
        /* Target container border dari st.container(border=True) */
        [data-testid="stVerticalBlock"]:has(.about-card-marker) {
            background: #transparent;
            border-radius: 20px !important;
            border: 1px solid #e2e8f0 !important;
            box-shadow: 0 4px 24px rgba(15,23,42,.06) !important;
            padding: 30px !important;
            margin-bottom: 30px !important;
            position: relative;
            overflow: hidden; /* Biar garis gak keluar dari border radius */
        }
        
        /* Garis Shimmer nempel di top border */
        .shimmer-line {
            position: absolute;
            top: -1px; /* Geser dikit biar pas nutupin top border */
            left: 0; right: 0;
            height: 4px;
            background: linear-gradient(90deg, #0d9488, #2dd4bf, #0d9488);
            background-size: 200%;
            animation: shimmer-anim 3s linear infinite;
            z-index: 1; /* Biar selalu di paling depan */
            border-radius: 20px 20px 0 0; /* Ngikutin lengkungan border atas */
        }
        @keyframes shimmer-anim {
            0% { background-position: 0%; }
            100% { background-position: 200%; }
        }
        </style>
        <div class="about-card-marker"></div>
        <div class="shimmer-line"></div>
        """, unsafe_allow_html=True)
        
        # 2. Bikin kolom di DALAM container
        col_anim, col_text = st.columns([1, 2], gap="large")
        
        with col_anim:
            st.markdown("<div style='height: 100%; display: flex; align-items: center; justify-content: center;'>", unsafe_allow_html=True)
            try:
                st_lottie(load_lottie("animasi.json"), height=240, key="about_anim")
            except:
                st.markdown("<div style='font-size:3rem; text-align:center;'>🧠</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_text:
            st.markdown("""
            <div style='display: flex; flex-direction: column; justify-content: center; height: 240px;'>
                <h3 style='font-family: "Syne", sans-serif; font-size: 1.6rem; color: #0f766e; font-weight: 800; margin: 0 0 12px;'>Tentang Sistem Ini</h3>
                <p style='font-family: "Plus Jakarta Sans", sans-serif; font-size: 1.05rem; color: #475569; line-height: 1.7; margin: 0;'>
                    Selamat datang! Aplikasi ini mendeteksi dini tingkat stres mahasiswa berdasarkan pola aktivitas digital sehari-hari. Masukkan data dengan jujur dan benar untuk mendapatkan hasil prediksi dan rekomendasi yang tepat.
                </p>
            </div>
            """, unsafe_allow_html=True)


    # ── Feature metric page ───────────────────────────────────────
    st.markdown("""
    <style>
    .sc-metrics {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 14px;
      margin-bottom: 40px;
    }
    .sc-metric {
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 16px;
      padding: 22px 18px;
      text-align: center;
      box-shadow: 0 2px 12px rgba(15,23,42,.05);
      transition: transform .2s, box-shadow .2s;
    }
    .sc-metric:hover {
      transform: translateY(-3px);
      box-shadow: 0 8px 28px rgba(13,148,136,.12);
    }
    .sc-metric-icon { font-size: 1.6rem; margin-bottom: 10px; }
    .sc-metric-val {
      font-family: 'Syne', sans-serif;
      font-size: 1.5rem; font-weight: 800;
      color: #0f766e;
      margin-bottom: 4px;
    }
    .sc-metric-lbl {
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 0.8rem; font-weight: 600;
      color: #94a3b8;
      text-transform: uppercase;
      letter-spacing: 0.06em;
    }
    </style>
    <div class="sc-metrics">
      <div class="sc-metric">
        <div class="sc-metric-icon">📊</div>
        <div class="sc-metric-val">6 Fitur</div>
        <div class="sc-metric-lbl">Input Digital</div>
      </div>
      <div class="sc-metric">
        <div class="sc-metric-icon">⚡</div>
        <div class="sc-metric-val">&lt; 5 Detik</div>
        <div class="sc-metric-lbl">Waktu Proses</div>
      </div>
      <div class="sc-metric">
        <div class="sc-metric-icon">🎯</div>
        <div class="sc-metric-val">3 Level</div>
        <div class="sc-metric-lbl">Klasifikasi Stres</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── CTA Button ────────────────────────────────────────────────
    _, btn_col, _ = st.columns([2, 1.4, 2])
    with btn_col:
        if st.button("Mulai Prediksi Sekarang 🚀", use_container_width=True):
            goto("FormInput")
            st.rerun()

    # ── Footer note ───────────────────────────────────────────────
    st.markdown("""
    <p style='text-align:center; margin-top:32px; font-size:0.78rem; color:#cbd5e1;
       font-family:"Plus Jakarta Sans",sans-serif;'>
      Hanya untuk keperluan edukasi dan penelitian. Bukan pengganti diagnosis profesional.
    </p>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# 📝  PAGE 2 — FORM INPUT (FIXED STREAMLIT RENDERING)
# ══════════════════════════════════════════════════════════════════
elif st.session_state.page == "FormInput":
    scroll_top()
    render_navbar()
    render_steps(active=2)

    # ── Section title ─────────────────────────────────────────────
    st.markdown("""
    <div style='text-align:center; margin-bottom:8px;'>
      <h2 style='font-family:"Syne",sans-serif!important; font-size:2rem!important;
         font-weight:900!important; color:#0f172a!important; letter-spacing:-0.03em!important;
         margin:0!important;'>
        Formulir Aktivitas Digital
      </h2>
      <p style='font-family:"Plus Jakarta Sans",sans-serif; color:#64748b;
         font-size:0.97rem; margin:8px 0 28px;'>
        Isi berdasarkan rata-rata kebiasaan Anda dalam <strong>satu minggu terakhir</strong>.
      </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Petunjuk banner ───────────────────────────────────────────
    st.markdown("""
    <style>
    .sc-tip {
      display: flex; align-items: flex-start; gap: 14px;
      background: #f0fdfa;
      border: 1px solid #99f6e4;
      border-radius: 14px;
      padding: 16px 20px;
      margin-bottom: 28px;
    }
    .sc-tip-icon { font-size: 1.2rem; margin-top: 1px; flex-shrink: 0; }
    .sc-tip p {
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 0.88rem; color: #115e59;
      line-height: 1.65; margin: 0;
    }
    .sc-tip strong { color: #0f766e; }
    </style>
    <div class="sc-tip">
      <span class="sc-tip-icon">💡</span>
      <p>
        <strong>Petunjuk Pengisian:</strong> Masukkan durasi dalam jam per hari.
        Untuk intensitas, pilih skala yang paling sesuai kondisi Anda.
        Kejujuran data menentukan kualitas prediksi.
      </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Two-column form ───────────────────────────────────────────
    col_l, col_r = st.columns(2, gap="large")

    with col_l:
        st.markdown("<h4 style='color:#0f766e; font-family:\"Syne\",sans-serif; font-size:1.1rem; font-weight:800; border-bottom:2px solid #f1f5f9; padding-bottom:10px; margin-bottom:20px;'>🕒 Durasi Penggunaan (Jam/Hari)</h4>", unsafe_allow_html=True)
        screentime = st.number_input(
            "Total Screen Time Keseluruhan",
            min_value=0.0, max_value=24.0, value=8.0, step=0.5,
            help="Total waktu menatap layar HP/Laptop dalam sehari",
        )
        medsos = st.number_input(
            "Durasi Media Sosial",
            min_value=0.0, max_value=24.0, value=3.0, step=0.5,
            help="Instagram, TikTok, Twitter, YouTube, dll.",
        )
        akademik = st.number_input(
            "Durasi Keperluan Akademik",
            min_value=0.0, max_value=24.0, value=2.0, step=0.5,
            help="Kuliah online, tugas, cari jurnal, dll.",
        )
        hiburan = st.number_input(
            "Durasi Hiburan",
            min_value=0.0, max_value=24.0, value=3.0, step=0.5,
            help="Main game, nonton film/series, dll.",
        )

    with col_r:
        st.markdown("<h4 style='color:#0f766e; font-family:\"Syne\",sans-serif; font-size:1.1rem; font-weight:800; border-bottom:2px solid #f1f5f9; padding-bottom:10px; margin-bottom:20px;'>📱 Intensitas & Kebiasaan Digital</h4>", unsafe_allow_html=True)

        st.markdown(
            "<p style='font-weight:700;font-size:.87rem;color:#475569;margin-bottom:4px;"
            "font-family:\"Plus Jakarta Sans\",sans-serif;'>Frekuensi Cek Notifikasi</p>",
            unsafe_allow_html=True,
        )
        notifikasi = st.slider(
            "Notif (1=Sangat Jarang · 5=Sangat Sering)",
            min_value=1, max_value=5, value=3,
            label_visibility="collapsed",
        )
        # Visual label row
        st.markdown("""
        <div style='display:flex;justify-content:space-between;
             font-size:.72rem;color:#94a3b8;
             font-family:"Plus Jakarta Sans",sans-serif;
             margin:2px 0 20px;'>
          <span>Sangat Jarang</span><span>Sangat Sering</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(
            "<p style='font-weight:700;font-size:.87rem;color:#475569;margin-bottom:8px;"
            "font-family:\"Plus Jakarta Sans\",sans-serif;'>Penggunaan Gadget Larut Malam</p>",
            unsafe_allow_html=True,
        )
        malam_radio = st.radio(
            "Seberapa sering memakai gadget melewati jam tidur?",
            ("Sangat Jarang", "Jarang", "Kadang-kadang", "Sering", "Sangat Sering"),
            index=2,
            label_visibility="collapsed",
        )

    malam_val = {
        "Sangat Jarang": 1, "Jarang": 2,
        "Kadang-kadang": 3, "Sering": 4, "Sangat Sering": 5,
    }[malam_radio]

# ── Summary preview bar (FIXED LOGIC & OVERFLOW) ───────────────
    total_tracked = medsos + akademik + hiburan
    # Hitung rasio asli
    raw_pct = (total_tracked / max(screentime, 0.01)) * 100
    
    # Kunci persentase maksimal di 100% buat progress bar biar gak bocor
    bar_pct = min(int(raw_pct), 100)
    
    # Tentukan status warna dan teks peringatan (SaaS feel)
    if raw_pct > 100:
        bar_color = "linear-gradient(90deg, #ef4444, #f87171)" # Merah peringatan
        status_text = f"<span style='color: #ef4444; font-size: 0.8rem; margin-left: auto; font-weight: 600;'>⚠️ Input melebihi Screentime</span>"
        display_pct = f"{int(raw_pct)}%" # Tetap tampilkan angka aslinya
    else:
        bar_color = "linear-gradient(90deg, #0d9488, #2dd4bf)" # Teal normal
        status_text = ""
        display_pct = f"{bar_pct}%"

    st.markdown(f"""
    <style>
    .sc-summary {{
      background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 14px;
      padding: 16px 22px; margin: 20px 0 8px; display: flex; align-items: center; gap: 20px; flex-wrap: wrap;
    }}
    .sc-summary-label {{ font-family:'Plus Jakarta Sans',sans-serif; font-size:.8rem;font-weight:700;color:#64748b; text-transform:uppercase;letter-spacing:.06em; flex-shrink:0; }}
    .sc-bar-wrap {{ flex:1;min-width:160px; height:8px;background:#e2e8f0;border-radius:999px;overflow:hidden; }}
    .sc-bar-fill {{ height:100%;border-radius:999px; background:{bar_color}; width:{bar_pct}%;transition:width .5s ease, background .3s ease; }}
    .sc-summary-pct {{ font-family:'Syne',sans-serif; font-size:1.1rem;font-weight:800;color:#0f172a; flex-shrink:0; }}
    </style>
    <div class="sc-summary">
      <span class="sc-summary-label">📊 Waktu tercatat vs total screen time</span>
      <div class="sc-bar-wrap"><div class="sc-bar-fill"></div></div>
      <span class="sc-summary-pct">{display_pct}</span>
      {status_text}
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    # ── Tempat Kosong untuk Notifikasi Error ──────────────────────
    error_placeholder = st.empty()

# ── Navigation buttons ────────────────────────────────────────
    col_back, _, col_submit = st.columns([1, 1, 1.6])

    with col_back:
        # Tambahkan key="btn_back_form"
        if st.button("⬅️  Kembali", use_container_width=True, key="btn_back_form"):
            goto("Beranda")
            st.rerun()

    with col_submit:
        # Tambahkan key="btn_submit_form"
        if st.button("Lihat Hasil Prediksi  🔍", use_container_width=True, key="btn_submit_form"):
            
            # CEK VALIDASI SAAT TOMBOL DIKLIK
            if raw_pct > 100:
                # Kalau input salah, isi tempat kosong tadi dengan notifikasi merah
                error_placeholder.markdown("""
                <div style='background: #fef2f2; border: 1px solid #fecaca; border-radius: 12px; padding: 14px 20px; margin-bottom: 20px; display: flex; gap: 12px; align-items: center;'>
                    <span style='font-size: 1.2rem;'>🚨</span>
                    <p style='font-family: "Plus Jakarta Sans", sans-serif; font-size: 0.95rem; color: #b91c1c; margin: 0; font-weight: 500;'>
                        <strong>Gagal Memproses:</strong> Total durasi aktivitas (Medsos + Akademik + Hiburan) melebihi Total Screen Time. Sesuaikan kembali sebelum melihat hasil.
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Kalau input benar (<= 100%), lanjut ke halaman Hasil
                if model:
                    input_df = pd.DataFrame({
                        "Medsos": [medsos],
                        "Akademik": [akademik],
                        "Hiburan": [hiburan],
                        "Screentime": [screentime],
                        "Frekuensi Notifikasi": [notifikasi],
                        "Frekuensi Malam": [malam_val],
                    })
                    st.session_state.hasil = model.predict(input_df)[0]
                else:
                    st.session_state.hasil = "SEDANG"  # Demo fallback
                
                goto("Hasil")
                st.rerun()


# ══════════════════════════════════════════════════════════════════
# 📊  PAGE 3 — HASIL PREDIKSI
# ══════════════════════════════════════════════════════════════════
elif st.session_state.page == "Hasil":
    scroll_top()
    render_navbar()
    render_steps(active=3)

# ── Level config ──────────────────────────────────────────────
    res = str(st.session_state.hasil).upper()

    LEVEL = {
        "RENDAH": {
            "ca":          "#059669",
            "ca_dark":     "#064e3b",
            "bg":          "#f0fdf4",
            "badge_bg":    "#d1fae5",
            "border":      "#a7f3d0",
            "glow":        "rgba(5,150,105,.22)",
            "glow_strong": "rgba(5,150,105,.35)",
            "icon":        "🌿",
            "badge":       "Status Aman",
            "anim":        "rendah.json",
            "pesan":       "Aktivitas digital Anda berada dalam batas wajar dan <strong>tidak memicu stres signifikan</strong>. Pertahankan kebiasaan sehat ini!",
            "rekom_title": "Tips Mempertahankan Kondisi Baik",
            "rekom_icon":  "✅",
            "items": [
                ("Konsistensi adalah kunci",
                 "Teruslah menyeimbangkan waktu layar dengan aktivitas fisik dan interaksi sosial langsung."),
                ("Tetapkan jadwal bebas gadget",
                 "Coba 1 jam tanpa layar sebelum tidur untuk kualitas istirahat yang lebih baik."),
                ("Jaga hubungan di dunia nyata",
                 "Perkuat koneksi interpersonal di luar dunia maya demi kesehatan mental jangka panjang."),
            ],
            "fun_fact": "Riset membuktikan membatasi screen time hiburan di bawah 2 jam sehari menjaga risiko depresi di titik terendah dan secara signifikan meningkatkan kebahagiaan Anda."
        },
        "SEDANG": {
            "ca":          "#d97706",
            "ca_dark":     "#78350f",
            "bg":          "#fffbeb",
            "badge_bg":    "#fef3c7",
            "border":      "#fcd34d",
            "glow":        "rgba(217,119,6,.20)",
            "glow_strong": "rgba(217,119,6,.35)",
            "icon":        "⚠️",
            "badge":       "Perlu Perhatian",
            "anim":        "sedang.json",
            "pesan":       "Aktivitas digital Anda mulai menimbulkan tekanan. <strong>Segera ambil langkah kecil</strong> sebelum stres meningkat lebih jauh.",
            "rekom_title": "Rekomendasi Manajemen Stres",
            "rekom_icon":  "💡",
            "items": [
                ("Batasi media sosial",
                 "Kurangi screen time yang tidak esensial, terutama scrolling tanpa tujuan."),
                ("Terapkan aturan 20-20-20",
                 "Setiap 20 menit, istirahatkan mata 20 detik dengan melihat benda sejauh 20 kaki."),
                ("Matikan notifikasi saat fokus",
                 "Non-aktifkan notifikasi saat belajar atau beristirahat untuk mengurangi gangguan kognitif."),
                ("Aktivitas fisik harian",
                 "Luangkan 30 menit sehari untuk olahraga ringan atau hobi di luar ruangan."),
            ],
            "fun_fact": "Sekadar melihat HP tergeletak di meja (meski layar mati) bisa bikin otak cepat lelah. Riset membuktikan otak kita diam-diam menguras energinya sendiri karena terus menahan godaan untuk mengecek HP."
        },
        "TINGGI": {
            "ca":          "#dc2626",
            "ca_dark":     "#7f1d1d",
            "bg":          "#fef2f2",
            "badge_bg":    "#fee2e2",
            "border":      "#fca5a5",
            "glow":        "rgba(220,38,38,.18)",
            "glow_strong": "rgba(220,38,38,.32)",
            "icon":        "🚨",
            "badge":       "Butuh Tindakan Segera",
            "anim":        "tinggi.json",
            "pesan":       "Pola aktivitas digital Anda <strong>berisiko serius</strong> terhadap kesehatan mental. Jangan tunda untuk mengambil tindakan.",
            "rekom_title": "Rekomendasi Ahli Psikologi",
            "rekom_icon":  "🩺",
            "items": [
                ("Detoks digital segera",
                 "<strong>Jauhkan diri dari semua gadget</strong> minimal beberapa jam sehari secara konsisten."),
                ("Ceritakan kepada orang terdekat",
                 "Berbagi perasaan dengan keluarga atau sahabat kepercayaan dapat meringankan beban mental."),
                ("Konsultasi profesional",
                 "<strong>Segera hubungi psikolog atau konselor kampus</strong> — ini langkah terpenting untuk kondisi Anda."),
            ],
            "fun_fact": "Menghabiskan waktu lebih dari 6 jam sehari di depan layar terbukti meningkatkan risiko kecemasan dan gejala depresi hingga dua kali lipat pada dewasa muda."
        },
    }

    # Default to SEDANG if unexpected value
    cfg = LEVEL.get(res, LEVEL["SEDANG"])

    # ── Section title ─────────────────────────────────────────────
    st.markdown("""
    <div style='text-align:center; margin-bottom:28px;'>
      <h2 style='font-family:"Syne",sans-serif!important; font-size:2rem!important;
         font-weight:900!important; color:#0f172a!important; letter-spacing:-0.03em!important;
         margin:0 0 6px!important;'>
        Hasil Prediksi Stres Anda
      </h2>
      <p style='font-family:"Plus Jakarta Sans",sans-serif; color:#64748b; font-size:.9rem; margin:0;'>
        Analisis berdasarkan 6 indikator aktivitas digital Anda
      </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Inject CSS vars ───────────────────────────────────────────
    st.markdown(f"""
    <style>
    :root {{
      --ca:    {cfg['ca']};
      --cad:   {cfg['ca_dark']};
      --cbg:   {cfg['bg']};
      --cbb:   {cfg['badge_bg']};
      --cbr:   {cfg['border']};
      --cglow: {cfg['glow']};
      --cgls:  {cfg['glow_strong']};
    }}

    /* ── HERO CARD ── */
    .sc-hero-card {{
      position: relative;
      background: var(--cbg);
      border: 1.5px solid var(--cbr);
      border-radius: 22px;
      overflow: hidden;
      padding: 0;
      margin-bottom: 24px;
      box-shadow:
        0 0 0 1px var(--cbr),
        0 8px 40px var(--cglow),
        0 24px 80px var(--cglow);
      animation: glow-pulse 3s ease-in-out infinite;
    }}
    @keyframes glow-pulse {{
      0%,100% {{ box-shadow: 0 0 0 1px var(--cbr), 0 8px 40px var(--cglow), 0 24px 80px var(--cglow); }}
      50%      {{ box-shadow: 0 0 0 1px var(--cbr), 0 12px 56px var(--cgls), 0 32px 100px var(--cglow); }}
    }}

    /* Top accent bar */
    .sc-hero-card::before {{
      content: '';
      position: absolute;
      top: 0; left: 0; right: 0;
      height: 4px;
      background: linear-gradient(90deg, transparent, var(--ca), transparent);
      background-size: 200%;
      animation: shimmer-bar 2.5s linear infinite;
    }}
    @keyframes shimmer-bar {{
      0%   {{ background-position: -100%; }}
      100% {{ background-position: 200%;  }}
    }}

    /* ── Orb decorations ── */
    .sc-hero-card::after {{
      content: '';
      position: absolute;
      top: -80px; right: -80px;
      width: 280px; height: 280px;
      border-radius: 50%;
      background: var(--ca);
      opacity: .06;
      pointer-events: none;
    }}

    /* ── Anim box ── */
    .sc-anim-wrap {{
      border-radius: 16px;
      background: rgba(255,255,255,.6);
      border: 1px solid var(--cbr);
      display: flex; align-items: center; justify-content: center;
      min-height: 220px;
      backdrop-filter: blur(6px);
      padding: 16px;
    }}

    /* ── Result text ── */
    .sc-result-block {{
      padding: 32px 28px;
      display: flex; flex-direction: column;
      justify-content: center;
    }}
    .sc-badge {{
      display: inline-flex; align-items: center; gap: 7px;
      padding: 5px 14px;
      border-radius: 999px;
      background: var(--cbb);
      border: 1px solid var(--cbr);
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: .75rem; font-weight: 700;
      letter-spacing: .04em; text-transform: uppercase;
      color: var(--cad);
      margin-bottom: 14px;
      width: fit-content;
    }}
    .sc-badge-dot {{
      width: 7px; height: 7px;
      border-radius: 50%;
      background: var(--ca);
      animation: pdot 1.8s ease-in-out infinite;
    }}
    @keyframes pdot {{
      0%,100% {{ transform:scale(1);opacity:1; }}
      50%      {{ transform:scale(1.6);opacity:.5; }}
    }}
    .sc-result-label {{
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: .7rem; font-weight: 700;
      letter-spacing: .14em; text-transform: uppercase;
      color: var(--ca);
      margin-bottom: 8px;
    }}
    .sc-result-level {{
      font-family: 'Syne', sans-serif;
      font-size: clamp(3.2rem, 8vw, 5rem);
      font-weight: 900;
      color: var(--ca);
      line-height: 1;
      letter-spacing: -.05em;
      margin-bottom: 16px;
      animation: pop-in .6s cubic-bezier(.34,1.56,.64,1) both;
    }}
    @keyframes pop-in {{
      from {{ transform:scale(.7);opacity:0; }}
      to   {{ transform:scale(1);opacity:1; }}
    }}
    .sc-result-pesan {{
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: .97rem; line-height: 1.7;
      color: #475569;
      max-width: 400px;
    }}
    .sc-result-pesan strong {{ color: var(--cad); }}

    /* ── REKOM CARD ── */
    .sc-rekom {{
      background: #ffffff;
      border: 1.5px solid #e2e8f0;
      border-radius: 20px;
      overflow: hidden;
      margin-bottom: 24px;
      box-shadow: 0 4px 24px rgba(15,23,42,.06);
    }}
    .sc-rekom-head {{
      padding: 18px 24px;
      background: var(--cbg);
      border-bottom: 1.5px solid var(--cbr);
      display: flex; align-items: center; gap: 12px;
    }}
    .sc-rekom-icon {{
      width: 40px; height: 40px;
      border-radius: 11px;
      background: var(--ca);
      display: flex; align-items: center;
      justify-content: center;
      font-size: 1.15rem; flex-shrink: 0;
    }}
    .sc-rekom-title {{
      font-family: 'Syne', sans-serif;
      font-size: 1.05rem; font-weight: 800;
      color: #0f172a;
      letter-spacing: -.02em;
    }}
    .sc-rekom-body {{ padding: 20px 24px; }}
    .sc-ritem {{
      display: flex; align-items: flex-start; gap: 14px;
      padding: 14px 16px;
      border-radius: 12px;
      background: var(--cbg);
      border: 1px solid var(--cbr);
      margin-bottom: 10px;
      animation: slide-up .45s ease both;
    }}
    .sc-ritem:nth-child(1){{animation-delay:.10s}}
    .sc-ritem:nth-child(2){{animation-delay:.20s}}
    .sc-ritem:nth-child(3){{animation-delay:.30s}}
    .sc-ritem:nth-child(4){{animation-delay:.40s}}
    @keyframes slide-up {{
      from{{transform:translateY(14px);opacity:0;}}
      to  {{transform:translateY(0);  opacity:1;}}
    }}
    .sc-rbullet {{
      width: 30px; height: 30px;
      border-radius: 8px;
      background: var(--ca);
      color: #fff;
      font-family: 'Syne', sans-serif;
      font-size: .72rem; font-weight: 900;
      display: flex; align-items: center; justify-content: center;
      flex-shrink: 0; margin-top: 2px;
    }}
    .sc-rtext {{
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: .9rem; color: #334155; line-height: 1.65;
    }}
    .sc-rtext strong {{ color: #0f172a; }}
    </style>
    """, unsafe_allow_html=True)

    # ── Hero Card — SaaS Style (Satu Kotak Besar) ─────────────────
    
    # 1. Bikin container utama yang mencakup lottie dan teks hasil
    result_card = st.container(border=True)
    
    with result_card:
        # Inject CSS khusus untuk container ini biar warnanya ngikutin level stres
        st.markdown(f"""
        <style>
        [data-testid="stVerticalBlock"]:has(.result-card-marker) {{
            background: var(--cbg);
            border: 1.5px solid var(--cbr) !important;
            border-radius: 22px !important;
            box-shadow: 0 8px 40px var(--cglow) !important;
            padding: 30px !important;
            margin-bottom: 24px !important;
            position: relative;
            overflow: hidden;
            animation: glow-pulse 3s ease-in-out infinite;
        }}
        
        /* Shimmer bar di atas card sesuai warna level */
        [data-testid="stVerticalBlock"]:has(.result-card-marker)::before {{
            content: '';
            position: absolute;
            top: -1px; left: 0; right: 0;
            height: 4px;
            background: linear-gradient(90deg, transparent, var(--ca), transparent);
            background-size: 200%;
            animation: shimmer-bar 2.5s linear infinite;
            z-index: 1;
            border-radius: 22px 22px 0 0;
        }}
        </style>
        <div class="result-card-marker"></div>
        """, unsafe_allow_html=True)
        
        col_anim, col_txt = st.columns([1, 1.6], gap="large")

        with col_anim:
            # Lottie sekarang tanpa kotak aneh, dibikin nyatu sama background card
            st.markdown("<div style='height: 100%; display: flex; align-items: center; justify-content: center;'>", unsafe_allow_html=True)
            try:
                st_lottie(load_lottie(cfg["anim"]), height=220, key=f"anim_{res}_v2")
            except Exception:
                st.markdown(f"<div style='font-size:5rem;text-align:center;'>{cfg['icon']}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_txt:
            # Teks hasil prediksi
            st.markdown(f"""
            <div style='display: flex; flex-direction: column; justify-content: center; height: 100%; padding-left: 10px;'>
                <div class='sc-badge'>
                  <span class='sc-badge-dot'></span>
                  {cfg['icon']} {cfg['badge']}
                </div>
                <p class='sc-result-label'>Tingkat Stres Terdeteksi</p>
                <div class='sc-result-level'>{res}</div>
                <p class='sc-result-pesan'>{cfg['pesan']}</p>
            </div>
            """, unsafe_allow_html=True)


   # ── Rekomendasi card ──────────────────────────────────────────
    # Bikin HTML-nya nyambung tanpa spasi indentasi biar gak dibaca sebagai code block
    items_html = "".join(
        f"<div class='sc-ritem'><div class='sc-rbullet'>0{i}</div><p class='sc-rtext'><strong>{title}.</strong> {body}</p></div>"
        for i, (title, body) in enumerate(cfg["items"], 1)
    )

    # Render card-nya (pastikan gak ada indentasi berlebih di dalam div body)
    st.markdown(f"""
<div class='sc-rekom'>
    <div class='sc-rekom-head'>
        <div class='sc-rekom-icon'>{cfg['rekom_icon']}</div>
        <p class='sc-rekom-title'>{cfg['rekom_title']}</p>
    </div>
    <div class='sc-rekom-body'>
{items_html}
    </div>
</div>
    """, unsafe_allow_html=True)


    # ── Fun Fact Banner (Penutup Manis) ───────────────────────────
    st.markdown(f"""
<div style="background: #ffffff; border: 1.5px solid {cfg['border']}; border-radius: 16px; padding: 20px 24px; margin-bottom: 24px; display: flex; align-items: flex-start; gap: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.03);">
<div style="width: 80px; height: 80px; border-radius: 12px; background: {cfg['badge_bg']}; display: flex; align-items: center; justify-content: center; font-size: 2.5rem; flex-shrink: 0;">
🕵️‍♂️
</div>
<div>
<p style="font-family: 'Syne', sans-serif; font-size: 1rem; font-weight: 800; color: {cfg['ca_dark']}; margin: 0 0 6px; letter-spacing: -0.01em;">
Tahukah Anda?
</p>
<p style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.92rem; color: #475569; margin: 0; line-height: 1.6;">
{cfg['fun_fact']}
</p>
</div>
</div>
    """, unsafe_allow_html=True)

    # ── Disclaimer ────────────────────────────────────────────────
    st.markdown(f"""
    <div style='background:{cfg["bg"]};border:1px solid {cfg["border"]};
         border-radius:12px;padding:14px 18px;margin-bottom:24px;
         display:flex;align-items:center;gap:10px;'>
      <span style='font-size:1.1rem;'>ℹ️</span>
      <p style='font-family:"Plus Jakarta Sans",sans-serif;font-size:.82rem;
         color:#475569;margin:0;line-height:1.6;'>
        Hasil ini bersifat indikatif. Untuk evaluasi mendalam, konsultasikan kondisi
        Anda kepada psikolog atau konselor akademik kampus.
      </p>
    </div>
    """, unsafe_allow_html=True)

    

 # ── Navigation buttons ────────────────────────────────────────
    col_retry, _, col_quit = st.columns([1, 1, 1])

    with col_retry:
        if st.button("🔄  Prediksi Ulang", use_container_width=True, key="btn_retry_hasil"):
            goto("FormInput")
            st.rerun()

    with col_quit:
        if st.button("🚪  Selesai", use_container_width=True, key="btn_quit_hasil"):
            goto("Akhir") # Arahkan ke halaman baru
            st.rerun()


# ══════════════════════════════════════════════════════════════════
# 🎉  PAGE 4 — HALAMAN AKHIR (REDESIGN EYE-CATCHING)
# ══════════════════════════════════════════════════════════════════
elif st.session_state.page == "Akhir":
    scroll_top()
    render_navbar()

    # ── CSS halaman akhir ──────────────────────────────────────────
    st.markdown("""
    <style>
    /* Confetti canvas — fixed overlay */
    #sc-confetti {
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        pointer-events: none;
        z-index: 9999;
    }

    /* ── Wrapper ── */
    .akhir-wrap {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 0px 16px 60px;
        gap: 0;
        margin-top: -25px;
    }

    /* ── Konfeti emoji row ── */
    .akhir-emoji-row {
        display: flex;
        justify-content: center;
        gap: 12px;
        font-size: 1.5rem;
        margin-bottom: 24px;
        animation: sc-drop .7s ease both;
    }
    @keyframes sc-drop {
        from { transform: translateY(-18px); opacity: 0; }
        to   { transform: translateY(0);    opacity: 1; }
    }

    /* ── Main card ── */
    .akhir-card {
        background: #ffffff;
        border: 1.5px solid #e2e8f0;
        border-radius: 24px;
        padding: 44px 36px 36px;
        max-width: 560px;
        width: 100%;
        text-align: center;
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 40px rgba(13,148,136,.10), 0 2px 12px rgba(15,23,42,.05);
    }

    /* Shimmer accent bar at top */
    .akhir-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 4px;
        background: linear-gradient(90deg, transparent, #0d9488, #2dd4bf, transparent);
        background-size: 200%;
        animation: sc-shimmer 2.8s linear infinite;
    }
    @keyframes sc-shimmer {
        0%   { background-position: -100%; }
        100% { background-position:  200%; }
    }

    /* Soft orb decoration */
    .akhir-card::after {
        content: '';
        position: absolute;
        bottom: -60px; right: -60px;
        width: 180px; height: 180px;
        border-radius: 50%;
        background: #0d9488;
        opacity: .04;
        pointer-events: none;
    }

    /* ── Trophy icon ── */
    .akhir-icon-wrap {
        width: 72px; height: 72px;
        border-radius: 50%;
        background: #f0fdfa;
        border: 1.5px solid #99f6e4;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 20px;
        font-size: 2rem;
        animation: sc-pop .6s cubic-bezier(.34,1.56,.64,1) .2s both;
    }
    @keyframes sc-pop {
        from { transform: scale(.6); opacity: 0; }
        to   { transform: scale(1);  opacity: 1; }
    }

    /* ── Badge ── */
    .akhir-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 13px;
        border-radius: 999px;
        background: #d1fae5;
        border: 1px solid #a7f3d0;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: .75rem;
        font-weight: 700;
        color: #065f46;
        letter-spacing: .04em;
        text-transform: uppercase;
        margin-bottom: 18px;
        animation: sc-fadein .5s ease .3s both;
    }
    .akhir-badge-dot {
        width: 7px; height: 7px;
        border-radius: 50%;
        background: #059669;
        animation: sc-bdot 1.8s ease-in-out infinite;
    }
    @keyframes sc-bdot {
        0%,100% { transform: scale(1);   opacity: 1; }
        50%      { transform: scale(1.6); opacity: .5; }
    }

    /* ── Title ── */
    .akhir-title {
        font-family: 'Syne', sans-serif !important;
        font-size: 1.9rem !important;
        font-weight: 900 !important;
        color: #0f172a !important;
        letter-spacing: -.035em !important;
        margin: 0 0 14px !important;
        animation: sc-fadein .5s ease .35s both;
    }

    /* ── Body text ── */
    .akhir-body {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: .97rem;
        color: #475569;
        line-height: 1.75;
        margin: 0 0 28px;
        animation: sc-fadein .5s ease .4s both;
    }
    .akhir-body strong { color: #0f766e; }

    @keyframes sc-fadein {
        from { opacity: 0; transform: translateY(10px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    /* ── Stats row ── */
    .akhir-stats {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 12px;
        margin-bottom: 28px;
        animation: sc-fadein .5s ease .45s both;
    }
    .akhir-stat {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 16px 10px;
    }
    .akhir-stat-val {
        font-family: 'Syne', sans-serif;
        font-size: 1.5rem;
        font-weight: 900;
        color: #0d9488;
        margin-bottom: 3px;
    }
    .akhir-stat-lbl {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: .71rem;
        font-weight: 600;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: .06em;
    }

    /* ── Divider ── */
    .akhir-divider {
        width: 100%;
        height: 1px;
        background: #f1f5f9;
        margin: 0 0 24px;
    }

    /* ── Tips list ── */
    .akhir-tips {
        text-align: left;
        margin-bottom: 28px;
        animation: sc-fadein .5s ease .5s both;
    }
    .akhir-tips-title {
        font-family: 'Syne', sans-serif;
        font-size: .82rem;
        font-weight: 800;
        color: #64748b;
        letter-spacing: .05em;
        text-transform: uppercase;
        display: flex;
        align-items: center;
        gap: 7px;
        margin-bottom: 14px;
    }
    .akhir-tip-item {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        padding: 12px 14px;
        border-radius: 12px;
        background: #f8fafc;
        border: 1px solid #f1f5f9;
        margin-bottom: 8px;
    }
    .akhir-tip-num {
        width: 22px; height: 22px;
        border-radius: 50%;
        background: #f0fdfa;
        border: 1px solid #99f6e4;
        font-family: 'Syne', sans-serif;
        font-size: .7rem;
        font-weight: 900;
        color: #0d9488;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        margin-top: 1px;
    }
    .akhir-tip-text {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: .88rem;
        color: #334155;
        line-height: 1.6;
        margin: 0;
    }

    /* ── Action buttons ── */
    .akhir-share-row {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 10px;
        margin-top: 12px;
        animation: sc-fadein .5s ease .6s both;
    }
    .akhir-share-btn {
        padding: 10px;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        background: #f8fafc;
        color: #64748b;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: .84rem;
        font-weight: 600;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 7px;
        transition: all .18s;
    }
    .akhir-share-btn:hover {
        background: #f0fdfa;
        border-color: #99f6e4;
        color: #0d9488;
    }

    /* ── Footer note ── */
    .akhir-footer-note {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: .75rem;
        color: #cbd5e1;
        margin-top: 28px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── Confetti canvas + JS trigger ──────────────────────────────
    components.html("""
    <canvas id="sc-confetti" style="position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:9999;"></canvas>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.2/dist/confetti.browser.min.js"></script>
    <script>
    (function() {
        var canvas = window.parent.document.getElementById('sc-confetti');
        if (!canvas) {
            canvas = window.parent.document.createElement('canvas');
            canvas.id = 'sc-confetti';
            canvas.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:9999;';
            window.parent.document.body.appendChild(canvas);
        }
        var myConfetti = confetti.create(canvas, { resize: true, useWorker: false });
        var colors = ['#0d9488','#2dd4bf','#fbbf24','#60a5fa','#f472b6','#a78bfa'];
        setTimeout(function() {
            myConfetti({ particleCount: 90, spread: 70, origin: { y: .55 }, colors: colors, gravity: 1.1 });
        }, 350);
        setTimeout(function() {
            myConfetti({ particleCount: 45, spread: 55, origin: { y: .6, x: .2 }, colors: colors, gravity: 1.2 });
        }, 700);
        setTimeout(function() {
            myConfetti({ particleCount: 45, spread: 55, origin: { y: .6, x: .8 }, colors: colors, gravity: 1.2 });
        }, 950);
    })();
    </script>
    """, height=0)

# ── Page content ──────────────────────────────────────────────
    
    # 1. CSS HACK BUAT NARIK STREAMLIT COLUMNS KE ATAS
    st.markdown("""
    <style>
    /* Targetkan kolom bawaan Streamlit di halaman ini dan tarik ke atas */
    div[data-testid="stHorizontalBlock"] {
        margin-top: -60px !important; /* Tarik lottie naik, gedein minusnya kalo kurang */
        margin-bottom: -15px !important; /* Rapatkan lottie dengan card di bawahnya */
    }
    </style>
    """, unsafe_allow_html=True)

    # 2. Buka Wrap Utama (Container background paling luar)
    # Kita buka div-nya di sini
    st.markdown('<div class="akhir-wrap" style="padding-top: 0;">', unsafe_allow_html=True)
    
    # 2. Render Lottie menggunakan st.columns (Gaya Claude agar PASTI rata tengah)
    # Posisinya di luar card, menggantikan deretan emoji: 🎉 ✨ 🏆 ✨ 🎉
    # Rasio [1, 1.5, 1] ini bikin kolom tengahnya pas banget buat Lottie
    _, col_lottie, _ = st.columns([1, 1.5, 1])
    with col_lottie:
        try:
            # Menggunakan load_lottiefile (sesuai definisi lu)
            st_lottie(load_lottie("achievement.json"), height=160, key="achievement_akhir")
        except Exception:
            # Fallback kalau lottie gagal load
            st.markdown('<div style="text-align:center; font-size:2rem; margin:16px 0;">🎉 ✨ 🏆 ✨ 🎉</div>', unsafe_allow_html=True)

    # 3. Render Card utuh dalam 1 blok (Gaya Gemini agar Card TIDAK pecah/kebongkar)
    st.markdown("""
<div class="akhir-card" style="margin: 0 auto; max-width: 600px; width: 100%;">
<div class="akhir-icon-wrap">🏆</div>
<div class="akhir-badge">
<span class="akhir-badge-dot"></span>
Asesmen Selesai
</div>
<h2 class="akhir-title">Terima Kasih!</h2>
<p class="akhir-body">
Anda telah menyelesaikan asesmen deteksi dini tingkat stres digital.
Kami berharap rekomendasi yang diberikan dapat membantu Anda menjaga
keseimbangan antara aktivitas digital dan kesehatan mental.<br><br>
<strong>Tetap sehat dan bijak berteknologi! 💚</strong>
</p>
<div class="akhir-stats">
<div class="akhir-stat">
<div class="akhir-stat-val">6</div>
<div class="akhir-stat-lbl">Indikator<br>dianalisis</div>
</div>
<div class="akhir-stat">
<div class="akhir-stat-val">&lt;5s</div>
<div class="akhir-stat-lbl">Waktu<br>proses</div>
</div>
<div class="akhir-stat">
<div class="akhir-stat-val">1</div>
<div class="akhir-stat-lbl">Laporan<br>personal</div>
</div>
</div>
<div class="akhir-divider"></div>
<div class="akhir-tips">
<div class="akhir-tips-title">💡 Langkah selanjutnya</div>
<div class="akhir-tip-item">
<div class="akhir-tip-num">1</div>
<p class="akhir-tip-text">
Tinjau kembali rekomendasi yang diberikan dan pilih
<strong>satu hal untuk dicoba hari ini.</strong>
</p>
</div>
<div class="akhir-tip-item">
<div class="akhir-tip-num">2</div>
<p class="akhir-tip-text">
Ulangi asesmen ini dalam <strong>2 minggu</strong> untuk
memantau perkembangan kondisi Anda.
</p>
</div>
<div class="akhir-tip-item">
<div class="akhir-tip-num">3</div>
<p class="akhir-tip-text">
Jika kondisi tidak membaik, jangan tunda untuk berkonsultasi
dengan <strong>psikolog atau konselor kampus.</strong>
</p>
</div>
</div>
</div><p class="akhir-footer-note" style="text-align: center; margin-top: 24px;">
Hanya untuk keperluan edukasi dan penelitian. Bukan pengganti diagnosis profesional.
</p>
</div>""", unsafe_allow_html=True)