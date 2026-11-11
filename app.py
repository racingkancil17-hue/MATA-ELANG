import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(page_title="RADIO KANCIL FM", page_icon="📻", layout="centered")
FILE = "requests.json"

def load_data():
    if os.path.exists(FILE):
        try:
            with open(FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f)

params = st.query_params
mode = params.get("mode", "user")

# --- STYLE WES DIBENERKE TOTAL ---
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {background-color: #0f0f0f;}
[data-testid="stHeader"] {background-color: #0f0f0f;}
h1, h2, h3, p, label, span {color: white !important;}
.stTextInput input, .stTextArea textarea {background-color: white !important; color: black !important;}
div[data-baseweb="input"] input {color: black !important;}
/* IKI SING MARAI TULISAN KOTAK DADI KETOK - DIPAKSA IRENG */
[data-testid="stAlert"] * {color: black !important;}
[data-testid="stAlert"] {background-color: #FFF3CD !important;}
.stButton>button {background-color: #FF2D55; color: white; border-radius: 20px; width: 100%; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

# ================= STUDIO FM - TANPA SANDI =================
if mode == "studio":
    st.title("🎙️ STUDIO FM - RADIO KANCIL FM")
    st.write("Halo DJ KANCIL! Selamat siaran!")
    st.write("🔴 LIVE ON AIR - Kamu sedang siaran!")
    st.divider()
    
    data = load_data()
    st.subheader(f"📩 Request & Titip Salam Masuk: {len(data)}")
    
    if not data:
        st.info("Durung ono request mlebu, DJ. Enteni Sobat Kancil request.")
    else:
        for i, d in enumerate(reversed(data)):
            with st.container(border=True):
                st.write(f"**🎧 {d['nama']}** - {d['jam']}")
                st.write(f"🎵 Request Lagu: **{d['lagu']}**")
                st.write(f"💌 Titip Salam: {d['salam']}")
    
    if st.button("Hapus Semua Request"):
        save_data([])
        st.rerun()

# ================= SOBAT KANCIL =================
else:
    st.title("📻 RADIO KANCIL FM")
    st.subheader("Bareng DJ KANCIL - Live dari STUDIO FM")
    st.write("Halo SOBAT KANCIL! Lagi dengerin radio paling gaul se-Bandung! 🔥")
    st.write("🔴 ON AIR SEKARANG | Request lagu mu bakal dibacakke DJ langsung!")
    st.divider()

    st.subheader("📩 Request Lagu & Titip Salam")
    nama = st.text_input("Nama Gaul / Nama Panggilan Mu:")
    lagu = st.text_input("Request Lagu Opo, Sob?")
    salam = st.text_area("Titip Salam Gawe Sopo?")

    if st.button("KIRIM REQUEST KE STUDIO 🚀"):
        if nama and lagu:
            data = load_data()
            data.append({
                "nama": nama,
                "lagu": lagu,
                "salam": salam if salam else "-",
                "jam": datetime.now().strftime("%H:%M - %d/%m")
            })
            save_data(data)
            st.success(f"JOS! Request mu wes mlebu Studio, {nama}!")
            st.balloons()
        else:
            st.error("Isi Nama Gaul karo Lagu ne disik, Sob!")

    st.divider()
    st.caption("RADIO KANCIL FM - Radio ne Sobat Kancil | Bandung")
