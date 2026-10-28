
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import datetime

# Load model
model = joblib.load('xgb_ispu_model.pkl')

st.title("🌤️ Dashboard Prediksi Kualitas Udara Jakarta")
st.write("Aplikasi ini memprediksi ISPU (Indeks Standar Pencemar Udara) 1-3 hari ke depan berdasarkan data historis.")

# Sidebar untuk input data historis terakhir (simulasi)
st.sidebar.header("Input Data Historis Terakhir")
st.sidebar.write("Masukkan 7 nilai ISPU terakhir (hari ini, kemarin, dst):")

# Default values (bisa diubah user)
lag1 = st.sidebar.number_input("ISPU Hari Ini (lag1)", value=85.0)
lag2 = st.sidebar.number_input("ISPU Kemarin (lag2)", value=90.0)
lag3 = st.sidebar.number_input("ISPU 2 Hari Lalu (lag3)", value=80.0)
lag7 = st.sidebar.number_input("ISPU 7 Hari Lalu (lag7)", value=75.0)

# Fitur tambahan
rolling_mean_7 = np.mean([lag1, lag2, lag3, lag7]) # Simplified
today = datetime.date.today()

# Tombol Prediksi
if st.button("Prediksi 1-3 Hari ke Depan"):
    history = [lag7, 0, 0, 0, 0, 0, 0, lag3, lag2, lag1] # Padding kasar untuk simulasi history
    
    predictions = []
    current_date = today
    
    for i in range(1, 4):
        next_date = current_date + datetime.timedelta(days=i)
        
        # Hitung fitur sederhana
        lag_1_val = lag1 if i == 1 else predictions[-1] if predictions else lag1
        lag_2_val = lag2 if i == 1 else (lag1 if i == 2 else predictions[-2] if len(predictions)>=2 else lag1)
        lag_3_val = lag3 if i == 1 else (lag2 if i == 2 else lag1 if i == 3 else lag1)
        
        input_df = pd.DataFrame([{
            'lag1': lag_1_val, 'lag2': lag_2_val, 'lag3': lag_3_val, 'lag7': lag7,
            'rolling_mean_7': (lag_1_val + lag_2_val + lag_3_val + lag7) / 4,
            'dayofweek': next_date.weekday(), 'month': next_date.month, 'dayofyear': next_date.timetuple().tm_yday
        }])
        
        pred = model.predict(input_df)[0]
        predictions.append(pred)
    
    result = pd.DataFrame({
        'Tanggal': [today + datetime.timedelta(days=i) for i in range(1, 4)],
        'Prediksi ISPU': predictions
    })
    
    def kategori(val):
        if val <= 50: return "Baik"
        elif val <= 100: return "Sedang"
        elif val <= 150: return "Tidak Sehat"
        else: return "Sangat Tidak Sehat"
    
    result['Kategori'] = result['Prediksi ISPU'].apply(kategori)
    
    st.subheader("Hasil Prediksi")
    st.dataframe(result.style.format({'Prediksi ISPU': '{:.1f}'}))
    
    st.line_chart(result.set_index('Tanggal')['Prediksi ISPU'])
