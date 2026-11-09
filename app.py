import streamlit as st
import requests

BIN_ID = "6aeeda8bac6210605a74a7b5"
API_KEY = "$2a$10$LqQMOcUMXjbfZswzJUFrReGYD5dloL2gTCOLRwT17Oo96mUzr7.aO"
URL = "https://api.jsonbin.io/v3/b/" + BIN_ID
HEADERS = {"X-Master-Key": API_KEY, "Content-Type": "application/json"}

st.set_page_config(page_title="MATA ELANG", layout="wide")
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

def earth_url(lat, lon):
    return f"https://earth.google.com/web/@{lat},{lon},500a,35y,0h,45t,0r"

if mode == "user":
    st.title("🦅 MATA ELANG - LIVE")
    nama = st.text_input("👤 ISI JENENGMU:", placeholder="Contoh: Budi")
    if not nama:
        st.warning("Isi jenengmu disik!")
        st.stop()
    nama = nama.strip()
    users, kicked = ambil()
    if nama in kicked:
        st.error(f"⛔ {nama} DIKELUARKAN KOMANDO! Tunggu link baru!")
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
          if(kicked.includes(myId)){{ document.getElementById('out').innerHTML = "⛔ KAMU DIKELUARKAN KOMANDO!"; return; }}
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
    st.title("🦅 MATA ELANG - DRONE CINEMATIC 3D")
    st.write("Diemin 10 detik biar peta ke-load, baru klik tombol ijo jeneng nang ngisor peta!")
    st.markdown("[⬅️ Balik ke KOMANDO](https://mata-elang.streamlit.app/?mode=komando)")
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
      .infoBox{background:#f0f0f0; padding:12px; border-radius:10px; margin-top:10px; font-family:monospace; font-size:14px; min-height:60px;}
      .orbitBar{width:100%; height:8px; background:#ddd; border-radius:4px; margin-top:8px; overflow:hidden;}
      .orbitFill{height:100%; width:0%; background:#00ff00; transition:width 0.3s;}
      .earthBtn{display:inline-block; margin:6px 6px 0 0; padding:10px 16px; border-radius:20px; font-weight:bold; font-size:14px; text-decoration:none; color:white;}
      .earthBtn:hover{opacity:0.85; color:white;}
      .maplibregl-marker{cursor:pointer !important; width:32px !important; height:44px !important;}
      .maplibregl-popup-content{font-size:14px; min-width:220px;}
      .popupBtn{display:block; width:100%; margin-top:8px; padding:10px; border:none; border-radius:10px; background:#ff0000; color:white; font-weight:bold; font-size:14px; cursor:pointer;}
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
    <div class="infoBox" id="infoBox">Klik tombol ijo jeneng nang ngisor gawe ndelok lokasi valid-e. Klik 🌍 gawe buka nang Google Earth asli!</div>
    <div class="orbitBar"><div class="orbitFill" id="orbitFill"></div></div>
    <div id="orbitText" style="font-family:monospace; font-size:13px; margin-top:4px;">ORBIT: 0% - 0° / 180° | ZOOM: 18 HALUS | KLIK PIN / TOMBOL IJO ISO!</div>
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
        terrain: { source: 'terrain', exaggeration: 0.8 }
      },
      center: [118.0, -2.5], zoom: 4, pitch: 0, bearing: 0,
      maxZoom: 18.5, minZoom: 2,
      fadeDuration: 500, maxTileCacheSize: 500, renderWorldCopies: false
    });
    map.addControl(new maplibregl.NavigationControl());
    let points = [];
    let sedangTerbang = false;
    let stopOrbit = false;
    let targetAktif = null;
    function zoomMax(){
      if(targetAktif){ map.easeTo({center:[targetAktif.lon, targetAktif.lat], zoom: 18, pitch: 60, duration: 2000}); }
      else if(points.length>0){ map.easeTo({center:[points[0].lon, points[0].lat], zoom: 18, pitch: 60, duration: 2000}); }
    }
    function linkEarth(p){ return "https://earth.google.com/web/@" + p.lat + "," + p.lon + ",500a,35y,0h,45t,0r"; }
    function linkMaps(p){ return "https://www.google.com/maps/search/?api=1&query=" + p.lat + "," + p.lon; }
    function linkStreet(p){ return "https://www.google.com/maps/@?api=1&map_action=pano&viewpoint=" + p.lat + "," + p.lon; }
    function updateInfoBox(p){
      document.getElementById('infoBox').innerHTML = "<b>LOKASI VALID - "+p.nama+"</b><br>Lat: "+p.lat+"<br>Lon: "+p.lon+"<br>Waktu: "+p.waktu +
      "<br><a class='earthBtn' style='background:#4285F4' target='_blank' href='"+linkEarth(p)+"'>🌍 BUKA DI GOOGLE EARTH</a>" +
      "<a class='earthBtn' style='background:#34A853' target='_blank' href='"+linkMaps(p)+"'>🗺️ BUKA DI GOOGLE MAPS</a>" +
      "<a class='earthBtn' style='background:#FBBC05; color:black' target='_blank' href='"+linkStreet(p)+"'>👀 STREET VIEW</a>";
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
          let el = document.createElement('div');
          el.style.width = '36px'; el.style.height = '48px'; el.style.background = 'red'; el.style.borderRadius = '50% 50% 50% 0'; el.style.transform = 'rotate(-45deg)'; el.style.border = '3px solid white'; el.style.boxShadow = '0 4px 10px rgba(0,0,0,0.5)'; el.style.cursor = 'pointer';
          el.style.display = 'flex'; el.style.alignItems = 'center'; el.style.justifyContent = 'center';
          el.innerHTML = '<div style="transform:rotate(45deg); color:white; font-weight:bold; font-size:16px;">📍</div>';
          let popupHtml = "<b>"+p.nama+"</b><br>LOKASI VALID<br>Lat: "+p.lat+"<br>Lon: "+p.lon+"<br>Waktu: "+p.waktu +
            "<button class='popupBtn' onclick=\\"window.terbangDariPopup('"+p.nama+"')\\">🚁 TERBANG KE SINI - ZOOM 18</button>" +
            "<a class='earthBtn' style='background:#4285F4; display:block; text-align:center; margin-top:8px' target='_blank' href='"+linkEarth(p)+"'>🌍 BUKA DI GOOGLE EARTH</a>";
          let marker = new maplibregl.Marker({element: el, draggable:false}).setLngLat([p.lon, p.lat]).setPopup(new maplibregl.Popup({closeOnClick:true, offset: 25}).setHTML(popupHtml)).addTo(map);
          el.addEventListener('click', (e)=>{ e.stopPropagation(); terbangKe(p); });
          marker.getElement().addEventListener('click', ()=>{ terbangKe(p); });
          let b = document.createElement('button');
          b.className = 'hpBtn';
          b.innerText = '📍 ' + p.nama + ' - TERBANG KE SINI';
          b.onclick = ()=>{ terbangKe(p); };
          listDiv.appendChild(b);
        }
      }
      document.getElementById('hud').innerHTML = "DRONE: SIAP<br>TARGET: "+points.length+" CHECKPOINT<br>ORBIT: 180° / 25 DETIK | ZOOM: 18 HALUS | PIN ISO DIKLIK!";
      window.terbangDariPopup = function(nama){
        let p = points.find(x => x.nama === nama);
        if(p) terbangKe(p);
      };
    });
    function sleep(ms){ return new Promise(r=>setTimeout(r,ms)); }
    async function orbit360(p){
      stopOrbit = false;
      let startBearing = map.getBearing();
      let totalDerajat = 180;
      let durasi = 25000;
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
          document.getElementById('orbitText').innerHTML = "ORBIT: " + Math.floor(progress*100) + "% - " + Math.floor(derajat) + "° / 180° - " + p.nama + " | ZOOM: 18 HALUS";
          document.getElementById('hud').innerHTML = "DRONE: ORBIT - MEMANTAU<br>CHECKPOINT: " + p.nama + "<br>PUTARAN: " + Math.floor(derajat) + "° / 180°<br>ALT: 120m | ZOOM 18 | STABIL";
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
      await sleep(300);
      document.getElementById('hud').innerHTML = "DRONE: TERBANG...<br>TARGET: "+p.nama+"<br>ALT: 120m | ZOOM 18 HALUS";
      updateInfoBox(p);
      map.flyTo({center:[p.lon, p.lat], zoom: 18, pitch: 60, bearing: 0, duration: 6000, essential:true, curve: 1.2, speed: 0.4});
      await sleep(6500);
      document.getElementById('hud').innerHTML = "DRONE: STABILISASI...<br>Loading peta satelit...";
      await sleep(1500);
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
        updateInfoBox(p);
        map.flyTo({center:[p.lon, p.lat], zoom: 18, pitch: 60, bearing: 0, duration: 6000, essential:true, curve: 1.2, speed: 0.4});
        await sleep(6500);
        await sleep(1500);
        await orbit360(p);
        await sleep(500);
      }
      document.getElementById('hud').innerHTML = "DRONE: PATROLI SELESAI<br>Semua "+points.length+" Checkpoint Terpantau - Orbit 180° | Zoom 18";
      map.flyTo({center:[118.0, -2.5], zoom: 4, pitch: 0, bearing: 0, duration: 3000});
      sedangTerbang = false;
    }
    </script>
    """
    st.components.v1.html(drone_html, height=980)

else:
    st.title("🦅 MATA ELANG - KOMANDO")
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
    st.info(f"Online: {len(users)} | Di-kick: {len(kicked)} | Zoom: 18 HALUS")
    if kicked:
        st.write("Di-kick: " + ", ".join(kicked))
    if users:
        import folium
        from streamlit_folium import st_folium
        first = list(users.values())[0]
        tengah = [first["lat"], first["lon"]] if users else [-2.5, 118.0]
        zoom_awal = 18 if users else 5
        if st.session_state.get("zoom_max"):
            zoom_awal = 18
        m = folium.Map(location=tengah, zoom_start=zoom_awal, max_zoom=19, min_zoom=2, tiles="Esri.WorldImagery", zoom_control=True)
        for n, v in users.items():
            popup_html = f"<b>{n}</b><br>{v.get('waktu','')}<br>Lat: {v['lat']}<br>Lon: {v['lon']}<br><a target='_blank' href='{earth_url(v['lat'], v['lon'])}'>🌍 BUKA DI GOOGLE EARTH</a><br><a target='_blank' href='https://www.google.com/maps/search/?api=1&query={v['lat']},{v['lon']}'>🗺️ GOOGLE MAPS</a>"
            folium.Marker([v["lat"], v["lon"]], popup=popup_html, tooltip=n, icon=folium.Icon(color="red", icon="eye-open")).add_to(m)
            folium.Circle([v["lat"], v["lon"]], radius=20, color="red", fill=True, fill_opacity=0.3).add_to(m)
            folium.CircleMarker([v["lat"], v["lon"]], radius=8, color="yellow", fill=True, fill_color="yellow").add_to(m)
        st_folium(m, width=1000, height=600, key="peta_max")
    st.markdown("### 📋 DAFTAR - KELUARKAN TEKO LAPTOP")
    for n, v in users.items():
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        with col1:
            st.write(f"🟢 **{n}** | {v.get('waktu','')} | {v['lat']:.6f}, {v['lon']:.6f}")
        with col2:
            st.link_button("🌍 EARTH", earth_url(v['lat'], v['lon']), use_container_width=True)
        with col3:
            if st.button(f"🔍 ZOOM", key=f"zoom_{n}", use_container_width=True):
                st.session_state["zoom_max"] = True
                st.rerun()
        with col4:
            if st.button(f"❌ KELUARKAN", key=f"kick_{n}", use_container_width=True):
                users_baru = {k:val for k,val in users.items() if k != n}
                kicked_baru = kicked + [n] if n not in kicked else kicked
                simpan(users_baru, kicked_baru)
                st.rerun()
    st.markdown("---")
    st.markdown("[🚁 BUKA MODE DRONE CINEMATIC 3D - ZOOM 18](https://mata-elang.streamlit.app/?mode=drone)")
    st.code("Link HP: https://mata-elang.streamlit.app/?mode=user")
