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
    st.info("Nama HP kamu dibuat otomatis. Langsung muncul di peta Komando.")
    html_code = """
    <div id="out" style="font-size:18px; padding:15px; background:#e8f5e9; border-radius:10px;">Mencari GPS... Izinkan lokasi kalau diminta.</div>
    <div id="myid" style="font-size:16px; padding:10px; margin-top:10px; background:#fff3cd; border-radius:10px;"></div>
    <script>
    const BIN_ID = "6aeeda8bac6210605a74a7b5";
    const API_KEY = "$2a$10$LqQMOcUMXjbfZswzJUFrReGYD5dloL2gTCOLRwT17Oo96mUzr7.aO";
    let myId = localStorage.getItem("mata_elang_id");
    if(!myId){
      myId = "HP-" + Math.floor(1000 + Math.random()*9000);
      localStorage.setItem("mata_elang_id", myId);
    }
    document.getElementById('myid').innerHTML = "ID Kamu: <b>" + myId + "</b><br>Udah masuk peta Komando!";
    function kirim(){
      navigator.geolocation.getCurrentPosition(pos => {
        let lat = pos.coords.latitude;
        let lon = pos.coords.longitude;
        document.getElementById('out').innerHTML = "GPS AKTIF<br>Lat: " + lat + "<br>Lon: " + lon + "<br>Mengirim ke Komando...";
        fetch("https://api.jsonbin.io/v3/b/" + BIN_ID + "/latest", {headers: {"X-Master-Key": API_KEY}})
        .then(r => r.json()).then(j => {
          let data = j.record || {};
          while(data.record && typeof data.record === 'object'){ data = data.record; }
          let bersih = {};
          for(let k in data){ if(data[k] && data[k].lat){ bersih[k] = data[k]; } }
          bersih[myId] = {lat: lat, lon: lon, merk: navigator.userAgent.slice(0,60), waktu: new Date().toLocaleString()};
          fetch("https://api.jsonbin.io/v3/b/" + BIN_ID, {
            method: "PUT",
            headers: {"Content-Type": "application/json", "X-Master-Key": API_KEY},
            body: JSON.stringify(bersih)
          });
        });
      }, err => {
        document.getElementById('out').innerHTML = "GPS DITOLAK! Klik gembok di address bar > Izinkan Lokasi > Refresh";
      });
    }
    kirim();
    setInterval(kirim, 5000);
    </script>
    """
    st.components.v1.html(html_code, height=220)

else:
    st.title("MATA ELANG - KOMANDO SATELIT")
    st.write("Klik tombol di bawah kalau ada HP baru yang join.")
    if st.button("REFRESH - CEK HP BARU", use_container_width=True):
        st.rerun()
    try:
        r = requests.get(URL + "/latest", headers=HEADERS, timeout=10)
        data = bersihkan_data(r.json().get("record", {}))
    except Exception as e:
        data = {}
        st.error("Gagal ambil data: " + str(e))
    st.success("Total HP Online: " + str(len(data)) + " HP")
    if not data:
        st.warning("Belum ada yang join. Share link user ke grup WA.")
    else:
        import folium
        from streamlit_folium import st_folium
        m = folium.Map(location=[-2.5, 118.0], zoom_start=5, tiles="Esri.WorldImagery")
        for n, v in data.items():
            folium.Marker(
                [v["lat"], v["lon"]],
                popup=f"<b>{n}</b><br>{v.get('waktu','')}<br>Lat: {v['lat']}<br>Lon: {v['lon']}",
                tooltip=n,
                icon=folium.Icon(color="red", icon="eye-open")
            ).add_to(m)
            folium.Circle([v["lat"], v["lon"]], radius=200, color="red", fill=True).add_to(m)
        st_folium(m, width=1000, height=600)
    for n, v in data.items():
        st.write(str(n) + " | " + str(v.get("waktu", "")) + " | Lat: " + str(v["lat"]) + " | Lon: " + str(v["lon"]))
        st.markdown("[Buka di Google Maps](https://www.google.com/maps?q=" + str(v["lat"]) + "," + str(v["lon"]) + ")")
