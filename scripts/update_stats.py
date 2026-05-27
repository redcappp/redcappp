import json
import re
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
STATS = ROOT / "stats"
ASSETS.mkdir(exist_ok=True)
STATS.mkdir(exist_ok=True)


def get(url, headers=None, data=None):
    base_headers = {"User-Agent": "Mozilla/5.0 GitHub Profile Stats Bot"}
    base_headers.update(headers or {})
    req = urllib.request.Request(url, headers=base_headers, data=data)
    with urllib.request.urlopen(req, timeout=25) as response:
        return response.read().decode("utf-8", errors="replace")


def codeforces():
    data = json.loads(get("https://codeforces.com/api/user.info?handles=redcapp"))
    user = data["result"][0]
    return {
        "current": user.get("rating"),
        "max": user.get("maxRating"),
        "rank": user.get("rank"),
        "max_rank": user.get("maxRank"),
    }


def atcoder():
    html = get("https://atcoder.jp/users/redcappp")
    def find_row(label):
        match = re.search(
            rf"<th[^>]*>{label}.*?</th><td>(.*?)</td>",
            html,
            flags=re.S,
        )
        if not match:
            return None
        cleaned = re.sub(r"<[^>]+>", " ", match.group(1)).strip()
        direct = re.search(r"(\d+)", cleaned)
        return int(direct.group(1)) if direct else None

    def find_rank():
        match = re.search(r"<span class=\"bold\">([^<]+)</span>", html)
        return match.group(1).strip() if match else "5 Kyu"

    return {
        "current": find_row("Rating"),
        "max": find_row("Highest Rating"),
        "matches": find_row("Rated Matches"),
        "rank": find_rank(),
    }


def repository_totals():
    return {"published": 29, "featured": 10}


def profile_header_svg():
    return """<svg width="1000" height="360" viewBox="0 0 1000 360" xmlns="http://www.w3.org/2000/svg">
<defs>
  <linearGradient id="g" x1="0" x2="1" y1="0" y2="1">
    <stop offset="0%" stop-color="#0ea5e9"/>
    <stop offset="52%" stop-color="#22c55e"/>
    <stop offset="100%" stop-color="#f97316"/>
  </linearGradient>
  <radialGradient id="soft" cx="50%" cy="42%" r="70%">
    <stop offset="0%" stop-color="#1d4ed8" stop-opacity=".32"/>
    <stop offset="55%" stop-color="#0f172a" stop-opacity=".12"/>
    <stop offset="100%" stop-color="#0f172a" stop-opacity="0"/>
  </radialGradient>
  <filter id="blur">
    <feGaussianBlur stdDeviation="18"/>
  </filter>
  <pattern id="grid" width="54" height="54" patternUnits="userSpaceOnUse">
    <path d="M54 0H0V54" fill="none" stroke="#1e293b" stroke-width="1"/>
  </pattern>
  <style>
    @keyframes driftA { 0% { transform: translateX(-110px) translateY(0); } 100% { transform: translateX(95px) translateY(-10px); } }
    @keyframes driftB { 0% { transform: translateX(100px) translateY(10px); } 100% { transform: translateX(-120px) translateY(-4px); } }
    @keyframes breathe { 0%,100% { opacity:.20; transform:scale(.96); } 50% { opacity:.42; transform:scale(1.08); } }
    @keyframes sweep { 0% { transform: translateX(-260px); opacity:.15; } 50% { opacity:.45; } 100% { transform: translateX(1160px); opacity:.08; } }
    @keyframes type1 { 0%,20%{opacity:1} 23%,100%{opacity:0} }
    @keyframes type2 { 0%,24%{opacity:0} 27%,46%{opacity:1} 49%,100%{opacity:0} }
    @keyframes type3 { 0%,50%{opacity:0} 53%,72%{opacity:1} 75%,100%{opacity:0} }
    @keyframes type4 { 0%,76%{opacity:0} 79%,97%{opacity:1} 100%{opacity:0} }
    .wave-a { animation: driftA 10s ease-in-out infinite alternate; transform-origin:center; }
    .wave-b { animation: driftB 13s ease-in-out infinite alternate; transform-origin:center; }
    .orb { animation: breathe 4.8s ease-in-out infinite; transform-origin:center; }
    .sweep { animation: sweep 7s linear infinite; }
    .line1 { animation: type1 10s infinite; }
    .line2 { animation: type2 10s infinite; }
    .line3 { animation: type3 10s infinite; }
    .line4 { animation: type4 10s infinite; }
  </style>
</defs>
<rect width="1000" height="360" rx="28" fill="#0b1120"/>
<rect width="1000" height="360" fill="url(#soft)"/>
<rect width="1000" height="360" fill="url(#grid)" opacity=".34"/>
<path class="wave-a" d="M-160 250 C60 138 210 308 390 214 C620 94 740 270 1160 148 V360 H-160 Z" fill="url(#g)" opacity=".32"/>
<path class="wave-b" d="M-180 300 C70 198 250 338 465 260 C660 190 825 292 1180 222 V360 H-180 Z" fill="#22c55e" opacity=".16"/>
<path class="wave-b" d="M-120 96 C120 30 242 118 420 72 C650 12 760 92 1120 36" fill="none" stroke="#38bdf8" stroke-width="2" opacity=".28"/>
<circle class="orb" cx="125" cy="95" r="76" fill="#22c55e" opacity=".24" filter="url(#blur)"/>
<circle class="orb" cx="855" cy="96" r="90" fill="#0ea5e9" opacity=".22" filter="url(#blur)"/>
<rect class="sweep" x="0" y="0" width="170" height="360" fill="#ffffff" opacity=".10" transform="skewX(-18)"/>
<text x="500" y="102" text-anchor="middle" font-family="Arial, sans-serif" font-size="42" font-weight="800" fill="#ffffff">Divyansh Kumar Singh Chauhan</text>
<text x="500" y="146" text-anchor="middle" font-family="Arial, sans-serif" font-size="20" font-weight="600" fill="#dbeafe">Competitive Programmer | ML + Systems Builder | IIIT Naya Raipur</text>
<g font-family="Consolas, monospace" font-size="19" text-anchor="middle">
  <text class="line1" x="500" y="208" fill="#bbf7d0">ICPC Regionalist 2025 | Codeforces Expert | LeetCode Top 3.82%</text>
  <text class="line2" x="500" y="208" fill="#bbf7d0">RAG platforms, cybersecurity ML, and operating-system research</text>
  <text class="line3" x="500" y="208" fill="#bbf7d0">YT AI Agent | FileWorld | OffChat Suite | CogniGen</text>
  <text class="line4" x="500" y="208" fill="#bbf7d0">Problem solving, product craft, and useful AI systems</text>
</g>
<text x="500" y="270" text-anchor="middle" font-family="Arial, sans-serif" font-size="15" font-weight="600" fill="#fed7aa">Codeforces Expert | CodeChef 4 star | AtCoder 5 Kyu | 1500+ problems solved</text>
</svg>"""


def project_glimpses_svg():
    projects = [
        ("CogniGen", "Adaptive RAG assessment platform", "FastAPI + React + PostgreSQL"),
        ("Adaptive CNN Malware Guard", "Binary-to-image malware classifier", "DenseNet121, 93.72% val acc"),
        ("YT AI Agent", "Autonomous YouTube analytics + upload agent", "YouTube API, trend planning, video generation"),
        ("FileWorld", "Android all-in-one file workspace", "Kotlin, local conversion, ZIP, sharing"),
        ("OffChat Suite", "Simulator + compression + Android implementation", "Nearby Connections, TTL, ACKs, buffers"),
        ("AI Vulnerability Scanner", "Agentic security triage workflow", "Python + LLM orchestration"),
        ("Vehicle QR Generator", "Structured vehicle QR app", "HTML, CSS, JS"),
        ("Unity Microgames", "FPS + platformer game prototypes", "Unity Assets/Packages/Settings"),
    ]
    cards = []
    for i, (name, desc, stack) in enumerate(projects):
        col = i % 2
        row = i // 2
        x = 28 + col * 462
        y = 58 + row * 112
        delay = i * 0.22
        cards.append(f"""
<g class="card" style="animation-delay:{delay}s">
  <rect x="{x}" y="{y}" width="430" height="88" rx="14" fill="#111827" stroke="#334155"/>
  <rect class="shine" x="{x-130}" y="{y}" width="110" height="88" fill="#ffffff" opacity=".08" transform="skewX(-18)"/>
  <circle cx="{x+390}" cy="{y+20}" r="32" fill="#0ea5e9" opacity=".10"/>
  <text x="{x+20}" y="{y+30}" class="pname">{name}</text>
  <text x="{x+20}" y="{y+54}" class="pdesc">{desc}</text>
  <text x="{x+20}" y="{y+75}" class="pstack">{stack}</text>
</g>""")
    return f"""<svg width="950" height="530" viewBox="0 0 950 530" xmlns="http://www.w3.org/2000/svg">
<style>
@keyframes floatCard {{ 0%,100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-7px); }} }}
@keyframes glide {{ 0% {{ transform: translateX(0) skewX(-18deg); }} 100% {{ transform: translateX(620px) skewX(-18deg); }} }}
@keyframes slowWave {{ 0% {{ transform: translateX(-80px); }} 100% {{ transform: translateX(80px); }} }}
.title{{font:800 26px Arial;fill:#fff}}.sub{{font:14px Arial;fill:#94a3b8}}.pname{{font:700 18px Arial;fill:#93c5fd}}.pdesc{{font:14px Arial;fill:#e5e7eb}}.pstack{{font:13px Consolas;fill:#bbf7d0}}
.card{{animation:floatCard 6s ease-in-out infinite; transform-origin:center}}
.shine{{animation:glide 5.8s ease-in-out infinite}}
.wave{{animation:slowWave 10s ease-in-out infinite alternate}}
</style>
<rect width="950" height="530" rx="18" fill="#0b1120"/>
<path class="wave" d="M-80 480 C140 380 270 522 450 438 C650 344 750 486 1030 398 V530 H-80 Z" fill="#0ea5e9" opacity=".12"/>
<path class="wave" d="M-80 508 C180 430 330 552 520 490 C690 434 810 512 1030 462 V530 H-80 Z" fill="#22c55e" opacity=".10"/>
<text x="28" y="34" class="title">Project Glimpses</text>
<text x="260" y="34" class="sub">things I have been building lately</text>
{''.join(cards)}
</svg>"""


def featured_work_svg():
    items = [
        ("CogniGen", "Adaptive RAG cognitive assessment", "multi-hop retrieval | adversarial filtering | teacher dashboards"),
        ("YT AI Agent", "Autonomous YouTube analytics and upload workflow", "trend signals | upload timing | generated scripts and metadata"),
        ("OffChat Suite", "Offline-first messaging research project", "mesh simulation | compression benchmark | Android Nearby Connections"),
        ("FileWorld", "Android file-workspace utility", "file picker | conversion | compression | ZIP | Play Store assets"),
    ]
    nodes = []
    for i, (name, desc, detail) in enumerate(items):
        x = 78 + (i % 2) * 420
        y = 86 + (i // 2) * 144
        delay = i * 0.35
        nodes.append(f"""
<g class="node" style="animation-delay:{delay}s">
  <circle cx="{x}" cy="{y}" r="54" fill="#111827" stroke="#38bdf8" stroke-width="2"/>
  <circle cx="{x}" cy="{y}" r="38" fill="#0ea5e9" opacity=".12"/>
  <text x="{x}" y="{y-6}" class="n">{name}</text>
  <text x="{x}" y="{y+15}" class="tag">featured</text>
  <text x="{x+78}" y="{y-16}" class="d">{desc}</text>
  <text x="{x+78}" y="{y+14}" class="m">{detail}</text>
</g>""")
    return f"""<svg width="950" height="360" viewBox="0 0 950 360" xmlns="http://www.w3.org/2000/svg">
<style>
@keyframes stream {{ from {{ stroke-dashoffset: 260; }} to {{ stroke-dashoffset: 0; }} }}
@keyframes hover {{ 0%,100% {{ transform:translateY(0); }} 50% {{ transform:translateY(-8px); }} }}
@keyframes shimmer {{ 0% {{ opacity:.10; }} 50% {{ opacity:.28; }} 100% {{ opacity:.10; }} }}
.title{{font:800 28px Arial;fill:#fff}}.sub{{font:14px Arial;fill:#94a3b8}}.n{{font:800 15px Arial;fill:#fff;text-anchor:middle}}.tag{{font:12px Consolas;fill:#bbf7d0;text-anchor:middle}}.d{{font:700 17px Arial;fill:#dbeafe}}.m{{font:13px Consolas;fill:#fed7aa}}.node{{animation:hover 7s ease-in-out infinite; transform-origin:center}}.path{{stroke-dasharray:14 18;animation:stream 7s linear infinite}}.glow{{animation:shimmer 4.5s ease-in-out infinite}}
</style>
<rect width="950" height="360" rx="20" fill="#0b1120"/>
<circle class="glow" cx="820" cy="48" r="90" fill="#22c55e"/>
<circle class="glow" cx="120" cy="302" r="120" fill="#0ea5e9"/>
<path class="path" d="M132 86 C280 26 360 182 498 86 C650 -18 745 152 918 76" fill="none" stroke="#38bdf8" stroke-width="2" opacity=".22"/>
<path class="path" d="M132 230 C270 150 392 306 498 230 C650 124 766 292 918 220" fill="none" stroke="#22c55e" stroke-width="2" opacity=".18"/>
<text x="28" y="38" class="title">Featured Work</text>
<text x="240" y="38" class="sub">projects with the strongest engineering signal</text>
{''.join(nodes)}
</svg>"""


def activity_svg(stats):
    return f"""<svg width="900" height="180" viewBox="0 0 900 180" xmlns="http://www.w3.org/2000/svg">
<style>
@keyframes breathe {{ 0%,100% {{ opacity:.18; transform:scale(.98); }} 50% {{ opacity:.36; transform:scale(1.03); }} }}
@keyframes slide {{ from {{ transform:translateX(-80px); }} to {{ transform:translateX(80px); }} }}
.label{{font:700 15px Arial;fill:#cbd5e1}}.num{{font:800 34px Arial;fill:#fff}}.small{{font:13px Arial;fill:#94a3b8}}.glow{{animation:breathe 5s ease-in-out infinite; transform-origin:center}}.flow{{animation:slide 9s ease-in-out infinite alternate}}
</style>
<rect width="900" height="180" rx="18" fill="#0f172a"/>
<path class="flow" d="M-80 146 C120 84 255 178 410 126 C610 60 718 150 980 94" fill="none" stroke="#22c55e" stroke-width="3" opacity=".20"/>
<circle class="glow" cx="806" cy="48" r="70" fill="#0ea5e9"/>
<text x="36" y="42" class="label">Portfolio Snapshot</text>
<text x="36" y="95" class="num">{stats['repositories']['published']}</text>
<text x="36" y="124" class="small">published repositories</text>
<text x="260" y="95" class="num">{stats['repositories']['featured']}</text>
<text x="260" y="124" class="small">featured engineering projects</text>
<text x="500" y="95" class="num">1500+</text>
<text x="500" y="124" class="small">algorithmic problems solved</text>
<text x="700" y="95" class="num">9.31</text>
<text x="700" y="124" class="small">CGPA / 10</text>
</svg>"""


def codechef():
    html = get("https://www.codechef.com/users/redcapp")
    current = re.search(r"CodeChef Rating.*?Highest Rating\s*(\d+)", html, flags=re.S)
    solved = re.search(r"Total Problems Solved:\s*(\d+)", html)
    rating = re.search(r">\s*(\d{4})\s*<.*?Rating", html, flags=re.S)
    return {
        "current": int(rating.group(1)) if rating else 1824,
        "max": int(current.group(1)) if current else 1852,
        "solved": int(solved.group(1)) if solved else 832,
    }


def leetcode():
    body = json.dumps({
        "query": """
        query userProfile($username: String!) {
          matchedUser(username: $username) {
            submitStatsGlobal { acSubmissionNum { difficulty count } }
          }
          userContestRanking(username: $username) {
            rating
            topPercentage
            attendedContestsCount
          }
        }
        """,
        "variables": {"username": "Redcapp"},
    }).encode()
    try:
        data = json.loads(get(
            "https://leetcode.com/graphql/",
            headers={"Content-Type": "application/json", "Referer": "https://leetcode.com/u/Redcapp/"},
            data=body,
        ))
    except Exception:
        return {"solved": 373, "rating": 1925.21, "top_percentage": 3.82, "contests": 28}
    solved = data["data"]["matchedUser"]["submitStatsGlobal"]["acSubmissionNum"][0]["count"]
    contest = data["data"]["userContestRanking"]
    return {
        "solved": solved,
        "rating": round(contest["rating"], 2),
        "top_percentage": contest["topPercentage"],
        "contests": contest["attendedContestsCount"],
    }


def youtube():
    html = get("https://www.youtube.com/channel/UCRZ2r96UTZtdes8CFx9kSXA/about")
    sub = re.search(r'"subscriberCountText":"([^"]+)"', html)
    views = re.search(r'"viewCountText":"([^"]+)"', html)
    return {
        "channel": "Redcapp",
        "subscribers": sub.group(1) if sub else "30 subscribers",
        "views": views.group(1) if views else "2,209 views",
    }


def safe(fetcher, fallback):
    try:
        return fetcher()
    except Exception:
        return fallback


def svg(stats):
    cards = [
        ("Codeforces", "Expert", f"{stats['codeforces']['current']} current", f"{stats['codeforces']['max']} max"),
        ("CodeChef", "4 star", f"{stats['codechef']['current']} current", f"{stats['codechef']['max']} max | {stats['codechef']['solved']} solved"),
        ("AtCoder", stats['atcoder'].get("rank", "5 Kyu"), f"{stats['atcoder']['current']} current", f"{stats['atcoder']['max']} max | {stats['atcoder']['matches']} rated"),
        ("LeetCode", "Top 3.82%", f"{stats['leetcode']['rating']} rating", f"{stats['leetcode']['solved']} solved | {stats['leetcode']['contests']} contests"),
        ("YouTube", "Redcapp", stats['youtube']['subscribers'], stats['youtube']['views']),
    ]
    rows = []
    for i, (name, rank, primary, secondary) in enumerate(cards):
        x = 28 + (i % 2) * 420
        y = 62 + (i // 2) * 100
        if i == 4:
            x = 238
            y = 262
        delay = i * 0.28
        rows.append(f"""
<g class="stat" style="animation-delay:{delay}s">
  <rect x="{x}" y="{y}" width="380" height="76" rx="13" fill="#111827" stroke="#334155"/>
  <path class="spark" d="M{x+18} {y+65} C{x+110} {y+42} {x+210} {y+84} {x+360} {y+34}" fill="none" stroke="#22c55e" stroke-width="2" opacity=".18"/>
  <text x="{x+18}" y="{y+28}" class="name">{name}</text>
  <text x="{x+190}" y="{y+28}" class="rank">{rank}</text>
  <text x="{x+18}" y="{y+52}" class="value">{primary}</text>
  <text x="{x+190}" y="{y+52}" class="muted">{secondary}</text>
</g>""")
    return f"""<svg width="880" height="370" viewBox="0 0 880 370" fill="none" xmlns="http://www.w3.org/2000/svg">
<style>
@keyframes lift {{ 0%,100% {{ transform:translateY(0); }} 50% {{ transform:translateY(-5px); }} }}
@keyframes wave {{ 0% {{ transform:translateX(-90px); }} 100% {{ transform:translateX(90px); }} }}
.bg{{fill:#0f172a}}.title{{font:800 24px Arial;fill:#fff}}.name{{font:700 17px Arial;fill:#93c5fd}}.rank{{font:700 15px Arial;fill:#fed7aa}}.value{{font:700 15px Arial;fill:#dcfce7}}.muted{{font:13px Arial;fill:#94a3b8}}.stat{{animation:lift 6.5s ease-in-out infinite; transform-origin:center}}.flow{{animation:wave 9s ease-in-out infinite alternate}}
</style>
<rect class="bg" width="880" height="370" rx="18"/>
<path class="flow" d="M-80 318 C90 238 230 360 405 286 C590 208 730 338 960 250 V370 H-80 Z" fill="#0ea5e9" opacity=".10"/>
<path class="flow" d="M-80 348 C130 292 300 382 490 328 C650 282 780 352 960 310 V370 H-80 Z" fill="#22c55e" opacity=".09"/>
<text x="28" y="34" class="title">Live Programming Stats</text>
{''.join(rows)}
</svg>"""


def main():
    stats = {
        "codeforces": safe(codeforces, {"current": 1624, "max": 1673, "rank": "expert", "max_rank": "expert"}),
        "codechef": safe(codechef, {"current": 1824, "max": 1852, "solved": 832}),
        "atcoder": safe(atcoder, {"current": 1075, "max": 1078, "matches": 64}),
        "leetcode": safe(leetcode, {"solved": 373, "rating": 1925.21, "top_percentage": 3.82, "contests": 28}),
        "youtube": safe(youtube, {"channel": "Redcapp", "subscribers": "30 subscribers", "views": "2,209 views"}),
        "repositories": repository_totals(),
    }
    (STATS / "competitive.json").write_text(json.dumps(stats, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
