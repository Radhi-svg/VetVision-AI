import streamlit as st
import streamlit as st
from tensorflow import keras
from PIL import Image, ImageOps
import numpy as np
from PIL import Image, ImageOps
import numpy as np
import os
from datetime import datetime

# 1. Tetapan Asas Halaman
st.set_page_config(
    page_title="VetVision AI — Kesihatan Haiwan",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Inisialisasi State (Navigasi, Tema, & Sejarah Imbasan)
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "Light ☀️"
if "scan_history" not in st.session_state:
    st.session_state.scan_history = []

# 3. Kamus Bahasa (Lengkap)
LANGUAGES = {
    "Bahasa Melayu 🇲🇾": {
        "nav_home": "🏠 Utama",
        "nav_services": "🩺 Perkhidmatan",
        "nav_about": "ℹ️ Tentang Kami",
        "nav_contact": "📞 Hubungi",
        "badge": "Healthy Naturally ♡",
        "hero_title": "Rawatan Semula Jadi untuk Hidup yang Lebih Sihat",
        "hero_sub": "Kami percaya setiap haiwan berhak mendapat penjagaan terbaik, secara semula jadi dan penuh kasih sayang.",
        "upload_title": "📸 Muat Naik Imej Diagnostik AI",
        "upload_desc": "Pilih imej bahagian kulit, mata, atau telinga haiwan anda untuk imbasan pantas.",
        "btn_upload_label": "Muat Naik Imej Haiwan",
        "preview_title": "👁️ Pratinjau Imej",
        "btn_analyze": "✨ Mula Analisis AI Sekarang",
        "analyzing": "🌿 Enjin AI sedang mengimbas imej haiwan anda...",
        "result_title": "🩺 KEPUTUSAN DIAGNOSTIK AI",
        "confidence": "Tahap Keyakinan AI",
        "disclaimer": "⚠️ Nota Mesra Veterinar: Keputusan ini diproses oleh kecerdasan buatan (AI) untuk pengesanan awal sahaja. Sila rujuk Doktor Veterinar untuk pengesahan & rawatan lanjut.",
        "history_title": "📋 Sejarah Imbasan Sesi Ini",
        "history_empty": "Tiada sejarah imbasan lagi dalam sesi ini.",
        "download_report_btn": "📥 Muat Turun Laporan Kesihatan (.txt)",
        "f1_icon": "🍃",
        "f1_title": "Diet & Pemakanan Semula Jadi",
        "f1_desc": "Pemakanan seimbang & organik",
        "f2_icon": "🏡",
        "f2_title": "Rawatan Selesa Seperti di Rumah",
        "f2_desc": "Penjagaan mesra & penuh kasih",
        "f3_icon": "🐾",
        "f3_title": "Perkhidmatan AI Premium",
        "f3_desc": "Pengesanan pantas kesihatan haiwan",
        "sec_services_title": "🩺 Perkhidmatan Utama VetVision AI",
        "services_subtitle": "Sistem pengesanan awal & penjagaan haiwan secara holistik:",
        "s1_title": "🧬 Imbasan AI Kulit & Mata",
        "s1_desc": "Menganalisis gambar bahagian berisiko untuk mengesan jangkitan kulat, ruam, atau katarak peringkat awal.",
        "s2_title": "🍃 Konsultasi Diet Organik",
        "s2_desc": "Pelan pemakanan berasaskan bahan semula jadi untuk meningkatkan imuniti dan kesihatan bulu haiwan.",
        "s3_title": "🏡 Penjagaan Terapi Selesa",
        "s3_desc": "Panduan penjagaan haiwan di rumah tanpa tekanan dengan teknik keselesaan organik.",
        "btn_test_scan": "🚀 Uji Imbasan Sekarang",
        "faq_title": "❓ Soalan Lazim (FAQ)",
        "faq_q1": "Apakah persediaan sebelum mengambil gambar haiwan?",
        "faq_a1": "Pastikan pencahayaan cukup terang, fokus pada bahagian kulit/mata yang terjejas, dan elakkan gambar yang kabur.",
        "faq_q2": "Adakah keputusan AI ini menggantikan nasihat Doktor Veterinar?",
        "faq_a2": "Tidak. VetVision AI berfungsi sebagai alatan pengesanan awal sahaja. Sentiasa dapatkan pengesahan fizikal daripada doktor veterinar bertauliah.",
        "sec_about_title": "ℹ️ Mengenai Platform VetVision AI",
        "about_p1": "<b>VetVision AI</b> diasaskan dengan visi untuk membawa teknologi Kecerdasan Buatan (AI) terdepan ke dalam dunia kesihatan haiwan kesayangan. Kami menggabungkan enjin pemprosesan imej visual bermutu tinggi dengan pendekatan perubatan semula jadi yang lembut dan mesra alam.",
        "metric_1_label": "⚡ Masa Imbasan AI",
        "metric_1_val": "< 3 Saat",
        "metric_2_label": "🎯 Ketepatan Model",
        "metric_2_val": "High Precision",
        "metric_3_label": "🌱 Pendekatan",
        "metric_3_val": "100% Holistik",
        "about_misi_title": "🎯 Misi Kami",
        "about_misi_desc": "Memastikan setiap pemilik haiwan mendapat akses pengesanan kesihatan awal yang pantas, mesra dan tepat.",
        "sec_contact_title": "📞 Hubungi Pasukan Veterinar Kami",
        "contact_subtitle": "Sila hubungi pasukan sokongan veterinar kami untuk sebarang pertanyaan:",
        "contact_address_label": "📍 Alamat",
        "contact_address_val": "VetVision Wellness Centre, Jalan Kesihatan Haiwan, Malaysia",
        "contact_phone_label": "📞 Talian Bantuan",
        "contact_email_label": "✉️ E-mel",
        "input_name": "Nama Anda",
        "input_email": "E-mel Anda",
        "input_msg": "Mesej Anda",
        "btn_send_msg": "Hantar Mesej"
    },
    "English 🇬🇧": {
        "nav_home": "🏠 Home",
        "nav_services": "🩺 Services",
        "nav_about": "ℹ️ About Us",
        "nav_contact": "📞 Contact",
        "badge": "Healthy Naturally ♡",
        "hero_title": "Natural Care for a Healthier & Happier Life",
        "hero_sub": "We believe every pet deserves the very best care, naturally and with unconditional love.",
        "upload_title": "📸 Upload Image for AI Diagnosis",
        "upload_desc": "Select a clear photo of your pet's skin, eyes, or ears for instant screening.",
        "btn_upload_label": "Upload Pet Image",
        "preview_title": "👁️ Image Preview",
        "btn_analyze": "✨ Start AI Analysis Now",
        "analyzing": "🌿 AI engine is scanning your pet's image...",
        "result_title": "🩺 AI DIAGNOSTIC RESULT",
        "confidence": "AI Confidence Level",
        "disclaimer": "⚠️ Veterinary Disclaimer: This screening is generated by AI for early detection. Please consult a licensed veterinarian for medical treatment.",
        "history_title": "📋 Session Scan History",
        "history_empty": "No scan history recorded in this session yet.",
        "download_report_btn": "📥 Download Health Report (.txt)",
        "f1_icon": "🍃",
        "f1_title": "Natural Diet & Nutrition",
        "f1_desc": "Balanced & organic meals",
        "f2_icon": "🏡",
        "f2_title": "Cozy Home-Like Care",
        "f2_desc": "Warm & stress-free environment",
        "f3_icon": "🐾",
        "f3_title": "Premium AI Services",
        "f3_desc": "Instant early health screening",
        "sec_services_title": "🩺 Core VetVision AI Services",
        "services_subtitle": "Early detection system & holistic pet wellness care:",
        "s1_title": "🧬 Skin & Eye AI Scanning",
        "s1_desc": "Analyzes photo regions to detect fungal infections, rashes, or early-stage cataracts.",
        "s2_title": "🍃 Organic Diet Consultation",
        "s2_desc": "Natural food plans to boost immunity and enhance coat health.",
        "s3_title": "🏡 Cozy Home Therapy Care",
        "s3_desc": "Stress-free home pet care guidance with organic comfort techniques.",
        "btn_test_scan": "🚀 Test Scan Now",
        "faq_title": "❓ Frequently Asked Questions (FAQ)",
        "faq_q1": "What preparation is needed before taking a pet's photo?",
        "faq_a1": "Ensure adequate lighting, focus closely on the affected skin/eye area, and avoid blurriness.",
        "faq_q2": "Does this AI result replace a Veterinarian's advice?",
        "faq_a2": "No. VetVision AI serves as an early detection tool only. Always consult a certified veterinarian for official diagnosis and treatment.",
        "sec_about_title": "ℹ️ About VetVision AI Platform",
        "about_p1": "<b>VetVision AI</b> was founded with a vision to bring cutting-edge Artificial Intelligence (AI) into pet care. We combine high-precision visual processing engines with gentle, eco-friendly natural wellness approaches.",
        "metric_1_label": "⚡ AI Scan Speed",
        "metric_1_val": "< 3 Secs",
        "metric_2_label": "🎯 Model Accuracy",
        "metric_2_val": "High Precision",
        "metric_3_label": "🌱 Approach",
        "metric_3_val": "100% Holistic",
        "about_misi_title": "🎯 Our Mission",
        "about_misi_desc": "Ensuring every pet owner gets fast, friendly, and accurate early health screening access.",
        "sec_contact_title": "📞 Contact Our Veterinary Team",
        "contact_subtitle": "Please get in touch with our veterinary support team for any inquiries:",
        "contact_address_label": "📍 Address",
        "contact_address_val": "VetVision Wellness Centre, Pet Health Avenue, Malaysia",
        "contact_phone_label": "📞 Helpline",
        "contact_email_label": "✉️ Email",
        "input_name": "Your Name",
        "input_email": "Your Email",
        "input_msg": "Your Message",
        "btn_send_msg": "Send Message"
    }
}

# 4. Tentukan Palet Warna Berdasarkan Tema Pilihan Pengguna
is_dark = "Dark" in st.session_state.theme_mode

bg_main = "#111827" if is_dark else "#F8F9FA"
card_bg = "#1F2937" if is_dark else "#FFFFFF"
text_primary = "#F9FAFB" if is_dark else "#111827"
text_secondary = "#E5E7EB" if is_dark else "#374151"
brand_green = "#52B788" if is_dark else "#2D6A4F"
brand_accent = "#1E3A2B" if is_dark else "#E8F5E9"
card_border = "#374151" if is_dark else "#D1D5DB"

# 5. CSS Dinamik
st.markdown(f"""
    <style>
    header[data-testid="stHeader"] {{ background-color: transparent !important; }}

    div[data-baseweb="select"] {{ background-color: transparent !important; }}
    div[data-baseweb="select"] > div {{
        background-color: {card_bg} !important;
        border: 1.5px solid {card_border} !important;
        border-radius: 14px !important;
        color: {text_primary} !important;
    }}
    div[data-baseweb="select"] * {{
        color: {text_primary} !important;
        background-color: transparent !important;
        font-weight: 700 !important;
    }}

    [data-testid="stFileUploader"] {{
        background-color: {card_bg} !important;
        border-radius: 20px !important;
        padding: 20px !important;
        border: 1.5px solid {card_border} !important;
    }}
    [data-testid="stFileUploaderDropzone"] {{
        background-color: {card_bg} !important;
        border: 2px dashed {brand_green} !important;
        border-radius: 14px !important;
    }}
    [data-testid="stFileUploaderDropzone"] button {{
        background-color: {brand_green} !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 8px 18px !important;
        font-weight: 700 !important;
    }}
    [data-testid="stFileUploaderDropzone"] button * {{ color: #FFFFFF !important; }}

    .stApp {{
        background-color: {bg_main} !important;
        color: {text_primary} !important;
    }}
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6, 
    .stApp p, .stApp label, .stApp span, .stMarkdown {{
        color: {text_primary} !important;
    }}
    .block-container {{
        padding-top: 1.8rem !important;
        padding-bottom: 2.5rem !important;
        max-width: 1150px !important;
    }}

    .brand-title {{
        font-size: 23px;
        font-weight: 800;
        color: {text_primary} !important;
        margin: 0;
        white-space: nowrap;
    }}
    .brand-sub {{
        font-size: 11px;
        color: {brand_green} !important;
        font-weight: 700;
        display: block;
        margin-top: -2px;
        white-space: nowrap;
    }}

    div[data-testid="stHorizontalBlock"] button {{
        border-radius: 25px !important;
        background-color: {card_bg} !important;
        color: {text_primary} !important;
        border: 1.5px solid {card_border} !important;
        font-weight: 700 !important;
        font-size: 13px !important;
        padding: 6px 12px !important;
        white-space: nowrap !important;
        box-shadow: 0 3px 8px rgba(0,0,0,0.04) !important;
        transition: all 0.25s ease-in-out !important;
    }}
    div[data-testid="stHorizontalBlock"] button:hover,
    div[data-testid="stHorizontalBlock"] button:focus,
    div[data-testid="stHorizontalBlock"] button:active {{
        background-color: {brand_green} !important;
        color: #FFFFFF !important;
        border-color: {brand_green} !important;
    }}
    div[data-testid="stHorizontalBlock"] button:hover p,
    div[data-testid="stHorizontalBlock"] button:focus p,
    div[data-testid="stHorizontalBlock"] button:active p {{
        color: #FFFFFF !important;
    }}

    .hero-banner {{
        background: {card_bg} !important;
        border-radius: 26px;
        padding: 35px 40px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.05);
        border: 1px solid {card_border} !important;
        position: relative;
        margin-bottom: 25px;
    }}
    .hero-badge {{
        position: absolute;
        top: 30px;
        right: 40px;
        font-family: 'Georgia', serif;
        font-style: italic;
        color: {brand_green} !important;
        font-size: 17px;
        font-weight: bold;
    }}
    .hero-h1 {{
        font-size: 2.2rem;
        font-weight: 800;
        line-height: 1.25;
        color: {text_primary} !important;
        max-width: 72%;
        margin-bottom: 10px;
    }}
    .hero-p {{
        font-size: 1.05rem;
        color: {text_secondary} !important;
        max-width: 70%;
        margin-bottom: 0;
    }}

    .feature-bar {{
        background-color: {brand_accent} !important;
        border-radius: 22px;
        padding: 20px 30px;
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 15px;
        margin-top: 30px;
        border: 1px solid {card_border} !important;
    }}
    .feature-card {{
        display: flex;
        align-items: center;
        gap: 12px;
    }}
    .feature-icon-box {{
        font-size: 24px;
        background: {card_bg} !important;
        width: 44px;
        height: 44px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
    }}
    .feature-text h4 {{
        margin: 0;
        font-size: 14px;
        font-weight: 700;
        color: {text_primary} !important;
    }}
    .feature-text p {{
        margin: 1px 0 0 0;
        font-size: 11px;
        color: {text_secondary} !important;
    }}

    .water-container {{
        width: 100%;
        height: 32px;
        background-color: {brand_accent} !important;
        border-radius: 20px;
        padding: 3px;
        border: 2px solid {brand_green} !important;
        box-shadow: inset 0 2px 6px rgba(0,0,0,0.15);
        position: relative;
        overflow: hidden;
        margin: 12px 0;
    }}
    .water-bar {{
        height: 100%;
        background: linear-gradient(90deg, #1d4ed8 0%, #3b82f6 30%, #06b6d4 70%, #1d4ed8 100%);
        background-size: 200% 100%;
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        padding-right: 12px;
        animation: fillWater 1.6s cubic-bezier(0.22, 1, 0.36, 1) forwards, liquidWave 2.5s linear infinite;
    }}
    @keyframes fillWater {{ from {{ width: 0%; }} }}
    @keyframes liquidWave {{ 0% {{ background-position: 0% 50%; }} 50% {{ background-position: 100% 50%; }} 100% {{ background-position: 0% 50%; }} }}
    .water-text {{ color: #FFFFFF !important; font-weight: 800; font-size: 13px; }}

    .btn-main button {{
        background: linear-gradient(135deg, {brand_green} 0%, #1B4332 100%) !important;
        color: #FFFFFF !important;
        border-radius: 50px !important;
        padding: 14px 30px !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        border: none !important;
    }}
    </style>
""", unsafe_allow_html=True)

# 6. Bar Navigasi Atas & Widget Utiliti (Bahasa & Tema)
c_brand, c_nav1, c_nav2, c_nav3, c_nav4, c_lang, c_theme = st.columns([2.0, 1.2, 1.4, 1.3, 1.2, 1.8, 1.5])

with c_brand:
    st.markdown("""
        <div>
            <p class="brand-title">🐾 VetVision AI</p>
            <span class="brand-sub">Natural Care, Lasting Health</span>
        </div>
    """, unsafe_allow_html=True)

with c_lang:
    selected_lang = st.selectbox("", list(LANGUAGES.keys()), key="lang_select", label_visibility="collapsed")
    t = LANGUAGES.get(selected_lang, LANGUAGES["Bahasa Melayu 🇲🇾"])

with c_theme:
    theme_options = ["Light ☀️", "Dark 🌙"]
    st.selectbox("", theme_options, key="theme_mode", label_visibility="collapsed")

with c_nav1:
    if st.button(t['nav_home'], key="nav_home_btn", use_container_width=True):
        st.session_state.current_page = "home"
        st.rerun()

with c_nav2:
    if st.button(t['nav_services'], key="nav_serv_btn", use_container_width=True):
        st.session_state.current_page = "services"
        st.rerun()

with c_nav3:
    if st.button(t['nav_about'], key="nav_ab_btn", use_container_width=True):
        st.session_state.current_page = "about"
        st.rerun()

with c_nav4:
    if st.button(t['nav_contact'], key="nav_con_btn", use_container_width=True):
        st.session_state.current_page = "contact"
        st.rerun()

st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)

# 7. Halaman Utama (Home)
if st.session_state.current_page == "home":
    
    st.markdown(f"""
    <div class="hero-banner">
        <div class="hero-badge">{t['badge']}</div>
        <div class="hero-h1">{t['hero_title']}</div>
        <div class="hero-p">{t['hero_sub']}</div>
    </div>
    """, unsafe_allow_html=True)

    MODEL_PATH = "keras_model.h5"
    LABELS_PATH = "labels.txt"

    if not os.path.exists(MODEL_PATH) or not os.path.exists(LABELS_PATH):
        st.error(f"⚠️ Fail `{MODEL_PATH}` atau `{LABELS_PATH}` tidak dijumpai dalam folder aplikasi!")
        st.stop()

    @st.cache_resource
    def load_ai_model():
        model = keras.models.load_model(MODEL_PATH, compile=False)
        with open(LABELS_PATH, "r") as f:
            labels = [line.strip() for line in f.readlines()]
        return model, labels

    model, class_names = load_ai_model()

    st.markdown(f"""
        <div style="margin-top: 10px; margin-bottom: 5px;">
            <h3 style="margin: 0; font-weight: 800; font-size: 1.4rem;">{t['upload_title']}</h3>
            <p style="margin-top: 4px; font-size: 0.95rem; opacity: 0.85;">{t['upload_desc']}</p>
        </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(t['btn_upload_label'], type=["jpg", "jpeg", "png"], label_visibility="collapsed")

    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        
        st.markdown("---")
        st.markdown(f"### {t['preview_title']}")
        
        col_img, col_act = st.columns([1.1, 1])
        with col_img:
            st.image(image, use_container_width=True)
        
        with col_act:
            st.markdown('<div class="btn-main">', unsafe_allow_html=True)
            if st.button(t['btn_analyze'], key="btn_run_ai", use_container_width=True):
                with st.spinner(t['analyzing']):
                    size = (224, 224)
                    image_resized = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
                    image_array = np.asarray(image_resized)
                    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1.0
                    
                    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
                    data[0] = normalized_image_array

                    prediction = model.predict(data)
                    index = np.argmax(prediction)
                    raw_label = class_names[index]
                    
                    clean_label = raw_label.split(" ", 1)[-1] if " " in raw_label else raw_label
                    confidence = float(prediction[0][index]) * 100
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    # Simpan ke Sejarah Imbasan (Session State)
                    st.session_state.scan_history.insert(0, {
                        "time": timestamp,
                        "result": clean_label,
                        "confidence": f"{confidence:.2f}%"
                    })

                    st.markdown(f"""
                        <div style='background: {card_bg}; padding: 20px; border-radius: 18px; border-left: 6px solid {brand_green}; box-shadow: 0 5px 18px rgba(0,0,0,0.05); margin-top: 10px;'>
                            <h4 style='margin:0; color: {brand_green}; font-size: 12px; letter-spacing: 1px;'>{t['result_title']}</h4>
                            <h2 style='margin-top: 5px; margin-bottom: 5px; color: {text_primary}; font-size: 24px;'><b>{clean_label}</b></h2>
                            <p style='margin:0; font-size: 14px; color: {text_secondary};'>{t['confidence']}: <b>{confidence:.2f}%</b></p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                        <div class="water-container">
                            <div class="water-bar" style="width: {confidence}%;">
                                <span class="water-text">🌊 {confidence:.2f}%</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

                    st.markdown(f"""
                        <div style='background-color: {brand_accent}; border-radius: 12px; padding: 12px 16px; margin-top: 15px; border: 1px solid {card_border}; font-size: 12px; color: {text_primary};'>
                            {t['disclaimer']}
                        </div>
                    """, unsafe_allow_html=True)

                    # Butang Muat Turun Laporan Ringkas (.txt)
                    report_content = f"--- VETVISION AI HEALTH REPORT ---\nTime: {timestamp}\nResult: {clean_label}\nConfidence: {confidence:.2f}%\nDisclaimer: {t['disclaimer']}"
                    st.download_button(
                        label=t['download_report_btn'],
                        data=report_content,
                        file_name=f"VetVision_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )

            st.markdown('</div>', unsafe_allow_html=True)

    # Paparan Sejarah Imbasan Sesi Ini
    st.markdown("---")
    st.markdown(f"### {t['history_title']}")
    if len(st.session_state.scan_history) == 0:
        st.info(t['history_empty'])
    else:
        for idx, item in enumerate(st.session_state.scan_history[:5]): # Papar 5 yang terkini
            st.markdown(f"""
                <div style='background: {card_bg}; padding: 12px 18px; border-radius: 12px; border: 1px solid {card_border}; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center;'>
                    <div>
                        <span style='font-size: 13px; font-weight: 700; color: {brand_green};'>#{idx+1} • {item['result']}</span>
                        <p style='margin: 0; font-size: 11px; opacity: 0.8;'>🕒 {item['time']}</p>
                    </div>
                    <div style='font-weight: 800; font-size: 14px;'>
                        {item['confidence']}
                    </div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="feature-bar">
        <div class="feature-card">
            <div class="feature-icon-box">{t['f1_icon']}</div>
            <div class="feature-text">
                <h4>{t['f1_title']}</h4>
                <p>{t['f1_desc']}</p>
            </div>
        </div>
        <div class="feature-card">
            <div class="feature-icon-box">{t['f2_icon']}</div>
            <div class="feature-text">
                <h4>{t['f2_title']}</h4>
                <p>{t['f2_desc']}</p>
            </div>
        </div>
        <div class="feature-card">
            <div class="feature-icon-box">{t['f3_icon']}</div>
            <div class="feature-text">
                <h4>{t['f3_title']}</h4>
                <p>{t['f3_desc']}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 8. Halaman Perkhidmatan (Services)
elif st.session_state.current_page == "services":
    st.markdown(f"## {t['sec_services_title']}")
    st.write(t['services_subtitle'])
    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        st.info(f"**{t['s1_title']}**\n\n{t['s1_desc']}")
        if st.button(t['btn_test_scan'], key="go_home_from_s1", use_container_width=True):
            st.session_state.current_page = "home"
            st.rerun()
    with col_s2:
        st.success(f"**{t['s2_title']}**\n\n{t['s2_desc']}")
    with col_s3:
        st.warning(f"**{t['s3_title']}**\n\n{t['s3_desc']}")

    st.markdown("---")
    st.markdown(f"### {t['faq_title']}")
    with st.expander(t['faq_q1']):
        st.write(t['faq_a1'])
    with st.expander(t['faq_q2']):
        st.write(t['faq_a2'])

# 9. Halaman Tentang Kami (About)
elif st.session_state.current_page == "about":
    st.markdown(f"## {t['sec_about_title']}")
    st.markdown(t['about_p1'], unsafe_allow_html=True)
    st.write("")
    
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.metric(label=t['metric_1_label'], value=t['metric_1_val'])
    with col_m2:
        st.metric(label=t['metric_2_label'], value=t['metric_2_val'])
    with col_m3:
        st.metric(label=t['metric_3_label'], value=t['metric_3_val'])

    st.write("")
    st.success(f"**{t['about_misi_title']}**: {t['about_misi_desc']}")

# 10. Halaman Hubungi (Contact)
elif st.session_state.current_page == "contact":
    st.markdown(f"## {t['sec_contact_title']}")
    st.write(t['contact_subtitle'])
    c_c1, c_c2 = st.columns(2)
    with c_c1:
        st.write(f"{t['contact_address_label']}: {t['contact_address_val']}")
        st.write(f"{t['contact_phone_label']}: +60 12-345 6789")
        st.write(f"{t['contact_email_label']}: support@vetvision.ai")
    with c_c2:
        st.text_input(t['input_name'])
        st.text_input(t['input_email'])
        st.text_area(t['input_msg'])
        if st.button(t['btn_send_msg'], use_container_width=True):
            st.success("Mesej anda telah berjaya dihantar! Pasukan kami akan menghubungi anda secepat mungkin." if selected_lang == "Bahasa Melayu 🇲🇾" else "Your message has been successfully sent! Our team will contact you shortly.")
