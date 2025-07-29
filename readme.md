# Python Chatbot dengan Llama 3.1
Chatbot sederhana yang dibangun menggunakan Python dan model Llama 3.1:8b melalui Ollama. Bot ini dapat melakukan percakapan interaktif dengan pengguna menggunakan model language yang canggih.
🚀 Fitur

# Percakapan real-time dengan AI
- Menggunakan model Llama 3.1:8b yang powerful
- Interface command line yang mudah digunakan
- Riwayat percakapan dalam sesi
- Dukungan untuk berbagai bahasa

# 📋 Prasyarat
## Sebelum menjalankan aplikasi ini, pastikan Anda memiliki:
- Python 3.8 atau lebih tinggi
- Ollama terinstall di sistem Anda
- Model Llama 3.1:8b sudah didownload


# 🛠️ Instalasi
1. Install Ollama
Windows/macOS : Download dari https://ollama.ai

2. Download Model Llama 3.1
ollama pull llama3.1:8b

3. Install Dependencies
pip install -r requirements.txt

# 📦 Dependencies
Buat file requirements.txt dengan konten berikut:
- requests>=2.28.0
- ollama>=0.1.0

# 🎯 Cara Penggunaan
## Menjalankan Chatbot
python chatbot.py

## Contoh Penggunaan
=== Python Chatbot dengan Llama 3.1 ===
Ketik 'quit', 'exit', atau 'bye' untuk keluar

You: Halo, siapa kamu?
Bot: Halo! Saya adalah assistant AI yang menggunakan model Llama 3.1. Saya bisa membantu Anda dengan berbagai pertanyaan dan percakapan. Ada yang bisa saya bantu?

You: Jelaskan tentang machine learning
Bot: Machine learning adalah cabang dari artificial intelligence (AI) yang memungkinkan komputer untuk belajar dan membuat keputusan tanpa diprogram secara eksplisit...

# 📁 Struktur Project
python-llama-chatbot/
│
├── chatbot.py          # File utama aplikasi
├── requirements.txt    # Dependencies Python
├── README.md          # Dokumentasi ini
└── config.py          # Konfigurasi (opsional)

# ⚙️ Konfigurasi
Anda dapat menyesuaikan pengaturan chatbot dengan mengedit parameter berikut :
### Dalam chatbot.py
- MODEL_NAME = "llama3.1:8b"
- OLLAMA_HOST = "http://localhost:11434"
- MAX_TOKENS = 2048
- TEMPERATURE = 0.7

# Connection Error
- Pastikan Ollama service berjalan di port 11434
- Periksa firewall atau antivirus yang mungkin memblokir koneksi

# 👤 Author
Nur Fadilah Zulfi - Polteknik Negeri Lhokseumawe - github.com/nurfadilahzulfi

# 🙏 Ucapan Terima Kasih
- Tim Meta AI untuk model Llama 3.1
- Ollama team untuk tool yang memudahkan deployment model
- Komunitas open source Python

# 📞 Support
Jika Anda mengalami masalah atau memiliki pertanyaan:

# Buat issue di GitHub Issues
Email: nurfadilahzulfi@gmail.com