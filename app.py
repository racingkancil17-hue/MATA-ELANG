import streamlit as st
import requests

BIN_ID = "6aeeda8bac6210605a74a7b5"
API_KEY = "$2a$10$LqQMOcUMXjbfZswzJUFrReGYD5dloL2gTCOLRwT17Oo96mUzr7.aO"
URL = f"https://api.jsonbin.io/v3/b/{BIN_ID}"
HEADERS = {"X-Master-Key": API_KEY, "Content-Type": "application/json"}

st.set_page_config(page_title="MATA ELANG")
params = st.query_params
mode = params.get("mode", "komando")
nama = params.get("nama", "Kancil")
merk = params.get("merk", "OPPO")

if mode == "user":
    st.title(f"🦅 MATA ELANG - {nama}")
    st.success(f"Halo {nama} | HP: {merk}")
    st.info("Biarin halaman ini NYALA. Jangan di-close. GPS jalan sendiri tiap 5 detik.")
    st.components.v1.html(f"""
    <div id="out" style="font-size:18px; padding:10px; background:#e8f5e9; border-radius:10px;">📍 Mencari GPS... Izinkan lokasi kalau diminta.</div>
    <script>
    const BIN_ID = "{BIN_ID}";
    const API_KEY = "{API_KEY}";
    function kirim(){{
      navigator.geolocation.getCurrentPosition(pos => {{
        let lat = pos.coords.latitude;
        let lon = pos.coords.longitude;
        document.getElementById('out').innerHTML = "✅ GPS AKTIF<br>Lat: " + lat + "<br>Lon: " + lon + "<br>Mengirim ke Komando...";
        fetch("https://api.jsonbin.io/v3/b/" + BIN_ID, {{
          method: "PUT",
          headers: {{"Content-Type": "application/json", "X-Master-Key": API_KEY}},
          body: JSON.stringify({{"record": {{"{nama}": {{"lat": lat, "lon": lon, "merk": "{merk}", "waktu": new Date().toLocaleString()}}}}}})
        }});
      }}, err => {{
        document.getElementById('out').innerHTML = "❌ GPS DITOLAK! Klik gembok di address bar > Izinkan Lokasi > Refresh";
      }});
    }}
    kirim();
    setInterval(kirim, 5000);
    </script>
    """, height=180)

else:
    st.title("🦅 MATA ELANG - KOMANDO")
    # Auto refresh tiap 5 detik, jadi tombol refresh gak perlu diklik lagi
    st.markdown('<meta http-equiv="refresh" content="5">', unsafe_allow_html=True)
    if st.button("🔄 REFRESH SEKARANG"):
        st.rerun()
    try:
        r = requests.get(URL + "/latest", headers=HEADERS, timeout=10)
        data = r.json().get("record", {{}})
    except Exception as e:
        data = {{}}
        st.error(f"Gagal ambil data: {{e}}")
    if not data:
        st.warning("Belum ada data. Pastikan HP Kancil masih nyala dan GPS aktif.")
    for n, v in data.items():
        st.success(f"{n} | {v.get('merk','')} | {v.get('waktu','')}")
        st.write(f"Lat: {v['lat']} | Lon: {v['lon']}")
        st.markdown(f"[📍 Buka di Google Maps](https://www.google.com/maps?q={v['lat']},{v['lon']})")
        st.map(data={{"lat": [v['lat']], "lon": [v['lon']]}})
