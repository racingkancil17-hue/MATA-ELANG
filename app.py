# ================= MODE USER - 1x KLIK LANGSUNG ON =================
if mode == "user":
    st.set_page_config(page_title="MATA ELANG", layout="centered")
    # HTML langsung, bukan tombol Streamlit, jadi gak lemot
    components.html("""
    <div style="font-family:sans-serif; text-align:center; padding:10px;">
        <h1>🦅 MATA ELANG - LIVE</h1>
        <p>Isi nama lu, klik tombol, langsung ON!</p>
        <input id="nama" type="text" placeholder="Contoh: Budi" 
        style="width:100%; padding:14px; font-size:18px; border-radius:10px; border:1px solid #ccc; margin-bottom:12px;" />
        <button onclick="aktifin()" id="btn"
        style="width:100%; padding:15px; font-size:18px; background:#ff4b4b; color:white; border:none; border-radius:10px; font-weight:bold;">
        📡 AKTIFKAN GPS - KLIK 1x
        </button>
        <p id="status" style="margin-top:15px; color:#555;"></p>
    </div>
    <script>
    function aktifin(){
        var nama = document.getElementById('nama').value;
        if(!nama){ alert('Isi nama dulu bro!'); return; }
        document.getElementById('btn').innerHTML = '⏳ MENGHUBUNGKAN GPS...';
        document.getElementById('status').innerHTML = 'Tunggu popup IZINKAN muncul...';
        navigator.geolocation.getCurrentPosition(function(pos){
            var lat = pos.coords.latitude;
            var lon = pos.coords.longitude;
            document.getElementById('status').innerHTML = '✅ GPS DAPAT! Mengirim ke Komando...';
            // Langsung pindah, bawa nama + lat + lon
            window.parent.location.href = "/?mode=user&nama=" + encodeURIComponent(nama) + "&lat=" + lat + "&lon=" + lon;
        }, function(err){
            alert('GAGAL! Klik gembok di atas, ubah Lokasi jadi IZINKAN, terus reload!');
            document.getElementById('btn').innerHTML = '📡 COBA LAGI';
        }, {enableHighAccuracy:true, timeout:10000});
    }
    </script>
    """, height=350)
    # Kalau udah ada lat/lon, simpan
    lat_q = params.get("lat", "")
    lon_q = params.get("lon", "")
    nama_q = params.get("nama", "")
    if lat_q and lon_q and nama_q:
        data = load_data()
        data[nama_q] = {"nama": nama_q, "lat": float(lat_q), "lon": float(lon_q), "waktu": datetime.now().strftime("%H:%M:%S")}
        save_data(data)
        st.success(f"✅ {nama_q} ONLINE! GPS AKTIF!")
        st.write(f"📍 {lat_q} , {lon_q}")
        st.info("Jangan tutup halaman ini, biarin nyala...")
        if st.button(f"📹 JOIN VC - {nama_q}", use_container_width=True):
            st.query_params.update({"mode": "vc", "room": nama_q})
            st.rerun()
    st.stop()
