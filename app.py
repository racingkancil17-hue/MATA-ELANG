import streamlit as st
import json, os
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

params = st.query_params
mode = params.get("mode", "komando")

# ============ MODE USER - HP KANCANE, ISI NAMA TOK ============
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
        st.info("Ojo ditutup halaman iki, ben tetep kepantau...")
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
        st.markdown("<h1 style='text-align:center'>🦅 MATA ELANG - LIVE</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center'>Isi jenengmu, aktifke GPS</p>", unsafe_allow_html=True)
        nama = st.text_input("👤 JENENGMU:", placeholder="Contoh: Budi")
        if nama:
            if st.button("📡 AKTIFKAN GPS", use_container_width=True):
                components.html(f"""
                <script>
                navigator.geolocation.getCurrentPosition(function(pos){{
                    window.parent.location.href = "/?mode=user&nama=" + encodeURIComponent("{nama}") + "&lat=" + pos.coords.latitude + "&lon=" + pos.coords.longitude;
                }}, function(err){{ alert("Tolong izinkan lokasi!"); }});
                </script>
                """, height=0)
                st.info("Klik IZINKAN / ALLOW nek muncul popup...")
        else:
            st.warning("Isi jeneng disik bro!")
    st.stop()

# ============ MODE KOMANDO - LAPTOPMU, WES DIPERBAIKI ============
data = load_data()
st.markdown("<h1 style='text-align:center'>🦅 MATA ELANG - KOMANDO</h1>", unsafe_allow_html=True)
st.write(f"**{len(data)} PERSONEL ONLINE** | Update otomatis tiap buka")

if not data:
    st.info("Durung ono sing online...")
    st.code("https://mata-elang.streamlit.app/?mode=user")
    st.stop()

# PETA
m = folium.Map(location=[-6.9, 107.6], zoom_start=7)
for key, v in data.items():
    folium.Marker(
        [v["lat"], v["lon"]],
        popup=f"<b>{v['nama']}</b><br>{v['waktu']}",
        tooltip=v["nama"],
        icon=folium.Icon(color="red", icon="user")
    ).add_to(m)

st_folium(m, width=1100, height=450)

# DAFTAR NAMA - SING MAU KODE HP, SAIKI WES JENENG
st.markdown("### 📋 DAFTAR PERSONEL")
for key, v in data.items():
    st.write(f"🟢 **{v['nama']}** | 📍 {v['lat']:.5f}, {v['lon']:.5f} | 🕒 Terakhir: {v['waktu']}")

st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    if st.button("🔄 REFRESH PETA", use_container_width=True):
        st.rerun()
with col2:
    if st.button("🗑️ HAPUS SEMUA", use_container_width=True):
        save_data({})
        st.rerun()

st.markdown("**Link gawe HP kancane:**")
st.code("https://mata-elang.streamlit.app/?mode=user")
