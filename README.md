# Political-RAG Indonesia

Aplikasi berbasis web untuk ekstraksi informasi politik dari media konten menggunakan Generative AI (RAG).

## Fitur
- **Upload Data**: Mendukung format CSV, Excel, dan TXT.
- **Analisis Insight**: Dashboard sederhana menampilkan statistik dan kata kunci.
- **Chat RAG**: Tanya jawab interaktif dengan dokumen yang diunggah menggunakan OpenAI GPT.
- **Konteks Indonesia**: Didesain untuk data politik Indonesia.

## Instalasi Lokal

1. Clone repositori ini.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Jalankan aplikasi:
   ```bash
   streamlit run app.py
   ```

## Deployment

### Streamlit Community Cloud (Rekomendasi)
Cara termudah untuk men-deploy aplikasi ini adalah menggunakan [Streamlit Community Cloud](https://streamlit.io/cloud).

1. Push kode ini ke GitHub.
2. Login ke Streamlit Cloud dan hubungkan akun GitHub Anda.
3. Pilih repositori dan file utama (`app.py`).
4. Klik **Deploy**.

### Catatan tentang Netlify
Netlify didesain untuk hosting situs statis (HTML/CSS/JS). Aplikasi Streamlit membutuhkan server Python yang berjalan aktif (backend) untuk memproses logika AI dan data. Oleh karena itu, **Netlify tidak dapat men-host aplikasi Streamlit secara langsung** kecuali menggunakan teknik lanjutan (seperti `stlite` yang memiliki keterbatasan dengan library berat seperti ChromaDB).

Disarankan menggunakan Streamlit Community Cloud, Railway, atau Render.
