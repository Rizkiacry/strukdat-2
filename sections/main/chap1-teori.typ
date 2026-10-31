#let kode(file, w, cap) = figure(
  image("../../media/" + file + ".png", width: w),
  kind: "gambar",
  caption: cap,
)

= LAPORAN TEORI

== Delete Kiri, Delete Kanan, dan Delete Tengah

Di single linked list, tiap node cuma punya pointer `next` @wiki-ll. Jadi sebelum node dibuang, pointer di sekitarnya harus disambung ulang dulu, kalau tidak sisa list-nya hilang. Pointer `awal` (head) dan `akhir` (tail) juga harus ikut diperbarui.

*Delete kiri* (`hapus_awal`) membuang node paling depan. Alurnya: cek `awal == NULL` (list kosong, berhenti), simpan node depan ke `hapus`, geser `awal = awal->next`, lalu `delete hapus` @cppref-delete. Kalau list cuma punya satu node, `akhir` juga jadi `NULL`. Tidak ada traversal, jadi cost-nya $O(1)$.

*Delete kanan* (`hapus_akhir`) membuang node paling belakang. Pointer `akhir` menunjuk node terakhir, tapi tidak ada pointer ke node sebelumnya. Jadi list ditelusuri dari `awal` sampai ketemu `b1` dengan `b1->next == akhir`, lalu `b1->next = NULL` dan `akhir = b1`. Karena ada traversal, cost-nya $O(n)$.

*Delete tengah* (`hapus_tengah`) membuang node berisi nilai `x`. Cari node sebelumnya (`b`), lalu lewati target dengan `b->next = b2` (`b2` = node sesudah target). Kalau `x` ada di ujung, fungsi tinggal memanggil delete kiri/kanan karena `awal`/`akhir` ikut berubah. Kalau `x` tidak ketemu, tampilkan pesan tidak valid.

#grid(
  columns: (1.44fr, 1.10fr),
  column-gutter: 0.4cm,
  align: bottom,
  kode("ll-asli-hapus_awal", 100%, [`hapus_awal`]),
  kode("ll-asli-hapus_akhir", 100%, [`hapus_akhir`]),
)

#grid(
  columns: (1.15fr, 1fr),
  column-gutter: 0.5cm,
  align: horizon,
  kode("ll-asli-hapus_tengah", 100%, [`hapus_tengah`]),
  figure(
    table(
      columns: (auto, 1fr, auto),
      align: left,
      inset: 4pt,
      [*Operasi*], [*Pointer berubah*], [*Cost*],
      [Kiri], [`awal` (+ `akhir` jika 1 node)], [$O(1)$],
      [Kanan], [`b1->next`, `akhir`], [$O(n)$],
      [Tengah], [`b->next` (+ `akhir` jika target terakhir)], [$O(n)$],
    ),
    kind: "tabel",
    caption: [Perbandingan Delete],
  ),
)

== Stack

Stack adalah struktur data LIFO (_Last In First Out_): data yang masuk terakhir keluar pertama @wiki-stack. Di program ini stack dibuat dari linked list. `atas` jadi puncak (top) dan `jumlah` membatasi maksimal 10 data. Operasi utamanya:

- *Push* (`tambah_stack`): kalau `jumlah == 10`, stack penuh. Kalau belum, buat node baru, sambungkan `data->next = atas`, baru `atas = data`. Urutannya penting, kalau `atas` diubah duluan node lama hilang.
- *Pop* (`hapus_stack`): kalau `atas == NULL`, stack kosong. Kalau tidak, simpan `atas` ke `hapus`, geser `atas = atas->next`, lalu `jumlah--`.
- *Hapus semua* (`hapus_semua`): pop diulang sampai `atas == NULL`, lalu `jumlah = 0`.

Push dan pop cuma menyentuh `atas`, jadi keduanya $O(1)$.

#grid(
  columns: (1.37fr, 1.82fr),
  column-gutter: 0.4cm,
  align: bottom,
  kode("st-asli-tambah_stack", 100%, [`tambah_stack` (push)]),
  kode("st-asli-hapus_stack", 100%, [`hapus_stack` (pop)]),
)
