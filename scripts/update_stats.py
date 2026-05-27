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
    return """<svg width="1000" height="300" viewBox="0 0 1000 300" xmlns="http://www.w3.org/2000/svg">
<defs>
  <linearGradient id="g" x1="0" x2="1" y1="0" y2="1">
    <stop offset="0%" stop-color="#0ea5e9"/>
    <stop offset="52%" stop-color="#22c55e"/>
    <stop offset="100%" stop-color="#f97316"/>
  </linearGradient>
  <pattern id="grid" width="42" height="42" patternUnits="userSpaceOnUse">
    <path d="M42 0H0V42" fill="none" stroke="#1e293b" stroke-width="1"/>
  </pattern>
  <style>
    @keyframes drift { from { transform: translateX(-80px); } to { transform: translateX(80px); } }
    @keyframes pulse { 0%,100% { opacity:.18 } 50% { opacity:.34 } }
    @keyframes type1 { 0%,22%{opacity:1} 24%,100%{opacity:0} }
    @keyframes type2 { 0%,24%{opacity:0} 26%,48%{opacity:1} 50%,100%{opacity:0} }
    @keyframes type3 { 0%,50%{opacity:0} 52%,74%{opacity:1} 76%,100%{opacity:0} }
    @keyframes type4 { 0%,76%{opacity:0} 78%,100%{opacity:1} }
    .wave { animation: drift 8s ease-in-out infinite alternate; transform-origin:center; }
    .orb { animation: pulse 3.8s ease-in-out infinite; }
    .line1 { animation: type1 9s infinite; }
    .line2 { animation: type2 9s infinite; }
    .line3 { animation: type3 9s infinite; }
    .line4 { animation: type4 9s infinite; }
  </style>
</defs>
<rect width="1000" height="300" rx="24" fill="#0f172a"/>
<rect width="1000" height="300" fill="url(#grid)" opacity=".55"/>
<path class="wave" d="M-90 218 C110 118 260 256 430 184 C620 84 730 232 1090 126 V300 H-90 Z" fill="url(#g)" opacity="0.30"/>
<path class="wave" d="M-90 248 C140 162 300 286 470 222 C650 152 780 260 1090 190 V300 H-90 Z" fill="#22c55e" opacity="0.13"/>
<circle class="orb" cx="96" cy="78" r="42" fill="#22c55e" opacity="0.22"/>
<circle class="orb" cx="902" cy="72" r="58" fill="#0ea5e9" opacity="0.20"/>
<text x="500" y="86" text-anchor="middle" font-family="Arial, sans-serif" font-size="38" font-weight="800" fill="#ffffff">Divyansh Kumar Singh Chauhan</text>
<text x="500" y="128" text-anchor="middle" font-family="Arial, sans-serif" font-size="19" font-weight="600" fill="#dbeafe">Competitive Programmer | ML + Systems Builder | IIIT Naya Raipur</text>
<g font-family="Consolas, monospace" font-size="18" text-anchor="middle">
  <text class="line1" x="500" y="178" fill="#bbf7d0">ICPC Regionalist 2025 | Codeforces Expert | LeetCode Top 3.82%</text>
  <text class="line2" x="500" y="178" fill="#bbf7d0">Building RAG platforms, cybersecurity ML, and OS-level systems</text>
  <text class="line3" x="500" y="178" fill="#bbf7d0">YT AI Agent | FileWorld | OffChat Suite | CogniGen</text>
  <text class="line4" x="500" y="178" fill="#bbf7d0">Teaching competitive programming on YouTube: Redcapp</text>
</g>
<text x="500" y="222" text-anchor="middle" font-family="Consolas, monospace" font-size="16" fill="#fed7aa">Animated profile README powered by local SVG assets and GitHub Actions stats</text>
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
        cards.append(f"""
<rect x="{x}" y="{y}" width="430" height="88" rx="12" fill="#111827" stroke="#334155"/>
<text x="{x+20}" y="{y+30}" class="pname">{name}</text>
<text x="{x+20}" y="{y+54}" class="pdesc">{desc}</text>
<text x="{x+20}" y="{y+75}" class="pstack">{stack}</text>""")
    return f"""<svg width="950" height="530" viewBox="0 0 950 530" xmlns="http://www.w3.org/2000/svg">
<style>
.title{{font:800 26px Arial;fill:#fff}}.sub{{font:14px Arial;fill:#94a3b8}}.pname{{font:700 18px Arial;fill:#93c5fd}}.pdesc{{font:14px Arial;fill:#e5e7eb}}.pstack{{font:13px Consolas;fill:#bbf7d0}}
</style>
<rect width="950" height="530" rx="18" fill="#0b1120"/>
<text x="28" y="34" class="title">Project Glimpses</text>
<text x="260" y="34" class="sub">real repositories and resume-grade work</text>
{''.join(cards)}
</svg>"""


def activity_svg(stats):
    return f"""<svg width="900" height="180" viewBox="0 0 900 180" xmlns="http://www.w3.org/2000/svg">
<style>
.label{{font:700 15px Arial;fill:#cbd5e1}}.num{{font:800 34px Arial;fill:#fff}}.small{{font:13px Arial;fill:#94a3b8}}
</style>
<rect width="900" height="180" rx="18" fill="#0f172a"/>
<text x="36" y="42" class="label">GitHub Portfolio Snapshot</text>
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
        rows.append(f"""
<rect x="{x}" y="{y}" width="380" height="76" rx="12" fill="#111827" stroke="#334155"/>
<text x="{x+18}" y="{y+28}" class="name">{name}</text>
<text x="{x+190}" y="{y+28}" class="rank">{rank}</text>
<text x="{x+18}" y="{y+52}" class="value">{primary}</text>
<text x="{x+190}" y="{y+52}" class="muted">{secondary}</text>""")
    return f"""<svg width="880" height="370" viewBox="0 0 880 370" fill="none" xmlns="http://www.w3.org/2000/svg">
<style>
.bg{{fill:#0f172a}}.title{{font:800 24px Arial;fill:#fff}}.name{{font:700 17px Arial;fill:#93c5fd}}.rank{{font:700 15px Arial;fill:#fed7aa}}.value{{font:700 15px Arial;fill:#dcfce7}}.muted{{font:13px Arial;fill:#94a3b8}}
</style>
<rect class="bg" width="880" height="370" rx="18"/>
<text x="28" y="34" class="title">Live Competitive Programming + Creator Stats</text>
{''.join(rows)}
<text x="28" y="352" class="muted">Auto-updated by GitHub Actions. Fallbacks keep the card stable if a platform blocks automated fetches.</text>
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
    (ASSETS / "live-stats.svg").write_text(svg(stats), encoding="utf-8")
    (ASSETS / "profile-header.svg").write_text(profile_header_svg(), encoding="utf-8")
    (ASSETS / "project-glimpses.svg").write_text(project_glimpses_svg(), encoding="utf-8")
    (ASSETS / "github-activity.svg").write_text(activity_svg(stats), encoding="utf-8")


if __name__ == "__main__":
    main()
