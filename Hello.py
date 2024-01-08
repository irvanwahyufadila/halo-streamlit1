# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
import numpy as np
import pandas as pd

if 'clicked' not in st.session_state:
    st.session_state.clicked = False

L = np.array(['benefit','benefit','benefit','cost','cost'])

W = np.array([0.3, 0.2, 0.2, 0.15, 0.15])

def click_button():
    st.session_state.clicked = True

def sample_topsis(values, label):
    if not values.shape[0] == label.shape[0]:
        st.write('Jumlah kriteria dan label tidak sama')
        return

    norm_value = []

    for i in range(values.shape[0]):
        if label[i] == 'benefit':
            norm_c = values[i] / np.sqrt(np.sum(values[i]**2))
        elif label[i] == 'cost':
            norm_c = np.sqrt(np.sum(values[i]**2)) / values[i]

        norm_value.append(norm_c)

    norm_all = np.transpose(norm_value)
    return norm_all

def calculate_topsis(values, weight):
    if not values.shape[0] == weight.shape[0]:
        print('Jumlah kriteria dan bobot tidak sama')
        return

    alt_crit_value = []
    all_value = []
    all_topsis = []

    values = np.transpose(values)

    for i in range(values.shape[0]):
        for j in range(values[i].shape[0]):
            val = values[i][j] * weight[j]
            alt_crit_value.append(val)

        all_value.append(alt_crit_value)
        alt_crit_value = []

        topsis = np.sqrt(np.sum(np.array(all_value)**2))
        all_topsis.append(topsis)
        all_value = []

    return all_topsis

def ranking(vector):
    temp = vector.argsort()
    ranks = np.empty_like(temp)
    ranks[temp] = np.arange(len(vector))

    return len(vector) - ranks

def run():
    st.set_page_config(
        page_title="Implementasi TOPSIS",
        page_icon="👋",
    )

    st.title("Metode TOPSIS")
    st.write("Irvan Wahyu Fadila.")

    st.markdown(
        """
        Metode Technique for Order of Preference by Similarity to Ideal Solution (TOPSIS) merupakan salah satu metode dalam Sistem Pendukung Keputusan yang digunakan untuk pemilihan alternatif terbaik. Metode ini mempertimbangkan kedekatan suatu alternatif dengan solusi ideal positif dan solusi ideal negatif.
        
        Contoh kasus yang akan diimplementasikan pada aplikasi ini adalah sebagai berikut:

        Sebuah perusahaan akan melakukan rekrutmen kerja terhadap **5 calon pekerja** untuk posisi operator mesin. Posisi yang dibutuhkan hanya **2 orang**. Kriteria seleksi yang digunakan adalah sebagai berikut:

        - Pengalaman kerja (C1), semakin lama pengalaman kerjanya semakin baik
        - Pendidikan (C2), semakin tinggi pendidika terakhirnya semakin baik
        - Usia (C3), semakin dewasa usianya semakin baik
        - Status Perkawinan (C4), yang masih single lebih baik dari pada yang sudah menikah
        - Alamat (C5), yang dekat domisilinya dengan kantor semakin baik.

    """
    )

    st.divider()

    st.write("## Input Nilai Kriteria")

    c1 = st.number_input("Nilai C1 (Pengalaman)", min_value=0.0, max_value=1.0, value=0.0, step=0.1)
    c2 = st.number_input("Nilai C2 (Pendidikan)", min_value=0.0, max_value=1.0, value=0.0, step=0.1)
    c3 = st.number_input("Nilai C3 (Usia)", min_value=0.0, max_value=1.0, value=0.0, step=0.1)
    c4 = st.number_input("Nilai C4 (Status Perkawinan)", min_value=0.0, max_value=1.0, value=0.0, step=0.1)
    c5 = st.number_input("Nilai C5 (Alamat)", min_value=0.0, max_value=1.0, value=0.0, step=0.1)

    if st.button("Simpan", type='primary', on_click=click_button):
        simpanData(c1,c2,c3,c4,c5)
    
    if st.session_state.clicked:
        data = st.session_state.nilai_kriteria
        df = pd.DataFrame(data, columns=('Pengalaman','Pendidikan','Usia','Status Perkawinan','Alamat'))
        st.dataframe(df)

        if st.button("Proses"):
            prosesData()


def simpanData(c1,c2,c3,c4,c5):
    if 'nilai_kriteria' not in st.session_state:
        st.session_state.nilai_kriteria = np.array([[c1,c2,c3,c4,c5]])
    else:
        dataLama = st.session_state.nilai_kriteria
        dataBaru = np.append(dataLama, [[c1,c2,c3,c4,c5]], axis=0)
        st.session_state.nilai_kriteria = dataBaru

def prosesData():
    A = st.session_state.nilai_kriteria

    norm_a = sample_topsis(A, L)
    topsis = calculate_topsis(norm_a, W)
    rank = ranking(np.asarray(topsis))

    st.write("Nilai alternatif:")
    st.dataframe(pd.DataFrame(A, columns=('Pengalaman','Pendidikan','Usia','Status Perkawinan','Alamat')))

    st.write("Normalisasi nilai alternatif:")
    st.dataframe(pd.DataFrame(norm_a, columns=('Pengalaman','Pendidikan','Usia','Status Perkawinan','Alamat')))

    st.write("Perhitungan nilai TOPSIS:")
    st.dataframe(pd.DataFrame(topsis, columns=['Nilai TOPSIS']))

    st.write("Perankingan:")
    st.dataframe(pd.DataFrame(rank, columns=['Peringkat']))


if __name__ == "__main__":
    run()
