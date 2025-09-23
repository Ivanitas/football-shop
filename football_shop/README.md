1. Mengapa perlu data delivery?
Data delivery memungkinkan pertukaran informasi terstruktur antara client-server, support API integration, dan memisahkan frontend-backend concerns.

2. XML vs JSON?
JSON lebih baik karena:
- Lebih ringan dan cepat
- Syntax lebih sederhana
- Native support di JavaScript
- Parsing lebih efisien
- Populer untuk REST APIs

3. Fungsi is_valid()?
- Validasi data input user
- Cek required fields, tipe data, constraints
- Return True/False + error messages
- Prevent invalid data masuk database

4. Mengapa csrf_token penting?
- Mencegah CSRF attacks
- Tanpa token: attacker bisa exploit session user
- Penyerang bisa buat request palsu seolah dari user
- Token ensure request berasal dari website legitimate

5. Cara Implementasi
- Buat 4 views (XML, JSON, XML by ID, JSON by ID)
- Routing URL untuk setiap endpoint
- Halaman main dengan tombol Add + Detail
- Form product dengan validation & csrf_token
- Halaman detail product
- Testing dengan Postman
- Deploy ke GitHub