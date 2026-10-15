"""Firma de correo estilo fastfetch: logo ASCII de Arch + ficha, paleta Tokyo Night.
Fotograma 0 = firma completa (20 ms) para clientes que no animan; se reproduce una vez."""
import sys
from PIL import Image, ImageDraw, ImageFont

S = 2
W = 414
BG, BAR, LINEA = "#1a1b26", "#16161e", "#292e42"
DIM, FG, ARCH, BLANCO = "#565f89", "#c0caf5", "#1793d1", "#e0e6ff"
F = "/usr/share/fonts/TTF/JetBrainsMonoNerdFontMono-"
reg, bold, peq = (ImageFont.truetype(F + "Regular.ttf", 13 * S), ImageFont.truetype(F + "Bold.ttf", 13 * S),
                  ImageFont.truetype(F + "Regular.ttf", 11 * S))
CW = reg.getlength("M") / S                       # ancho de carácter a 1x

LOGO = [r"      /\      ", r"     /  \     ", r"    /\   \    ", r"   /      \   ",
        r"  /   ,,   \  ", r" /   |  |  -\ ", r"/_-''    ''-_\ "]
INFO = [
    [("ekaitz", ARCH, bold), ("@", FG, bold), ("cachyos", ARCH, bold)],
    [("─" * 14, DIM, reg)],
    [("Name   ", ARCH, bold), ("Ekaitz Llano Alonso", BLANCO, bold)],
    [("Role   ", ARCH, bold), ("Técnico Modern Workplace", FG, reg)],
    [("OS     ", ARCH, bold), ("CachyOS · Linux", FG, reg)],
    [("Stack  ", ARCH, bold), ("Linux · Microsoft 365", FG, reg)],
    [("Git    ", ARCH, bold), ("github.com/EkaitzLlano", FG, reg)],
]
LH, X0, TOP_CMD = 19, 22, 47
TOP_INFO = TOP_CMD + LH + 8
XI = X0 + 15 * CW + 6
TOP_FIN = TOP_INFO + len(INFO) * LH + 8
H = TOP_FIN + LH + 9
CMD = "fastfetch"

def base(d):
    d.rounded_rectangle((0, 0, W * S - 1, H * S - 1), radius=7 * S, fill=BG)
    d.rounded_rectangle((0, 0, W * S - 1, 31 * S), radius=7 * S, fill=BAR)
    d.rectangle((0, 20 * S, W * S - 1, 31 * S), fill=BAR)
    d.line((0, 31 * S, W * S, 31 * S), fill=LINEA, width=S)
    for i, c in enumerate((ARCH, LINEA, LINEA)):
        cx = (19 + i * 16) * S
        d.ellipse((cx - 5 * S, 10.5 * S, cx + 5 * S, 20.5 * S), fill=c)
    d.text((64 * S, 19.8 * S), "ekaitz@cachyos ~", font=peq, fill=DIM, anchor="ls")
    d.text(((W - 14) * S, 19.8 * S), "fish", font=peq, fill=DIM, anchor="rs")

def bl(top): return (top + 14) * S              # línea base dentro de la caja de 19 px

def fotograma(nchar, nlin, final, cursor):
    im = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im); base(d)
    d.text((X0 * S, bl(TOP_CMD)), "❯", font=bold, fill=ARCH, anchor="ls")
    x = X0 * S + d.textlength("$ ", font=reg)
    d.text((x, bl(TOP_CMD)), CMD[:nchar], font=reg, fill=FG, anchor="ls")
    if not final and nlin == 0 and cursor:
        cx = x + d.textlength(CMD[:nchar], font=reg)
        d.rectangle((cx, bl(TOP_CMD) - 11 * S, cx + CW * S - S, bl(TOP_CMD) + 3 * S), fill=ARCH)
    for i in range(min(nlin, len(INFO))):
        top = TOP_INFO + i * LH
        if i < len(LOGO): d.text((X0 * S, bl(top)), LOGO[i], font=bold, fill=ARCH, anchor="ls")
        x = XI * S
        for txt, col, fnt in INFO[i]:
            d.text((x, bl(top)), txt, font=fnt, fill=col, anchor="ls"); x += d.textlength(txt, font=fnt)
        if i == 6: d.line((XI * S + d.textlength("Git    ", font=bold), bl(top) + 4 * S, x, bl(top) + 4 * S), fill=LINEA, width=S)
    if final:
        d.text((X0 * S, bl(TOP_FIN)), "❯", font=bold, fill=ARCH, anchor="ls")
        if cursor:
            cx = X0 * S + d.textlength("$ ", font=reg)
            d.rectangle((cx, bl(TOP_FIN) - 11 * S, cx + CW * S - S, bl(TOP_FIN) + 3 * S), fill=ARCH)
    return im

N = len(INFO)
cuadros = [(fotograma(len(CMD), N, True, True), 20)]                       # respaldo estático
cuadros += [(fotograma(0, 0, False, True), 500), (fotograma(0, 0, False, False), 400)]
for k in range(1, len(CMD) + 1): cuadros.append((fotograma(k, 0, False, True), 75))
cuadros.append((fotograma(len(CMD), 0, False, True), 350))
for n in range(1, N + 1): cuadros.append((fotograma(len(CMD), n, False, False), 70))
for _ in range(6): cuadros += [(fotograma(len(CMD), N, True, True), 550), (fotograma(len(CMD), N, True, False), 550)]
cuadros.append((fotograma(len(CMD), N, True, True), 1000))
ims = [c[0] for c in cuadros]
ims[0].save(sys.argv[1], save_all=True, append_images=ims[1:], duration=[c[1] for c in cuadros],
            disposal=1, optimize=True)
print(f"{len(ims)} fotogramas, {sum(c[1] for c in cuadros)/1000:.1f} s")
