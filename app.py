import streamlit as st
import json, os, re
from datetime import datetime
import folium
from streamlit_folium import st_folium
import streamlit.components.v1 as components

st.set_page_config(page_title="MATA ELANG", layout="wide")
FILE = "lokasi.json"

def load_data():
    if not os.path.exists(FILE):
        return {}
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f)

def bersih_nama(nama):
    # Buat nama room Jitsi, cuma huruf angka aja biar aman
    return re.sub(r'[^a-zA-Z0-9]', '', nama)

params = st.query_params
mode = params.get("mode", "komando")

# ================= MODE VC - RUANG VIDEO CALL =================
if mode == "vc":
    room = params.get("room", "MATAELANG")
    nama_room = bersih_nama(room)
    st.markdown(f"<h2 style='text-align:center'>📹 VC - {room}</h2>", unsafe_allow_html=True)
    st.write("Klik **Join** kalau diminta izin kamera/mic. Biarin halaman ini nyala selama VC.")
    st.info(f"Link VC ini kirim ke temen lu: `https://mata-elang.streamlit.app/?mode=vc&room={room}`")
    # Jitsi Meet Embed - Gratis kayak Zoom, tanpa login
    components.html(f"""
    <iframe src="https://meet.jit.si/MATAELANG-{nama_room}#config.prejoinPageEnabled=false" 
    style="width:100%; height:600px; border:0; border-radius:12px;" 
    allow="camera; microphone; fullscreen; display-capture; autoplay; clipboard-write"></iframe>
    """, height=620)
    if st.button("⬅️ KEMBALI KE KOMANDO"):
        st.query_params.clear()
        st.rerun()
    st.stop()

# ================= MODE USER - ISI NAMA =================
if mode == "user":
    st.markdown("<h1 style='text-align:center'>🦅 MATA ELANG - LIVE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center'>Isi nama lu, aktifin GPS, biar ke-pantau komando</p>", unsafe_allow_html=True)
    nama = st.text_input("👤 NAMA KAMU:", placeholder="Contoh: Budi Bandung")
    lat_q = params.get("lat", "")
    lon_q = params.get("lon", "")
    nama_q = params.get("nama", "")
    if lat_q and lon_q and nama_q:
        data = load_data()
        data[nama_q] = {"nama": nama_q, "lat": float(lat_q), "lon": float(lon_q), "waktu": datetime.now().strftime("%H:%M:%S")}
        save_data(data)
        st.success(f"✅ GPS AKTIF - {nama_q} TERPANTAU!")
        st.write(f"📍 {lat_q} , {lon_q}")
        st.info("Jangan tutup halaman ini ya...")
        # Kalau ada yang ngajak VC, kasih tombol join VC
        st.markdown("---")
        st.write("Kalau Komando ngajak VC, klik ini:")
        if st.button(f"📹 JOIN VC - {nama_q}", use_container_width=True):
            st.query_params.update({"mode": "vc", "room": nama_q})
            st.rerun()
        components.html(f"""
        <script>
        setTimeout(function(){{
            navigator.geolocation.getCurrentPosition(function(pos){{
                window.parent.location.href = "/?mode=user&nama=" + encodeURIComponent("{nama_q}") + "&lat=" + pos.coords.latitude + "&lon=" + pos.coords.longitude;
            }});
        }}, 5000);
        </script>
        """, height=0)
    elif nama:
        if st.button("📡 AKTIFKAN GPS", use_container_width=True):
            components.html(f"""
            <script>
            navigator.geolocation.getCurrentPosition(function(pos){{
                window.parent.location.href = "/?mode=user&nama=" + encodeURIComponent("{nama}") + "&lat=" + pos.coords.latitude + "&lon=" + pos.coords.longitude;
            }}, function(err){{ alert("Tolong izinkan lokasi!"); }});
            </script>
            """, height=0)
            st.info("Klik IZINKAN / ALLOW kalau muncul popup...")
    else:
        st.warning("Isi nama dulu bro!")
    st.stop()

# ================= MODE KOMANDO - PETA + KLIK TITIK -> VC =================
data = load_data()
st.markdown("<h1 style='text-align:center'>🦅 MATA ELANG - KOMANDO</h1>", unsafe_allow_html=True)

# Cek lagi ada yang lagi VC?
vc_target = params.get("vc", "")

if vc_target:
    # Lagi VC sama orang ini
    room = vc_target
    st.markdown(f"### 📹 SEDANG VC DENGAN: **{room}**")
    st.warning(f"Kirim link ini ke {room} biar dia join: https://mata-elang.streamlit.app/?mode=vc&room={room}")
    components.html(f"""
    <iframe src="https://meet.jit.si/MATAELANG-{bersih_nama(room)}#config.prejoinPageEnabled=false" 
    style="width:100%; height:550px; border:0; border-radius:12px;" 
    allow="camera; microphone; fullscreen; display-capture; autoplay"></iframe>
    """, height=570)
    if st.button("❌ TUTUP VC"):
        st.query_params.clear()
        st.rerun()
    st.markdown("---")

st.write(f"**{len(data)} PERSONEL ONLINE**")
if not data:
    st.info("Belum ada yang online...")
    st.code("https://mata-elang.streamlit.app/?mode=user")
    st.stop()

m = folium.Map(location=[-6.9, 107.6], zoom_start=7)
for key, v in data.items():
    folium.Marker([v["lat"], v["lon"]], popup=f"<b>{v['nama']}</b>", tooltip=v["nama"], icon=folium.Icon(color="red", icon="user")).add_to(m)
st_folium(m, width=1100, height=450)

st.markdown("### 📋 KLIK TITIK UNTUK INTERAKSI 1-1")
for key, v in data.items():
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.write(f"🟢 **{v['nama']}** | 📍 {v['lat']:.5f}, {v['lon']:.5f} | 🕒 {v['waktu']}")
    with col2:
        # Tombol VC 1-1
        if st.button(f"📹 VC {v['nama']}", key=f"vc_{v['nama']}"):
            st.query_params.update({"vc": v['nama']})
            st.rerun()
    with col3:
        st.write(f"[🔗 Copy Link VC](https://mata-elang.streamlit.app/?mode=vc&room={v['nama']})")

st.markdown("---")
st.markdown("**Link buat teman (isi nama):**")
st.code("https://mata-elang.streamlit.app/?mode=user")
