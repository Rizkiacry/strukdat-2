# Generate semua gambar laporan: screenshot kode (watermark), diff git, output terminal
import io, re, subprocess, sys, os
sys.path.insert(0, ".")
from PIL import Image, ImageDraw, ImageFont
from pygments import highlight
from pygments.lexers import CppLexer
from pygments.formatters import ImageFormatter
from drive import run

WM = "zain_akbar_rizkia_202531091"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
os.makedirs("media", exist_ok=True)

def git_show(path, rev="asli"):
    return subprocess.check_output(["git", "show", f"{rev}:{path}"], text=True).split("\n")

def block(lines, sig):
    """cari fungsi dari signature sampai kurung kurawal penutup -> (start,end) 1-based"""
    s = next(i for i, l in enumerate(lines) if l.startswith(sig))
    depth, seen = 0, False
    for i in range(s, len(lines)):
        depth += lines[i].count("{") - lines[i].count("}")
        if "{" in lines[i]: seen = True
        if seen and depth == 0: return s + 1, i + 1
    raise ValueError(sig)

def watermark(img, dark=False):
    img = img.convert("RGBA"); w, h = img.size
    f = ImageFont.truetype(FONT, max(16, w // 32)); tw = int(f.getlength(WM))
    layer = Image.new("RGBA", (int(w * 1.6), int(h * 1.6)), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    col = (255, 255, 255, 55) if dark else (120, 120, 120, 70)
    sy = f.size * 5; sx = tw + f.size * 3
    for row, y in enumerate(range(0, layer.size[1], sy)):
        for x in range(-sx + (row % 2) * sx // 2, layer.size[0], sx):
            d.text((x, y), WM, font=f, fill=col)
    layer = layer.rotate(25, resample=Image.BICUBIC)
    ox = (layer.size[0] - w) // 2; oy = (layer.size[1] - h) // 2
    return Image.alpha_composite(img, layer.crop((ox, oy, ox + w, oy + h))).convert("RGB")

def render(lines, start):
    fm = ImageFormatter(font_name="DejaVu Sans Mono", font_size=20, line_numbers=True, line_number_start=start,
        style="default", image_pad=12, line_pad=1, line_number_bg="#f0f0f0", line_number_fg="#888888",
        line_number_separator=True)
    data = highlight("\n".join(lines) + "\n", CppLexer(), fm)
    return Image.open(io.BytesIO(data)).convert("RGB")

def save_code(name, lines, a, b):
    watermark(render(lines[a - 1:b], a)).save(f"media/{name}.png")

def stitch(imgs, line=True):
    H = max(i.size[1] for i in imgs); W = sum(i.size[0] for i in imgs) + 10 * (len(imgs) - 1)
    st = Image.new("RGB", (W, H), "white"); x = 0
    for k, im in enumerate(imgs):
        st.paste(im, (x, 0)); x += im.size[0]
        if k < len(imgs) - 1:
            ImageDraw.Draw(st).line([(x + 4, 0), (x + 4, H)], fill="#cccccc", width=2); x += 10
    return st

def save_full(name, lines):
    mid = (len(lines) + 1) // 2
    st = stitch([render(lines[:mid], 1), render(lines[mid:], mid + 1)])
    watermark(st).save(f"media/{name}.png")

# ---------- source
LL, ST = "src/01-linkedlist.cpp", "src/02-stack.cpp"
for tag, path, pre in (("ll", LL, "ll"), ("st", ST, "st")):
    o = git_show(path); n = open(path).read().rstrip("\n").split("\n")
    o = [l for l in o]
    if o[-1] == "": o.pop()
    save_full(f"{pre}-0-asli", o)
    fns = ["void muncul()", "void tambah_awal", "void tambah_akhir", "void tambah_tengah",
           "void hapus_awal()", "void hapus_akhir()", "void hapus_tengah", "void main()"] if tag == "ll" else \
          ["void muncul()", "void tambah_stack", "void hapus_stack()", "void hapus_semua()", "void main()"]
    for fn in fns:
        key = re.sub(r"[^a-z_]", "", fn.replace("void ", "").split("(")[0].split(" ")[0])
        a, b = block(o, fn); save_code(f"{pre}-asli-{key}", o, a, b)
        a, b = block(n, fn.replace("void main", "int main")); save_code(f"{pre}-baru-{key}", n, a, b)
    # struct + global
    last = next(i for i, l in enumerate(o) if l.startswith("tsimpul *"))
    save_code(f"{pre}-asli-struct", o, 5, last + 1 + (1 if tag == "st" else 0))
    if tag == "ll":
        s = next(i for i, l in enumerate(o) if "switch(pilih)" in l)
        save_code("ll-asli-switch", o, s + 1, s + 26)
    else:
        s = next(i for i, l in enumerate(o) if "switch(pilih)" in l)
        save_code("st-asli-switch", o, s + 1, s + 20)

# ---------- diff (git)
def diff_img(path, name, cols=1, a="syntax", b="fix"):
    txt = subprocess.check_output(["git", "diff", "-U1", a, b, "--", path], text=True).split("\n")
    txt = [l for l in txt if not l.startswith(("diff --git", "index "))]
    while txt and txt[-1] == "": txt.pop()
    f = ImageFont.truetype(FONT, 20); lh = 27; pad = 14
    def draw(lines):
        W = int(max(f.getlength(l.replace("\t", "    ")) for l in lines)) + pad * 2
        im = Image.new("RGB", (W, lh * len(lines) + pad * 2), "white"); d = ImageDraw.Draw(im)
        for i, l in enumerate(lines):
            y = pad + i * lh
            bg, fg = None, "#222222"
            if l.startswith("+") and not l.startswith("+++"): bg, fg = "#d9f2d9", "#116611"
            elif l.startswith("-") and not l.startswith("---"): bg, fg = "#f8d7d7", "#881111"
            elif l.startswith("@@"): bg, fg = "#e4ecf7", "#224488"
            elif l.startswith(("---", "+++")): fg = "#666666"
            if bg: d.rectangle([0, y - 2, W, y + lh - 3], fill=bg)
            d.text((pad, y), l.replace("\t", "    "), font=f, fill=fg)
        return im
    if cols == 1: im = draw(txt)
    else:
        mid = (len(txt) + 1) // 2
        # jangan potong tepat di tengah hunk-header: geser ke baris @@ terdekat
        cand = [i for i, l in enumerate(txt) if l.startswith("@@") and i >= mid - 8]
        mid = cand[0] if cand else mid
        im = stitch([draw(txt[:mid]), draw(txt[mid:])])
    watermark(im).save(f"media/{name}.png")

diff_img(LL, "ll-diff", cols=2); diff_img(ST, "st-diff", cols=1)
diff_img(LL, "ll-sintaks", cols=1, a="asli", b="syntax"); diff_img(ST, "st-sintaks", cols=1, a="asli", b="syntax")

# ---------- terminal
def term(name, text, title, w_min=0):
    lines = text.rstrip("\n").split("\n"); f = ImageFont.truetype(FONT, 18); lh = 25; pad = 18; bar = 34
    W = max(int(max(f.getlength(l) for l in lines)) + pad * 2 + 20, w_min); H = bar + pad * 2 + lh * len(lines)
    im = Image.new("RGB", (W, H), "#0c0c0c"); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, bar], fill="#2d2d2d"); d.text((12, 8), title, font=ImageFont.truetype(FONT, 15), fill="#dddddd")
    for i, l in enumerate(lines): d.text((pad, bar + pad + i * lh), l, font=f, fill="#cccccc")
    watermark(im, dark=True).save(f"media/{name}.png")

def screens(out): return [s.strip("\n") for s in out.split("\f")]
def trim(scr):  # buang banner supaya screenshot ringkas
    ls = scr.split("\n"); return "\n".join(l for l in ls if not l.startswith(("====", "||")))

B = "/home/claude/build/"
# list: 1,2,3,4 ditambah, lalu hapus tengah(3) , tengah invalid, akhir, awal
seq_ll = "2 1 y 2 2 y 2 3 y 2 4 y 2 5 y 6 3 y 6 99 y 5 y 4 t".split()
out = screens(run(B + "ll_new", seq_ll, leaks=True))
sc = [trim(s) for s in out]
# pilih layar: setelah hapus tengah(3) -> idx 6 pesan; tengah invalid idx 7; akhir 8; awal 9; layar terakhir 10
term("ll-out-tengah", sc[6] + "\n" + sc[7].split("\n")[1] if False else sc[6], "C:\\TC\\BIN\\linkedlist.exe")
for i, nm in ((6, "tengah"), (7, "invalid"), (8, "akhir"), (9, "awal")):
    term(f"ll-out-{nm}", sc[i], "C:\\TC\\BIN\\linkedlist.exe")
seq_st = "1 10 y 1 20 y 1 30 y 2 y 3 y 2 t".split()
sc2 = [trim(s) for s in screens(run(B + "st_new", seq_st))]
for i, nm in ((3, "pop"), (4, "semua"), (5, "kosong")):
    term(f"st-out-{nm}", sc2[i], "C:\\TC\\BIN\\stack.exe")

# leak: asli vs baru (list)
seq_leak = "2 1 y 2 2 y 2 3 y 4 y 4 t".split()
seq_leak_st = "1 10 y 1 20 y 1 30 y 1 40 y 3 t".split()
lk_old = run(B + "ll_old", seq_leak); lk_new = run(B + "ll_new", seq_leak)
def leakpart(o):
    ls = [l for l in o.split("\n") if "ERROR: LeakSanitizer" in l or "Direct leak" in l or "SUMMARY" in l]
    return "\n".join(ls) if ls else "(tidak ada laporan leak)"
open("media/leak.txt", "w").write("ASLI:\n" + leakpart(lk_old) + "\n\nBARU:\n" + leakpart(lk_new) + "\n")
term("ll-leak-asli", "$ ./linkedlist_asli\n" + leakpart(lk_old), "bash - AddressSanitizer")
term("ll-leak-baru", "$ ./linkedlist_baru\n" + leakpart(lk_new), "bash - AddressSanitizer")
sk_old = run(B + "st_old", seq_leak_st); sk_new = run(B + "st_new", seq_leak_st)
open("media/leak.txt", "a").write("STACK ASLI:\n" + leakpart(sk_old) + "\nSTACK BARU:\n" + leakpart(sk_new) + "\n")
print(open("media/leak.txt").read())
print(sorted(os.listdir("media")))
