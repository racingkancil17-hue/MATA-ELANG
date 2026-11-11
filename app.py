import streamlit as st
import pandas as pd
import os
import requests
import urllib.parse
import streamlit.components.v1 as components

st.set_page_config(page_title="RADIO KANCIL FM - STUDIO FM", layout="wide")
PERSONIL_FILE = "personil.csv"

def load_personil():
    if not os.path.exists(PERSONIL_FILE):
        return pd.DataFrame(columns=["nama","merk"])
    try:
        return pd.read_csv(PERSONIL_FILE)
    except:
        return pd.DataFrame(columns=["nama","merk"])

def get_posisi(nama):
    kode = "radio-kancil-" + nama.lower().replace(" ", "-")
    try:
        r = requests.get(f"https://dweet.io/get/latest/dweet/for/{kode}", timeout=5)
        j = r.json()
        if j.get("this") == "succeeded":
            return j["with"][0]["content"]
    except:
        pass
    return None

def kick_personil(nama_kick):
    dfp = load_personil()
    dfp = dfp[dfp["nama"] != nama_kick]
    dfp.to_csv(PERSONIL_FILE, index=False)

def drone_orbit_html(lat, lon, nama):
    # Peta satelit muter orbit koyok drone
    return f"""
    <div id="map" style="width:100%; height:380px; border-radius:15px;"></div>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script>
    var map = L.map('map').setView([{lat}, {lon}], 19);
    L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{{z}}/{{y}}/{{x}}').addTo(map);
    var target = L.marker([{lat}, {lon}]).addTo(map);
    target.bindPopup("<b>🚁 TARGET: {nama}</b><br>Drone lagi orbit...").openPopup();
    L.circle([{lat}, {lon}], {{radius: 80, color: 'red', fillOpacity: 0.1}}).addTo(map);
    // Orbit drone - muter ngubengi target
    var angle = 0;
    var drone = L.circleMarker([{lat}, {lon}], {{radius: 8, color: 'yellow', fillColor: 'yellow', fillOpacity: 1}}).addTo(map);
    setInterval(function(){{
        angle += 0.08;
        var r = 0.0007;
        var nlat = {lat} + Math.sin(angle)*r;
        var nlon = {lon} + Math.cos(angle)*r;
        drone.setLatLng([nlat, nlon]);
    }}, 100);
    </script>
    <p style="color:white; font-family:sans-serif;">🚁 DRONE ORBIT AKTIF - Muteri {nama} | Titik kuning = Drone</p>
    """

params = st.query_params
mode = params.get("mode", "")
nama_url = params.get("nama", "")

if mode == "":
    st.title("📻 RADIO KANCIL FM - Bandung")
    if st.button("MASUK SEBAGAI STUDIO FM (LAPTOP)", type="primary", use_container_width=True):
        st.query_params["mode"] = "studio"
        st.rerun()
    st.stop()

# === HP SOBAT KANCIL - TETEP SAMA, JANGAN DIUBAH ===
if mode == "user":
    nama = nama_url or "HP-TANPA-NAMA"
    merk = params.get("merk", "HP")
    kode = "radio-kancil-" + nama.lower().replace(" ", "-")
    st.title(f"📻 RADIO KANCIL FM - {nama}")
    st.success(f"Halo {nama} | Merk: {merk}")
    st.write("Biarin halaman ini nyala, GPS jalan sendiri.")
    html = f"""
    <div id="s" style="padding:15px;background:#e8f5e9;border-radius:10px;font-family:sans-serif;">📍 GPS: Mencari...</div>
    <script>
    const kode = "{kode}";
    function kirim(lat, lon) {{
        document.getElementById('s').innerHTML = "✅ GPS AKTIF<br>Lat: "+lat+"<br>Lon: "+lon+"<br>Mengirim...";
        fetch("https://dweet.io/dweet/for/"+kode+"?lat="+lat+"&lon="+lon+"&nama="+encodeURIComponent("{nama}")+"&update="+new Date().toLocaleTimeString())
        .then(()=>{{ document.getElementById('s').innerHTML = "✅ GPS AKTIF<br>Lat: "+lat+"<br>Lon: "+lon+"<br>📍 TERKIRIM KE STUDIO FM! "+new Date().toLocaleTimeString(); }});
    }}
    setInterval(()=>{{ navigator.geolocation.getCurrentPosition((p)=>{{ kirim(p.coords.latitude, p.coords.longitude); }}); }}, 10000);
    navigator.geolocation.getCurrentPosition((p)=>{{ kirim(p.coords.latitude, p.coords.longitude); }},
    (e)=>{{ document.getElementById('s').innerHTML = "❌ GPS DITOLAK! Klik gembok, izinkan Lokasi."; }}, {{enableHighAccuracy:true}});
    </script>
    """
    components.html(html, height=130)
    st.stop()

# === STUDIO FM LAPTOP ===
if mode == "studio":
    st.title("🎙️ RADIO KANCIL FM - STUDIO FM LAPTOP")
    c1, c2 = st.columns([1,1])
    with c1:
        if st.button("🔄 REFRESH MANUAL", use_container_width=True, type="primary"):
            st.rerun()
    with c2:
        if st.button("🌍 BUKA GOOGLE EARTH WEB", use_container_width=True):
            st.markdown("[Klik Disini Buka Google Earth ->](https://earth.google.com/web/)")

    st.subheader("➕ Tambah Sobat Kancil Baru")
    nama_baru = st.text_input("Nama Sobat Kancil, contoh: Kancil 1")
    merk_baru = st.selectbox("Merk HP", ["OPPO","SAMSUNG","VIVO","XIAOMI","REALME","IPHONE","LAINNYA"])
    if st.button("TAMBAH", type="primary"):
        if nama_baru.strip() != "":
            dfp = load_personil()
            if nama_baru.strip() not in dfp["nama"].values:
                dfp = pd.concat([dfp, pd.DataFrame([{"nama":nama_baru.strip(),"merk":merk_baru}])], ignore_index=True)
                dfp.to_csv(PERSONIL_FILE, index=False)
            st.rerun()

    dfp = load_personil()
    st.subheader(f"📋 Daftar Sobat Kancil ({len(dfp)} orang) - Mode Studio")

    # TOMBOL KICK SEMUA OFFLINE - BEN GAK SAMPAH
    if not dfp.empty:
        if st.button("🧹 KICK SEMUA SING OFFLINE", type="secondary", use_container_width=True):
            for _, p in dfp.iterrows():
                if not get_posisi(p["nama"]):
                    kick_personil(p["nama"])
            st.success("Wes tak kick kabeh sing OFFLINE!")
            st.rerun()

    if dfp.empty:
        st.info("Belum ada Sobat Kancil.")
    else:
        try:
            host = st.context.headers.get("host", "radio-kancil-fm.streamlit.app")
            base = f"https://{host}"
        except:
            base = "https://radio-kancil-fm.streamlit.app"

        all_pos = []
        for _, p in dfp.iterrows():
            data = get_posisi(p["nama"])
            if data:
                try:
                    lat = float(data.get('lat')); lon = float(data.get('lon'))
                    all_pos.append({"nama":p["nama"],"lat":lat,"lon":lon,"update":data.get('update')})
                    st.success(f"🟢 {p['nama']} | ONLINE | {lat}, {lon} | {data.get('update')}")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.link_button(f"🛰️ SATELIT", f"https://www.google.com/maps/@?api=1&map_action=map&center={lat},{lon}&zoom=19&basemap=satellite")
                    with col2:
                        st.link_button(f"🌍 EARTH", f"https://earth.google.com/web/@{lat},{lon},500a,500d,35y,0h,0t,0r")
                    with col3:
                        if st.button(f"🚁 DRONE ORBIT {p['nama']}", key=f"drone_{p['nama']}"):
                            st.session_state["orbit"] = {"nama":p["nama"],"lat":lat,"lon":lon}
                    with col4:
                        st.link_button(f"🗺️ MAPS", f"https://www.google.com/maps?q={lat},{lon}")
                    # Nek tombol drone dipencet, munculke peta orbit
                    if st.session_state.get("orbit", {}).get("nama") == p["nama"]:
                        components.html(drone_orbit_html(lat, lon, p["nama"]), height=430)
                        if st.button(f"❌ TUTUP DRONE {p['nama']}", key=f"tutup_{p['nama']}"):
                            st.session_state["orbit"] = {}
                            st.rerun()
                except:
                    st.error(f"🔴 {p['nama']} | Data GPS Rusak")
                    if st.button(f"👢 KICK {p['nama']}", key=f"kick_rusak_{p['nama']}"):
                        kick_personil(p["nama"]); st.rerun()
            else:
                st.error(f"🔴 {p['nama']} - {p['merk']} | OFFLINE")
                # FITUR KICK PER ORANG - SING OFFLINE
                if st.button(f"👢 KICK / HAPUS {p['nama']} - Ben Gak Sampah", key=f"kick_{p['nama']}", type="primary"):
                    kick_personil(p["nama"])
                    st.success(f"{p['nama']} wes tak kick!")
                    st.rerun()

            link = f"{base}/?mode=user&nama={urllib.parse.quote(p['nama'])}&merk={urllib.parse.quote(p['merk'])}"
            st.code(link, language="text")
            st.caption("Copy link ini kirim ke WA Sobat Kancil.")
            st.markdown("---")

        if all_pos:
            st.subheader("🛰️ PETA SATELIT - SEMUA SOBAT KANCIL")
            df_map = pd.DataFrame(all_pos)
            st.map(df_map, latitude="lat", longitude="lon", size=20, color="#FF0000")
            st.caption("Titik merah = posisi Sobat Kancil. Zoom in/out di peta.")
            kml = '<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2"><Document><name>RADIO KANCIL FM</name>'
            for pos in all_pos:
                kml += f"<Placemark><name>{pos['nama']}</name><description>Update: {pos['update']}</description><Point><coordinates>{pos['lon']},{pos['lat']},0</coordinates></Point></Placemark>"
            kml += '</Document></kml>'
            st.download_button("📥 DOWNLOAD KML BUAT GOOGLE EARTH PRO", data=kml, file_name="radio_kancil.kml", mime="application/vnd.google-earth.kml+xml", use_container_width=True)
