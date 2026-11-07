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
        # Pisahke data user vs data kicked
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

# ========== HP KANCAMU - MUNG ISI JENENG TOK ==========
if mode == "user":
    st.title("🦅 MATA ELANG - LIVE")
    nama = st.text_input("👤 ISI JENENGMU:", placeholder="Contoh: Budi")
    if not nama:
        st.warning("Isi jenengmu disik!")
        st.stop()
    nama = nama.strip()
    users, kicked = ambil()
    if nama in kicked:
        st.error(f"⛔ {nama} DIKELUARKAN KOMANDO! Tunggu link baru dari Komando!")
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
          // Nek di-kick, mandek, ojo ngirim maneh
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

# ========== LAPTOPMU - KOMANDO NGATUR KABEH ==========
else:
    st.title("🦅 MATA ELANG - KOMANDO")
    users, kicked = ambil()

    # TOMBOL UTAMA NANG NDUWUR
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🔄 REFRESH", use_container_width=True):
            st.rerun()
    with c2:
        if st.button("🗑️ KELUARKAN SEMUA", use_container_width=True):
            # Kick kabeh sing online saiki
            kicked_baru = list(set(kicked + list(users.keys())))
            simpan({}, kicked_baru)
            st.rerun()
    with c3:
        if st.button("🔗 BUAT LINK BARU (RESET)", use_container_width=True):
            # Resik kabeh + buka blokiran, siap bagi link anyar
            simpan({}, [])
            st.success("Link baru siap! Bagi link HP maneh!")
            st.rerun()

    st.info(f"Online: {len(users)} | Di-kick: {len(kicked)}")
    if kicked:
        st.write("Daftar di-kick: " + ", ".join(kicked))

    # PETA
    if users:
        import folium
        from streamlit_folium import st_folium
        m = folium.Map(location=[-2.5, 118.0], zoom_start=5, tiles="Esri.WorldImagery")
        for n, v in users.items():
            folium.Marker([v["lat"], v["lon"]], popup=n, tooltip=n, icon=folium.Icon(color="red")).add_to(m)
        st_folium(m, width=1000, height=500)

    # DAFTAR + TOMBOL KELUARKAN PER-ORANG - IKI SING KOE PENCET NANG LAPTOP
    st.markdown("### 📋 DAFTAR - KLIK KELUARKAN NANG LAPTOPMU")
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
    st.markdown("**Link HP kancamu (bagi iki nek wes Reset):**")
    st.code("https://mata-elang.streamlit.app/?mode=user")
    st.markdown("[🚁 Mode Drone](https://mata-elang.streamlit.app/?mode=drone)")
