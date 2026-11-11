import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="RADIO KANCIL FM", page_icon="📻", layout="centered")

params = st.query_params
mode = params.get("mode", "user")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {background-color: #0f0f0f;}
[data-testid="stHeader"] {background-color: #0f0f0f;}
h1, h2, h3, p, label, span {color: white !important;}
[data-testid="stAlert"] * {color: black !important;}
.stButton>button {background-color: #FF2D55; color: white; border-radius: 25px; width: 100%; font-weight: bold; font-size: 20px; padding: 15px;}
</style>
""", unsafe_allow_html=True)

# ================= STUDIO FM =================
if mode == "studio":
    st.title("🎙️ STUDIO FM - RADIO KANCIL FM")
    st.write("🔴 LIVE ON AIR - DJ KANCIL Lagi Siaran!")
    st.write("Enteni Sobat Kancil mlebu...")
    st.divider()
    # GPS tracking Sobat Kancil sing mlebu - live nang kene
    components.html("""
    <div style="color:white; font-family:sans-serif; background:#1a1a1a; padding:15px; border-radius:15px;">
    <h3>📍 Sobat Kancil Sing Lagi Online:</h3>
    <p id="lok">Ngenteni sinyal GPS...</p>
    <script>
    function update(){ navigator.geolocation.getCurrentPosition(p=>{
      document.getElementById('lok').innerHTML = "Lat: "+p.coords.latitude.toFixed(5)+" | Lon: "+p.coords.longitude.toFixed(5);
    });}
    setInterval(update, 3000);
    </script>
    </div>
    """, height=150)

# ================= SOBAT KANCIL - VERSI WINGI =================
else:
    st.title("📻 RADIO KANCIL FM")
    st.subheader("Bareng DJ KANCIL - Bandung")
    st.write("Halo SOBAT KANCIL!")

    # 1. MUSIK BUNYI 18 DETIK - OTOMATIS
    st.write("🎵 **Lagi Muter Jingle Kancil...**")
    # Jingle / musik pembuka
    st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", autoplay=True)

    st.divider()
    st.write("⏳ **Enteni 18 detik, musik e entek, langsung GAS GPS!**")

    # 2. GPS AKTIF - TINGGAL KLIK GAS
    components.html("""
    <div style="text-align:center; font-family:sans-serif;">
      <button onclick="gas()" style="background:#FF2D55; color:white; border:none; padding:18px 40px; border-radius:30px; font-size:20px; font-weight:bold; width:100%;">📍 GAS AKTIFKAN GPS</button>
      <p id="hasil" style="color:white; margin-top:15px; font-size:16px;">Klik GAS, GPS langsung aktif!</p>
      <script>
      function gas(){
        document.getElementById('hasil').innerHTML = "⏳ Lagi golek lokasi mu...";
        navigator.geolocation.getCurrentPosition(
          p => { document.getElementById('hasil').innerHTML = "✅ JOS! GPS AKTIF!<br>Lat: "+p.coords.latitude.toFixed(5)+" | Lon: "+p.coords.longitude.toFixed(5)+"<br><br>🔴 Kowe wes nyambung nang STUDIO FM!"; },
          e => { document.getElementById('hasil').innerHTML = "❌ GPS ditolak. Aktifkan Lokasi nang HP mu disik, trus klik GAS maneh!"; },
          {enableHighAccuracy:true}
        );
      }
      // Otomatis nyoba GPS bar 18 detik
      setTimeout(gas, 18000);
      </script>
    </div>
    """, height=200)

    st.divider()
    st.caption("RADIO KANCIL FM - Radio ne Sobat Kancil")
