import streamlit as st
import json, os, re
from datetime import datetime
import folium
from streamlit_folium import st_folium
import streamlit.components.v1 as components

# CUMA 1x, PALING ATAS, JANGAN ADA LAGI DI BAWAH!
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
    return re.sub(r'[^a-zA-Z0-9]', '', nama)

params = st.query_params
mode = params.get("mode", "komando")

# ============ MODE VC ============
if mode == "vc":
    room = params.get("room", "MATAELANG")
    st.markdown(f"<h2 style='text-align:center'>📹 VC - {room}</h2>", unsafe_allow_html=True)
    st.info(f"Kirim link ini ke temen lu: https://mata-elang.streamlit.app/?mode=vc&room={room}")
    components.html(f"""
    <iframe src="https://meet.jit.si/MATAELANG-{bersih_nama(room)}#config.prejoinPageEnabled=false"
    style="width:100%; height:600px; border:0; border-radius:12px;"
    allow="camera; microphone; fullscreen; display-capture; autoplay"></iframe>
    """, height=620)
    if st.button("⬅️ KEMBALI KE KOMANDO"):
        st.query_params.clear()
        st.rerun()
    st.stop()

# ============ MODE USER - 1x KLIK LANGSUNG ON ============
if mode == "user":
    lat_q = params.get("lat", "")
    lon_q = params.get("lon", "")
    nama_q = params.get("nama", "")

    if lat_q and lon_q and nama_q:
        data = load_data()
        data[nama_q] = {"nama": nama_q, "lat": float(lat_q), "lon": float(lon_q), "waktu": datetime.now().strftime("%H:%M:%S")}
        save_data(data)
        st.success(f"✅ {nama_q} ONLINE! GPS AKTIF!")
        st.write(f"📍 {lat_q} , {lon_q}")
        st.info("Jangan tutup halaman ini, biarin nyala...")
        if st.button(f"📹 JOIN VC - {nama_q}", use_container_width=True):
            st.query_params.update({"mode": "vc", "room": nama_q})
            st.rerun()
        # Auto update 5 detik
        components.html(f"""
        <script>
        setTimeout(function(){{
            navigator.geolocation.getCurrentPosition(function(pos){{
                window.parent.location.href = "/?mode=user&nama=" + encodeURIComponent("{nama_q}") + "&lat=" + pos.coords.latitude + "&lon=" + pos.coords.longitude;
            }});
        }}, 5000);
        </script>
        """, height=0)
    else:
        # TOMBOL HTML LANGSUNG, BUKAN TOMBOL STREAMLIT BIAR GAK LEMOT
        components.html("""
        <div style="font-family:sans-serif; text-align:center; padding:10px;">
            <h1>🦅 MATA ELANG - LIVE</h1>
            <p>Isi nama lu, klik tombol, langsung ON!</p>
            <input id="nama" type="text" placeholder="Contoh: Budi"
            style="width:100%; padding:14px; font-size:18px; border-radius:10px; border:1px solid #ccc; margin-bottom:12px;" />
            <button onclick="aktifin()" id="btn"
            style="width:100%; padding:15px; font-size:18px; background:#ff4b4b; color:white; border:none; border-radius:10px; font-weight:bold;">
            📡 AKTIFKAN GPS - KLIK 1x
            </button>
            <p id="status" style="margin-top:15px; color:#555;"></p>
        </div>
        <script>
        function aktifin(){
            var nama = document.getElementById('nama').value;
            if(!nama){ alert('Isi nama dulu bro!'); return; }
            document.getElementById('btn').innerHTML = '⏳ MENGHUBUNGKAN GPS...';
            document.getElementById('status').innerHTML = 'Tunggu popup IZINKAN muncul...';
            navigator.geolocation.getCurrentPosition(function(pos){
                window.parent.location.href = "/?mode=user&nama=" + encodeURIComponent(nama) + "&lat=" + pos.coords.latitude + "&lon=" + pos.coords.longitude;
            }, function(err){
                alert('GAGAL! Klik gembok di atas, ubah Lokasi jadi IZINKAN, terus reload!');
                document.getElementById('btn').innerHTML = '📡 COBA LAGI';
            }, {enableHighAccuracy:true, timeout:10000});
        }
        </script>
        """, height=350)
    st.stop()

# ============ MODE KOMANDO ============
data = load_data()
st.markdown("<h1 style='text-align:center'>🦅 MATA ELANG - KOMANDO</h1>", unsafe_allow_html=True)
vc_target = params.get("vc", "")
if vc_target:
    st.markdown(f"### 📹 SEDANG VC DENGAN: **{vc_target}**")
    st.warning(f"Kirim link ini ke {vc_target}: https://mata-elang.streamlit.app/?mode=vc&room={vc_target}")
    components.html(f"""
    <iframe src="https://meet.jit.si/MATAELANG-{bersih_nama(vc_target)}#config.prejoinPageEnabled=false"
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
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(f"🟢 **{v['nama']}** | 📍 {v['lat']:.5f}, {v['lon']:.5f} | 🕒 {v['waktu']}")
    with col2:
        if st.button(f"📹 VC {v['nama']}", key=f"vc_{v['nama']}"):
            st.query_params.update({"vc": v['nama']})
            st.rerun()

st.markdown("---")
st.code("https://mata-elang.streamlit.app/?mode=user")
