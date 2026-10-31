#let kode(file, w, cap) = figure(
  image("../../media/" + file + ".png", width: w),
  kind: "gambar",
  caption: cap,
)

= LAPORAN PRAKTIKUM

== Source Code Lengkap

Source code asli dipotong dua, lalu digabung horizontal. Bagian kiri baris 1--111, bagian kanan baris 112--221.

#kode("ll-0-asli", 88%, [Source Code Single Linked List (`01-linkedlist.cpp`)])

#kode("st-0-asli", 100%, [Source Code Stack (`02-stack.cpp`)])

== Alur Kerja Delete Kiri, Delete Kanan, dan Delete Tengah

Semua fungsi memakai variabel global dari struct `simpul` di baris 5--11: `awal`, `akhir`, `hapus` (node yang akan dibuang), serta `b1` dan `b2` (pointer bantu).

=== Delete Kiri

#kode("ll-asli-hapus_awal", 46%, [Kode `hapus_awal` Asli])

Baris 93 mengecek list kosong. Baris 97 menangani list dengan satu node: `awal` dan `akhir` di-`NULL`-kan. Kasus umum ada di baris 103--106: `hapus` menyimpan node depan, lalu `awal` pindah ke `awal->next`. Tidak ada loop, jadi satu langkah saja.

#kode("dg-delete-kiri", 78%, [Diagram Alur Delete Kiri])

=== Delete Kanan

#kode("ll-asli-hapus_akhir", 46%, [Kode `hapus_akhir` Asli])

Kasus satu node sama seperti delete kiri (baris 116--121). Kasus umum: `b1` mulai dari `awal` lalu maju selama `b1->next != akhir` (baris 124--128), jadi berhenti di node sebelum terakhir. Baris 129--131: `hapus` menunjuk node terakhir, `b1->next = NULL` memutus sambungan, dan `akhir = b1` memindahkan tail. Loop inilah yang bikin delete kanan lebih lambat.

#kode("dg-delete-kanan", 74%, [Diagram Alur Delete Kanan])

=== Delete Tengah

#kode("ll-asli-hapus_tengah", 66%, [Kode `hapus_tengah` Asli])

#kode("dg-delete-tengah", 66%, [Diagram Alur Delete Tengah])

Baris 142 dan 144 mengalihkan ke `hapus_awal()` / `hapus_akhir()` kalau `x` ada di ujung. Baris 148--157 menghitung dulu apakah `x` ada lewat variabel `ada`, kalau 0 muncul pesan tidak valid. Baris 160--164 mencari `b`, yaitu node sebelum `x`. Lalu baris 165--168: `b1` = target, `b2` = node sesudahnya, dan `b->next = b2` melewati target.

== Alur Kerja Stack

Stack memakai struct yang sama, tetapi cuma satu pointer utama `atas`, ditambah penghitung `jumlah` (baris 5--12).

=== Push

#kode("st-asli-tambah_stack", 42%, [Kode `tambah_stack` Asli])

Baris 33 menolak data baru kalau `jumlah == 10`. Baris 39--40 membuat node dan mengisi `info`. Baris 41 menyambungkan node baru ke stack lama (`data->next = atas`), baru baris 42 memindahkan `atas`. Baris 43 menambah `jumlah`.

#kode("dg-stack-push", 78%, [Diagram Alur Push])

=== Pop

#kode("st-asli-hapus_stack", 48%, [Kode `hapus_stack` Asli])

Baris 49 mengecek stack kosong. Baris 55--57: `hapus` menyimpan puncak, `atas` turun ke node bawahnya, `jumlah` dikurangi.

#kode("dg-stack-pop", 78%, [Diagram Alur Pop])

=== Hapus Semua

#kode("st-asli-hapus_semua", 48%, [Kode `hapus_semua` Asli])

Loop di baris 70--74 mengulang pop sampai `atas == NULL`, lalu baris 75 mereset `jumlah = 0`.

#kode("dg-stack-hapus-semua", 78%, [Diagram Alur Hapus Semua])

== Perbaikan Program

Perubahan dicatat dengan git: `git diff asli syntax` untuk syntax dan `git diff syntax fix` untuk logika. Merah = baris dihapus, hijau = baris ditambah. Hasilnya dikompilasi dengan `g++ -std=c++17 -Wall -Wextra -pedantic` tanpa error maupun warning, lalu diuji dengan AddressSanitizer.

=== Syntax Standar C++

Source asli ditulis untuk Turbo C++, jadi banyak syntax yang ditolak compiler modern:

- `#include <iostream.h>` diganti `<iostream>`, karena header lama sudah tidak ada. `<conio.h>` dan `<stdio.h>` dibuang karena tidak dipakai lagi.
- `cout` dan `cin` dipakai lewat `using std::cout;` dan `using std::cin;`, bukan `using namespace std;`. Alasannya variabel global `data` bentrok dengan `std::data` di C++17.
- `void main()` diganti `int main()` dan diakhiri `return 0;`, sebab standar C++ mewajibkan `main` mengembalikan `int`.
- `clrscr()` (conio) diganti `system(CLS)`, dengan `CLS` bernilai `"cls"` di Windows dan `"clear"` di Linux/macOS. `getch()` pada stack diganti `cin.ignore(); cin.get();`.

#grid(
  columns: (1fr, 1fr),
  column-gutter: 0.5cm,
  align: top,
  kode("ll-sintaks", 100%, [`git diff` Syntax Linked List]),
  kode("st-sintaks", 100%, [`git diff` Syntax Stack]),
)

=== Logika Delete Kiri, Delete Kanan, dan Delete Tengah

#kode("ll-diff", 100%, [`git diff` Single Linked List (dipotong dua, digabung horizontal)])

Masalah di versi asli dan perbaikannya:

- *Node tidak pernah di-`delete`.* Ketiga fungsi cuma melepas node dari list, memorinya tetap terpakai (memory leak). Sekarang tiap fungsi diakhiri `delete hapus; hapus = NULL;`. Buktinya, AddressSanitizer melaporkan leak di versi asli dan bersih di versi baru.
- *Tidak ada pesan sukses.* Ditambah `Hapus Awal/Akhir/Tengah Berhasil` supaya hasilnya kelihatan.
- *`hapus_awal` lebih pendek.* Cabang `awal == akhir` digabung ke satu pengecekan `if(awal==NULL) akhir=NULL` setelah `awal` bergeser.
- *`hapus_tengah` disederhanakan.* Dua loop (hitung `ada`, lalu cari) jadi satu loop `b->next != NULL && b->next->info != x`. Variabel `ada` dan `b2` dibuang, dan `akhir = b` di-update kalau yang terhapus node terakhir. Di versi asli, list `1 2 3 2` dihapus `2` menghasilkan `1 2 3` (yang terhapus kemunculan terakhir karena cek `akhir->info` duluan), sekarang menghasilkan `1 3 2` (kemunculan pertama).

#grid(
  columns: (2.37fr, 1fr),
  column-gutter: 0.5cm,
  align: bottom,
  kode("ll-leak-asli", 100%, [Versi Asli (ada leak)]),
  kode("ll-leak-baru", 100%, [Versi Baru (bersih)]),
)

=== Logika Stack

#kode("st-diff", 75%, [`git diff` Stack])

Di `hapus_stack` dan `hapus_semua` versi asli juga tidak ada `delete`. Sekarang node dibebaskan, dan `hapus_stack` menampilkan nilai yang dibuang (`Data 30 Berhasil Dihapus`), bukan cuma "Penghapusan Berhasil".

#pagebreak(weak: true)

== Hasil Eksekusi

Tiap screenshot menampilkan satu layar program setelah operasi dijalankan.

#grid(
  columns: (1fr, 1fr),
  column-gutter: 0.5cm,
  row-gutter: 0.4cm,
  align: bottom,
  kode("ll-out-tengah", 100%, [Delete Tengah (data 3)]),
  kode("ll-out-invalid", 100%, [Delete Tengah, Data Tidak Ada]),
  kode("ll-out-akhir", 100%, [Delete Kanan]),
  kode("ll-out-awal", 100%, [Delete Kiri]),
)

#grid(
  columns: (1fr, 1fr, 1fr),
  column-gutter: 0.4cm,
  align: bottom,
  kode("st-out-pop", 100%, [Pop]),
  kode("st-out-semua", 100%, [Hapus Semua]),
  kode("st-out-kosong", 100%, [Pop Saat Kosong]),
)
