# AGENTS.md — Panduan Agent AI untuk Project Ini

> File ini dibaca otomatis oleh Codex setiap sesi dimulai.
> Ikuti semua instruksi di sini sebelum mengeksekusi perintah apapun.

---

## 🧠 PRINSIP UTAMA: THINK BEFORE YOU ACT

Sebelum menulis satu baris kode atau memberikan jawaban apapun, agent **WAJIB** menjalankan urutan berikut:

```
1. BACA konteks → 2. ANALISIS situasi → 3. RENCANAKAN → 4. EKSEKUSI → 5. VERIFIKASI → 6. UPDATE progress.md
```

Jangan pernah langsung eksekusi tanpa memahami kondisi saat ini.

---

## 📋 FASE 1 — ORIENTASI PROJECT (Wajib saat sesi baru)

Setiap kali sesi dimulai atau perintah baru diterima, jalankan langkah ini:

### 1.1 Baca Struktur Project
```bash
# Pahami layout project
find . -maxdepth 3 -not -path '*/node_modules/*' -not -path '*/.git/*' -not -path '*/__pycache__/*'
```

### 1.2 Baca File Konfigurasi Utama
Cek file-file ini secara berurutan jika ada:
- `package.json` / `pyproject.toml` / `go.mod` / `Cargo.toml` — dependencies & scripts
- `.env.example` atau `.env` — variabel environment
- `docker-compose.yml` / `Dockerfile` — infrastruktur
- `README.md` — konteks umum project
- File konfigurasi framework (e.g. `next.config.js`, `vite.config.ts`, `settings.py`)

### 1.3 Identifikasi Stack Teknologi
Tentukan:
- **Bahasa**: TypeScript / Python / Go / Rust / dll
- **Framework**: Next.js / FastAPI / Express / dll
- **Database**: PostgreSQL / MongoDB / SQLite / dll
- **State Management / ORM**: Prisma / SQLAlchemy / Drizzle / dll
- **Testing**: Jest / Pytest / Vitest / dll

### 1.4 Cek Git Status (Jika Relevan)
```bash
git log --oneline -10        # 10 commit terakhir
git status                   # perubahan yang belum di-commit
git branch -a                # branch yang ada
```

---

## 🔍 FASE 2 — ANALISIS SEBELUM EKSEKUSI

Sebelum mengubah atau membuat file apapun:

### 2.1 Baca File yang Relevan Terlebih Dahulu
- Jangan asumsikan isi file — **baca dulu**
- Jika akan edit UI/Tampilan, **WAJIB baca `DESIGN.md`** untuk memastikan konsistensi warna, font, dan pola UX.
- Jika akan edit fungsi, baca seluruh file, bukan cuma bagian yang diminta
- Identifikasi dependensi: siapa yang memanggil fungsi ini? Apa yang dipanggil fungsi ini?

### 2.2 Cek Pola yang Sudah Ada
- Ikuti konvensi kode yang sudah ada di project (naming, struktur folder, style)
- Cek apakah sudah ada utilitas/helper yang bisa dipakai ulang
- Jangan reinvent the wheel — cari dulu di codebase

### 2.3 Identifikasi Risiko
Sebelum mengubah kode, jawab:
- Apakah perubahan ini breaking change?
- Ada berapa tempat yang terpengaruh?
- Apakah ada test yang perlu diupdate?
- Apakah ada migrasi database yang diperlukan?

### 2.4 Buat Rencana Eksplisit
Untuk task yang kompleks, tulis rencana dulu:
```
Rencana:
1. [langkah 1]
2. [langkah 2]
3. [langkah 3]
```
Minta konfirmasi jika tidak yakin.

---

## ⚙️ FASE 3 — ATURAN EKSEKUSI

### 3.1 Aturan Umum
- **Satu perubahan per waktu** — jangan ubah banyak file sekaligus tanpa alasan jelas
- **Selalu baca sebelum tulis** — gunakan `Read` sebelum `Edit`
- **Minimal footprint** — hanya ubah yang diminta, tidak lebih
- **Jangan hapus kode** tanpa konfirmasi eksplisit dari user

### 3.2 Penanganan Error
Jika ada error saat eksekusi:
1. Baca pesan error secara lengkap
2. Cek log yang relevan
3. Analisis root cause, bukan symptom
4. Perbaiki dari akar masalah, bukan workaround

### 3.3 Aturan Shell & Terminal
```bash
# Cek versi Python yang aktif
python --version
pip --version

# Install dependency baru (selalu update requirements.txt juga!)
pip install nama-package
pip freeze > requirements.txt

# Gunakan timeout untuk command yang bisa hang
timeout 30 python app.py

# Selalu cek exit code
python app.py && echo "SUCCESS" || echo "FAILED"
```

### 3.4 Aturan File & Folder
- Simpan file baru di lokasi yang konsisten dengan struktur project
- Gunakan nama file sesuai konvensi yang ada (kebab-case / snake_case / PascalCase)
- Jangan buat file di root project kecuali memang harus

---

## 🧪 FASE 4 — VERIFIKASI SETELAH EKSEKUSI

Setelah selesai eksekusi, selalu lakukan:

### 4.1 Verifikasi Fungsional
```bash
# Jalankan app pastikan tidak ada error saat startup
python app.py

# Cek syntax Python (tidak ada error parse)
python -m py_compile app.py && echo "OK"

# Cek linting (jika flake8/ruff tersedia)
flake8 . --exclude=instance/ || ruff check .
```

### 4.2 Verifikasi Manual
- Baca ulang kode yang baru ditulis
- Pastikan tidak ada `console.log`, `print()`, atau debug statement yang tertinggal
- Pastikan tidak ada hardcoded secret/credential

### 4.3 Ringkasan Perubahan
Setelah selesai, berikan ringkasan:
```
✅ Yang dilakukan:
- [perubahan 1]
- [perubahan 2]

📁 File yang diubah:
- path/to/file1.ts
- path/to/file2.py

⚠️ Perlu diperhatikan:
- [catatan penting jika ada]
```

---

## 📝 FASE 5 — UPDATE PROGRESS.MD (WAJIB Setelah Setiap Task Selesai)

Setiap kali task atau perintah selesai dikerjakan, agent **WAJIB** memperbarui file `progress.md` di root project.

### 5.1 Jika `progress.md` Belum Ada — Buat Dulu
```markdown
# 📊 Progress Log — [Nama Project]

> File ini di-update otomatis oleh Codex setiap kali task selesai.
> Jangan diedit manual kecuali untuk koreksi.

---

## 🗓️ Log Aktivitas

<!-- Entri terbaru selalu di ATAS -->

```

### 5.2 Format Entri Progress (Tambahkan di Paling Atas Log)

```markdown
### [YYYY-MM-DD HH:MM] — [Judul Task Singkat]

**Status:** ✅ Selesai | ⚠️ Selesai dengan catatan | ❌ Gagal / Dibatalkan

**Yang Dikerjakan:**
- [deskripsi singkat perubahan 1]
- [deskripsi singkat perubahan 2]

**File yang Diubah/Dibuat:**
- `path/to/file1.ts` — [apa yang berubah]
- `path/to/file2.py` — [apa yang berubah]

**Catatan Penting:**
- [risiko, keputusan teknis, atau hal yang perlu diketahui]

**Next Step (jika ada):**
- [ ] [task lanjutan yang disarankan]

---
```

### 5.3 Aturan Update Progress
- **Selalu tambahkan di paling atas** — entri terbaru harus paling mudah dilihat
- **Gunakan timestamp lokal** — format `YYYY-MM-DD HH:MM`
- **Jujur tentang status** — jika ada yang belum beres, tulis apa adanya
- **Ringkas tapi informatif** — cukup untuk dipahami oleh developer lain tanpa baca kodenya
- **Jangan skip** — meski task kecil sekalipun (fix typo, update config), tetap dicatat
- **Tandai next step** — jika ada pekerjaan lanjutan yang teridentifikasi, tulis sebagai checklist

### 5.4 Contoh Entri yang Baik

```markdown
### [2025-01-15 14:30] — Tambah validasi Zod di endpoint POST /api/users

**Status:** ✅ Selesai

**Yang Dikerjakan:**
- Tambah schema validasi Zod untuk body request `createUser`
- Tambah error handling dengan response 400 jika validasi gagal
- Update unit test untuk cover case validasi gagal

**File yang Diubah/Dibuat:**
- `src/app/api/users/route.ts` — tambah validasi Zod
- `src/lib/schemas/user.schema.ts` — buat file baru, definisi schema
- `__tests__/api/users.test.ts` — tambah 3 test case baru

**Catatan Penting:**
- Schema sengaja strict (tidak pakai `.passthrough()`) agar field asing ditolak
- Validasi email menggunakan `.email()` bawaan Zod, bukan regex custom

**Next Step (jika ada):**
- [ ] Terapkan pola validasi yang sama ke endpoint PUT /api/users/:id

---
```

---

## 🚫 HAL YANG TIDAK BOLEH DILAKUKAN

- ❌ Jangan jalankan `rm -rf` tanpa konfirmasi eksplisit
- ❌ Jangan push ke git tanpa instruksi user
- ❌ Jangan install dependency baru tanpa memberitahu user
- ❌ Jangan ekspos atau log credential/secret
- ❌ Jangan assume — jika tidak yakin, tanya
- ❌ Jangan tulis kode yang tidak ditest untuk path kritis
- ❌ Jangan ubah `.env` production tanpa konfirmasi
- ❌ Jangan jalankan migrasi database di production tanpa konfirmasi

---

## 💬 ATURAN KOMUNIKASI

### Jika Task Ambigu
Tanyakan hal yang paling penting saja — **satu pertanyaan** per giliran:
```
"Sebelum saya mulai, boleh saya tahu: [pertanyaan paling kritis]?"
```

### Jika Menemukan Masalah Lain
Laporkan temuan tambahan tanpa langsung memperbaikinya:
```
"Saya menemukan potensi bug di [lokasi] saat mengerjakan ini.
Mau saya perbaiki juga, atau fokus ke task utama dulu?"
```

### Jika Ada Pilihan Implementasi
Presentasikan opsi dengan trade-off, bukan langsung pilihkan:
```
Opsi A: [deskripsi] — lebih cepat, tapi [trade-off]
Opsi B: [deskripsi] — lebih robust, tapi [trade-off]
Rekomendasi: [pilihan] karena [alasan]
```

---

## 🗂️ KONTEKS PROJECT INI

```yaml
project_name: "Flask Photobooth App"
tipe: "Web App"
bahasa_utama: "Python"
framework: "Flask"
database: "SQLite — file: instance/database.db (via Flask-SQLAlchemy)"
environment_utama: "development"
```

### Perintah Penting
```bash
# Install semua dependency
pip install -r requirements.txt

# Jalankan aplikasi
python app.py
```

### Stack & Library Utama
| Komponen | Detail |
|---|---|
| **Framework** | Flask (Python) |
| **Database** | SQLite via Flask-SQLAlchemy |
| **Auth** | Flask-Login (session) + Werkzeug (password hashing) |
| **Storage** | Captured images disimpan sebagai PNG di `static/uploads/` |
| **Templating** | Jinja2 — template di folder `templates/` |

### Models
| Model | Fungsi |
|---|---|
| `User` | Identity, email, hashed password, role (`admin` atau `consumer`) |
| `Photo` | Metadata gambar: `file_path`, `smile_score`, FK ke `User` |

### Routing Map
```
Auth:
  GET/POST  /register          → Registrasi user baru
  GET/POST  /login             → Login
  GET/POST  /forgot-password   → Reset password
  GET       /logout            → Logout

User (login required):
  GET       /dashboard         → Halaman utama user
  GET       /photobooth        → Halaman ambil foto
  POST      /save-photo        → API simpan foto (JSON response)
  GET       /gallery           → Galeri foto user
  GET/POST  /profile           → Profil user

Admin (role: admin only):
  GET       /admin             → Dashboard admin
```

### Path Penting
```
app.py                  → Entry point aplikasi
requirements.txt        → Dependencies Python
templates/              → Semua HTML template (Jinja2)
static/uploads/         → Hasil foto tersimpan (PNG)
instance/database.db    → File database SQLite
```

### Konvensi Kode
- Password **selalu** di-hash dengan Werkzeug sebelum disimpan — jangan pernah simpan plaintext
- Proteksi route user pakai decorator `@login_required` dari Flask-Login
- Proteksi route admin cek `current_user.role == 'admin'` secara eksplisit
- Response dari endpoint `/save-photo` harus berupa JSON
- Nama file gambar yang disimpan ke `static/uploads/` harus unik (gunakan UUID atau timestamp)

### Catatan Khusus
- Database SQLite ada di `instance/` — **jangan di-commit** file ini ke git
- Jika ada perubahan model (`User` atau `Photo`), jalankan migrasi atau `db.create_all()` dengan hati-hati
- Role user hanya dua nilai valid: `"admin"` dan `"consumer"` — validasi saat registrasi

---

## 🔄 CHECKLIST SEBELUM & SESUDAH SETIAP PERINTAH

### Sebelum eksekusi:
- [ ] Sudah baca file/konteks yang relevan?
- [ ] Sudah paham apa yang diminta?
- [ ] Sudah tahu risiko perubahan ini?
- [ ] Sudah punya rencana yang jelas?
- [ ] Sudah konfirmasi jika ada ambiguitas?

### Setelah eksekusi:
- [ ] Test/lint sudah dijalankan dan passed?
- [ ] Tidak ada debug statement yang tertinggal?
- [ ] Tidak ada hardcoded secret?
- [ ] **`progress.md` sudah diupdate?** ← jangan lupa ini!

Jika semua **ya** → task benar-benar selesai.
Jika ada yang **tidak** → selesaikan dulu sebelum lanjut.

---

*File ini di-maintain bersama. Update jika ada konvensi baru atau penemuan penting selama development.*