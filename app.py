import streamlit as st
import requests

BIN_ID = "6aeeda8bac6210605a74a7b5"
API_KEY = "$2a$10$LqQMOcUMXjbfZswzJUFrReGYD5dloL2gTCOLRwT17Oo96mUzr7.aO"
URL = "https://api.jsonbin.io/v3/b/" + BIN_ID
HEADERS = {"X-Master-Key": API_KEY, "Content-Type": "application/json"}

st.set_page_config(page_title="MATA ELANG")
params = st.query_params
mode = params.get("mode", "komando")
nama = params.get("nama", "Kancil")
merk = params.get("merk", "OPPO")

def bersihkan_data(data):
    # Kalau data ke-bungkus record dobel, buka bungkusnya
    while isinstance(data, dict) and "record" in data and isinstance(data["record"], dict):
        data = data["record"]
    # Buang yang bukan HP (yang gak ada lat/lon)
    bersih = {}
    if isinstance(data, dict):
        for k, v in data.items():
            if isinstance(v, dict) and "lat" in v and "lon" in v:
                bersih[k] = v
    return bersih

if mode == "user":
    st.title("MATA ELANG - " + nama)
    st.success("Halo " + nama + " | HP: " + merk)
    st.info("Biarin halaman ini NYALA. Jangan di-close. GPS jalan sendiri tiap 5 detik.")
    html_code = """
    <div id="out" style="font-size:18px; padding:10px; background:#e8f5e9; border-radius:10px;">Mencari GPS... Izinkan lokasi kalau diminta.</div>
    <script>
    const BIN_ID = "6aeeda8bac6210605a74a7b5";
    const API_KEY = "$2a$10$LqQMOcUMXjbfZswzJUFrReGYD5dloL2gTCOLRwT17Oo96mUzr7.aO";
    const NAMA = "%s";
    const MERK = "%s";
    function kirim(){
      navigator.geolocation.getCurrentPosition(pos => {
        let lat = pos.coords.latitude;
        let lon = pos.coords.longitude;
        document.getElementById('out').innerHTML = "GPS AKTIF<br>Lat: " + lat + "<br>Lon: " + lon + "<br>Mengirim ke Komando...";
        fetch("https://api.jsonbin.io/v3/b/" + BIN_ID + "/latest", {headers: {"X-Master-Key": API_KEY}})
        .then(r => r.json()).then(j => {
          let data = j.record || {};
          while(data.record && typeof data.record === 'object'){ data = data.record; }
          // Buang yang rusak
          let bersih = {};
          for(let k in data){ if(data[k] && data[k].lat){ bersih[k] = data[k]; } }
          bersih[NAMA] = {lat: lat, lon: lon, merk: MERK, waktu: new Date().toLocaleString()};
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
    """ % (nama, merk)
    st.components.v1.html(html_code, height=180)

else:
    st.title("MATA ELANG - KOMANDO")
    if st.button("REFRESH SEKARANG"):
        st.rerun()
    st.divider()
    st.subheader("Tambah HP Baru")
    new_nama = st.text_input("Nama HP Baru, contoh: Budi", "")
    new_merk = st.text_input("Merk HP, contoh: Vivo", "")
    if new_nama:
        link_baru = "https://mata-elang.streamlit.app/?mode=user&nama=" + new_nama.replace(" ", "%20") + "&merk=" + new_merk.replace(" ", "%20")
        st.success("Kirim link ini ke HP " + new_nama + ":")
        st.code(link_baru)
    st.divider()
    try:
        r = requests.get(URL + "/latest", headers=HEADERS, timeout=10)
        raw = r.json().get("record", {})
        data = bersihkan_data(raw)
    except Exception as e:
        data = {}
        st.error("Gagal ambil data: " + str(e))
    if not data:
        st.warning("Belum ada data. Buka link HP dulu, biarin 10 detik, baru Refresh di sini.")
    if data:
        all_lat = []
        all_lon = []
        for n, v in data.items():
            all_lat.append(v["lat"])
            all_lon.append(v["lon"])
        st.map(data={"lat": all_lat, "lon": all_lon})
    for n, v in data.items():
        st.success(str(n) + " | " + str(v.get("merk", "")) + " | " + str(v.get("waktu", "")))
        st.write("Lat: " + str(v["lat"]) + " | Lon: " + str(v["lon"]))
        st.markdown("[Buka di Google Maps](https://www.google.com/maps?q=" + str(v["lat"]) + "," + str(v["lon"]) + ")")
