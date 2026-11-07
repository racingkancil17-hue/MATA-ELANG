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

# ========== 1. HP KANCAMU ==========
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

# ========== 2. DRONE CINEMATIC 3D - IKI SING KOE TAKOKKE! ==========
elif mode == "drone":
    st.title("🦅 MATA ELANG - DRONE CINEMATIC 3D")
    st.write("Diemin 10 detik biar peta ke-load, baru klik tombol ijo jeneng nang ngisor peta!")
    st.markdown("[⬅️ Balik ke KOMANDO](https://mata-elang.streamlit.app/?mode=komando)")
    drone_html = """
    <link href="https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.css" rel="stylesheet" />
    <script src="https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.js"></script>
    <style>
      #map{width:100%; height:600px; border-radius:12px;}
      .hud{position:absolute; top:12px; left:12px; z-index:10; background:rgba(0,0,0,0.55); color:white; padding:10px 14px; border-radius:10px; font-family:monospace; font-size:14px; border:1px solid rgba(255,255,255,0.3);}
      .btn{position:absolute; bottom:18px; left:50%; transform:translateX(-50%); z-index:10; background:#ff0000; color:white; border:none; padding:14px 28px; font-size:18px; font-weight:bold; border-radius:30px; cursor:pointer;}
      .wrap{position:relative;}
      .target{position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); z-index:1; font-size:36px; pointer-events:none; opacity:0.7;}
      #listBtn{margin-top:10px; display:flex; flex-wrap:wrap; gap:8px;}
      .hpBtn{background:#1a1a1a; color:#00ff00; border:1px solid #00ff00; padding:10px 16px; border-radius:20px; cursor:pointer; font-weight:bold; font-size:14px;}
      .hpBtn:hover{background:#00ff00; color:black;}
      .infoBox{background:#f0f0f0; padding:12px; border-radius:10px; margin-top:10px; font-family:monospace; font-size:14px; min-height:50px;}
    </style>
    <div class="wrap">
      <div class="hud" id="hud">DRONE: STANDBY<br>Menunggu data...</div>
      <div class="target">⊕</div>
      <div id="map"></div>
      <button class="btn" onclick="startPatroli()">▶️ MULAI PATROLI DRONE</button>
    </div>
    <div id="listBtn"></div>
    <div class="infoBox" id="infoBox">Klik tombol ijo jeneng nang nduwur gawe ndelok lokasi valid-e.</div>
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
      fadeDuration: 300, maxTileCacheSize: 200
    });
    map.addControl(new maplibregl.NavigationControl());
    let points = [];
    let sedangTerbang = false;
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
          let marker = new maplibregl.Marker({color:'red', draggable:false}).setLngLat([p.lon, p.lat]).setPopup(new maplibregl.Popup({closeOnClick:true}).setHTML("<b>"+p.nama+"</b><br>LOKASI VALID<br>Lat: "+p.lat+"<br>Lon: "+p.lon+"<br>Waktu: "+p.waktu+"<br><a href='https://www.google.com/maps?q="+p.lat+","+p.lon+"' target='_blank'>Buka di Google Maps</a>")).addTo(map);
          marker.getElement().addEventListener('click', ()=>{ terbangKe(p); });
          let b = document.createElement('button');
          b.className = 'hpBtn';
          b.innerText = '📍 ' + p.nama + ' - TERBANG KE SINI';
          b.onclick = ()=>{ terbangKe(p); };
          listDiv.appendChild(b);
        }
      }
      document.getElementById('hud').innerHTML = "DRONE: SIAP<br>TARGET: "+points.length+" CHECKPOINT<br>Klik nama di bawah untuk cek lokasi";
      document.getElementById('infoBox').innerHTML = "Total: "+points.length+" Online. Klik salah satu tombol ijo.";
    });
    function sleep(ms){ return new Promise(r=>setTimeout(r,ms)); }
    async function terbangKe(p){
      if(sedangTerbang) return;
      sedangTerbang = true;
      document.getElementById('hud').innerHTML = "DRONE: TERBANG...<br>TARGET: "+p.nama+"<br>ALT: 350m | SPD: 60 km/j";
      document.getElementById('infoBox').innerHTML = "<b>LOKASI VALID - "+p.nama+"</b><br>Lat: "+p.lat+"<br>Lon: "+p.lon+"<br>Waktu: "+p.waktu+"<br><a href='https://www.google.com/maps?q="+p.lat+","+p.lon+"' target='_blank'>Buka di Google Maps</a>";
      map.flyTo({center:[p.lon, p.lat], zoom: 17, pitch: 60, bearing: 0, duration: 3500, essential:true, curve: 1.1, speed: 0.7});
      await sleep(3800);
      document.getElementById('hud').innerHTML = "DRONE: HOVER - MEMANTAU<br>CHECKPOINT: "+p.nama+"<br>Lat: "+p.lat+"<br>Lon: "+p.lon+"<br>STATUS: STABIL - MENGAMATI...";
      map.easeTo({bearing: 25, pitch: 65, duration: 8000, easing: t=>t*(2-t)});
      await sleep(8200);
      sedangTerbang = false;
    }
    async function startPatroli(){
      if(points.length===0){ alert("Belum ada HP online!"); return; }
      if(sedangTerbang) return;
      sedangTerbang = true;
      for(let i=0; i<points.length; i++){
        let p = points[i];
        document.getElementById('hud').innerHTML = "DRONE: TERBANG...<br>TARGET "+(i+1)+"/"+points.length+": "+p.nama+"<br>ALT: 350m | SPD: 60 km/j";
        document.getElementById('infoBox').innerHTML = "<b>LOKASI VALID - "+p.nama+"</b><br>Lat: "+p.lat+"<br>Lon: "+p.lon+"<br>Waktu: "+p.waktu;
        map.flyTo({center:[p.lon, p.lat], zoom: 17, pitch: 60, bearing: 0, duration: 3500, essential:true, curve: 1.1, speed: 0.7});
        await sleep(3800);
        document.getElementById('hud').innerHTML = "DRONE: HOVER - MEMANTAU<br>CHECKPOINT: "+p.nama+"<br>Lat: "+p.lat+"<br>Lon: "+p.lon+"<br>STATUS: STABIL...";
        map.easeTo({bearing: 25, pitch: 65, duration: 8000, easing: t=>t*(2-t)});
        await sleep(8200);
        map.easeTo({bearing: 0, duration: 1000});
        await sleep(1100);
      }
      document.getElementById('hud').innerHTML = "DRONE: PATROLI SELESAI<br>Semua "+points.length+" Checkpoint Terpantau";
      map.flyTo({center:[118.0, -2.5], zoom: 4, pitch: 0, bearing: 0, duration: 3000});
      sedangTerbang = false;
    }
    </script>
    """
    st.components.v1.html(drone_html, height=780)

# ========== 3. KOMANDO - LAPTOPMU NGATUR KABEH ==========
else:
    st.title("🦅 MATA ELANG - KOMANDO")
    users, kicked = ambil()
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🔄 REFRESH", use_container_width=True):
            st.rerun()
    with c2:
        if st.button("🗑️ KELUARKAN SEMUA", use_container_width=True):
            kicked_baru = list(set(kicked + list(users.keys())))
            simpan({}, kicked_baru)
            st.rerun()
    with c3:
        if st.button("🔗 BUAT LINK BARU (RESET)", use_container_width=True):
            simpan({}, [])
            st.rerun()
    st.info(f"Online: {len(users)} | Di-kick: {len(kicked)}")
    if kicked:
        st.write("Di-kick: " + ", ".join(kicked))
    if users:
        import folium
        from streamlit_folium import st_folium
        m = folium.Map(location=[-2.5, 118.0], zoom_start=5, tiles="Esri.WorldImagery")
        for n, v in users.items():
            folium.Marker([v["lat"], v["lon"]], popup=n, tooltip=n, icon=folium.Icon(color="red")).add_to(m)
        st_folium(m, width=1000, height=500)
    st.markdown("### 📋 DAFTAR - KELUARKAN TEKO LAPTOP")
    for n, v in users.items():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"🟢 **{n}** | {v.get('waktu','')} | {v['lat']:.5f}, {v['lon']:.5f}")
        with col2:
            if st.button(f"❌ KELUARKAN", key=f"kick_{n}", use_container_width=True):
                users_baru = {k:val for k,val in users.items() if k != n}
                kicked_baru = kicked + [n] if n not in kicked else kicked
                simpan(users_baru, kicked_baru)
                st.rerun()
    st.markdown("---")
    st.markdown("[🚁 BUKA MODE DRONE CINEMATIC 3D](https://mata-elang.streamlit.app/?mode=drone)")
    st.code("Link HP: https://mata-elang.streamlit.app/?mode=user")
