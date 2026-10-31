# Generate diagram alur: PNG (preview) + .drawio (bisa dibuka & diedit di draw.io)
import os, html
from PIL import Image, ImageDraw, ImageFont
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
S = 2  # scale PNG
SIZE = {"term": (150, 40), "proc": (250, 50), "dec": (250, 84)}
FILL = {"term": "#e6e6e6", "proc": "#ffffff", "dec": "#fff4cc"}

class D:
    def __init__(s, name, w, h): s.name, s.w, s.h, s.n, s.e = name, w, h, {}, []
    def node(s, id, kind, text, x, y, size=None):
        s.n[id] = dict(kind=kind, text=text, x=x, y=y, wh=size or SIZE[kind])
    def anchor(s, id, p):
        n = s.n[id]; w, h = n["wh"]; x, y = n["x"], n["y"]
        return {"t": (x, y - h / 2), "b": (x, y + h / 2), "l": (x - w / 2, y), "r": (x + w / 2, y)}[p]
    def edge(s, a, pa, b, pb, label=None, via=(), lpos=None):
        s.e.append(dict(a=a, pa=pa, b=b, pb=pb, label=label, via=list(via), lpos=lpos))
    def pts(s, e): return [s.anchor(e["a"], e["pa"])] + e["via"] + [s.anchor(e["b"], e["pb"])]

    def png(s, path):
        im = Image.new("RGB", (s.w * S, s.h * S), "white"); d = ImageDraw.Draw(im)
        f = ImageFont.truetype(FONT, 13 * S); fb = ImageFont.truetype(FONT, 12 * S)
        for e in s.e:
            p = [(x * S, y * S) for x, y in s.pts(e)]
            d.line(p, fill="#222222", width=2)
            (x1, y1), (x2, y2) = p[-2], p[-1]; ah = 9 * S
            if abs(x2 - x1) < 1:  # vertikal
                sg = 1 if y2 > y1 else -1; tri = [(x2, y2), (x2 - 5 * S, y2 - sg * ah), (x2 + 5 * S, y2 - sg * ah)]
            else:
                sg = 1 if x2 > x1 else -1; tri = [(x2, y2), (x2 - sg * ah, y2 - 5 * S), (x2 - sg * ah, y2 + 5 * S)]
            d.polygon(tri, fill="#222222")
            if e["label"]:
                lx, ly = e["lpos"] if e["lpos"] else (p[0][0] / S + 8, p[0][1] / S + 4)
                d.text((lx * S, ly * S), e["label"], font=fb, fill="#aa0000" if e["label"] == "Tidak" else "#116611")
        for n in s.n.values():
            w, h = n["wh"]; x, y = n["x"], n["y"]
            box = [(x - w / 2) * S, (y - h / 2) * S, (x + w / 2) * S, (y + h / 2) * S]
            k = n["kind"]
            if k == "term": d.rounded_rectangle(box, radius=h / 2 * S, fill=FILL[k], outline="#222222", width=2)
            elif k == "proc": d.rectangle(box, fill=FILL[k], outline="#222222", width=2)
            else:
                d.polygon([(x * S, box[1]), (box[2], y * S), (x * S, box[3]), (box[0], y * S)], fill=FILL[k], outline="#222222", width=2)
            lines = n["text"].split("\n"); lh = 16 * S; y0 = y * S - lh * len(lines) / 2
            for i, l in enumerate(lines):
                tw = d.textlength(l, font=f); d.text((x * S - tw / 2, y0 + i * lh), l, font=f, fill="#111111")
        im.save(path)

    def xml(s, idx):
        out = [f'<diagram name="{html.escape(s.name)}" id="d{idx}"><mxGraphModel dx="800" dy="800" grid="1" gridSize="10" page="1" pageWidth="{s.w}" pageHeight="{s.h}"><root><mxCell id="0"/><mxCell id="1" parent="0"/>']
        st = {"term": "rounded=1;arcSize=50;whiteSpace=wrap;html=1;fillColor=#e6e6e6;strokeColor=#222222;",
              "proc": "rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#222222;",
              "dec": "rhombus;whiteSpace=wrap;html=1;fillColor=#fff4cc;strokeColor=#222222;"}
        for id, n in s.n.items():
            w, h = n["wh"]; txt = html.escape(n["text"]).replace("\n", "&lt;br&gt;")
            out.append(f'<mxCell id="{s.name}-{id}" value="{txt}" style="{st[n["kind"]]}" vertex="1" parent="1"><mxGeometry x="{n["x"]-w/2}" y="{n["y"]-h/2}" width="{w}" height="{h}" as="geometry"/></mxCell>')
        ex = {"t": (0.5, 0), "b": (0.5, 1), "l": (0, 0.5), "r": (1, 0.5)}
        for i, e in enumerate(s.e):
            a, b = ex[e["pa"]], ex[e["pb"]]
            style = (f"edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;endFill=1;"
                     f"exitX={a[0]};exitY={a[1]};entryX={b[0]};entryY={b[1]};")
            pts = "".join(f'<mxPoint x="{x}" y="{y}"/>' for x, y in e["via"])
            arr = f'<Array as="points">{pts}</Array>' if e["via"] else ""
            out.append(f'<mxCell id="{s.name}-e{i}" value="{e["label"] or ""}" style="{style}" edge="1" parent="1" source="{s.name}-{e["a"]}" target="{s.name}-{e["b"]}"><mxGeometry relative="1" as="geometry">{arr}</mxGeometry></mxCell>')
        out.append("</root></mxGraphModel></diagram>"); return "".join(out)

ds = []
M, R, L, FR = 280, 580, 90, 700  # kolom utama, kanan, kiri, kanan-jauh

# ---------- DELETE KIRI (hapus_awal)
d = D("delete-kiri", 760, 560); ds.append(d)
d.node("s", "term", "Mulai", M, 30)
d.node("c1", "dec", "awal == NULL ?", M, 110)
d.node("kosong", "proc", 'cetak "List Kosong"', R, 110)
d.node("p1", "proc", "hapus = awal", M, 200)
d.node("p2", "proc", "awal = awal->next", M, 270)
d.node("c2", "dec", "awal == NULL ?\n(list jadi kosong)", M, 355)
d.node("p3", "proc", "akhir = NULL", R, 355)
d.node("p4", "proc", "delete hapus", M, 445)
d.node("e", "term", "Selesai", M, 520)
d.edge("s", "b", "c1", "t"); d.edge("c1", "r", "kosong", "l", "Ya", lpos=(M + 130, 92))
d.edge("c1", "b", "p1", "t", "Tidak", lpos=(M + 6, 158)); d.edge("p1", "b", "p2", "t")
d.edge("p2", "b", "c2", "t"); d.edge("c2", "r", "p3", "l", "Ya", lpos=(M + 130, 337))
d.edge("c2", "b", "p4", "t", "Tidak", lpos=(M + 6, 405))
d.edge("p3", "b", "p4", "r", via=[(R, 445)]); d.edge("p4", "b", "e", "t")
d.edge("kosong", "r", "e", "r", via=[(R + 125 + 30, 110), (R + 155, 520)])

# ---------- DELETE KANAN (hapus_akhir)
d = D("delete-kanan", 800, 700); ds.append(d)
d.node("s", "term", "Mulai", M, 30)
d.node("c1", "dec", "awal == NULL ?", M, 105)
d.node("kosong", "proc", 'cetak "List Kosong"', R + 40, 105)
d.node("c2", "dec", "awal == akhir ?\n(cuma 1 node)", M, 205)
d.node("p1", "proc", "hapus = awal\nawal = akhir = NULL", 110, 305, (190, 56))
d.node("p2", "proc", "b1 = awal", M, 305, (150, 44))
d.node("c3", "dec", "b1->next != akhir ?", M, 395)
d.node("p3", "proc", "b1 = b1->next", R + 40, 395, (190, 50))
d.node("p4", "proc", "hapus = akhir\nb1->next = NULL\nakhir = b1", M, 495, (230, 64))
d.node("p5", "proc", "delete hapus", M, 590)
d.node("e", "term", "Selesai", M, 665, (150, 40))
d.edge("s", "b", "c1", "t"); d.edge("c1", "r", "kosong", "l", "Ya", lpos=(M + 130, 87))
d.edge("c1", "b", "c2", "t", "Tidak", lpos=(M + 6, 150))
d.edge("c2", "l", "p1", "t", "Ya", lpos=(M - 150, 187), via=[(110, 205)])
d.edge("c2", "b", "p2", "t", "Tidak", lpos=(M + 6, 258))
d.edge("p2", "b", "c3", "t")
d.edge("c3", "r", "p3", "l", "Ya", lpos=(M + 130, 377))
d.edge("p3", "t", "c3", "t", via=[(R + 40, 340), (M, 340)])
d.edge("c3", "b", "p4", "t", "Tidak", lpos=(M + 6, 445))
d.edge("p1", "b", "p5", "l", via=[(110, 590)]); d.edge("p4", "b", "p5", "t")
d.edge("p5", "b", "e", "t")
d.edge("kosong", "r", "e", "r", via=[(R + 40 + 125 + 20, 105), (R + 40 + 145, 665)])

# ---------- DELETE TENGAH (hapus_tengah)
d = D("delete-tengah", 800, 900); ds.append(d)
d.node("s", "term", "Mulai (x = data dicari)", M, 30, (200, 40))
d.node("c1", "dec", "awal == NULL ?", M, 105)
d.node("kosong", "proc", 'cetak "List Kosong"', R + 40, 105)
d.node("c2", "dec", "awal->info == x ?", M, 205)
d.node("pa", "proc", "hapus_awal()", 70, 205, (120, 44))
d.node("p1", "proc", "b = awal", M, 295)
d.node("c3", "dec", "b->next != NULL &&\nb->next->info != x ?", M, 385, (270, 90))
d.node("p2", "proc", "b = b->next", R + 40, 385, (170, 50))
d.node("c4", "dec", "b->next == NULL ?\n(x tidak ketemu)", M, 495, (250, 84))
d.node("inv", "proc", 'cetak "Data Tidak Valid"', R + 40, 495, (210, 50))
d.node("p3", "proc", "hapus = b->next\nb->next = hapus->next", M, 590, (250, 56))
d.node("c5", "dec", "hapus == akhir ?", M, 680)
d.node("p4", "proc", "akhir = b", 520, 680, (130, 50))
d.node("p5", "proc", "delete hapus", M, 770)
d.node("e", "term", "Selesai", M, 845)
d.edge("s", "b", "c1", "t"); d.edge("c1", "r", "kosong", "l", "Ya", lpos=(M + 130, 87))
d.edge("c1", "b", "c2", "t", "Tidak", lpos=(M + 6, 150))
d.edge("c2", "l", "pa", "r", "Ya", lpos=(M - 122, 187))
d.edge("c2", "b", "p1", "t", "Tidak", lpos=(M + 6, 250)); d.edge("p1", "b", "c3", "t")
d.edge("c3", "r", "p2", "l", "Ya", lpos=(M + 140, 367))
d.edge("p2", "t", "c3", "t", via=[(R + 40, 335), (M, 335)])
d.edge("c3", "b", "c4", "t", "Tidak", lpos=(M + 6, 440))
d.edge("c4", "r", "inv", "l", "Ya", lpos=(M + 130, 477))
d.edge("c4", "b", "p3", "t", "Tidak", lpos=(M + 6, 540)); d.edge("p3", "b", "c5", "t")
d.edge("c5", "r", "p4", "l", "Ya", lpos=(M + 130, 662))
d.edge("c5", "b", "p5", "t", "Tidak", lpos=(M + 6, 730))
d.edge("p4", "b", "p5", "r", via=[(520, 770)]); d.edge("p5", "b", "e", "t")
d.edge("pa", "b", "e", "l", via=[(70, 845)])
d.edge("kosong", "r", "e", "r", via=[(R + 40 + 105 + 20, 105), (R + 40 + 125, 845)])
d.edge("inv", "b", "e", "r", via=[(R + 40, 845)])

# ---------- STACK PUSH (tambah_stack)
d = D("stack-push", 760, 560); ds.append(d)
d.node("s", "term", "Mulai (push x)", M, 30, (170, 40))
d.node("c1", "dec", "jumlah == 10 ?", M, 110)
d.node("pen", "proc", 'cetak "Data Penuh"', R, 110)
d.node("p1", "proc", "data = new simpul\ndata->info = x", M, 205, (250, 56))
d.node("p2", "proc", "data->next = atas", M, 290)
d.node("p3", "proc", "atas = data", M, 360)
d.node("p4", "proc", "jumlah++", M, 430)
d.node("e", "term", "Selesai", M, 510)
d.edge("s", "b", "c1", "t"); d.edge("c1", "r", "pen", "l", "Ya", lpos=(M + 130, 92))
d.edge("c1", "b", "p1", "t", "Tidak", lpos=(M + 6, 158)); d.edge("p1", "b", "p2", "t")
d.edge("p2", "b", "p3", "t"); d.edge("p3", "b", "p4", "t"); d.edge("p4", "b", "e", "t")
d.edge("pen", "r", "e", "r", via=[(R + 125 + 30, 110), (R + 155, 510)])

# ---------- STACK POP (hapus_stack)
d = D("stack-pop", 760, 600); ds.append(d)
d.node("s", "term", "Mulai (pop)", M, 30, (170, 40))
d.node("c1", "dec", "atas == NULL ?", M, 110)
d.node("kos", "proc", 'cetak "Data Kosong"', R, 110)
d.node("p1", "proc", "hapus = atas", M, 205)
d.node("p2", "proc", "atas = atas->next", M, 275)
d.node("p3", "proc", "jumlah--", M, 345)
d.node("p4", "proc", "cetak hapus->info", M, 415)
d.node("p5", "proc", "delete hapus", M, 485)
d.node("e", "term", "Selesai", M, 555)
d.edge("s", "b", "c1", "t"); d.edge("c1", "r", "kos", "l", "Ya", lpos=(M + 130, 92))
d.edge("c1", "b", "p1", "t", "Tidak", lpos=(M + 6, 158))
for a, b in (("p1", "p2"), ("p2", "p3"), ("p3", "p4"), ("p4", "p5"), ("p5", "e")): d.edge(a, "b", b, "t")
d.edge("kos", "r", "e", "r", via=[(R + 125 + 30, 110), (R + 155, 555)])

# ---------- STACK HAPUS SEMUA
d = D("stack-hapus-semua", 760, 600); ds.append(d)
d.node("s", "term", "Mulai (hapus semua)", M, 30, (200, 40))
d.node("c1", "dec", "atas == NULL ?", M, 110)
d.node("kos", "proc", 'cetak "Data Kosong"', R, 110)
d.node("c2", "dec", "atas != NULL ?", M, 220)
d.node("p1", "proc", "hapus = atas\natas = atas->next\ndelete hapus", R, 220, (210, 70))
d.node("p2", "proc", "jumlah = 0", M, 330)
d.node("p3", "proc", 'cetak "Semua Data Terhapus"', M, 410, (250, 50))
d.node("e", "term", "Selesai", M, 490)
d.edge("s", "b", "c1", "t"); d.edge("c1", "r", "kos", "l", "Ya", lpos=(M + 130, 92))
d.edge("c1", "b", "c2", "t", "Tidak", lpos=(M + 6, 160))
d.edge("c2", "r", "p1", "l", "Ya", lpos=(M + 130, 202))
d.edge("p1", "t", "c2", "t", via=[(R, 170), (M, 170)])
d.edge("c2", "b", "p2", "t", "Tidak", lpos=(M + 6, 275))
d.edge("p2", "b", "p3", "t"); d.edge("p3", "b", "e", "t")
d.edge("kos", "r", "e", "r", via=[(R + 125 + 30, 110), (R + 155, 490)])

os.makedirs("diagram", exist_ok=True)
for d in ds: d.png(f"media/dg-{d.name}.png")
x = '<mxfile host="app.diagrams.net">' + "".join(d.xml(i) for i, d in enumerate(ds)) + "</mxfile>"
open("diagram/alur-kerja.drawio", "w").write(x)
print([d.name for d in ds])
