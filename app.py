import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import streamlit.components.v1 as components

st.set_page_config(page_title="MATA ELANG", layout="wide")
DATA_FILE = "mata_elang_data.csv"
PERSONIL_FILE = "personil.csv"

def load_data():
    if not os.path.exists(DATA_FILE):
        return pd.DataFrame(columns=["nama","merk","lat","lon","update","timestamp"])
    try:
        return pd.read_csv(DATA_FILE)
    except:
        return pd.DataFrame(columns=["nama","merk","lat","lon","update","timestamp"])

def load_personil():
    if not os.path.exists(PERSONIL_FILE):
        return pd.DataFrame(columns=["nama","merk"])
    try:
        return pd.read_csv(PERSONIL_FILE)
    except:
        return pd.DataFrame(columns=["nama","merk"])

def save_data(nama, merk, lat, lon):
    df = load_data()
    now = datetime.now()
    df = df[df["nama"] != nama]
    new = pd.DataFrame([{"nama":nama,"merk":merk,"lat":lat,"lon":lon,"update":now.strftime("%H:%M:%S"),"timestamp":now}])
    df = pd.concat([df, new], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

def clean_old():
    if not os.path.exists(DATA_FILE):
        return
    try:
        df = load_data()
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df[df["timestamp"] > datetime.now() - timedelta(minutes=2)]
        df.to_csv(DATA_FILE, index=False)
    except:
        pass

params = st.query_params
mode = params.get("mode", "")
nama_url = params.get("nama", "")
merk_url = params.get("merk", "")
lat_url = params.get("lat", "")
lon_url = params.get("lon", "")

if mode == "user" and nama_url and lat_url and lon_url:
    try:
        save_data(nama_url, merk_url or "HP", float(lat_url), float(lon_url))
    except:
        pass

# === LANDING ===
if mode == "":
    st.title("🦅 MATA ELANG - Bandung")
    st.write("Halaman Komando. HP lapangan jangan buka ini, tunggu link dari Komando.")
    if st.button("MASUK SEBAGAI KOMANDO", type="primary", use_container_width=True):
        st.query_params["mode"] = "komando"
        st.rerun()
    st.stop()

# === HP LAPANGAN - TETEP AUTO KIRIM GPS ===
if mode == "user":
    nama = nama_url or "HP-TANPA-NAMA"
    merk = merk_url or "HP"
    st.title(f"🦅 MATA ELANG - {nama}")
    st.success(f"Halo {nama} | Merk: {merk}")
    st.write("Kamu udah terdaftar sama Komando. Biarin halaman ini nyala, GPS jalan sendiri.")
    if lat_url:
        st.success(f"📍 TERKIRIM KE KOMANDO! Lat: {lat_url} Lon: {lon_url} | {datetime.now().strftime('%H:%M:%S')}")
    else:
        st.info("📍 Mencari GPS... Izinkan lokasi kalau diminta.")
    html = f"""
    <div id="s" style="padding:15px;background:#e8f5e9;border-radius:10px;font-family:sans-serif;">📍 GPS: Mencari...</div>
    <script>
    const nama = "{nama}";
    const merk = "{merk}";
    let sudahKirim = false;
    function kirim(lat, lon) {{
        document.getElementById('s').innerHTML = "✅ GPS AKTIF<br>Lat: "+lat+"<br>Lon: "+lon+"<br>Mengirim ke Komando...";
        if (sudahKirim) return;
        sudahKirim = true;
        setTimeout(()=>{{
            const u = new URL(window.top.location.href);
            u.searchParams.set('mode','user');
            u.searchParams.set('nama', nama);
            u.searchParams.set('merk', merk);
            u.searchParams.set('lat', lat);
            u.searchParams.set('lon', lon);
            window.top.location.href = u.toString();
        }}, 3000);
    }}
    navigator.geolocation.watchPosition(
        (p)=>{{ kirim(p.coords.latitude, p.coords.longitude); }},
        (e)=>{{ document.getElementById('s').innerHTML = "❌ GPS DITOLAK! Klik gembok di atas, izinkan Lokasi, refresh."; }},
        {{enableHighAccuracy:true}}
    );
    </script>
    """
    components.html(html, height=120)
    st.stop()

# === KOMANDO - UDAH GAK AUTO REFRESH ===
if mode == "komando":
    st.title("🦅 MATA ELANG - KOMANDO")
    st.write("Komando yang input data. HP tinggal klik link.")
    
    if st.button("🔄 REFRESH MANUAL - Cek Posisi Terbaru", use_container_width=True):
        st.rerun()

    st.subheader("➕ Tambah Personil Baru")
    nama_baru = st.text_input("Nama Personil, contoh: Kancil 1")
    merk_baru = st.selectbox("Merk HP", ["OPPO","SAMSUNG","VIVO","XIAOMI","REALME","IPHONE","LAINNYA"])
    if st.button("TAMBAH", type="primary", use_container_width=True):
        if nama_baru.strip() != "":
            dfp = load_personil()
            if nama_baru.strip() not in dfp["nama"].values:
                dfp = pd.concat([dfp, pd.DataFrame([{"nama":nama_baru.strip(),"merk":merk_baru}])], ignore_index=True)
                dfp.to_csv(PERSONIL_FILE, index=False)
            st.rerun()
    
    st.markdown("---")
    dfp = load_personil()
    clean_old()
    df = load_data()
    st.subheader(f"📋 Daftar Personil ({len(dfp)} orang)")
    if dfp.empty:
        st.info("Belum ada personil. Tambah dulu di atas, contoh: Kancil 1")
    else:
        try:
            host = st.context.headers.get("host", "mata-elang.streamlit.app")
            base = f"https://{host}"
        except:
            base = "https://mata-elang.streamlit.app"
        for _, p in dfp.iterrows():
            cari = df[df["nama"]==p["nama"]] if not df.empty else pd.DataFrame()
            if not cari.empty:
                r = cari.iloc[0]
                st.success(f"🟢 {p['nama']} - {p['merk']} | ONLINE | {r['lat']}, {r['lon']} | Update: {r['update']}")
                st.link_button(f"BUKA MAPS {p['nama']}", f"https://www.google.com/maps?q={r['lat']},{r['lon']}")
            else:
                st.error(f"🔴 {p['nama']} - {p['merk']} | OFFLINE / BELUM KIRIM GPS")
            link = f"{base}/?mode=user&nama={p['nama'].replace(' ','%20')}&merk={p['merk']}"
            st.code(link, language="text")
            st.caption("Copy link di atas, kirim ke WA personilnya. Dia tinggal klik!")
            if st.button(f"Hapus {p['nama']}", key=f"del_{p['nama']}"):
                dfp = dfp[dfp["nama"] != p["nama"]]
                dfp.to_csv(PERSONIL_FILE, index=False)
                st.rerun()
            st.markdown("---")
    if st.button("🗑️ HAPUS SEMUA DATA GPS"):
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
        st.rerun()
    if st.button("Keluar"):
        st.query_params.clear()
        st.rerun()
