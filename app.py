import streamlit as st
import requests

BIN_ID = "6aeeda8bac6210605a74a7b5"
API_KEY = "$2a$10$LqQMOcUMXjbfZswzJUFrReGYD5dloL2gTCOLRwT17Oo96mUzr7.aO"
URL = "https://api.jsonbin.io/v3/b/" + BIN_ID
HEADERS = {"X-Master-Key": API_KEY, "Content-Type": "application/json"}

st.set_page_config(page_title="RADIO KANCIL FM", layout="wide")
params = st.query_params
mode = params.get("mode", "komando")

def ambil():
    try:
        r = requests.get(URL + "/latest", headers=HEADERS, timeout=10)
        d = r.json().get("record", {})
        while isinstance(d, dict) and "record" in d:
            d = d["record"]
        if not isinstance(d, dict): d = {}
        users = {k:v for k,v in d.items() if k != "_kicked" and isinstance(v, dict) and "lat" in v}
        kicked = d.get("_kicked", [])
        if not isinstance(kicked, list): kicked = []
        return users, kicked
    except:
        return {}, []

def simpan(users, kicked):
    data = dict(users)
    data["_kicked"] = kicked
    requests.put(URL, headers=HEADERS, json=data, timeout=10)

if mode == "user":
    st.title("📻 RADIO KANCIL FM - LIVE")
    nama = st.text_input("👤 ISI JENENGMU:", placeholder="Contoh: NamaMu")
    if not nama:
        st.warning("Isi jenengmu disik!")
        st.stop()
    nama = nama.strip()
    users, kicked = ambil()
    if nama in kicked:
        st.error(f"⛔ {nama} DIKELUARKAN STUDIO FM! Tunggu link baru!")
        st.stop()
    st.success(f"Halo {nama}! GPS Jalan! Ojo ditutup!")
    html_code = f"""
    <div id="out" style="padding:15px;background:#e8f5e9;border-radius:10px;">Mencari GPS...</div>
    <script>
    const BIN_ID = "6aeeda8bac6210605a74a7b5";
    const API_KEY = "$2a$10$LqQMOcUMXjbfZswzJUFrReGYD5dloL2gTCOLRwT17Oo96mUzr7.aO";
    let myId = "{nama}";
    function kirim(){{
      navigator.geolocation.getCurrentPosition(pos => {{
        document.getElementById('out').innerHTML = "GPS AKTIF - " + myId + "<br>Lat: " + pos.coords.latitude;
        fetch("https://api.jsonbin.io/v3/b/" + BIN_ID + "/latest", {{headers: {{"X-Master-Key": API_KEY}}}})
        .then(r => r.json()).then(j => {{
          let d = j.record || {{}}; while(d.record){{ d = d.record; }}
          let users = {{}}; let kicked = d._kicked || [];
          for(let k in d){{ if(k != "_kicked" && d[k] && d[k].lat){{ users[k] = d[k]; }} }}
          if(kicked.includes(myId)){{ document.getElementById('out').innerHTML = "⛔ KAMU DIKELUARKAN STUDIO FM!"; return; }}
          users[myId] = {{lat: pos.coords.latitude, lon: pos.coords.longitude, waktu: new Date().toLocaleString()}};
          users["_kicked"] = kicked;
          fetch("https://api.jsonbin.io/v3/b/" + BIN_ID, {{method: "PUT", headers: {{"Content-Type": "application/json", "X-Master-Key": API_KEY}}, body: JSON.stringify(users)}});
        }});
      }});
    }}
    kirim(); setInterval(kirim, 5000);
    </script>
    """
    st.components.v1.html(html_code, height=120)

elif mode == "drone":
    st.title("📻 RADIO KANCIL FM - DRONE CINEMATIC 3D")
    st.write("Diemin 10 detik biar peta ke-load, baru klik tombol ijo jeneng nang ngisor peta!")
    st.markdown("[⬅️ Balik ke STUDIO FM](https://radio-kancil-fm.streamlit.app/?mode=komando)")
    drone_html = """
    <link href="https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.css" rel="stylesheet" />
    <script src="https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.js"></script>
    <style>
      #map{width:100%; height:650px; border-radius:12px;}
      .hud{position:absolute; top:12px; left:12px; z-index:10; background:rgba(0,0,0,0.65); color:white; padding:10px 14px; border-radius:10px; font-family:monospace; font-size:14px; border:1px solid rgba(255,255,255,0.3);}
      .btn{position:absolute; bottom:18px; left:50%; transform:translateX(-50%); z-index:10; background:#ff0000; color:white; border:none; padding:14px 28px; font-size:18px; font-weight:bold; border-radius:30px; cursor:pointer;}
      .zoomBtn{position:absolute; top:12px; right:12px; z-index:10; display:flex; flex-direction:column; gap:6px;}
      .zoomBtn button{background:#fff; border:none; width:42px; height:42px; font-size:22px; font-weight:bold; border-radius:8px; cursor:pointer; box-shadow:0 2px 8px rgba(0,0,0,0.4);}
      .wrap{position:relative;}
      .target{position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); z-index:1; font-size:36px; pointer-events:none; opacity:0.7;}
      #listBtn{margin-top:10px; display:flex; flex-wrap:wrap; gap:8px;}
      .hpBtn{background:#1a1a1a; color:#00ff00; border:1px solid #00ff00; padding:10px 16px; border-radius:20px; cursor:pointer; font-weight:bold; font-size:14px;}
      .hpBtn:hover{background:#00ff00; color:black;}
      .infoBox{background:#f0f0f0; padding:12px; border-radius:10px; margin-top:10px; font-family:monospace; font-size:14px; min-height:50px;}
      .orbitBar{width:100%; height:8px; background:#ddd; border-radius:4px; margin-top:8px; overflow:hidden;}
      .orbitFill{height:100%; width:0%; background:#00ff00; transition:width 0.3s;}
    </style>
    <div class="wrap">
      <div class="hud" id="hud">DRONE: STANDBY<br>Menunggu data...</div>
      <div class="zoomBtn">
        <button onclick="map.zoomIn()">+</button>
        <button onclick="map.zoomOut()">-</button>
        <button onclick="zoomMax()" title="Zoom Maksimal">🎯</button>
      </div>
      <div class="target">⊕</div>
      <div id="map"></div>
      <button class="btn" onclick="startPatroli()">▶️ MULAI PATROLI DRONE</button>
    </div>
    <div id="listBtn"></div>
    <div class="infoBox" id="infoBox">Klik tombol ijo jeneng nang nduwur gawe ndelok lokasi valid-e.</div>
    <div class="orbitBar"><div class="orbitFill" id="orbitFill"></div></div>
    <div id="orbitText" style="font-family:monospace; font-size:13px; margin-top:4px;">ORBIT: 0% - 0° / 180° | ZOOM: MAKSIMAL 16</div>
    <script>
    const BIN_ID = "6aeeda8bac6210605a74a7b5";
    const API_KEY = "$2a$10$LqQMOcUMXjbfZswzJUFrReGYD5dloL2gTCOLRwT17Oo96mUzr7.aO";
    const map = new maplibregl.Map({
      container: 'map',
      style: {
        version: 8,
        sources: {
          sat: { type: 'raster', tiles: ['https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'], tileSize: 256 },
          terrain: { type: 'raster-dem', tiles: ['https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png'], encoding: 'terrarium', tileSize: 256 }
        },
        layers: [{ id: 'sat', type: 'raster', source: 'sat' }],
        terrain: { source: 'terrain', exaggeration: 1.2 }
      },
      center: [118.0, -2.5], zoom: 4, pitch: 0, bearing: 0,
      maxZoom: 16.5, minZoom: 2,
      fadeDuration: 500, maxTileCacheSize: 500, renderWorldCopies: false
    });
    map.addControl(new maplibregl.NavigationControl());
    let points = [];
    let sedangTerbang = false;
    let stopOrbit = false;
    let targetAktif = null;
    function zoomMax(){
      if(targetAktif){ map.easeTo({center:[targetAktif.lon, targetAktif.lat], zoom: 16, pitch: 65, duration: 1200}); }
      else if(points.length>0){ map.easeTo({center:[points[0].lon, points[0].lat], zoom: 16, pitch: 65, duration: 1200}); }
    }
    fetch("https://api.jsonbin.io/v3/b/" + BIN_ID + "/latest", {headers: {"X-Master-Key": API_KEY}})
    .then(r=>r.json()).then(j=>{
      let data = j.record || {};
      while(data.record){ data = data.record; }
      let listDiv = document.getElementById('listBtn');
      let kicked = data._kicked || [];
      for(let k in data){
        if(k === "_kicked") continue;
        if(kicked.includes(k)) continue;
        if(data[k] && data[k].lat){
          let p = {nama:k, lat:data[k].lat, lon:data[k].lon, waktu:data[k].waktu};
          points.push(p);
          let marker = new maplibregl.Marker({color:'red', draggable:false}).setLngLat([p.lon, p.lat]).setPopup(new maplibregl.Popup({closeOnClick:true}).setHTML(
  "<b>"+p.nama+"</b><br>LOKASI VALID<br>Lat: "+p.lat+"<br>Lon: "+p.lon+"<br>Waktu: "+p.waktu+
  "<br><br>"+
  "<a href='https://www.google.com/maps/dir/?api=1&destination="+p.lat+","+p.lon+"' target='_blank' style='display:block;background:#1a73e8;color:#fff;text-align:center;padding:12px;border-radius:20px;text-decoration:none;font-weight:bold;font-size:15px;margin-bottom:8px;'>🧭 RUTE KE SINI - GOOGLE MAPS</a>"+
  "<a href='https://www.google.com/maps/search/?api=1&query="+p.lat+","+p.lon+"' target='_blank' style='display:block;background:#fff;color:#1a73e8;border:1px solid #1a73e8;text-align:center;padding:10px;border-radius:20px;text-decoration:none;font-weight:bold;font-size:14px;'>📍 BUKA DI GOOGLE MAPS</a>"
)).addTo(map);
          marker.getElement().addEventListener('click', ()=>{ terbangKe(p); });
          let b = document.createElement('button');
          b.className = 'hpBtn';
          b.innerText = '📍 ' + p.nama + ' - TERBANG KE SINI';
          b.onclick = ()=>{ terbangKe(p); };
          listDiv.appendChild(b);
        }
      }
      document.getElementById('hud').innerHTML = "DRONE: SIAP<br>TARGET: "+points.length+" CHECKPOINT<br>ORBIT: 180° / 15 DETIK | ZOOM: 16 MAKSIMAL";
    });
    function sleep(ms){ return new Promise(r=>setTimeout(r,ms)); }
    async function orbit360(p){
      stopOrbit = false;
      let startBearing = map.getBearing();
      let totalDerajat = 180;
      let durasi = 15000;
      let startTime = performance.now();
      document.getElementById('orbitFill').style.width = "0%";
      return new Promise((resolve)=>{
        function frame(now){
          if(stopOrbit){ resolve(); return; }
          let elapsed = now - startTime;
          let progress = Math.min(elapsed / durasi, 1);
          let eased = progress < 0.1 ? progress * progress * 10 : progress < 0.9 ? 0.1 + (progress - 0.1) * 1.05 : 1 - Math.pow(1 - progress, 2);
          let derajat = totalDerajat * eased;
          let bearingBaru = startBearing + derajat;
          map.setBearing(bearingBaru);
          document.getElementById('orbitFill').style.width = (progress * 100) + "%";
          document.getElementById('orbitText').innerHTML = "ORBIT: " + Math.floor(progress*100) + "% - " + Math.floor(derajat) + "° / 180° - " + p.nama + " | ZOOM: 16 MAKSIMAL";
          document.getElementById('hud').innerHTML = "DRONE: ORBIT - MEMANTAU<br>CHECKPOINT: " + p.nama + "<br>PUTARAN: " + Math.floor(derajat) + "° / 180°<br>ALT: 120m | ZOOM 16 | STABIL";
          if(progress < 1){ requestAnimationFrame(frame); } else { document.getElementById('orbitText').innerHTML = "ORBIT SELESAI - 180° - " + p.nama; resolve(); }
        }
        requestAnimationFrame(frame);
      });
    }
    async function terbangKe(p){
      if(sedangTerbang) return;
      sedangTerbang = true;
      stopOrbit = true;
      targetAktif = p;
      await sleep(200);
      document.getElementById('hud').innerHTML = "DRONE: TERBANG...<br>TARGET: "+p.nama+"<br>ALT: 120m | ZOOM 16 MAKSIMAL";
      document.getElementById('infoBox').innerHTML = "<b>LOKASI VALID - "+p.nama+"</b><br>Lat: "+p.lat+"<br>Lon: "+p.lon+"<br>Waktu: "+p.waktu;
      map.flyTo({center:[p.lon, p.lat], zoom: 19, pitch: 65, bearing: 0, duration: 4000, essential:true, curve: 1.05, speed: 0.5});
      await sleep(4300);
      document.getElementById('hud').innerHTML = "DRONE: STABILISASI...<br>Loading peta satelit...";
      await sleep(1200);
      await orbit360(p);
      sedangTerbang = false;
    }
    async function startPatroli(){
      if(points.length===0){ alert("Belum ada HP online!"); return; }
      if(sedangTerbang) return;
      sedangTerbang = true;
      for(let i=0; i<points.length; i++){
        let p = points[i];
        targetAktif = p;
        document.getElementById('hud').innerHTML = "DRONE: TERBANG...<br>TARGET "+(i+1)+"/"+points.length+": "+p.nama;
        document.getElementById('infoBox').innerHTML = "<b>LOKASI VALID - "+p.nama+"</b><br>Lat: "+p.lat+"<br>Lon: "+p.lon+"<br>Waktu: "+p.waktu;
        map.flyTo({center:[p.lon, p.lat], zoom: 16, pitch: 65, bearing: 0, duration: 4000, essential:true, curve: 1.05, speed: 0.5});
        await sleep(4300);
        await sleep(1200);
        await orbit360(p);
        await sleep(500);
      }
      document.getElementById('hud').innerHTML = "DRONE: PATROLI SELESAI<br>Semua "+points.length+" Checkpoint Terpantau - Orbit 180° | Zoom 16";
      map.flyTo({center:[118.0, -2.5], zoom: 4, pitch: 0, bearing: 0, duration: 3000});
      sedangTerbang = false;
    }
    </script>
    """
    st.components.v1.html(drone_html, height=820)

else:
    st.title("📻 RADIO KANCIL FM - STUDIO FM")
    users, kicked = ambil()
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("🔄 REFRESH", use_container_width=True):
            st.rerun()
    with c2:
        if st.button("🔍 ZOOM MAKSIMAL", use_container_width=True):
            st.session_state["zoom_max"] = True
            st.rerun()
    with c3:
        if st.button("🗑️ KELUARKAN SEMUA", use_container_width=True):
            kicked_baru = list(set(kicked + list(users.keys())))
            simpan({}, kicked_baru)
            st.rerun()
    with c4:
        if st.button("🔗 BUAT LINK BARU (RESET)", use_container_width=True):
            simpan({}, [])
            st.rerun()
    st.info(f"Online: {len(users)} | Di-kick: {len(kicked)} | Zoom: MAKSIMAL 16")
    if kicked:
        st.write("Di-kick: " + ", ".join(kicked))
    if users:
        import folium
        from streamlit_folium import st_folium
        first = list(users.values())[0]
        tengah = [first["lat"], first["lon"]] if users else [-2.5, 118.0]
        zoom_awal = 16 if users else 5
        if st.session_state.get("zoom_max"):
            zoom_awal = 16
        m = folium.Map(location=tengah, zoom_start=zoom_awal, max_zoom=20, min_zoom=2, tiles="Esri.WorldImagery", zoom_control=True)
        for n, v in users.items():
            folium.Marker([v["lat"], v["lon"]], popup=f"<b>{n}</b><br>{v.get('waktu','')}<br>Lat: {v['lat']}<br>Lon: {v['lon']}", tooltip=n, icon=folium.Icon(color="red", icon="eye-open")).add_to(m)
            folium.Circle([v["lat"], v["lon"]], radius=20, color="red", fill=True, fill_opacity=0.3).add_to(m)
            folium.CircleMarker([v["lat"], v["lon"]], radius=8, color="yellow", fill=True, fill_color="yellow").add_to(m)
        st_folium(m, width=1000, height=600, key="peta_max")
    st.markdown("### 📋 DAFTAR - KELUARKAN TEKO LAPTOP")
    for n, v in users.items():
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.write(f"🟢 **{n}** | {v.get('waktu','')} | {v['lat']:.6f}, {v['lon']:.6f}")
        with col2:
            if st.button(f"🔍 ZOOM", key=f"zoom_{n}", use_container_width=True):
                st.session_state["zoom_max"] = True
                st.rerun()
        with col3:
            if st.button(f"❌ KELUARKAN", key=f"kick_{n}", use_container_width=True):
                users_baru = {k:val for k,val in users.items() if k != n}
                kicked_baru = kicked + [n] if n not in kicked else kicked
                simpan(users_baru, kicked_baru)
                st.rerun()
    st.markdown("---")
    st.markdown("[🚁 MODE DRONE CINEMATIC 3D - ZOOM 16](https://radio-kancil-fm.streamlit.app/?mode=drone)")
    st.code("Link HP: https://radio-kancil-fm.streamlit.app/?mode=user")
