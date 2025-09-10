# football-shop
Membuat e-shop untuk tugas 1
Nama: Muhammad Iffan Chalif Aziz
Kelas: PBP B
NPM: 2406435250

SOAL DAN JAWABAN:
1. Jelaskan bagaimana cara kamu mengimplementasikan checklist di atas secara step-by-step (bukan hanya sekadar mengikuti tutorial).
JWB: - Mengikuti tutorial 0 dan 1 untuk membuat template untuk nanti modifikasi untuk tugas 2
     - melihat sumber external untuk memodifikasi model dan settings
     - setelah selesai semua, hasil di push ke master pws dan origin

2. Buatlah bagan yang berisi request client ke web aplikasi berbasis Django beserta responnya dan jelaskan pada bagan tersebut kaitan antara urls.py, views.py, models.py, dan berkas html.
JWB: Client  -->  urls.py  -->  views.py   -->  models.py --> Database --> template --> CLient --> ...
Penjelasan: urls.py: Bertugas sebagai router yang menentukan view mana yang akan menangani request berdasarkan URL pattern
views.py: Berisi logika aplikasi, menerima request, berinteraksi dengan model, dan mengembalikan response
models.py: Mendefinisikan struktur data dan berinteraksi dengan database
Template (HTML): Bertanggung jawab untuk presentasi data yang dikirim dari view
Database: Menyimpan data aplikasi yang diakses melalui model

3. Jelaskan peran settings.py dalam proyek Django!
JWB:
- Aplikasi yang Terinstall: Mengatur aplikasi apa saja yang digunakan (INSTALLED_APPS)
- Konfigurasi Database: Menentukan jenis database, nama, credential (DATABASES)
- Static & Media Files: Mengatur lokasi dan URL untuk static files dan media uploads
- Middleware: Menentukan urutan middleware yang diproses untuk setiap request
- Internationalization: Mengatur bahasa, timezone, dan format lokal
- Security Settings: Mengatur SECRET_KEY, DEBUG mode, ALLOWED_HOSTS, dll.
- Template Configuration: Mengatur bagaimana template diproses dan dicari
- Authentication: Konfigurasi sistem autentikasi dan authorization

4. Bagaimana cara kerja migrasi database di Django?
JWB:
- Membuat Migrasi:
python manage.py makemigrations membuat file migrasi berdasarkan perubahan model
Django membandingkan model saat ini dengan versi sebelumnya
File migrasi berisi operasi untuk mengubah skema database
- Menerapkan Migrasi:
python manage.py migrate menerapkan migrasi ke database
Django mengeksekusi perintah SQL sesuai dengan operasi di file migrasi
Sistem melacak migrasi yang sudah diterapkan di tabel django_migrations
- Version Control:
Setiap migrasi memiliki dependencies yang menentukan urutan eksekusi
Memungkinkan rollback ke versi sebelumnya dengan migrate app_name migration_name
- Sinkronisasi Model-Database:
Memastikan struktur database sesuai dengan definisi model di Python
Menangani perubahan seperti menambah/menghapus field, mengubah tipe data, dll.

5. Menurut Anda, dari semua framework yang ada, mengapa framework Django dijadikan permulaan pembelajaran pengembangan perangkat lunak?
JWB:
Batteries Included: Sudah menyediakan banyak komponen siap pakai (admin, ORM, auth)
Documentation Excellent: Dokumentasi yang sangat lengkap dan terorganisir dengan baik
Design Pattern Clear: MVT pattern yang jelas memudahkan pemahaman separation of concerns
Python-Based: Python adalah bahasa yang mudah dipelajari dengan syntax yang clean

6. Feedback:
JWB: Belum ada
