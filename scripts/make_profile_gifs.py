from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)


def font(size, bold=False):
    names = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
    ]
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default()


F_TITLE = font(42, True)
F_H2 = font(22, True)
F_BODY = font(18)
F_SMALL = font(14)
F_MONO = font(18)


def lerp(a, b, t):
    return int(a + (b - a) * t)


def gradient(size, c1, c2, c3):
    w, h = size
    img = Image.new("RGB", size)
    pix = img.load()
    for y in range(h):
        for x in range(w):
            t = (x / max(1, w - 1) + y / max(1, h - 1)) / 2
            if t < 0.55:
                k = t / 0.55
                c = tuple(lerp(c1[i], c2[i], k) for i in range(3))
            else:
                k = (t - 0.55) / 0.45
                c = tuple(lerp(c2[i], c3[i], k) for i in range(3))
            pix[x, y] = c
    return img


def centered(draw, xy, text, fnt, fill):
    x, y = xy
    box = draw.textbbox((0, 0), text, font=fnt)
    draw.text((x - (box[2] - box[0]) / 2, y), text, font=fnt, fill=fill)


def rounded_panel(draw, xy, radius=18, fill=(15, 23, 42), outline=(51, 65, 85)):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=1)


def wave(draw, width, height, phase, base, amp, fill):
    pts = []
    for x in range(-80, width + 81, 20):
        y = base + math.sin((x + phase) / 90.0) * amp + math.sin((x + phase) / 43.0) * (amp * 0.35)
        pts.append((x, y))
    poly = pts + [(width + 80, height + 80), (-80, height + 80)]
    draw.polygon(poly, fill=fill)


def make_header():
    lines = [
        "ICPC Regionalist 2025 | Codeforces Expert | LeetCode Top 3.82%",
        "RAG platforms, cybersecurity ML, OS research, and product builds",
        "YT AI Agent | FileWorld | OffChat Suite | CogniGen",
        "Problem solving, useful AI systems, and competitive programming",
    ]
    frames = []
    w, h = 1000, 330
    base = Image.new("RGBA", (w, h), (8, 15, 35, 255))
    base_draw = ImageDraw.Draw(base)
    for y in range(h):
        alpha = int(70 * (1 - y / h))
        base_draw.line((0, y, w, y), fill=(14, 165, 233, alpha))
    for i in range(24):
        img = base.copy()
        draw = ImageDraw.Draw(img)

        for x in range(-20, w, 52):
            draw.line((x + i * 2, 0, x + i * 2, h), fill=(30, 41, 59, 80), width=1)
        for y in range(0, h, 52):
            draw.line((0, y, w, y), fill=(30, 41, 59, 70), width=1)

        wave(draw, w, h, i * 13, 242, 42, (14, 165, 233, 75))
        wave(draw, w, h, -i * 10, 284, 30, (34, 197, 94, 55))
        sweep_x = -220 + (i / 43) * 1320
        draw.polygon([(sweep_x, 0), (sweep_x + 145, 0), (sweep_x - 35, h), (sweep_x - 180, h)], fill=(255, 255, 255, 25))

        draw.ellipse((70 + math.sin(i / 5) * 12, 42, 210 + math.sin(i / 5) * 12, 182), fill=(34, 197, 94, 34))
        draw.ellipse((790 + math.cos(i / 6) * 12, 38, 955 + math.cos(i / 6) * 12, 203), fill=(14, 165, 233, 36))

        centered(draw, (w / 2, 76), "Divyansh Kumar Singh Chauhan", F_TITLE, (255, 255, 255, 255))
        centered(draw, (w / 2, 128), "Competitive Programmer | ML + Systems Builder | IIIT Naya Raipur", F_H2, (219, 234, 254, 255))
        current = lines[(i // 11) % len(lines)]
        centered(draw, (w / 2, 198), current, F_MONO, (187, 247, 208, 255))
        centered(draw, (w / 2, 266), "Codeforces Expert | CodeChef 4 star | AtCoder 5 Kyu | 1500+ problems solved", F_SMALL, (254, 215, 170, 255))
        frames.append(img.convert("P", palette=Image.Palette.ADAPTIVE, colors=128))
    frames[0].save(ASSETS / "profile-header.gif", save_all=True, append_images=frames[1:], duration=120, loop=0, optimize=True)


def make_stats():
    cards = [
        ("Codeforces", "1624 current", "1673 max | Expert"),
        ("CodeChef", "1824 current", "1852 max | 832 solved"),
        ("AtCoder", "1075 current", "1078 max | 64 rated"),
        ("LeetCode", "1925.21 rating", "373 solved | Top 3.82%"),
        ("YouTube", "Redcapp", "30 subscribers | 2,209 views"),
    ]
    frames = []
    w, h = 900, 300
    for i in range(20):
        img = Image.new("RGBA", (w, h), (11, 17, 32, 255))
        draw = ImageDraw.Draw(img)
        wave(draw, w, h, i * 9, 245, 30, (14, 165, 233, 34))
        wave(draw, w, h, -i * 7, 275, 20, (34, 197, 94, 30))
        draw.text((30, 24), "Live Programming Stats", font=F_H2, fill=(255, 255, 255, 255))
        for idx, (name, primary, secondary) in enumerate(cards):
            x = 35 + (idx % 2) * 420
            y = 70 + (idx // 2) * 76
            if idx == 4:
                x = 245
                y = 222
            y += int(math.sin((i + idx * 4) / 7) * 3)
            rounded_panel(draw, (x, y, x + 370, y + 58), 14)
            draw.text((x + 18, y + 11), name, font=font(16, True), fill=(147, 197, 253, 255))
            draw.text((x + 170, y + 11), primary, font=font(15, True), fill=(220, 252, 231, 255))
            draw.text((x + 170, y + 34), secondary, font=F_SMALL, fill=(148, 163, 184, 255))
        frames.append(img.convert("P", palette=Image.Palette.ADAPTIVE, colors=128))
    frames[0].save(ASSETS / "stats.gif", save_all=True, append_images=frames[1:], duration=130, loop=0, optimize=True)


def make_projects():
    projects = [
        ("CogniGen", "Adaptive RAG assessment platform"),
        ("YT AI Agent", "YouTube analytics and upload automation"),
        ("FileWorld", "Android all-in-one file workspace"),
        ("OffChat Suite", "Simulation, compression, and Android implementation"),
        ("Adaptive CNN Malware Guard", "Binary-to-image malware classifier"),
        ("AI Vulnerability Scanner", "Agentic security triage workflow"),
    ]
    frames = []
    w, h = 950, 390
    for i in range(22):
        img = Image.new("RGBA", (w, h), (11, 17, 32, 255))
        draw = ImageDraw.Draw(img)
        wave(draw, w, h, i * 7, 330, 34, (14, 165, 233, 35))
        wave(draw, w, h, -i * 8, 365, 22, (34, 197, 94, 32))
        draw.text((28, 24), "Featured Work", font=F_H2, fill=(255, 255, 255, 255))
        draw.text((225, 30), "projects with the strongest engineering signal", font=F_SMALL, fill=(148, 163, 184, 255))
        for idx, (name, desc) in enumerate(projects):
            x = 40 + (idx % 2) * 455
            y = 78 + (idx // 2) * 92 + int(math.sin((i + idx * 5) / 8) * 4)
            rounded_panel(draw, (x, y, x + 410, y + 68), 16)
            draw.ellipse((x + 342, y + 10, x + 388, y + 56), fill=(14, 165, 233, 30))
            draw.text((x + 18, y + 13), name, font=font(17, True), fill=(147, 197, 253, 255))
            draw.text((x + 18, y + 40), desc, font=F_SMALL, fill=(226, 232, 240, 255))
        frames.append(img.convert("P", palette=Image.Palette.ADAPTIVE, colors=128))
    frames[0].save(ASSETS / "featured-work.gif", save_all=True, append_images=frames[1:], duration=125, loop=0, optimize=True)


def make_activity():
    frames = []
    w, h = 900, 150
    nums = [("29", "published repositories"), ("10", "featured projects"), ("1500+", "problems solved"), ("9.31", "CGPA / 10")]
    for i in range(18):
        img = Image.new("RGBA", (w, h), (15, 23, 42, 255))
        draw = ImageDraw.Draw(img)
        wave(draw, w, h, i * 8, 124, 18, (34, 197, 94, 32))
        draw.text((32, 24), "Portfolio Snapshot", font=font(16, True), fill=(203, 213, 225, 255))
        for idx, (num, label) in enumerate(nums):
            x = 35 + idx * 215
            draw.text((x, 62), num, font=font(34, True), fill=(255, 255, 255, 255))
            draw.text((x, 104), label, font=F_SMALL, fill=(148, 163, 184, 255))
        frames.append(img.convert("P", palette=Image.Palette.ADAPTIVE, colors=128))
    frames[0].save(ASSETS / "activity.gif", save_all=True, append_images=frames[1:], duration=140, loop=0, optimize=True)


if __name__ == "__main__":
    make_header()
    make_stats()
    make_projects()
    make_activity()
    print("profile gifs generated")
