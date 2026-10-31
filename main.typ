#import "config.typ": *

#set document(title: [#report_type #author_name], author: author_name)
#set page(
  margin: page_margin,
  paper: "a4",
  header: context [
    #grid(
      columns: (1fr, 1fr),
      align(left)[Laporan ke-#report_number],
      align(right)[Tanggal Pengumpulan: #submit_date],
    )
  ],
)
#set text(
  font: root_font,
  size: root_font_size,
  lang: lang,
  hyphenate: hyphenate,
  top-edge: "ascender",
  bottom-edge: "descender",
)
#set par(
  justify: true,
  leading: 1em,
  first-line-indent: (
    amount: par_first_line_indent,
    all: par_first_line_indent_all,
  ),
)

// === Cover
#include "sections/cover/cover_proposal.typ"

// === Style
#set figure.caption(separator: " ")
#set figure(numbering: it => [#counter(heading).get().at(0).#it])
#show figure.where(kind: "gambar"): set figure(supplement: "Gambar")
#show figure.where(kind: "tabel"): set figure(supplement: "Tabel")
#show figure: set block(breakable: true)
#show figure.where(kind: "tabel"): set figure.caption(position: top)
#set table.header(repeat: true)

#set page(
  numbering: "1",
  footer: context [
    #grid(
      columns: (1fr, 1fr),
      align(left)[#author_id],
      align(right)[#author_name],
    )
  ],
)

#set heading(numbering: "1.")
#show heading.where(level: 1): it => [
  #counter(figure.where(kind: "tabel")).update(0)
  #counter(figure.where(kind: "gambar")).update(0)
  #pagebreak()
  #set align(center)
  #set text(heading_1_font_size, weight: heading_1_font_weight)
  #let level = counter(selector(heading).before(here()))
  #pad(bottom: heading_1_bottom_padding)[
    #upper([BAB #level.display("I") \ #it.body])
  ]
]
#show: rest => {
  for i in (2, 3) {
    rest = {
      show heading.where(level: i): it => [
        #set text(heading_n_font_size, weight: heading_n_font_weight)
        #let level = counter(selector(heading).before(here()))
        #pad(bottom: heading_n_bottom_padding)[
          #grid(
            columns: (par_first_line_indent, auto),
            [ #level.display() ],
            [ #it.body ],
          )
        ]
      ]
      rest
    }
  }
  rest
}

// === Isi
#include "sections/main/chap1-teori.typ"

#include "sections/cover/cover_proposal.typ"
#include "sections/main/chap2-praktikum.typ"

// === Daftar Pustaka
#set heading(numbering: none)
#show heading.where(level: 1): it => [
  #pagebreak()
  #set align(center)
  #set text(heading_1_font_size, weight: heading_1_font_weight)
  #pad(bottom: heading_1_bottom_padding)[#upper(it.body)]
]
= Daftar Pustaka

#bibliography(
  "citations/bibtex.bib",
  title: none,
  full: false,
  style: "citations/apa.csl",
)
