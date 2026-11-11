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

params = st.query_params
mode = params.get("mode", "")
nama_url = params.get("nama", "")

if mode == "":
    st.title("📻 RADIO KANCIL FM - Bandung")
    if st.button("MASUK SEBAGAI STUDIO FM (LAPTOP)", type="primary", use_container_width=True):
        st.query_params["mode"] = "studio"
        st.rerun()
    st.stop()

# === HP LAPANGAN - TETEP SAMA ===
if mode == "user":
    nama = nama_url or "HP-TANPA-NAMA"
    merk = params.get("merk", "HP")
    kode = "radio-kancil-" + nama.lower().replace(" ", "-")
    st.title(f"📻 RADIO KANCIL FM - {nama}")
    st.success(f"Halo {nama} | Merk: {merk}")
    st.write("Biarin halaman ini nyala, GPS jalan sendiri.")
    html = f"""
    <div id="s" style="padding:15px;background:#e8f5e9;border-radius:10px;font-family:sans-serif;">📍 GPS: Mencari...</div>
    <button onclick="sos()" style="width:100%; margin-top:10px; background:#FF0000; color:white; border:none; padding:18px; border-radius:15px; font-size:20px; font-weight:bold;">🆘 SOS - BUTUH BANTUAN!</button>
    <p id="sos_status" style="font-family:sans-serif; font-weight:bold; color:red; text-align:center;"></p>
    <script>
    const kode = "{kode}";
    let lastLat=0, lastLon=0, status="AMAN";
    function kirim(lat, lon) {{
        lastLat=lat; lastLon=lon;
        fetch("https://dweet.io/dweet/for/"+kode+"?lat="+lat+"&lon="+lon+"&nama="+encodeURIComponent("{nama}")+"&status="+status+"&update="+new Date().toLocaleTimeString())
        .then(()=>{{ document.getElementById('s').innerHTML = "✅ GPS AKTIF<br>Lat: "+lat+"<br>Lon: "+lon+"<br>Status: "+status+"<br>📍 TERKIRIM KE STUDIO FM! "+new Date().toLocaleTimeString(); }});
    }}
    function sos(){{ status="SOS-BUTUH-BANTUAN"; document.getElementById('sos_status').innerHTML="🆘 SOS TERKIRIM! STUDIO FM LAGI MLUNCUR!"; kirim(lastLat,lastLon); alert("SOS Terkirim!"); }}
    setInterval(()=>{{ navigator.geolocation.getCurrentPosition((p)=>{{ kirim(p.coords.latitude, p.coords.longitude); }}); }}, 10000);
    navigator.geolocation.getCurrentPosition((p)=>{{ kirim(p.coords.latitude, p.coords.longitude); }},
    (e)=>{{ document.getElementById('s').innerHTML = "❌ GPS DITOLAK! Klik gembok, izinkan Lokasi."; }}, {{enableHighAccuracy:true}});
    </script>
    """
    components.html(html, height=280)
    st.stop()

# === STUDIO FM ===
if mode == "studio":
    st.title("🎙️ RADIO KANCIL FM - STUDIO FM LAPTOP")

    # ===== TAMBAH PODCAST TOK - NANG KENE =====
    st.subheader("🎙️ PODCAST KANCIL FM - Siaran Studio")
    st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
    st.caption("Podcast Kancil FM - Putar sambil mantau Sobat Kancil di lapangan. Ganti link audio iki karo link podcast mu dewe (Spotify / mp3 mu).")
    st.divider()

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🔄 REFRESH MANUAL", use_container_width=True, type="primary"):
            st.rerun()
    with c2:
        if st.button("🌍 BUKA GOOGLE EARTH WEB", use_container_width=True):
            st.markdown("[Klik Disini Buka Google Earth ->](https://earth.google.com/web/)")
    with c3:
        if st.button("🚁 BUKA DRONE CINEMATIC 3D", use_container_width=True, type="primary"):
            st.query_params["mode"] = "drone"
            st.rerun()

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
    if not dfp.empty:
        if st.button("🧹 KICK SEMUA SING OFFLINE", type="secondary", use_container_width=True):
            for _, p in dfp.iterrows():
                if not get_posisi(p["nama"]):
                    kick_personil(p["nama"])
            st.success("Wes tak kick kabeh sing OFFLINE!"); st.rerun()

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
                    status = data.get('status','AMAN'); update = data.get('update','-')
                    all_pos.append({"nama":p["nama"],"lat":lat,"lon":lon,"update":update,"status":status})
                    if "SOS" in str(status):
                        st.error(f"🆘 SOS!!! {p['nama']} BUTUH BANTUAN!!! | {lat}, {lon}")
                        st.link_button(f"🚨 MELUNCUR SEKARANG KE {p['nama']}", f"https://www.google.com/maps/dir/?api=1&destination={lat},{lon}&travelmode=driving", type="primary", use_container_width=True)
                    else:
                        st.success(f"🟢 {p['nama']} | ONLINE | {lat}, {lon} | {update}")
                    col1, col2, col3 = st.columns(3)
                    with col1: st.link_button(f"🛰️ SATELIT {p['nama']}", f"https://www.google.com/maps/@?api=1&map_action=map&center={lat},{lon}&zoom=19&basemap=satellite")
                    with col2: st.link_button(f"🌍 GOOGLE EARTH {p['nama']}", f"https://earth.google.com/web/@{lat},{lon},500a,500d,35y,0h,0t,0r")
                    with col3: st.link_button(f"🗺️ MAPS BIASA", f"https://www.google.com/maps?q={lat},{lon}")
                except:
                    st.error(f"🔴 {p['nama']} | Data GPS Rusak")
                    if st.button(f"👢 KICK {p['nama']}", key=f"kr_{p['nama']}"):
                        kick_personil(p["nama"]); st.rerun()
            else:
                st.error(f"🔴 {p['nama']} - {p['merk']} | OFFLINE")
                if st.button(f"👢 KICK / HAPUS {p['nama']}", key=f"k_{p['nama']}", type="primary"):
                    kick_personil(p["nama"]); st.success("Wes tak kick!"); st.rerun()
            link = f"{base}/?mode=user&nama={urllib.parse.quote(p['nama'])}&merk={urllib.parse.quote(p['merk'])}"
            st.code(link, language="text")
            st.caption("Copy link ini kirim ke WA Sobat Kancil.")
            st.markdown("---")
        if all_pos:
            st.subheader("🛰️ PETA SATELIT - SEMUA SOBAT KANCIL")
            st.map(pd.DataFrame(all_pos), latitude="lat", longitude="lon", size=20, color="#FF0000")
            kml = '<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2"><Document><name>RADIO KANCIL FM</name>'
            for pos in all_pos:
                kml += f"<Placemark><name>{pos['nama']}</name><description>Update: {pos['update']}</description><Point><coordinates>{pos['lon']},{pos['lat']},0</coordinates></Point></Placemark>"
            kml += '</Document></kml>'
            st.download_button("📥 DOWNLOAD KML BUAT GOOGLE EARTH PRO", data=kml, file_name="radio_kancil.kml", mime="application/vnd.google-earth.kml+xml", use_container_width=True)
    st.stop()

# === DRONE CINEMATIC 3D - PERSIS VIDEO MU ===
if mode == "drone":
    st.title("🦅 RADIO KANCIL FM - DRONE CINEMATIC 3D")
    st.write("Diemin 10 detik biar peta ke-load, baru klik tombol ijo nang ngisor peta!")
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
        st.warning("Durung ono sing ONLINE. Aktifke HP Sobat Kancil disik.")
        st.stop()
    import json as _json
    pos_json = _json.dumps(all_pos)
    html_drone = f"""
    <div style="position:relative; width:100%; height:600px;">
      <div id="map" style="width:100%; height:600px; border-radius:12px; overflow:hidden;"></div>
      <div id="hud" style="position:absolute; top:10px; left:10px; background:rgba(0,0,0,0.75); color:white; padding:10px 12px; border-radius:8px; font-family:monospace; font-size:12px; z-index:1000;">DRONE: SIAP<br>TARGET: {len(all_pos)} CHECKPOINT<br>Klik nama di bawah untuk cek lokasi</div>
      <div style="position:absolute; top:10px; right:10px; background:white; border-radius:8px; padding:4px; z-index:1000;">
        <button onclick="map.zoomIn()" style="display:block; width:28px; height:28px;">+</button>
        <button onclick="map.zoomOut()" style="display:block; width:28px; height:28px;">-</button>
      </div>
      <div style="position:absolute; bottom:55px; left:50%; transform:translateX(-50%); z-index:1000;">
        <button onclick="mulaiPatroli()" style="background:#FF2D55; color:white; border:none; padding:12px 28px; border-radius:25px; font-weight:bold; font-size:16px; cursor:pointer;">🎥 MULAI PATROLI DRONE</button>
      </div>
      <div style="position:absolute; bottom:12px; left:10px; right:10px; display:flex; gap:8px; z-index:1000; flex-wrap:wrap;">
        {''.join([f'<button onclick="terbangKe({i})" style="background:#111; color:#00FF66; border:1px solid #00FF66; padding:8px 14px; border-radius:20px; font-weight:bold; cursor:pointer;">📍 {p["nama"]} - TERBANG KE SINI</button>' for i,p in enumerate(all_pos)])}
      </div>
      <div style="position:absolute; bottom:-28px; left:0; right:0; background:#f0f0f0; padding:8px; font-family:sans-serif; font-size:13px;">Total: {len(all_pos)} Online. Klik salah satu tombol ijo.</div>
      <div id="valid" style="position:absolute; bottom:-52px; left:0; font-family:sans-serif; font-size:13px;">LOKASI VALID - {all_pos[0]["nama"]}</div>
    </div>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script>
    var data = {pos_json};
    var map = L.map('map').setView([-6.9175, 107.6191], 6);
    L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{{z}}/{{y}}/{{x}}').addTo(map);
    var markers = [];
    data.forEach(function(p, i){{
      var m = L.marker([p.lat, p.lon]).addTo(map);
      m.bindPopup("<b>"+p.nama+"</b><br>Lat: "+p.lat+"<br>Lon: "+p.lon);
      markers.push(m);
    }});
    var droneIcon = L.divIcon({{html:'<div style="font-size:28px;">⊕</div>', iconSize:[30,30]}});
    var drone = L.marker([-6.9175, 107.6191], {{icon: droneIcon}}).addTo(map);
    function setHUD(t){{ document.getElementById('hud').innerHTML = t; }}
    function animateTo(lat, lon, zoom, done){{
      var start = map.getCenter(); var startZoom = map.getZoom();
      var steps = 60; var i=0;
      var iv = setInterval(function(){{
        i++;
        var f = i/steps;
        var nlat = start.lat + (lat-start.lat)*f;
        var nlon = start.lng + (lon-start.lng)*f;
        var nz = startZoom + (zoom-startZoom)*f;
        map.setView([nlat, nlon], nz);
        drone.setLatLng([nlat, nlon]);
        if(i>=steps){{ clearInterval(iv); if(done) done(); }}
      }}, 30);
    }}
    function terbangKe(i){{
      var p = data[i];
      document.getElementById('valid').innerHTML = "LOKASI VALID - " + p.nama;
      setHUD("DRONE: TERBANG...<br>TARGET: "+p.nama+"<br>ALT: 500m | SPD: 60 Km/j");
      animateTo(p.lat, p.lon, 18, function(){{
        setHUD("DRONE: HOVER - MEMANTAU<br>CHECKPOINT: "+p.nama+"<br>Lat: "+p.lat.toFixed(5)+"<br>Lon: "+p.lon.toFixed(5)+"<br>STATUS: STABIL...");
        markers[i].openPopup();
      }});
    }}
    var patroliIdx = 0; var patroliJalan = false;
    function mulaiPatroli(){{
      if(patroliJalan) return; patroliJalan = true; patroliIdx = 0;
      setHUD("DRONE: PATROLI DIMULAI...");
      patroliNext();
    }}
    function patroliNext(){{
      if(patroliIdx >= data.length){{
        setHUD("DRONE: PATROLI SELESAI<br>Semua "+data.length+" Checkpoint Terpantau");
        patroliJalan = false;
        animateTo(-6.9175, 107.6191, 6, null);
        return;
      }}
      var p = data[patroliIdx];
      setHUD("DRONE: TERBANG...<br>TARGET "+(patroliIdx+1)+"/"+data.length+": "+p.nama+"<br>ALT: 500m | SPD: 60 Km/j");
      document.getElementById('valid').innerHTML = "LOKASI VALID - " + p.nama;
      animateTo(p.lat, p.lon, 18, function(){{
        setHUD("DRONE: HOVER - MEMANTAU<br>CHECKPOINT: "+p.nama+"<br>Lat: "+p.lat.toFixed(5)+"<br>Lon: "+p.lon.toFixed(5)+"<br>STATUS: STABIL...");
        setTimeout(function(){{ patroliIdx++; patroliNext(); }}, 2500);
      }});
    }}
    </script>
    """
    components.html(html_drone, height=680)
    st.caption("Podcast tetep jalan nang Studio. Drone iki persis video mu: klik TERBANG KE SINI -> drone mabur, zoom mudun, hover, stabil. Klik MULAI PATROLI DRONE -> drone patroli kabeh checkpoint siji-siji sampe SELESAI.")
