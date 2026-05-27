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
    def find(label):
        match = re.search(label + r".*?(\d+)", html, flags=re.S)
        return int(match.group(1)) if match else None
    return {
        "current": find(r"Rating"),
        "max": find(r"Highest Rating"),
        "matches": find(r"Rated Matches"),
    }


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
        ("Codeforces", f"{stats['codeforces']['current']} / max {stats['codeforces']['max']}"),
        ("CodeChef", f"{stats['codechef']['current']} / max {stats['codechef']['max']}"),
        ("AtCoder", f"{stats['atcoder']['current']} / max {stats['atcoder']['max']}"),
        ("LeetCode", f"{stats['leetcode']['solved']} solved, {stats['leetcode']['rating']} rating"),
        ("YouTube", f"{stats['youtube']['subscribers']}, {stats['youtube']['views']}"),
    ]
    rows = []
    for i, (name, value) in enumerate(cards):
        y = 46 + i * 40
        rows.append(f'<text x="28" y="{y}" class="name">{name}</text><text x="220" y="{y}" class="value">{value}</text>')
    return f"""<svg width="720" height="260" viewBox="0 0 720 260" fill="none" xmlns="http://www.w3.org/2000/svg">
<style>
.bg{{fill:#0f172a}}.title{{font:700 22px Arial;fill:#fff}}.name{{font:700 16px Arial;fill:#93c5fd}}.value{{font:600 16px Arial;fill:#dcfce7}}.muted{{font:12px Arial;fill:#94a3b8}}
</style>
<rect class="bg" width="720" height="260" rx="14"/>
<text x="28" y="28" class="title">Live Competitive Programming + Creator Stats</text>
{''.join(rows)}
<text x="28" y="240" class="muted">Auto-updated by GitHub Actions</text>
</svg>"""


def main():
    stats = {
        "codeforces": safe(codeforces, {"current": 1624, "max": 1673, "rank": "expert", "max_rank": "expert"}),
        "codechef": safe(codechef, {"current": 1824, "max": 1852, "solved": 832}),
        "atcoder": safe(atcoder, {"current": 1075, "max": 1078, "matches": 64}),
        "leetcode": safe(leetcode, {"solved": 373, "rating": 1925.21, "top_percentage": 3.82, "contests": 28}),
        "youtube": safe(youtube, {"channel": "Redcapp", "subscribers": "30 subscribers", "views": "2,209 views"}),
    }
    (STATS / "competitive.json").write_text(json.dumps(stats, indent=2), encoding="utf-8")
    (ASSETS / "live-stats.svg").write_text(svg(stats), encoding="utf-8")


if __name__ == "__main__":
    main()
