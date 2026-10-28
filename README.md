# 🌤️ Prediksi Kualitas Udara (ISPU) Jakarta & Dashboard Interaktif

## 📌 Ringkasan Eksekutif
Proyek ini bertujuan untuk memprediksi Indeks Standar Pencemar Udara (ISPU) di DKI Jakarta untuk 1–3 hari ke depan. Polusi udara adalah masalah kesehatan publik yang kritis; kemampuan untuk memprediksi kualitas udara di masa depan memungkinkan masyarakat dan pemerintah untuk mengambil tindakan preventif (seperti membatasi aktivitas luar ruangan atau menerapkan rekayasa lalu lintas).

Proyek ini membandingkan tiga pendekatan *time-series forecasting* dan menghasilkan sebuah **Dashboard Interaktif (Streamlit)** yang dapat digunakan oleh pengguna awam untuk melihat prediksi.

**Hasil Utama:**
- Model **XGBoost dengan *Lag Features*** terbukti sebagai model yang paling superior dibandingkan baseline Naive dan Prophet.
- Berdasarkan evaluasi pada data uji, XGBoost menghasilkan **MAE (Mean Absolute Error)** terendah, yang berarti prediksi model paling dekat dengan nilai ISPU aktual.
- Hasil akhir dikemas dalam Dashboard Streamlit yang dapat diakses secara publik.

---

## 📊 Data & Metodologi

### 1. Sumber Data
- **Dataset:** Air Quality Index in Jakarta (2010-2025).
- **Sumber:** [Kaggle - Satu Data Jakarta](https://www.kaggle.com/datasets/senadu34/air-quality-index-in-jakarta-2010-2021).
- Data berisi rekaman harian ISPU dari 5 Stasiun Pemantauan Kualitas Udara (SPKU) di Jakarta. Pada proyek ini, data diagregasi (dirata-ratakan) per hari untuk mendapatkan representasi ISPU harian DKI Jakarta.

### 2. Feature Engineering (Rekayasa Fitur)
Untuk memprediksi masa depan, model Machine Learning membutuhkan konteks masa lalu. Kami membuat fitur sebagai berikut:
- **Lag Features:** Nilai ISPU 1 hari (`lag1`), 2 hari (`lag2`), 3 hari (`lag3`), dan 7 hari (`lag7`) sebelumnya.
- **Rolling Mean:** Rata-rata ISPU 7 hari terakhir untuk menangkap tren jangka pendek.
- **Fitur Kalender:** Hari dalam seminggu (`dayofweek`), Bulan (`month`), dan Hari ke-berapa dalam setahun (`dayofyear`) untuk menangkap pola musiman.

### 3. Model yang Dibandingkan
Kami mengevaluasi tiga pendekatan:
1.  **Naive Baseline:** Memprediksi ISPU besok sama dengan ISPU hari ini. (Model pembanding standar).
2.  **Prophet (Meta):** Model *additive* yang sangat baik dalam menangkap musiman dan tren, dengan tambahan regresi `lag1`.
3.  **XGBoost Regressor:** Algoritma *gradient boosting* yang sangat kuat dalam menemukan pola non-linear pada data tabular dan fitur lag.

### 4. Metrik Evaluasi
Karena ini adalah regresi (memprediksi angka kontinu), kami menggunakan:
- **MAE (Mean Absolute Error):** Rata-rata selisih absolut antara prediksi dan aktual. (Semakin kecil, semakin baik).
- **RMSE (Root Mean Squared Error):** Memberikan penalti lebih besar pada error yang sangat jauh.

### 5. Strategi Validasi
Kami **tidak menggunakan random split** karena akan menyebabkan *data leakage* (kebocoran data masa depan ke masa lalu). Data dibagi secara kronologis (*Time-Based Split*): 80% data awal untuk *Training*, dan 20% data terakhir untuk *Testing*.

---

## 💡 Temuan Kunci

1.  **XGBoost Sangat Efektif untuk Data Tabular Harian:** Dengan memanfaatkan *lag features*, XGBoost mampu mengungguli Prophet karena algoritma ini sangat baik dalam memetakan hubungan non-linear antar hari (misalnya: jika 3 hari terakhir ISPU naik drastis, besok akan seperti apa).
2.  **Pentingnya Baseline:** Selalu membandingkan model kompleks dengan Naive Baseline sangat penting. Jika Prophet atau XGBoost tidak bisa mengalahkan Naive, berarti ada yang salah dengan data atau fitur kita.
3.  **Visualisasi:** Grafik perbandingan antara nilai aktual vs prediksi (terdapat di notebook) menunjukkan bahwa XGBoost sangat responsif terhadap perubahan tren jangka pendek.

---

## 🖥️ Dashboard Interaktif (Streamlit)

Proyek ini dilengkapi dengan *dashboard* interaktif yang memungkinkan pengguna memasukkan data ISPU beberapa hari terakhir, lalu melihat hasil prediksi 1-3 hari ke depan beserta kategorinya (Baik, Sedang, Tidak Sehat, dll).

🔗 **[https://prediksikualitasudara-jakarta.streamlit.app](#)** 
