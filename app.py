import streamlit as st
import requests

BIN_ID = "6aeeda8bac6210605a74a7b5"
API_KEY = "$2a$10$LqQMOcUMXjbfZswzJUFrReGYD5dloL2gTCOLRwT17Oo96mUzr7.aO"
URL = "https://api.jsonbin.io/v3/b/" + BIN_ID
HEADERS = {"X-Master-Key": API_KEY, "Content-Type": "application/json"}

st.set_page_config(page_title="MATA ELANG", layout="wide")
params = st.query_params
mode = params.get("mode", "komando")

def bersihkan_data(data):
    while isinstance(data, dict) and "record" in data and isinstance(data["record"], dict):
        data = data["record"]
    bersih = {}
    if isinstance(data, dict):
        for k, v in data.items():
            if isinstance(v, dict) and "lat" in v and "lon" in v:
                bersih[k] = v
    return bersih

if mode == "user":
    st.title("MATA ELANG - LIVE")
    st.success("Kamu udah JOIN! Biarin halaman ini NYALA. Jangan di-close.")
    html_code = """
    <div id="out" style="font-size:18px; padding:15px; background:#e8f5e9; border-radius:10px;">Mencari GPS... Izinkan lokasi kalau diminta.</div>
    <div id="myid" style="font-size:16px; padding:10px; margin-top:10px; background:#fff3cd; border-radius:10px;"></div>
    <script>
    const BIN_ID = "6aeeda8bac6210605a74a7b5";
    const API_KEY = "$2a$10$LqQMOcUMXjbfZswzJUFrReGYD5dloL2gTCOLRwT17Oo96mUzr7.aO";
    let myId = localStorage.getItem("mata_elang_id");
    if(!myId){ myId = "HP-" + Math.floor(1000 + Math.random()*9000); localStorage.setItem("mata_elang_id", myId); }
    document.getElementById('myid').innerHTML = "ID Kamu: <b>" + myId + "</b><br>Udah masuk peta Komando!";
    function kirim(){
      navigator.geolocation.getCurrentPosition(pos => {
        let lat = pos.coords.latitude; let lon = pos.coords.longitude;
        document.getElementById('out').innerHTML = "GPS AKTIF<br>Lat: " + lat + "<br>Lon: " + lon + "<br>Mengirim ke Komando...";
        fetch("https://api.jsonbin.io/v3/b/" + BIN_ID + "/latest", {headers: {"X-Master-Key": API_KEY}})
        .then(r => r.json()).then(j => {
          let data = j.record || {};
          while(data.record && typeof data.record === 'object'){ data = data.record; }
          let bersih = {};
          for(let k in data){ if(data[k] && data[k].lat){ bersih[k] = data[k]; } }
          bersih[myId] = {lat: lat, lon: lon, merk: navigator.userAgent.slice(0,60), waktu: new Date().toLocaleString()};
          fetch("https://api.jsonbin.io/v3/b/" + BIN_ID, {method: "PUT", headers: {"Content-Type": "application/json", "X-Master-Key": API_KEY}, body: JSON.stringify(bersih)});
        });
      }, err => { document.getElementById('out').innerHTML = "GPS DITOLAK! Klik gembok > Izinkan Lokasi > Refresh"; });
    }
    kirim(); setInterval(kirim, 5000);
    </script>
    """
    st.components.v1.html(html_code, height=220)

elif mode == "drone":
    st.title("MATA ELANG - DRONE CINEMATIC 3D")
    st.write("Buat laporan ke Panglima. Klik MULAI PATROLI, kamera terbang sendiri ke tiap HP.")
    st.warning("Tips Laporan: Klik MULAI PATROLI > langsung Screen Record (Win + G) > kirim videonya ke Panglima.")
    drone_html = """
    <link href="https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.css" rel="stylesheet" />
    <script src="https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.js"></script>
    <style>
      #map{width:100%; height:650px; border-radius:12px;}
      .hud{position:absolute; top:12px; left:12px; z-index:10; background:rgba(0,0,0,0.7); color:#00ff00; padding:10px 14px; border-radius:10px; font-family:monospace; font-size:14px;}
      .hud2{position:absolute; top:12px; right:12px; z-index:10; background:red; color:white; padding:6px 12px; border-radius:20px; font-weight:bold; font-family:sans-serif;}
      .btn{position:absolute; bottom:18px; left:50%; transform:translateX(-50%); z-index:10; background:#ff0000; color:white; border:none; padding:14px 28px; font-size:18px; font-weight:bold; border-radius:30px; cursor:pointer;}
      .wrap{position:relative;}
      .target{position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); z-index:5; font-size:42px; pointer-events:none; opacity:0.8;}
    </style>
    <div class="wrap">
      <div class="hud" id="hud">DRONE: STANDBY<br>TARGET: -<br>ALT: 800m | SPD: 0 km/j</div>
      <div class="hud2">● REC 00:00</div>
      <div class="target">⊕</div>
      <div id="map"></div>
      <button class="btn" onclick="startPatroli()">▶️ MULAI PATROLI DRONE</button>
    </div>
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
        terrain: { source: 'terrain', exaggeration: 1.8 }
      },
      center: [118.0, -2.5], zoom: 4, pitch: 0, bearing: 0
    });
    map.addControl(new maplibregl.NavigationControl());
    let points = [];
    let recSec = 0;
    setInterval(()=>{ recSec++; let m=String(Math.floor(recSec/60)).padStart(2,'0'); let s=String(recSec%60).padStart(2,'0'); document.querySelector('.hud2').innerText = '● REC '+m+':'+s; }, 1000);
    fetch("https://api.jsonbin.io/v3/b/" + BIN_ID + "/latest", {headers: {"X-Master-Key": API_KEY}})
    .then(r=>r.json()).then(j=>{
      let data = j.record || {};
      while(data.record){ data = data.record; }
      for(let k in data){
        if(data[k] && data[k].lat){
          points.push({nama:k, lat:data[k].lat, lon:data[k].lon, waktu:data[k].waktu});
          new maplibregl.Marker({color:'red'}).setLngLat([data[k].lon, data[k].lat]).setPopup(new maplibregl.Popup().setHTML("<b>"+k+"</b><br>"+data[k].waktu)).addTo(map);
        }
      }
      document.getElementById('hud').innerHTML = "DRONE: SIAP<br>TARGET: "+points.length+" CHECKPOINT<br>ALT: 800m | SPD: 0 km/j";
    });
    function sleep(ms){ return new Promise(r=>setTimeout(r,ms)); }
    async function startPatroli(){
      if(points.length===0){ alert("Belum ada HP online!"); return; }
      for(let i=0; i<points.length; i++){
        let p = points[i];
        document.getElementById('hud').innerHTML = "DRONE: TERBANG...<br>TARGET "+(i+1)+"/"+points.length+": "+p.nama+"<br>ALT: 350m | SPD: 85 km/j";
        map.flyTo({center:[p.lon, p.lat], zoom: 16, pitch: 65, bearing: 45, duration: 4500, essential:true});
        await sleep(4700);
        document.getElementById('hud').innerHTML = "DRONE: DI ATAS TARGET<br>CHECKPOINT: "+p.nama+"<br>Lat: "+p.lat+"<br>Lon: "+p.lon+"<br>Waktu: "+p.waktu;
        map.flyTo({center:[p.lon, p.lat], zoom: 18, pitch: 75, bearing: 180, duration: 3000, essential:true});
        await sleep(3500);
      }
      document.getElementById('hud').innerHTML = "DRONE: PATROLI SELESAI<br>Semua "+points.length+" Checkpoint Terpantau<br>Kembali ke Markas...";
      map.flyTo({center:[118.0, -2.5], zoom: 4, pitch: 0, bearing: 0, duration: 4000});
    }
    </script>
    """
    st.components.v1.html(drone_html, height=700)

else:
    st.title("MATA ELANG - KOMANDO SATELIT")
    if st.button("REFRESH - CEK HP BARU", use_container_width=True):
        st.rerun()
    if st.button("🗑️ HAPUS SEMUA DATA TES", use_container_width=True):
        requests.put(URL, headers=HEADERS, json={})
        st.rerun()
    st.markdown("[🚁 BUKA MODE DRONE CINEMATIC 3D](https://mata-elang.streamlit.app/?mode=drone)")
    try:
        r = requests.get(URL + "/latest", headers=HEADERS, timeout=10)
        data = bersihkan_data(r.json().get("record", {}))
    except Exception as e:
        data = {}
        st.error("Gagal ambil data: " + str(e))
    st.success("Total HP Online: " + str(len(data)) + " HP")
    if data:
        import folium
        from streamlit_folium import st_folium
        m = folium.Map(location=[-2.5, 118.0], zoom_start=5, tiles="Esri.WorldImagery")
        for n, v in data.items():
            folium.Marker([v["lat"], v["lon"]], popup=f"<b>{n}</b><br>{v.get('waktu','')}", tooltip=n, icon=folium.Icon(color="red", icon="eye-open")).add_to(m)
            folium.Circle([v["lat"], v["lon"]], radius=200, color="red", fill=True).add_to(m)
        st_folium(m, width=1000, height=600)
    for n, v in data.items():
        st.write(str(n) + " | " + str(v.get("waktu", "")) + " | Lat: " + str(v["lat"]) + " | Lon: " + str(v["lon"]))
