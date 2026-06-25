"""
=============================================
  SISTEM PERPUSTAKAAN
  Final Project - Aplikasi Manajemen Data
  Menggunakan: CSV, Queue, Hash Map,
               Sorting, Searching
=============================================
"""

import csv
import os
from datetime import datetime

# ============================================================
# STRUKTUR DATA 1: QUEUE (antrian peminjaman buku yg stoknya habis)
# ============================================================
class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        """Masukkan permintaan pinjam ke antrian (belakang)"""
        self.items.append(item)

    def dequeue(self):
        """Keluarkan permintaan paling depan dari antrian"""
        if self.is_empty():
            return None
        return self.items.pop(0)

    def dequeue_match(self, predicate):
        """Keluarkan permintaan PERTAMA dalam antrian yang cocok dengan predicate
        (mis: id_buku yang sama dengan buku yang baru dikembalikan)"""
        for i, item in enumerate(self.items):
            if predicate(item):
                return self.items.pop(i)
        return None

    def peek(self):
        if self.is_empty():
            return None
        return self.items[0]

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def tampilkan(self):
        return self.items.copy()

# ============================================================
# STRUKTUR DATA 2: HASH MAP (cari buku cepat by ID)
# ============================================================
class HashMap:
    def __init__(self):
        self.data = {}

    def set(self, key, value):
        self.data[key] = value

    def get(self, key):
        return self.data.get(key, None)

    def delete(self, key):
        if key in self.data:
            del self.data[key]
            return True
        return False

    def exists(self, key):
        return key in self.data

# ============================================================
# FILE CSV - DATA BUKU
# ============================================================
FILE_BUKU = "data_buku.csv"
HEADER_BUKU = ['id', 'judul', 'penulis', 'kategori', 'stok']

def inisialisasi_csv_buku():
    if not os.path.exists(FILE_BUKU):
        with open(FILE_BUKU, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=HEADER_BUKU)
            writer.writeheader()
        print(f"[INFO] File '{FILE_BUKU}' berhasil dibuat.")

def baca_semua_buku():
    daftar = []
    try:
        with open(FILE_BUKU, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for baris in reader:
                daftar.append(dict(baris))
    except FileNotFoundError:
        pass
    return daftar

def tulis_semua_buku(daftar_buku):
    with open(FILE_BUKU, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=HEADER_BUKU)
        writer.writeheader()
        writer.writerows(daftar_buku)

def generate_id_buku(daftar_buku):
    if not daftar_buku:
        return "B001"
    id_terakhir = daftar_buku[-1]['id']
    nomor = int(id_terakhir[1:]) + 1
    return f"B{nomor:03d}"

# ============================================================
# FILE CSV - ANTRIAN PEMINJAMAN
# ============================================================
FILE_ANTRIAN = "data_antrian.csv"
HEADER_ANTRIAN = ['no_antrian', 'id_buku', 'judul_buku', 'nama_peminjam', 'tanggal_daftar']

def inisialisasi_csv_antrian():
    if not os.path.exists(FILE_ANTRIAN):
        with open(FILE_ANTRIAN, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=HEADER_ANTRIAN)
            writer.writeheader()

def baca_semua_antrian():
    daftar = []
    try:
        with open(FILE_ANTRIAN, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for baris in reader:
                daftar.append(dict(baris))
    except FileNotFoundError:
        pass
    return daftar

def tulis_semua_antrian(daftar_antrian):
    with open(FILE_ANTRIAN, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=HEADER_ANTRIAN)
        writer.writeheader()
        writer.writerows(daftar_antrian)

def generate_no_antrian(daftar_antrian):
    if not daftar_antrian:
        return "1"
    return str(int(daftar_antrian[-1]['no_antrian']) + 1)

# ============================================================
# ALGORITMA SORTING - Bubble Sort berdasarkan judul
# ============================================================
def bubble_sort_judul(daftar_buku):
    """Urutkan buku berdasarkan judul (A-Z) dengan Bubble Sort"""
    data = daftar_buku.copy()
    n = len(data)
    for i in range(n - 1):
        for j in range(n - i - 1):
            if data[j]['judul'].lower() > data[j+1]['judul'].lower():
                data[j], data[j+1] = data[j+1], data[j]
    return data

# ============================================================
# ALGORITMA SEARCHING - Linear Search berdasarkan judul
# ============================================================
def linear_search_judul(daftar_buku, keyword):
    """Cari buku berdasarkan judul (tidak case sensitive)"""
    hasil = []
    keyword = keyword.lower()
    for buku in daftar_buku:
        if keyword in buku['judul'].lower():
            hasil.append(buku)
    return hasil

# ============================================================
# INISIALISASI STRUKTUR DATA GLOBAL
# ============================================================
hashmap_buku = HashMap()
antrian_peminjaman = Queue()

def muat_data_ke_struktur():
    """Muat data dari CSV ke dalam HashMap dan Queue"""
    global hashmap_buku, antrian_peminjaman
    hashmap_buku = HashMap()
    antrian_peminjaman = Queue()

    for buku in baca_semua_buku():
        hashmap_buku.set(buku['id'], buku)

    for antri in baca_semua_antrian():
        antrian_peminjaman.enqueue(antri)

# ============================================================
# FUNGSI TAMPILAN
# ============================================================
def cetak_baris():
    print("=" * 60)

def cetak_garis():
    print("-" * 60)

def cetak_header_tabel():
    print(f"{'ID':<6} {'Judul':<25} {'Penulis':<18} {'Stok':<6}")
    cetak_garis()

def cetak_baris_buku(b):
    print(f"{b['id']:<6} {b['judul']:<25} {b['penulis']:<18} {b['stok']:<6}")

# ============================================================
# MENU 1: TAMBAH BUKU (CREATE)
# ============================================================
def tambah_buku():
    cetak_baris()
    print("            TAMBAH BUKU BARU")
    cetak_baris()

    judul = input("Judul Buku   : ").strip()
    if not judul:
        print("[ERROR] Judul tidak boleh kosong!")
        return

    penulis = input("Penulis      : ").strip()
    kategori = input("Kategori     : ").strip()

    stok_input = input("Jumlah Stok  : ").strip()
    if not stok_input.isdigit():
        print("[ERROR] Stok harus berupa angka!")
        return

    semua_buku = baca_semua_buku()
    id_baru = generate_id_buku(semua_buku)

    buku_baru = {
        'id': id_baru,
        'judul': judul,
        'penulis': penulis,
        'kategori': kategori,
        'stok': stok_input,
    }

    semua_buku.append(buku_baru)
    tulis_semua_buku(semua_buku)
    hashmap_buku.set(id_baru, buku_baru)

    print(f"\n[SUKSES] Buku '{judul}' berhasil ditambahkan dengan ID {id_baru}")

# ============================================================
# MENU 2: LIHAT SEMUA BUKU (READ)
# ============================================================
def lihat_semua_buku():
    cetak_baris()
    print("            DAFTAR SELURUH BUKU")
    cetak_baris()

    semua_buku = baca_semua_buku()
    if not semua_buku:
        print("[INFO] Belum ada data buku.")
        return

    cetak_header_tabel()
    for b in semua_buku:
        cetak_baris_buku(b)
    print(f"\nTotal: {len(semua_buku)} judul buku")

# ============================================================
# MENU 3: UPDATE DATA BUKU
# ============================================================
def update_buku():
    cetak_baris()
    print("            UPDATE DATA BUKU")
    cetak_baris()

    id_input = input("Masukkan ID Buku (contoh: B001): ").strip().upper()

    # Cari via HashMap (O(1) - cepat!)
    buku = hashmap_buku.get(id_input)
    if not buku:
        print(f"[ERROR] Buku dengan ID '{id_input}' tidak ditemukan.")
        return

    print(f"\nData saat ini:")
    print(f"  Judul : {buku['judul']}")
    print(f"  Stok  : {buku['stok']}")

    judul_baru = input(f"Judul baru (kosongkan jika tidak diubah): ").strip()
    stok_baru = input(f"Stok baru (kosongkan jika tidak diubah): ").strip()

    semua_buku = baca_semua_buku()
    for b in semua_buku:
        if b['id'] == id_input:
            if judul_baru:
                b['judul'] = judul_baru
            if stok_baru.isdigit():
                b['stok'] = stok_baru
            buku = b
            break
    tulis_semua_buku(semua_buku)
    hashmap_buku.set(id_input, buku)

    print(f"\n[SUKSES] Data buku '{buku['judul']}' berhasil diupdate.")

# ============================================================
# MENU 4: HAPUS BUKU (DELETE)
# ============================================================
def hapus_buku():
    cetak_baris()
    print("             HAPUS DATA BUKU")
    cetak_baris()

    id_input = input("Masukkan ID Buku yang dihapus: ").strip().upper()

    buku = hashmap_buku.get(id_input)
    if not buku:
        print(f"[ERROR] Buku dengan ID '{id_input}' tidak ditemukan.")
        return

    print(f"\nData yang akan dihapus:")
    print(f"  ID    : {buku['id']}")
    print(f"  Judul : {buku['judul']}")

    konfirmasi = input("\nYakin ingin menghapus? (y/n): ").strip().lower()
    if konfirmasi != 'y':
        print("[BATAL] Penghapusan dibatalkan.")
        return

    semua_buku = baca_semua_buku()
    semua_buku = [b for b in semua_buku if b['id'] != id_input]
    tulis_semua_buku(semua_buku)
    hashmap_buku.delete(id_input)

    print(f"\n[SUKSES] Buku '{buku['judul']}' berhasil dihapus.")

# ============================================================
# MENU 5: PINJAM BUKU
# ============================================================
def pinjam_buku():
    cetak_baris()
    print("              PINJAM BUKU")
    cetak_baris()

    id_input = input("Masukkan ID Buku: ").strip().upper()
    buku = hashmap_buku.get(id_input)
    if not buku:
        print(f"[ERROR] Buku dengan ID '{id_input}' tidak ditemukan.")
        return

    if int(buku['stok']) > 0:
        # Stok masih ada -> langsung dipinjam
        semua_buku = baca_semua_buku()
        for b in semua_buku:
            if b['id'] == id_input:
                b['stok'] = str(int(b['stok']) - 1)
                buku = b
                break
        tulis_semua_buku(semua_buku)
        hashmap_buku.set(id_input, buku)
        print(f"\n[SUKSES] Buku '{buku['judul']}' berhasil dipinjam. Sisa stok: {buku['stok']}")
    else:
        # Stok habis -> masuk antrian (QUEUE)
        nama = input("Stok habis. Masukkan nama Anda untuk masuk antrian: ").strip()
        if not nama:
            print("[ERROR] Nama tidak boleh kosong!")
            return

        semua_antrian = baca_semua_antrian()
        no_baru = generate_no_antrian(semua_antrian)
        antrian_baru = {
            'no_antrian': no_baru,
            'id_buku': id_input,
            'judul_buku': buku['judul'],
            'nama_peminjam': nama,
            'tanggal_daftar': datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
        semua_antrian.append(antrian_baru)
        tulis_semua_antrian(semua_antrian)
        antrian_peminjaman.enqueue(antrian_baru)

        print(f"\n[INFO] Stok '{buku['judul']}' habis. Anda masuk antrian nomor {no_baru}.")

# ============================================================
# MENU 6: KEMBALIKAN BUKU
# ============================================================
def kembalikan_buku():
    cetak_baris()
    print("            KEMBALIKAN BUKU")
    cetak_baris()

    id_input = input("Masukkan ID Buku yang dikembalikan: ").strip().upper()
    buku = hashmap_buku.get(id_input)
    if not buku:
        print(f"[ERROR] Buku dengan ID '{id_input}' tidak ditemukan.")
        return

    # Tambah stok dulu
    semua_buku = baca_semua_buku()
    for b in semua_buku:
        if b['id'] == id_input:
            b['stok'] = str(int(b['stok']) + 1)
            buku = b
            break
    tulis_semua_buku(semua_buku)
    hashmap_buku.set(id_input, buku)
    print(f"\n[SUKSES] Buku '{buku['judul']}' berhasil dikembalikan.")

    # Cek antrian (QUEUE) - apakah ada yang menunggu buku ini?
    permintaan = antrian_peminjaman.dequeue_match(lambda x: x['id_buku'] == id_input)
    if permintaan:
        # Langsung pinjamkan ke orang pertama dalam antrian
        semua_buku = baca_semua_buku()
        for b in semua_buku:
            if b['id'] == id_input:
                b['stok'] = str(int(b['stok']) - 1)
                buku = b
                break
        tulis_semua_buku(semua_buku)
        hashmap_buku.set(id_input, buku)

        semua_antrian = baca_semua_antrian()
        semua_antrian = [a for a in semua_antrian if a['no_antrian'] != permintaan['no_antrian']]
        tulis_semua_antrian(semua_antrian)

        print(f"[INFO] Buku otomatis diberikan ke '{permintaan['nama_peminjam']}' (antrian nomor {permintaan['no_antrian']}).")

# ============================================================
# MENU 7: LIHAT ANTRIAN PEMINJAMAN (QUEUE)
# ============================================================
def lihat_antrian():
    cetak_baris()
    print("          ANTRIAN PEMINJAMAN BUKU")
    cetak_baris()

    antrian = antrian_peminjaman.tampilkan()
    if not antrian:
        print("[INFO] Tidak ada antrian saat ini.")
        return

    print(f"Jumlah antrian: {len(antrian)} orang\n")
    for i, a in enumerate(antrian):
        simbol = ">>> " if i == 0 else f"  {i+1}. "
        print(f"{simbol}{a['nama_peminjam']} menunggu buku '{a['judul_buku']}' (ID:{a['id_buku']})")

# ============================================================
# MENU 8: CARI BUKU (SEARCHING)
# ============================================================
def cari_buku():
    cetak_baris()
    print("              PENCARIAN BUKU")
    cetak_baris()
    print("  1. Cari berdasarkan Judul (Linear Search)")
    print("  2. Cari berdasarkan ID    (Hash Map - O(1))")
    cetak_baris()
    pilih = input("Pilihan: ").strip()

    if pilih == '1':
        keyword = input("Masukkan judul yang dicari: ").strip()
        semua_buku = baca_semua_buku()
        hasil = linear_search_judul(semua_buku, keyword)
        if not hasil:
            print(f"\n[INFO] Tidak ditemukan buku dengan judul '{keyword}'")
        else:
            print(f"\nDitemukan {len(hasil)} buku:")
            cetak_header_tabel()
            for b in hasil:
                cetak_baris_buku(b)

    elif pilih == '2':
        id_input = input("Masukkan ID Buku: ").strip().upper()
        buku = hashmap_buku.get(id_input)
        if not buku:
            print(f"\n[INFO] Buku dengan ID '{id_input}' tidak ditemukan.")
        else:
            print(f"\nData Buku Ditemukan:")
            cetak_garis()
            print(f"  ID       : {buku['id']}")
            print(f"  Judul    : {buku['judul']}")
            print(f"  Penulis  : {buku['penulis']}")
            print(f"  Kategori : {buku['kategori']}")
            print(f"  Stok     : {buku['stok']}")
    else:
        print("[ERROR] Pilihan tidak valid!")

# ============================================================
# MENU 9: URUTKAN BUKU (SORTING)
# ============================================================
def urutkan_buku():
    cetak_baris()
    print("        URUTKAN DATA BUKU (BUBBLE SORT)")
    cetak_baris()
    print("  1. Urutkan berdasarkan Judul (A-Z)")
    print("  2. Urutkan berdasarkan Stok (terbanyak)")
    cetak_baris()
    pilih = input("Pilihan: ").strip()

    semua_buku = baca_semua_buku()
    if not semua_buku:
        print("[INFO] Belum ada data buku.")
        return

    if pilih == '1':
        terurut = bubble_sort_judul(semua_buku)
        print("\nData Buku (Urut Judul A-Z):")
    elif pilih == '2':
        terurut = semua_buku.copy()
        n = len(terurut)
        for i in range(n - 1):
            for j in range(n - i - 1):
                if int(terurut[j]['stok']) < int(terurut[j+1]['stok']):
                    terurut[j], terurut[j+1] = terurut[j+1], terurut[j]
        print("\nData Buku (Urut Stok Terbanyak):")
    else:
        print("[ERROR] Pilihan tidak valid!")
        return

    cetak_header_tabel()
    for b in terurut:
        cetak_baris_buku(b)

# ============================================================
# MENU UTAMA
# ============================================================
def menu_utama():
    inisialisasi_csv_buku()
    inisialisasi_csv_antrian()
    muat_data_ke_struktur()

    while True:
        cetak_baris()
        print("        SISTEM PERPUSTAKAAN CERDAS BANGSA")
        cetak_baris()
        print("    1. Tambah Buku Baru")
        print("    2. Lihat Semua Buku")
        print("    3. Update Data Buku")
        print("    4. Hapus Data Buku")
        print("    5. Pinjam Buku")
        print("    6. Kembalikan Buku")
        print("    7. Lihat Antrian Peminjaman")
        print("    8. Cari Buku")
        print("    9. Urutkan Data Buku")
        print("    0. Keluar")
        cetak_baris()
        print(f"  Antrian peminjaman saat ini: {antrian_peminjaman.size()} orang")
        cetak_baris()

        pilihan = input("  Pilihan Anda: ").strip()

        if pilihan == '1':
            tambah_buku()
        elif pilihan == '2':
            lihat_semua_buku()
        elif pilihan == '3':
            update_buku()
        elif pilihan == '4':
            hapus_buku()
        elif pilihan == '5':
            pinjam_buku()
        elif pilihan == '6':
            kembalikan_buku()
        elif pilihan == '7':
            lihat_antrian()
        elif pilihan == '8':
            cari_buku()
        elif pilihan == '9':
            urutkan_buku()
        elif pilihan == '0':
            print("\n  Terima kasih telah menggunakan Sistem Perpustakaan!")
            print("  Sampai jumpa!\n")
            break
        else:
            print("\n  [ERROR] Pilihan tidak valid! Masukkan angka 0-9.")

        input("\n  Tekan Enter untuk kembali ke menu...")

# ============================================================
# JALANKAN PROGRAM
# ============================================================
if __name__ == "__main__":
    menu_utama()