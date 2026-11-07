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
        let data = {};
        data[NAMA] = {lat: lat, lon: lon, merk: MERK, waktu: new Date().toLocaleString()};
        fetch("https://api.jsonbin.io/v3/b/" + BIN_ID, {
          method: "PUT",
          headers: {"Content-Type": "application/json", "X-Master-Key": API_KEY},
          body: JSON.stringify({record: data})
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
    try:
        r = requests.get(URL + "/latest", headers=HEADERS, timeout=10)
        j = r.json()
        data = j.get("record", {})
        if data is None:
            data = {}
    except Exception as e:
        data = {}
        st.error("Gagal ambil data: " + str(e))
    if not data:
        st.warning("Belum ada data. Pastikan HP Kancil masih nyala dan GPS aktif.")
    for n, v in data.items():
        st.success(str(n) + " | " + str(v.get("merk", "")) + " | " + str(v.get("waktu", "")))
        st.write("Lat: " + str(v["lat"]) + " | Lon: " + str(v["lon"]))
        st.markdown("[Buka di Google Maps](https://www.google.com/maps?q=" + str(v["lat"]) + "," + str(v["lon"]) + ")")
        st.map(data={"lat": [v["lat"]], "lon": [v["lon"]]})
