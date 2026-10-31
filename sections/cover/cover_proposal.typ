#import "../../config.typ": *

#page(
  numbering: none,
  header: none,
  footer: none,
)[
  #align(horizon + center)[
    #text(1.2em, weight: "bold")[#upper[
      #context {
        let current_page = counter(page).get().first()
        if current_page == 1 {
          report_type
        } else {
          report_type2
        }
      }
    ]]
    \
    #text(1.2em, weight: "bold")[#upper[#title_block]]
    #image("../../media/logo_icl.png", width: 2.6in)
    #align(left)[
      #pad(left: 4cm)[
        #grid(
          columns: (auto, auto, 1fr),
          row-gutter: 1em,
          column-gutter: 1em,
          [NAMA], [:], [#author_name],
          [NIM], [:], [#author_id],
          [KELAS], [:], [#author_class],
          [DOSEN], [:], [#advisor_name],
          [NO. PC], [:], [#author_pc],
          [ASISTEN], [:], [1. #reviewer_names.first()],
          ..for (i, name) in reviewer_names.slice(1).enumerate() {
          ([], [:], [#(i + 2). #name])
        }
        )
      ]
    ]
    #text(weight: "bold")[
      #upper[
        \
        \
        #campus_name \
        #program_of_study\
        #year
      ]
    ]
  ]
]

