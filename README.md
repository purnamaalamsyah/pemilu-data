# Political-RAG Indonesia

Aplikasi berbasis web untuk ekstraksi informasi politik dari media konten menggunakan Generative AI (RAG). Aplikasi ini dirancang untuk membantu analis politik, jurnalis, atau peneliti dalam memahami konteks berita politik Indonesia secara cepat dan mendalam.

## Fitur Utama
- **Upload Data Fleksibel**: Mendukung format CSV, Excel, dan TXT (bisa banyak file sekaligus).
- **Dashboard Analisis AI**:
  - Statistik dasar dokumen.
  - Visualisasi kata kunci.
  - **Analisis Mendalam**: Menggunakan AI untuk mengekstrak Sentimen, Tokoh Kunci, dan Isu Utama dari dokumen.
- **Chat RAG (Retrieval-Augmented Generation)**: Tanya jawab interaktif dengan dokumen Anda. Chatbot memahami konteks dokumen yang diunggah.
- **Manajemen Memori**: Menyimpan riwayat percakapan untuk konteks diskusi yang lebih baik.

## Prasyarat
- Python 3.8 - 3.12
- **OpenAI API Key**: Diperlukan untuk mengakses fitur Generative AI.

## Panduan Instalasi & Menjalankan (Lokal)

1. **Clone Repositori**
   ```bash
   git clone <repository-url>
   cd political-rag-app
   ```

2. **Siapkan Environment (Opsional tapi Disarankan)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Untuk Linux/Mac
   # venv\Scripts\activate   # Untuk Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Jalankan Aplikasi**
   ```bash
   streamlit run app.py
   ```
   Aplikasi akan terbuka di browser Anda (biasanya di `http://localhost:8501`).

## Cara Menggunakan

1. **Konfigurasi**: Masukkan OpenAI API Key Anda di sidebar sebelah kiri.
2. **Upload Data**: Unggah file berita/politik (CSV, Excel, TXT). Jika tidak ada file, aplikasi akan menggunakan data sampel.
3. **Analisis**: Buka tab "Dashboard Insight" untuk melihat ringkasan dan menekan tombol "Generate Insight Politik" untuk analisis AI.
4. **Chat**: Buka tab "Chat RAG AI" untuk bertanya tentang dokumen yang diunggah (contoh: "Bagaimana sentimen media terhadap kandidat X?").

## Deployment

### Streamlit Community Cloud (Rekomendasi)
Cara termudah untuk men-deploy aplikasi ini adalah menggunakan [Streamlit Community Cloud](https://streamlit.io/cloud).

1. Push kode ini ke GitHub.
2. Login ke Streamlit Cloud dan hubungkan akun GitHub Anda.
3. Pilih repositori dan file utama (`app.py`).
4. Klik **Deploy**.

### Catatan tentang Netlify
Netlify didesain untuk hosting situs statis (HTML/CSS/JS). Aplikasi Streamlit membutuhkan server Python yang berjalan aktif (backend) untuk memproses logika AI dan data. Oleh karena itu, **Netlify tidak dapat men-host aplikasi Streamlit secara langsung**. Gunakan Streamlit Cloud, Railway, atau Render.
