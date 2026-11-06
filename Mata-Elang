import streamlit as st
import pandas as pd

st.set_page_config(page_title="MATA ELANG", page_icon="🦅", layout="wide")
st.title("🦅 MATA ELANG - Bandung")
st.caption("Sistem Cek Kendaraan | racingkancil17")

plat = st.text_input("Masukkan Plat Nomor", placeholder="Contoh: D 1234 ABC").upper()
nama = st.text_input("Nama Personil", placeholder="Nama lu")
lokasi = st.selectbox("Lokasi", ["Buah Batu", "Dago", "Cibiru", "Cimahi", "Pasteur", "Lainnya"])

if st.button("🔍 CEK KENDARAAN", use_container_width=True):
    if not plat:
        st.warning("Isi dulu plat-nya bro!")
    else:
        st.success(f"Hasil Cek: {plat}")
        st.write(f"**Personil:** {nama}")
        st.write(f"**Lokasi:** {lokasi}")
        st.write("**Status:** ✅ AMAN - Tidak ada pelanggaran")
        st.balloons()

st.divider()
st.subheader("📋 Riwayat Cek Hari Ini")
data = {"Plat": ["D 1234 ABC", "D 5678 XYZ"], "Lokasi": ["Buah Batu", "Dago"], "Status": ["AMAN", "AMAN"]}
st.table(pd.DataFrame(data))
st.info("Versi HP - Nanti bisa di-upgrade dari laptop kalau udah di rumah")
