# ===================== WEB VERSION (STREAMLIT) =====================
# Jalankan dengan: streamlit run nama_file.py

import math
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.title("Perhitungan Sudut Theta")

# ===================== INPUT =====================

D_bar = st.number_input("D_bar", value=0.05)
Db = st.number_input("Db", value=0.04)
Ds = st.number_input("Ds", value=0.03)
Wb = st.number_input("Wb", value=0.02)
Ws = st.number_input("Ws", value=0.015)
Wbar = st.number_input("Wbar", value=0.018)
H1 = st.number_input("H1", value=0.01)
Zb = st.number_input("Zb", value=0.1)
fs = st.number_input("f_s", value=0.3)
fb = st.number_input("f_b", value=0.25)
P1 = st.number_input("P1", value=100000.0)
P2 = st.number_input("P2", value=200000.0)

phi = 17.67
phib = 17.67
phis = 17.67

# ===================== FUNGSI =====================

def hitung_K(D_bar, Db, phi, fs):
    phi = math.radians(phi)
    return (D_bar / Db) * ((math.sin(phi) + fs * math.cos(phi)) / (math.cos(phi) - fs * math.sin(phi)))


def hitung_M(Wb, Ws, Wbar, H1, Zb, D_bar, Ds, Db, fs, fb, phi, phib, phis, P1, P2, K):
    phi = math.radians(phi)
    phib = math.radians(phib)
    phis = math.radians(phis)

    term1 = 2 * (H1 / Wb) * (fs / fb) * math.sin(phib) * (K + (D_bar / Db) * (1 / math.tan(phi)))
    term2 = (Ws / Wb) * (fs / fb) * math.sin(phib) * (K + (Ds / Db) * (1 / math.tan(phis)))
    term3 = (Wbar / Wb) * (H1 / Zb) * (1 / fb) * math.sin(phi) * (K + (D_bar / Db) * (1 / math.tan(phi))) * math.log(P2 / P1)

    return term1 + term2 + term3

# ===================== HITUNG =====================

if st.button("Hitung"):
    if D_bar <= Db:
        st.warning("D_bar harus lebih besar dari Db")

    K = hitung_K(D_bar, Db, phi, fs)
    M = hitung_M(Wb, Ws, Wbar, H1, Zb, D_bar, Ds, Db, fs, fb, phi, phib, phis, P1, P2, K)
    theta = math.degrees(math.atan(M / (1 - K)))

    st.success(f"K = {K:.4f}")
    st.success(f"M = {M:.4f}")
    st.success(f"Theta = {theta:.2f}°")

# ===================== GRAFIK =====================

if st.button("Tampilkan Grafik"):
    fs_vals = []
    theta_vals = []

    for i in range(1, 10):
        fs_val = i * 0.1
        K = hitung_K(D_bar, Db, phi, fs_val)
        M = hitung_M(Wb, Ws, Wbar, H1, Zb, D_bar, Ds, Db, fs_val, fb, phi, phib, phis, P1, P2, K)
        theta = math.degrees(math.atan(M / (1 - K)))

        fs_vals.append(fs_val)
        theta_vals.append(theta)

    fig, ax = plt.subplots()
    ax.plot(fs_vals, theta_vals)
    ax.set_xlabel("f_s")
    ax.set_ylabel("Theta")
    ax.set_title("Grafik Theta vs f_s")

    st.pyplot(fig)

# ===================== EXPORT =====================

if st.button("Export ke Excel"):
    data = []

    for i in range(1, 10):
        fs_val = i * 0.1
        K = hitung_K(D_bar, Db, phi, fs_val)
        M = hitung_M(Wb, Ws, Wbar, H1, Zb, D_bar, Ds, Db, fs_val, fb, phi, phib, phis, P1, P2, K)
        theta = math.degrees(math.atan(M / (1 - K)))

        data.append([fs_val, K, M, theta])

    df = pd.DataFrame(data, columns=["f_s", "K", "M", "Theta"])
    st.download_button("Download Excel", df.to_csv(index=False), file_name="theta.csv")

